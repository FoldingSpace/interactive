#!/usr/bin/env python3
"""Build the street network for the relative-distance widget.

Writes web/relative-distance/data.js and web/relative-distance/basemap.jpg.

    python3 tools/relative-distance-extract.py

Needs GDAL's Python bindings, numpy, and network access. It caches everything it
downloads under tools/rd-cache, so a second run is cheap: the OpenStreetMap fetch is
twenty requests and the elevation is a gigabyte. Delete the cache to start clean.

Check the result with tools/relative-distance-verify.py, which reads the data.js this
writes and rebuilds the routing from the written description, sharing no code with
either this file or the widget.

Why the choices are what they are, since none of them are forced:

  City     Vancouver. Burrard Inlet is what makes the widget's point unmissable:
           Lonsdale Quay is 3.47 km from Waterfront Station in a straight line and
           two and a quarter hours away on foot, while Commercial Drive is 3.06 km
           away and thirty-eight minutes. Same distance, four times the trip.

           No GEOG 370 lab asks for anything on a network, so nothing here can serve
           as an answer key. Lab 1 is linguistic diversity, Lab 2 is terrain and
           multi-criteria evaluation in the Okanagan, Lab 3 is the modifiable areal
           unit problem, Lab 4 is least-cost paths. Read, not assumed.

  Window   49.25 to 49.36 N, -123.22 to -123.00 W. Jericho to Boundary Road, Broadway
           to the Capilano foothills. It holds both crossings of the inlet, which the
           lesson needs, and stops short of the Fraser, which it does not.

  Streets  OpenStreetMap, ODbL. Separately mapped sidewalks and pedestrian crossings
           are dropped: they were 25,043 of the 61,441 ways in the window, they would
           have drawn a sidewalk diagram rather than a city, and walkers route along
           street centrelines here as they do in most routing engines. What stays is
           roads, plus the paths, steps and bike routes that are their own way through
           somewhere. That last part matters more than it looks: both crossings of the
           inlet are tagged in OSM as separate cycleways carrying foot=designated,
           because the roadway itself is foot=no or a motorway. Drop cycleways and
           Vancouver loses its bridges for everyone but drivers. Note that not every
           segment of the named bike routes carries foot=designated — several approach
           pieces are foot=no — so the blanket statement holds of the decks, not of the
           whole route.

  Slopes   NRCan's High Resolution Digital Elevation Model, 1 m bare-earth LiDAR from
           the Lower Mainland 2016 project, averaged to 4 m, under the Open Government
           Licence - Canada. 94 junctions at the northern fringe fall outside that
           mosaic and take the 20 m Canadian Digital Elevation Model instead.

           This began on CDEM alone, and the reason for the change is worth keeping.
           On flat East Vancouver ground a 43 m block with two metres of error reads as
           a five per cent hill, and one of the four travellers is defined by a five
           per cent threshold, so the noise would have decided the lesson. Measured
           against LiDAR, the two models agree: over the 648 residential segments in
           that flat box the median grade is 1.8% under both, and the share over 5% is
           11.4% under LiDAR against 13.7% under CDEM. East Vancouver's north-south
           streets really do run that steep, because they fall to the inlet. The grades
           were real all along, and the noise argument was wrong. The LiDAR is kept
           anyway, because the agreement is what makes the numbers quotable.

           Grades are clamped to plus or minus 35%. Above that they are stairs, walls
           or a bridge the bridge tag missed.

           Bridges and tunnels are forced flat. A bare-earth model holds the water
           under a bridge, not the deck, so without this every crossing of the inlet
           is a cliff.

  Modes    A traveller is a speed and a set of permissions, and the two are kept apart
           on purpose. Someone on foot and someone on foot avoiding steep ground move
           at exactly the same speed; only what they will use differs. So whatever
           changes between those two maps is the ground refusing, not the walker
           slowing down.

  Free-flow  Every mode moves as though the way were clear: posted limits with no
           traffic, cycling with no stop signs, walking with no crossings. That is not
           a simplification chosen for convenience. There is no openly licensed record
           of Vancouver traffic by time of day, and inventing one would put a
           fabricated claim on a page whose whole subject is that the assumptions make
           the map. It is held constant across all four travellers, and it is said on
           the page.
"""

import collections
import glob
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request
import zipfile

import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()
osr.UseExceptions()

S, W, N, E = 49.25, -123.22, 49.36, -123.00

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("RD_CACHE", os.path.join(HERE, "rd-cache"))
OUT = os.path.join(HERE, "..", "web", "relative-distance", "data.js")

OVERPASS = "https://overpass-api.de/api/interpreter"
HRDEM = ("https://ftp.maps.canada.ca/pub/elevation/dem_mne/highresolution_hauteresolution/"
         "dtm_mnt/1m/BC/Lower_Mainland_2016/utm10/dtm_1m_utm10_%s.tif")
HRDEM_TILES = ["w_0_145", "w_0_146", "w_1_145", "w_1_146"]
CDEM_ZIP = ("https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/092/"
            "cdem_dem_092G_tif.zip")

# The photograph under the streets. Two Sentinel-2 tiles from the same satellite on the
# same cloud-free day, so there is no seam of date or sensor across the middle of the
# window; 10 m, already in UTM zone 10N, so nothing is reprojected. Copernicus.
S2 = ("/vsicurl/https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/"
      "10/U/%s/2025/8/S2C_10U%s_20250812_0_L2A/TCI.tif")
S2_TILES = ["DV", "EV"]
IMG = (483000, 5453100, 501400, 5471200)      # UTM 10N, and the widget repeats it
IMG_RES = 16.0
IMG_OUT = os.path.join(HERE, "..", "web", "relative-distance", "basemap.jpg")

SIMPLIFY = 6.0          # metres, Douglas-Peucker on the geometry between junctions
QUANT = 2.0             # metres per stored coordinate unit in data.js

# highway value -> (foot, bike, car, default speed km/h) before any tag overrides
CLASS = {
    "motorway": (0, 0, 1, 90), "motorway_link": (0, 0, 1, 50),
    "trunk": (1, 1, 1, 80), "trunk_link": (1, 1, 1, 50),
    "primary": (1, 1, 1, 60), "primary_link": (1, 1, 1, 40),
    "secondary": (1, 1, 1, 50), "secondary_link": (1, 1, 1, 40),
    "tertiary": (1, 1, 1, 50), "tertiary_link": (1, 1, 1, 40),
    "unclassified": (1, 1, 1, 40), "residential": (1, 1, 1, 30),
    "living_street": (1, 1, 1, 20), "pedestrian": (1, 1, 0, 0),
    "footway": (1, 0, 0, 0), "path": (1, 1, 0, 0), "steps": (1, 0, 0, 0),
    "cycleway": (0, 1, 0, 0), "track": (1, 1, 0, 0),
}
DROP_FOOTWAY = ("sidewalk", "crossing", "traffic_island", "link", "access_aisle")
NO = {"no", "private", "customers", "delivery", "permit", "military"}
YES = {"yes", "designated", "permissive", "destination", "official", "yes;designated"}

MAJOR = {"motorway", "motorway_link", "trunk", "trunk_link", "primary", "primary_link",
         "secondary", "secondary_link"}
MINOR = {"tertiary", "tertiary_link", "unclassified", "residential", "living_street"}

# Name, longitude, latitude. These are the labels on the map and the starting points
# offered as buttons, so each has to be somewhere a reader would recognise and somewhere
# a traveller could plausibly stand.
PLACES = [
    ["Waterfront Station", -123.1116, 49.2859],
    ["Lonsdale Quay", -123.0827, 49.3096],
    ["Commercial & Hastings", -123.0700, 49.2812],
    ["Stanley Park", -123.1440, 49.3020],
    ["Kitsilano Beach", -123.1534, 49.2745],
    ["Park Royal", -123.1391, 49.3253],
    ["Upper Lonsdale", -123.0725, 49.3355],
    ["Broadway & Main", -123.1008, 49.2626],
    ["Burnaby Heights", -123.0200, 49.2820],
    ["Capilano", -123.1150, 49.3430],
    ["Jericho Beach", -123.1963, 49.2726],
    ["Second Narrows", -123.0240, 49.2950],
]


# ---------------------------------------------------------------- fetching
def fetch_osm():
    """Twenty tiles. One query for the whole window times the server out, and a plain
    way["highway"] query is about thirty times faster than a regex over highway values,
    so everything is filtered here instead."""
    os.makedirs(CACHE, exist_ok=True)
    ny, nx = 4, 5
    for j in range(ny):
        for i in range(nx):
            tag = "%d_%d" % (j, i)
            path = os.path.join(CACHE, "tile_%s.json" % tag)
            if os.path.exists(path) and os.path.getsize(path) > 500:
                continue
            s0 = S + (N - S) * j / ny
            n0 = S + (N - S) * (j + 1) / ny
            w0 = W + (E - W) * i / nx
            e0 = W + (E - W) * (i + 1) / nx
            q = ('[out:json][timeout:280];way["highway"](%.5f,%.5f,%.5f,%.5f);out body geom;'
                 % (s0, w0, n0, e0))
            for attempt in range(8):
                try:
                    req = urllib.request.Request(
                        OVERPASS, data=urllib.parse.urlencode({"data": q}).encode(),
                        headers={"User-Agent": "foldingspace-interactive/1.0"})
                    raw = urllib.request.urlopen(req, timeout=320).read()
                    json.loads(raw)
                    open(path, "wb").write(raw)
                    print("osm %s ok" % tag, file=sys.stderr)
                    break
                except Exception as exc:
                    print("osm %s retry %d: %s" % (tag, attempt, exc), file=sys.stderr)
                    time.sleep(20 + 15 * attempt)
            else:
                raise SystemExit("could not fetch tile " + tag)
            time.sleep(4)


def fetch_elevation():
    os.makedirs(CACHE, exist_ok=True)
    tiles = []
    for t in HRDEM_TILES:
        path = os.path.join(CACHE, "dtm_1m_utm10_%s.tif" % t)
        if not os.path.exists(path):
            print("hrdem %s downloading (about 250 MB)" % t, file=sys.stderr)
            urllib.request.urlretrieve(HRDEM % t, path)
        tiles.append(path)
    mosaic = os.path.join(CACHE, "hrdem_4m.tif")
    if not os.path.exists(mosaic):
        gdal.Warp(mosaic, tiles, xRes=4, yRes=4, resampleAlg="average",
                  outputBounds=(482800, 5452900, 500400, 5471400),
                  dstNodata=-9999, multithread=True)
    cdem = os.path.join(CACHE, "cdem", "cdem_dem_092G.tif")
    if not os.path.exists(cdem):
        z = os.path.join(CACHE, "cdem.zip")
        if not os.path.exists(z):
            print("cdem downloading (about 39 MB)", file=sys.stderr)
            urllib.request.urlretrieve(CDEM_ZIP, z)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(os.path.join(CACHE, "cdem"))
    return mosaic, cdem


# ---------------------------------------------------------------- tags
def parse_maxspeed(v):
    if not v:
        return None
    v = v.strip().lower()
    try:
        if v.endswith("mph"):
            return float(v[:-3].strip()) * 1.609344
        return float(v.split()[0])
    except ValueError:
        return None


def classify(tags):
    """(foot, bike, car, speed) after tag overrides, or None to drop the way."""
    hw = tags.get("highway")
    base = CLASS.get(hw)
    if base is None or tags.get("area") == "yes":
        return None
    if hw == "footway" and tags.get("footway") in DROP_FOOTWAY:
        return None
    foot, bike, car, speed = base

    if tags.get("access") in NO:
        foot = 1 if tags.get("foot") in YES else 0
        bike = 1 if tags.get("bicycle") in YES else 0
        car = 1 if tags.get("motor_vehicle") in YES or tags.get("vehicle") in YES else 0
    if tags.get("foot") in NO:
        foot = 0
    elif tags.get("foot") in YES:
        foot = 1
    if tags.get("bicycle") in NO:
        bike = 0
    elif tags.get("bicycle") in YES:
        bike = 1
    for k in ("motor_vehicle", "motorcar", "vehicle"):
        if tags.get(k) in NO:
            car = 0
        elif tags.get(k) in YES and hw not in (
                "footway", "steps", "path", "cycleway", "pedestrian"):
            car = 1
    if tags.get("construction") or hw in ("construction", "proposed"):
        return None
    if not (foot or bike or car):
        return None

    ms = parse_maxspeed(tags.get("maxspeed"))
    return foot, bike, car, (ms if ms else speed)


def oneway_flags(tags):
    """See below. This wrapper exists so the shared-use rule is applied in one place
    and is impossible to forget."""
    cf, cb, bf, bb = _oneway_flags(tags)
    if shared_use_path(tags):
        bf = bb = 1
    return cf, cb, bf, bb


def shared_use_path(tags):
    """A path pedestrians are designated to use is a shared footway, and the direction
    written on it is a recommendation rather than a restriction.

    OSM maps the Lions Gate crossing, and the Stanley Park Causeway approach to it, as
    a pair of one-way cycleways — one for each side. Taking that literally sends a
    cyclist heading north the long way round, and the cost is not small: from Waterfront
    Station, Park Royal by bike was 57.7 minutes and is 21.8, Lonsdale Quay was 43.1 and
    is 33.8. Luke, who cycles the city, says the bridge takes bikes both ways.

    **Both of those wrong numbers had been verified.** A second implementation reproduced
    them to six decimals, because it read the same input. Checking by recomputation
    cannot see a wrong input, and this is the clearest case of it in the repository:
    what caught it was somebody who knows the bridge.

    The rule is narrow where it counts. In this window there are 984 one-way cycleways;
    it frees 42, and those are the bridge and causeway sidewalks. The other 942 are
    contraflow bike lanes on real streets — Quebec Street, the Burrard Street Cycleway,
    Carrall Street, the 10th Avenue Bikeway — which are one-way and stay that way. The
    Stanley Park Seawall bike path stays one-way too, correctly, because it is
    foot=no: it is a cycle-only path and it really does run one direction.
    """
    return tags.get("highway") == "cycleway" and tags.get("foot") == "designated"


def _oneway_flags(tags):
    """(car forward, car back, bike forward, bike back). Walking ignores one-way.

    Both pedestrian crossings of the inlet are tagged as one-way cycleways carrying
    foot=designated, and `oneway` there means the bike direction. Measured, the rule is
    worth less than it first looked: because each bridge is a pair of one-way ways, a
    walker obeying `oneway` simply uses the correctly directed side and loses nothing
    northbound, and up to about twelve minutes southbound. It is still right — a
    pedestrian is not bound by a one-way street — but it does not save the bridges, and
    the first version of this comment said it did."""
    ow = tags.get("oneway", "no")
    cf = cb = 1
    if ow in ("yes", "true", "1"):
        cb = 0
    elif ow in ("-1", "reverse"):
        cf = 0
    if tags.get("junction") == "roundabout" and "oneway" not in tags:
        cb = 0
    bf, bb = cf, cb
    owb = tags.get("oneway:bicycle")
    if owb in ("no", "false"):
        bf = bb = 1
    elif owb in ("yes", "true"):
        bb = 0
    if tags.get("cycleway") in ("opposite", "opposite_lane", "opposite_track"):
        bf = bb = 1
    return cf, cb, bf, bb


# ---------------------------------------------------------------- geometry
_src = osr.SpatialReference(); _src.ImportFromEPSG(4326)
_src.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
_dst = osr.SpatialReference(); _dst.ImportFromEPSG(32610)
_dst.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
_tr = osr.CoordinateTransformation(_src, _dst)


def project(lonlat):
    return [(p[0], p[1]) for p in _tr.TransformPoints(list(lonlat))]


def douglas_peucker(pts, tol):
    if len(pts) < 3:
        return list(range(len(pts)))
    keep = [0, len(pts) - 1]
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        d2 = dx * dx + dy * dy
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            if d2 == 0:
                h = math.hypot(px - ax, py - ay)
            else:
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / d2))
                h = math.hypot(px - ax - t * dx, py - ay - t * dy)
            if h > best:
                best, bi = h, i
        if best > tol:
            keep.append(bi)
            stack.append((a, bi))
            stack.append((bi, b))
    keep.sort()
    return keep


# ---------------------------------------------------------------- elevation
def binomial_blur(a, passes):
    k = np.array([1, 4, 6, 4, 1], dtype=np.float32)
    k /= k.sum()
    for _ in range(passes):
        a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)
        a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)
    return a


class Elevation(object):
    """LiDAR where it reaches, the national model elsewhere, and a count of the
    difference so the fallback can never be silent."""

    def __init__(self, hrdem, cdem):
        d = gdal.Open(hrdem)
        self.hgt = d.GetGeoTransform()
        a = d.GetRasterBand(1).ReadAsArray().astype(np.float32)
        self.hmask = np.isfinite(a) & (a > -1000)
        self.h = binomial_blur(np.where(self.hmask, a, 0.0), 1)

        c = gdal.Open(cdem)
        self.cgt = c.GetGeoTransform()
        band = c.GetRasterBand(1)
        nd = band.GetNoDataValue()
        ca = band.ReadAsArray().astype(np.float32)
        ca[(ca == nd) | (ca < -100)] = 0.0
        self.c = binomial_blur(ca, 2)
        self.fallback = 0

    @staticmethod
    def _bilinear(arr, gt, x, y, mask=None):
        fx = (x - gt[0]) / gt[1] - 0.5
        fy = (y - gt[3]) / gt[5] - 0.5
        i0, j0 = int(math.floor(fx)), int(math.floor(fy))
        if i0 < 0 or j0 < 0 or i0 + 1 >= arr.shape[1] or j0 + 1 >= arr.shape[0]:
            return None
        if mask is not None and not mask[j0:j0 + 2, i0:i0 + 2].all():
            return None
        u, v = fx - i0, fy - j0
        return float((arr[j0, i0] * (1 - u) + arr[j0, i0 + 1] * u) * (1 - v) +
                     (arr[j0 + 1, i0] * (1 - u) + arr[j0 + 1, i0 + 1] * u) * v)

    def at(self, x, y, lon, lat):
        v = self._bilinear(self.h, self.hgt, x, y, self.hmask)
        if v is not None:
            return v
        self.fallback += 1
        v = self._bilinear(self.c, self.cgt, lon, lat)
        return 0.0 if v is None else v


# ---------------------------------------------------------------- the graph
def build_graph(hrdem, cdem):
    ways = {}
    for f in sorted(glob.glob(os.path.join(CACHE, "tile_*.json"))):
        for el in json.load(open(f))["elements"]:
            if el["type"] == "way" and el["id"] not in ways:
                ways[el["id"]] = el
    print("ways in the window: %d" % len(ways), file=sys.stderr)

    kept = []
    for w in ways.values():
        t = w.get("tags", {})
        c = classify(t)
        if not c or "nodes" not in w or len(w.get("geometry", [])) < 2:
            continue
        if len(w["nodes"]) != len(w["geometry"]):
            continue
        kept.append((w, t, c))
    print("routable ways: %d" % len(kept), file=sys.stderr)

    use = collections.Counter()
    for w, t, c in kept:
        for nid in w["nodes"]:
            use[nid] += 1
    junction = set()
    for w, t, c in kept:
        ns = w["nodes"]
        junction.add(ns[0])
        junction.add(ns[-1])
        for nid in ns[1:-1]:
            if use[nid] > 1:
                junction.add(nid)

    lonlat = {}
    for w, t, c in kept:
        for nid, g in zip(w["nodes"], w["geometry"]):
            lonlat[nid] = (g["lon"], g["lat"])
    ids = list(lonlat)
    P = dict(zip(ids, project(lonlat[i] for i in ids)))

    index, nodes, edges = {}, [], []

    def nid_of(osm):
        i = index.get(osm)
        if i is None:
            i = len(nodes)
            index[osm] = i
            nodes.append([P[osm][0], P[osm][1], osm, 0.0])
        return i

    for w, t, c in kept:
        foot, bike, car, speed = c
        cf, cb, bf, bb = oneway_flags(t)
        flat = 1 if (t.get("bridge") or t.get("tunnel")) else 0
        steps = 1 if t.get("highway") == "steps" else 0
        ns = w["nodes"]
        cuts = [0] + [i for i in range(1, len(ns) - 1) if ns[i] in junction] + [len(ns) - 1]
        for a, b in zip(cuts, cuts[1:]):
            seg = ns[a:b + 1]
            if len(seg) < 2 or seg[0] == seg[-1]:
                continue
            pts = [P[i] for i in seg]
            pts = [pts[i] for i in douglas_peucker(pts, SIMPLIFY)]
            length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
            if length <= 0:
                continue
            edges.append(dict(u=nid_of(seg[0]), v=nid_of(seg[-1]), pts=pts, L=length,
                              foot=foot, bike=bike, car=car, speed=speed,
                              cf=cf, cb=cb, bf=bf, bb=bb, flat=flat, steps=steps,
                              hw=t.get("highway")))
    print("junctions: %d  segments: %d" % (len(nodes), len(edges)), file=sys.stderr)

    elev = Elevation(hrdem, cdem)
    for nd in nodes:
        lon, lat = lonlat[nd[2]]
        nd[3] = elev.at(nd[0], nd[1], lon, lat)
    print("junctions off the LiDAR mosaic: %d" % elev.fallback, file=sys.stderr)
    for e in edges:
        rise = 0.0 if e["flat"] else nodes[e["v"]][3] - nodes[e["u"]][3]
        e["grade"] = max(-0.35, min(0.35, rise / e["L"]))

    # Largest connected part. What falls off is footpath fragments and slivers cut by
    # the window edge; anything bigger would mean the window is wrong.
    adj = collections.defaultdict(list)
    for e in edges:
        adj[e["u"]].append(e["v"])
        adj[e["v"]].append(e["u"])
    seen = [False] * len(nodes)
    best = []
    for s in range(len(nodes)):
        if seen[s]:
            continue
        comp, seen[s], i = [s], True, 0
        while i < len(comp):
            x = comp[i]; i += 1
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    comp.append(y)
        if len(comp) > len(best):
            best = comp
    keep = set(best)
    print("largest connected part: %d of %d junctions" % (len(best), len(nodes)), file=sys.stderr)
    edges = [e for e in edges if e["u"] in keep and e["v"] in keep]
    remap, newnodes = {}, []
    for i in sorted(keep):
        remap[i] = len(newnodes)
        newnodes.append(nodes[i])
    for e in edges:
        e["u"], e["v"] = remap[e["u"]], remap[e["v"]]
    return newnodes, edges


# ---------------------------------------------------------------- packing
def draw_class(hw):
    if hw in MAJOR:
        return 0
    if hw in MINOR:
        return 1
    return 2


def pack(nodes, edges, out):
    # Anchored to a round 100 m, not to floor(min). Two runs over the same input put
    # the southernmost junction either side of a whole metre — a sub-millimetre wobble
    # in the projection, which floor() turns into a one-metre shift of the origin and
    # so into a different delta for half the nodes in the file. The graph was identical
    # both times; only the anchor moved. A round anchor cannot move.
    x0 = int(math.floor(min(n[0] for n in nodes) / 100.0) * 100)
    y0 = int(math.floor(min(n[1] for n in nodes) / 100.0) * 100)

    # Nodes go in rows, alternating direction, so consecutive coordinates are close and
    # the deltas stay one or two digits.
    def row(i):
        return int((nodes[i][1] - y0) // 200)
    order = sorted(range(len(nodes)),
                   key=lambda i: (row(i), nodes[i][0] * (1 if row(i) % 2 == 0 else -1)))
    rank = [0] * len(nodes)
    for r, i in enumerate(order):
        rank[i] = r

    nx, ny = [], []
    px = py = 0
    for i in order:
        x = int(round((nodes[i][0] - x0) / QUANT))
        y = int(round((nodes[i][1] - y0) / QUANT))
        nx.append(x - px)
        ny.append(y - py)
        px, py = x, y

    E = sorted(edges, key=lambda e: (rank[e["u"]], rank[e["v"]]))
    eu, ev, el, eg, es, ef, ec, epn, ep = [], [], [], [], [], [], [], [], []
    pu = 0
    for e in E:
        u, v = rank[e["u"]], rank[e["v"]]
        eu.append(u - pu)
        pu = u
        ev.append(v - u)
        el.append(int(round(e["L"] * 10)))                       # decimetres
        eg.append(max(-350, min(350, int(round(e["grade"] * 1000)))))   # per mille
        es.append(int(round(e["speed"])))
        ef.append(e["foot"] | (e["bike"] << 1) | (e["car"] << 2) | (e["steps"] << 3) |
                  (e["cf"] << 4) | (e["cb"] << 5) | (e["bf"] << 6) | (e["bb"] << 7))
        ec.append(draw_class(e["hw"]))
        mid = e["pts"][1:-1]
        epn.append(len(mid))
        qx = int(round((nodes[e["u"]][0] - x0) / QUANT))
        qy = int(round((nodes[e["u"]][1] - y0) / QUANT))
        for p in mid:
            x = int(round((p[0] - x0) / QUANT))
            y = int(round((p[1] - y0) / QUANT))
            ep.append(x - qx)
            ep.append(y - qy)
            qx, qy = x, y

    places = []
    for name, lon, lat in PLACES:
        px_, py_ = project([(lon, lat)])[0]
        places.append([name, int(round((px_ - x0) / QUANT)), int(round((py_ - y0) / QUANT))])

    def arr(a):
        return "[" + ",".join(str(v) for v in a) + "]"

    text = "\n".join([
        "// Street network for the relative-distance widget. Written by",
        "// tools/relative-distance-extract.py — do not edit by hand.",
        "// Streets: OpenStreetMap contributors, ODbL.",
        "// Slopes: Natural Resources Canada, HRDEM Lower Mainland 2016 and CDEM,",
        "// under the Open Government Licence — Canada.",
        "window.RD = {",
        "x0:%d,y0:%d,q:%s,n:%d,m:%d," % (x0, y0, QUANT, len(nodes), len(E)),
        "nx:" + arr(nx) + ",", "ny:" + arr(ny) + ",",
        "eu:" + arr(eu) + ",", "ev:" + arr(ev) + ",",
        "el:" + arr(el) + ",", "eg:" + arr(eg) + ",",
        "es:" + arr(es) + ",", "ef:" + arr(ef) + ",",
        "ec:" + arr(ec) + ",", "epn:" + arr(epn) + ",", "ep:" + arr(ep) + ",",
        "places:" + json.dumps(places, separators=(",", ":")),
        "};", ""])
    open(out, "w").write(text)
    print("wrote %s: %d bytes, %d junctions, %d segments, %d shape points"
          % (out, len(text), len(nodes), len(E), len(ep) // 2), file=sys.stderr)


def build_basemap():
    """Wash the photograph out until street lines survive on top of it.

    Measured rather than eyeballed, and the measurement decided the widget's palette.
    Sentinel-2's true-colour product is dark — the median luminance over this window is
    0.089 — so it is stretched between the 2nd and 99th percentiles, gamma-lifted, most
    of its colour taken out, and blended toward the map's own land colour. Even then the
    fifth percentile over land sits around 0.32, against which the widget's pale street
    colour scores 1.6:1. Lightening far enough to fix that leaves no photograph, so the
    widget carries a darker palette for when this is switched on. See the note beside
    `body[data-basemap="1"]` in index.html.

    These three numbers are the whole negotiation between the photograph and the streets,
    and they were set by measurement in both directions. Washed harder, the streets are
    comfortable and the ground is a rumour. Washed less, the ground reads and the paths
    stop being lines. This is the strongest photograph the palette can carry.
    """
    gdal.SetConfigOption("AWS_NO_SIGN_REQUEST", "YES")
    x0, y0, x1, y1 = IMG
    w, h = int((x1 - x0) / IMG_RES), int((y1 - y0) / IMG_RES)
    ds = gdal.Warp("", [S2 % (t, t) for t in S2_TILES], format="MEM",
                   outputBounds=(x0, y0, x1, y1), width=w, height=h,
                   resampleAlg="average", srcNodata=0, dstNodata=0)
    rgb = np.moveaxis(ds.ReadAsArray().astype(np.float32) / 255.0, 0, -1)
    blank = rgb.sum(-1) == 0
    if blank.mean() > 0.001:
        raise SystemExit("the two tiles do not cover the window: %.2f%% empty"
                         % (100 * blank.mean()))
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    lo, hi = np.percentile(lum, 2), np.percentile(lum, 99)
    gam = np.clip((lum - lo) / max(1e-6, hi - lo), 0, 1) ** 0.48
    col = rgb / np.maximum(lum, 1e-4)[..., None]
    out = np.clip(np.clip(col, 0, 3) * gam[..., None], 0, 1)
    grey = out.mean(-1, keepdims=True)
    out = np.clip(grey + (out - grey) * 0.32, 0, 1)
    land = np.array([0xf4, 0xf2, 0xee], np.float32) / 255.0
    out = np.clip(land * 0.50 + out * 0.50, 0, 1)
    m = gdal.GetDriverByName("MEM").Create("", w, h, 3, gdal.GDT_Byte)
    for i in range(3):
        m.GetRasterBand(i + 1).WriteArray((out[..., i] * 255).astype(np.uint8))
    path = os.path.normpath(IMG_OUT)
    gdal.GetDriverByName("JPEG").CreateCopy(path, m, options=["QUALITY=64"])
    print("wrote %s: %d bytes, %d x %d" % (path, os.path.getsize(path), w, h), file=sys.stderr)


def main():
    fetch_osm()
    hrdem, cdem = fetch_elevation()
    nodes, edges = build_graph(hrdem, cdem)
    pack(nodes, edges, os.path.normpath(OUT))
    build_basemap()


if __name__ == "__main__":
    main()
