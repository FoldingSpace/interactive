#!/usr/bin/env python3
"""Build the data block for the zone-design widget: Vancouver dissemination areas,
median household income, and mean summer greenness.

Everything here is openly licensed and downloadable by anyone. Nothing in it came from
course material, and no record describes a person.

Sources, all fetched by this script into --cache:

  Dissemination area boundaries, 2021 Census (cartographic)
    https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/
      files-fichiers/lda_000a21a_e.zip                                (98 MB)
  Census tract boundaries, 2021 Census (cartographic)
    .../lct_000a21a_e.zip                                             (10 MB)
  Census Profile, 2021, dissemination areas
    https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/
      download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=006   (2.2 GB)
    All three: Statistics Canada Open Licence.
  Local area boundaries, City of Vancouver
    https://opendata.vancouver.ca/explore/dataset/local-area-boundary/
    Open Government Licence - Vancouver.
  Sentinel-2 L2A, tile 10UDV, 7 August 2026, via the Earth Search catalogue
    https://earth-search.aws.element84.com/v1  collection sentinel-2-c1-l2a
    Copernicus open and free data policy.

Usage:  python3 tools/zone-design-extract.py --cache /tmp/zone-design \\
            > web/zone-design/data.js

Geometry is reprojected to UTM zone 10N (EPSG:32610), which is the projection the
satellite scene already uses, quantised to a 5 m grid and delta-encoded as base64
varints. Quantising before encoding snaps shared boundaries to identical vertices, so
neighbouring areas stay coincident and adjacency falls out of the shared edges.

Run it twice and diff the output. A data file that cannot be reproduced cannot be
checked (docs/review.md).
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import zipfile
import base64
import random

from osgeo import ogr, osr, gdal

ogr.UseExceptions()
gdal.UseExceptions()

Q = 5.0                       # quantisation, metres
K_PAINT = 8                    # zones in the family a student draws
SEED_BALANCED = 7             # the eight-zone starting point the page opens on
SEEDS_SEARCH = (11, 23, 37)   # starting points the gerrymander search is run from
SEEDS_MANY = tuple(range(1, 25))   # starting points the principled families are drawn from
EPSG_OUT = 32610              # UTM zone 10N, the scene's own projection
# How far past the City of Vancouver's own boundary an area's centre may sit and still be
# drawn. Two and a half kilometres takes in the university and the endowment lands, which
# are the other half of the Point Grey peninsula, and with them the western edge of Burnaby
# and the northern edge of Richmond.
# The study area, stated once and drawn on the page as its own edge. It is the City of
# Vancouver's own outline joined to three rectangles in UTM zone 10N, so the data end on a
# line somebody chose rather than on a ragged fringe of whichever areas a distance rule
# happened to catch.
#   UBC      the other half of the Point Grey peninsula: the university and the
#            University Endowment Lands, which are a different census subdivision and
#            which the City's own outline stops short of.
#   EAST     Burnaby west of 501,500 E, which is about two kilometres past Boundary Road.
#            New Westminster is not in: it sits east of that line, and taking it would mean
#            taking the whole of Burnaby with it, which triples the file for ground that
#            adds nothing the widget asks about.
#   SOUTH    Lulu Island north of 5,443,500 N, which is the northern half of Richmond.
# Every rectangle's top edge is south of Burrard Inlet, so nothing on the North Shore is in.
LAND_SHARE = 1.0 / 3.0        # of an area's land, how much must be inside to keep it
LAND_FLOOR = 1.0e6            # ...and at least this much of it, in square metres
STUDY_RECTS = [
    ("the university and the endowment lands", 479500.0, 5452500.0, 484500.0, 5459500.0),
    ("Burnaby west of 501,500 E", 496000.0, 5450000.0, 501500.0, 5458000.0),
    ("Lulu Island north of 5,443,500 N", 483000.0, 5443500.0, 501500.0, 5451500.0),
]

# The window the satellite bands are cut to, in EPSG:32610. Round numbers, chosen to
# hold the whole City of Vancouver with a margin. An extent is a claim about what is
# inside it, so it is one constant, asserted in the test suite.
WIN = (479000.0, 5460500.0, 502000.0, 5443000.0)   # ulx uly lrx lry

SCENE = "S2C_T10UDV_20260807T191738_L2A"
SCENE_HREF = ("https://e84-earth-search-sentinel-data.s3.us-west-2.amazonaws.com/"
              "sentinel-2-c1-l2a/10/U/DV/2026/8/" + SCENE)
# Earth Search publishes these on the asset, and they are what turns a stored integer
# into reflectance: reflectance = DN * SCALE + OFFSET. Processing baseline 05.12 carries
# the -0.1 radiometric offset, and ignoring it biases NDVI.
S2_SCALE, S2_OFFSET = 0.0001, -0.1
# Scene classification values kept. 4 vegetation, 5 not vegetated, 7 unclassified.
# Water (6) is dropped on purpose: a waterfront area's greenness is a fact about its
# land, and averaging the inlet into it would make the shoreline look bare.
# Cloud, shadow, snow and saturated pixels are dropped as unusable.
SCL_KEEP = (4, 5, 7)
# Water, for the clip and for the pale ground behind the maps. The scene classification
# layer's water class on its own picks up building shadows, so a pixel has to be class 6
# *and* dark in the near infrared, which water is and shadow is not. Anything smaller than
# two hectares is dropped, which removes speckle without removing a lake.
SCL_WATER = 6
NIR_WATER_MAX = 0.12
WATER_MIN_M2 = 20000.0
WATER_SIMPLIFY = 15.0

STATCAN = ("https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/"
           "boundary-limites/files-fichiers/")
PROFILE = ("https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/"
           "download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=006")
COV_AREAS = ("https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/"
             "local-area-boundary/exports/geojson")

# The three census characteristics used. Matched on their published names *and* on their
# published numbers, so a renumbering or a rewording between census years fails loudly
# instead of quietly handing back the wrong column. Names are compared with their leading
# indentation stripped, which the file carries and the documentation does not.
WANT = [
    ("pop", 1, "Population, 2021"),
    ("hh", 50, "Total - Private households by household size - 100% data"),
    ("inc", 243, "Median total income of household in 2020 ($)"),
]
# One geography is one block of this many rows in the profile file, which is what makes it
# possible to read three rows per area out of 3.6 GB instead of parsing all of it.
BLOCK = 2631
PROFILE_MEMBER = "98-401-X2021006_English_CSV_data_BritishColumbia.csv"
PROFILE_INDEX = "98-401-X2021006_Geo_starting_row_BritishColumbia.CSV"
DA_DGUID = "2021S0512"


# ---------------------------------------------------------------- fetching

def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 4096:
        return dest
    sys.stderr.write("fetching %s\n" % url)
    subprocess.check_call(["curl", "-sSL", "--retry", "3", "-o", dest, url])
    return dest


def unzip(path, into):
    with zipfile.ZipFile(path) as z:
        z.extractall(into)


# ---------------------------------------------------------------- encoding

def varint(n, out):
    """Zigzag + LEB128, the same encoding protobuf uses for signed ints."""
    z = (n << 1) ^ (n >> 63) if n < 0 else n << 1
    while True:
        b = z & 0x7F
        z >>= 7
        if z:
            out.append(b | 0x80)
        else:
            out.append(b)
            return


# ---------------------------------------------------------------- geometry

def load_layer(shp, name):
    ds = ogr.Open(shp)
    lyr = ds.GetLayerByName(name)
    return ds, lyr


def transformer(src_srs, epsg):
    dst = osr.SpatialReference()
    dst.ImportFromEPSG(epsg)
    dst.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    src = src_srs.Clone()
    src.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    return osr.CoordinateTransformation(src, dst)


def rings_of(geom):
    """Every exterior and interior ring of a polygon or multipolygon, as point lists."""
    out = []
    t = geom.GetGeometryType()
    if t in (ogr.wkbMultiPolygon, ogr.wkbMultiPolygon25D):
        for i in range(geom.GetGeometryCount()):
            out += rings_of(geom.GetGeometryRef(i))
        return out
    for i in range(geom.GetGeometryCount()):
        r = geom.GetGeometryRef(i)
        pts = [(r.GetX(k), r.GetY(k)) for k in range(r.GetPointCount())]
        if len(pts) > 1 and pts[0] == pts[-1]:
            pts.pop()
        if len(pts) >= 3:
            out.append(pts)
    return out


def quantise(rings):
    """Snap to the grid and drop points a ring repeats. Shared boundaries survive this
    because identical input vertices land on identical output vertices."""
    out = []
    for pts in rings:
        q = []
        for x, y in pts:
            p = (int(round(x / Q)), int(round(y / Q)))
            if not q or p != q[-1]:
                q.append(p)
        while len(q) > 1 and q[0] == q[-1]:
            q.pop()
        if len(q) >= 3:
            out.append(q)
    return out


def ring_area(pts):
    a = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a * 0.5


# ---------------------------------------------------------------- the build

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/zone-design")
    ap.add_argument("--out-dir", default="web/zone-design",
                    help="where the greenness picture is written; data.js goes to stdout")
    args = ap.parse_args()
    C = args.cache
    os.makedirs(C, exist_ok=True)

    # ---- sources -----------------------------------------------------------
    da_zip = fetch(STATCAN + "lda_000a21a_e.zip", os.path.join(C, "lda.zip"))
    ct_zip = fetch(STATCAN + "lct_000a21a_e.zip", os.path.join(C, "lct.zip"))
    prof_zip = fetch(PROFILE, os.path.join(C, "profile-da.zip"))
    cov = fetch(COV_AREAS, os.path.join(C, "cov-local-areas.geojson"))
    for z in (da_zip, ct_zip):
        unzip(z, C)

    # ---- the ground the widget covers ---------------------------------------
    # The City of Vancouver's own outline, joined to the three rectangles named above.
    covds = ogr.Open(cov)
    covlyr = covds.GetLayer(0)
    to_out = transformer(covlyr.GetSpatialRef(), EPSG_OUT)
    city = ogr.Geometry(ogr.wkbMultiPolygon)
    areas = []
    for f in covlyr:
        g = f.GetGeometryRef().Clone()
        g.Transform(to_out)
        areas.append((f.GetField("name"), g.Clone()))
        city = city.Union(g)
    areas.sort(key=lambda a: a[0])
    region = city
    for name, x0, y0, x1, y1 in STUDY_RECTS:
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for x, y in [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]:
            ring.AddPoint(x, y)
        box = ogr.Geometry(ogr.wkbPolygon)
        box.AddGeometry(ring)
        region = region.Union(box)
    region = region.Buffer(0)
    e0 = region.GetEnvelope()
    sys.stderr.write("city of vancouver: %d local areas ; study area %.1f x %.1f km, "
                     "%.0f km2, %d rectangles joined to the city\n"
                     % (len(areas), (e0[1] - e0[0]) / 1000, (e0[3] - e0[2]) / 1000,
                        region.GetArea() / 1e6, len(STUDY_RECTS)))
    city = region

    # ---- dissemination areas inside it -------------------------------------
    dads, dalyr = load_layer(os.path.join(C, "lda_000a21a_e.shp"), "lda_000a21a_e")
    da_to_out = transformer(dalyr.GetSpatialRef(), EPSG_OUT)
    ext = city.GetEnvelope()
    # _to_src hands back (minx, maxx, miny, maxy); the filter wants them interleaved.
    fx = _to_src(ext, dalyr.GetSpatialRef())
    dalyr.SetSpatialFilterRect(fx[0], fx[2], fx[1], fx[3])

    # ---- which areas are in, and the land they are cut back to ---------------
    # Census areas are published out over the water: English Bay, False Creek, Burrard
    # Inlet and both arms of the Fraser are each inside a dissemination area as published.
    # A map of them is not recognisable as Vancouver, so every area is cut back to land.
    #
    # An area is in if the centre of its land lies inside the study area, **or** if a
    # third of its land and at least a square kilometre of it does.
    #
    # Sea Island is why the second clause exists. One dissemination area covers the whole
    # island - the airport, Burkeville and Iona - and it is 112.6 km2 as published, because
    # it runs west across Sturgeon Bank into the Strait of Georgia. Its centre falls at
    # 482,017 E, out at sea and outside this study area, so the island was missing from the
    # map while every one of its neighbours was drawn. Taking the centre of its land does
    # not rescue it either: Sturgeon Bank is mudflat, the satellite reads it as ground
    # rather than as water, and the land centre is still out west. What is true of it is
    # that 19.1 km2 of its 47.6 km2 of land, 40 per cent, is inside.
    #
    # Measured against every area that straddles the edge, that pair of thresholds admits
    # exactly one area, this one: the next nearest candidate has 0.59 km2 inside. So it is
    # a rule for a real case rather than a licence for a fringe. Nothing is dropped for a
    # suppressed figure - an area with no published income is drawn and shown as no data.
    water = water_polygon(C)
    feats = []
    rescued = 0
    for f in dalyr:
        g = f.GetGeometryRef().Clone()
        g.Transform(da_to_out)
        land = g.Difference(water)
        if land.IsEmpty() or land.GetArea() < 1000.0:
            continue
        inside = land.Intersection(region)
        by_centre = region.Contains(land.Centroid())
        by_share = (inside.GetArea() >= LAND_SHARE * land.GetArea()
                    and inside.GetArea() >= LAND_FLOOR)
        if not (by_centre or by_share):
            continue
        if not region.Contains(g.Centroid()):
            rescued += 1
        feats.append((f.GetField("DAUID"), g.Clone()))
    feats.sort(key=lambda a: a[0])
    sys.stderr.write("dissemination areas in the study area: %d (%d kept by their land "
                     "centre or by the share of it inside)\n"
                     % (len(feats), rescued))

    kept = []
    for d, g in feats:
        land = g.Intersection(city).Difference(water)
        if land.IsEmpty() or land.GetArea() < 1000.0:
            continue
        kept.append((d, land))
    sys.stderr.write("clipped to land: %d areas kept, %d dropped as all water\n"
                     % (len(kept), len(feats) - len(kept)))
    feats = kept

    # ---- census tracts and local areas, by the centroid of each area ---------
    ctds, ctlyr = load_layer(os.path.join(C, "lct_000a21a_e.shp"), "lct_000a21a_e")
    ct_to_out = transformer(ctlyr.GetSpatialRef(), EPSG_OUT)
    fc = _to_src(ext, ctlyr.GetSpatialRef())
    ctlyr.SetSpatialFilterRect(fc[0], fc[2], fc[1], fc[3])
    cts = []
    for f in ctlyr:
        g = f.GetGeometryRef().Clone()
        g.Transform(ct_to_out)
        cts.append((f.GetField("CTUID"), g.Clone()))
    cts.sort(key=lambda a: a[0])

    def which(polys, geom):
        c = geom.Centroid()
        for i, (_, g) in enumerate(polys):
            if g.Contains(c):
                return i
        best, bd = -1, None
        for i, (_, g) in enumerate(polys):
            d = g.Distance(c)
            if bd is None or d < bd:
                best, bd = i, d
        return best

    ct_of = [which(cts, g) for _, g in feats]
    la_of = [which(areas, g) for _, g in feats]
    used_ct = sorted(set(ct_of))
    ct_ix = {c: i for i, c in enumerate(used_ct)}
    ct_of = [ct_ix[c] for c in ct_of]
    sys.stderr.write("census tracts touched: %d ; local areas: %d\n"
                     % (len(used_ct), len(set(la_of))))


    # ---- greenness ----------------------------------------------------------
    ndvi, ndvi_px = zonal_ndvi(C, feats)

    # ---- census attributes --------------------------------------------------
    attrs = profile(prof_zip, [d for d, _ in feats])

    # ---- geometry out -------------------------------------------------------
    qrings = [quantise(rings_of(g)) for _, g in feats]
    minx = min(p[0] for rs in qrings for r in rs for p in r)
    miny = min(p[1] for rs in qrings for r in rs for p in r)
    # Anchored to a round number below the minimum, not to floor(min): taking the origin
    # from a projected extent lets the last bit of the projection decide it, and two runs
    # then disagree about every delta. docs/review.md.
    ox, oy = (minx // 100) * 100, (miny // 100) * 100
    maxx = max(p[0] for rs in qrings for r in rs for p in r) - ox
    maxy = max(p[1] for rs in qrings for r in rs for p in r) - oy

    buf, ringlens = bytearray(), []
    px = py = 0
    for rs in qrings:
        ringlens.append([len(r) for r in rs])
        for r in rs:
            for x, y in r:
                x -= ox
                y -= oy
                varint(x - px, buf)
                varint(y - py, buf)
                px, py = x, y

    nbr = adjacency(qrings)

    # The water, in the same quantised frame, so the maps can draw it behind everything.
    wrings = quantise([[(x - ox * Q, y - oy * Q) for x, y in r]
                       for r in rings_of(water.Intersection(_box(ox, oy, maxx, maxy)))])
    wbuf = bytearray()
    wlens = [len(r) for r in wrings]
    px = py = 0
    for r in wrings:
        for x, y in r:
            varint(x - px, wbuf)
            varint(y - py, wbuf)
            px, py = x, y

    # The picture the zonal means were taken from, for the "original data" section. Written
    # beside the page rather than inlined: it is only fetched when a reader opens that
    # section, and inlining it would put a third of a megabyte of base64 in the data file.
    nd_breaks = quantile_breaks([v for v in ndvi if v is not None], 7)
    img = os.path.join(args.out_dir, "ndvi.png")
    ndvi_image(C, img, (ox * Q, oy * Q, (ox + maxx) * Q, (oy + maxy) * Q),
               nd_breaks, water)

    # ---- zonings chosen for what they do to the line ------------------------
    # Eight zones, because eight is what a pair can redraw in five minutes, and because
    # holding the count fixed is what makes the comparison about the boundaries.
    attrs["ct"] = ct_of
    attrs["nct"] = len(used_ct)
    attrs["la"] = la_of
    attrs["nla"] = len(areas)
    picked = search_zonings(nbr, attrs, ndvi, ndvi_px, centres(qrings), K_PAINT)

    out = {
        "note": "Vancouver dissemination areas. See docs/widgets/zone-design.md.",
        "quant": Q, "epsg": EPSG_OUT, "origin": [ox * Q, oy * Q],
        "size": [maxx, maxy],
        "n": len(feats),
        "geom": base64.b64encode(bytes(buf)).decode("ascii"),
        "rings": ringlens,
        "nbr": nbr,
        "water": base64.b64encode(bytes(wbuf)).decode("ascii"),
        "wrings": wlens,
        "ct": ct_of, "nct": len(used_ct),
        "la": la_of, "laname": [a[0] for a in areas],
        "inc": attrs["inc"], "hh": attrs["hh"], "pop": attrs["pop"],
        "ndvi": [None if v is None else round(v, 4) for v in ndvi],
        "ndvipx": ndvi_px,
        "scene": SCENE, "scenedate": "2026-08-07",
        "zonings": picked,
    }
    sys.stdout.write("var ZONES = " + json.dumps(out, separators=(",", ":")) + ";\n")


def _to_src(env, srs):
    """An envelope in EPSG_OUT, expressed in some other spatial reference, for a filter."""
    src = osr.SpatialReference()
    src.ImportFromEPSG(EPSG_OUT)
    src.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    dst = srs.Clone()
    dst.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    tr = osr.CoordinateTransformation(src, dst)
    xs, ys = [], []
    for x in (env[0], env[1]):
        for y in (env[2], env[3]):
            p = tr.TransformPoint(x, y)
            xs.append(p[0])
            ys.append(p[1])
    return (min(xs) - 2000, max(xs) + 2000, min(ys) - 2000, max(ys) + 2000)


# ---------------------------------------------------------------- pictures

def quantile_breaks(vals, n):
    s = sorted(vals)
    return [s[len(s) * i // n] for i in range(1, n)]


def _box(ox, oy, w, h):
    """The map's own extent as a geometry, in metres."""
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for x, y in [(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h), (ox, oy)]:
        ring.AddPoint(x * Q, y * Q)
    p = ogr.Geometry(ogr.wkbPolygon)
    p.AddGeometry(ring)
    return p


# The same seven-class YlGn the page uses, and the same pale blue for water, so the
# picture and the choropleths beside it are read off one legend.
ND_RAMP_RGB = [(255, 255, 229), (247, 252, 185), (217, 240, 163), (173, 221, 142),
               (120, 198, 121), (65, 171, 93), (35, 132, 67)]
WATER_RGB = (183, 210, 230)


def ndvi_image(C, path, extent, breaks, water, width=900):
    """Write the greenness of the window as a small picture, in the page's own colours."""
    import numpy as np
    cuts = bands(C)
    red = gdal.Open(cuts["B04"])
    nir = gdal.Open(cuts["B08"])
    scls = gdal.Open(cuts["SCL"])
    gt = red.GetGeoTransform()
    r = red.GetRasterBand(1).ReadAsArray().astype("float64")
    n = nir.GetRasterBand(1).ReadAsArray().astype("float64")
    scl = scls.GetRasterBand(1).ReadAsArray()
    ok = (r > 0) & (n > 0)
    keep = np.zeros(scl.shape, dtype=bool)
    for c in SCL_KEEP:
        keep |= (scl == c)
    r = r * S2_SCALE + S2_OFFSET
    n = n * S2_SCALE + S2_OFFSET
    den = n + r
    good = ok & keep & (den != 0)
    nd = np.zeros(r.shape)
    nd[good] = (n[good] - r[good]) / den[good]

    # Eight values and no more: the seven bands of the page's own ramp plus water. Written
    # as one band with a colour table, which is a tenth of the size of the same picture in
    # three bands and is the same picture.
    cls = np.zeros(nd.shape, dtype="uint8")
    for b in breaks:
        cls += (nd >= b).astype("uint8")
    wet = ((scl == SCL_WATER) & (n < NIR_WATER_MAX)) | (~good)
    cls[wet] = len(ND_RAMP_RGB)

    mem = gdal.GetDriverByName("MEM").Create("", nd.shape[1], nd.shape[0], 1, gdal.GDT_Byte)
    mem.SetGeoTransform(gt)
    mem.SetProjection(red.GetProjection())
    mem.GetRasterBand(1).WriteArray(cls)
    table = gdal.ColorTable()
    for i, c in enumerate(ND_RAMP_RGB):
        table.SetColorEntry(i, c + (255,))
    table.SetColorEntry(len(ND_RAMP_RGB), WATER_RGB + (255,))
    mem.GetRasterBand(1).SetRasterColorTable(table)

    x0, y0, x1, y1 = extent
    h = int(round(width * (y1 - y0) / (x1 - x0)))
    # Nearest, not average: averaging class numbers invents classes that are not there.
    cut = gdal.Translate("", mem, format="MEM", projWin=[x0, y1, x1, y0],
                         projWinSRS="EPSG:%d" % EPSG_OUT, width=width, height=h,
                         resampleAlg="near")
    gdal.GetDriverByName("PNG").CreateCopy(path, cut, strict=0)
    # GDAL writes a sidecar of statistics beside the picture; it is not part of the widget.
    if os.path.exists(path + ".aux.xml"):
        os.remove(path + ".aux.xml")
    sys.stderr.write("greenness picture: %d x %d, %d bytes\n"
                     % (width, h, os.path.getsize(path)))


# ---------------------------------------------------------------- water

def bands(C):
    """The three band cuts, made once and reused by the water mask and the greenness."""
    os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
    os.environ.setdefault("AWS_NO_SIGN_REQUEST", "YES")
    out = {}
    for band in ("B04", "B08", "SCL"):
        dest = os.path.join(C, "s2_%s.tif" % band)
        if not os.path.exists(dest):
            sys.stderr.write("cutting %s from %s\n" % (band, SCENE))
            gdal.Translate(dest, "/vsicurl/%s/%s.tif" % (SCENE_HREF, band),
                           projWin=list(WIN), projWinSRS="EPSG:%d" % EPSG_OUT,
                           xRes=10, yRes=10, resampleAlg="near")
        out[band] = dest
    return out


_WATER = {}


def water_polygon(C):
    """Water as this scene saw it that morning, as one geometry.

    The scene classification layer's own water class picks up building shadows, so a pixel
    counts as water only if it is class 6 *and* dark in the near infrared. Anything under
    two hectares goes, which clears speckle and keeps the lakes."""
    if "geom" in _WATER:
        return _WATER["geom"]
    import numpy as np
    cuts = bands(C)
    nir = gdal.Open(cuts["B08"])
    scls = gdal.Open(cuts["SCL"])
    gt = nir.GetGeoTransform()
    w, h = nir.RasterXSize, nir.RasterYSize
    n = nir.GetRasterBand(1).ReadAsArray().astype("float64") * S2_SCALE + S2_OFFSET
    scl = scls.GetRasterBand(1).ReadAsArray()
    mask = ((scl == SCL_WATER) & (n < NIR_WATER_MAX)).astype("uint8")

    mem = gdal.GetDriverByName("MEM").Create("", w, h, 1, gdal.GDT_Byte)
    mem.SetGeoTransform(gt)
    mem.SetProjection(nir.GetProjection())
    mem.GetRasterBand(1).WriteArray(mask)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(EPSG_OUT)
    vds = ogr.GetDriverByName("MEM").CreateDataSource("w")
    vl = vds.CreateLayer("w", srs, ogr.wkbPolygon)
    vl.CreateField(ogr.FieldDefn("v", ogr.OFTInteger))
    gdal.Polygonize(mem.GetRasterBand(1), mem.GetRasterBand(1), vl, 0)

    union = ogr.Geometry(ogr.wkbMultiPolygon)
    kept = 0
    for f in vl:
        if f.GetField("v") != 1:
            continue
        g = f.GetGeometryRef()
        if g.GetArea() < WATER_MIN_M2:
            continue
        # An island inside a lake comes back as an interior ring; a ring that is only a
        # few pixels is speckle rather than an island, so it is filled in.
        out = ogr.Geometry(ogr.wkbPolygon)
        for r in range(g.GetGeometryCount()):
            ring = g.GetGeometryRef(r)
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring.Clone())
            if r > 0 and poly.GetArea() < WATER_MIN_M2:
                continue
            out.AddGeometry(ring.Clone())
        union.AddGeometry(out)
        kept += 1
    union = union.UnionCascaded()
    union = union.SimplifyPreserveTopology(WATER_SIMPLIFY).Buffer(0)
    sys.stderr.write("water: %d patches, %.1f km2\n" % (kept, union.GetArea() / 1e6))
    _WATER["geom"] = union
    return union


# ---------------------------------------------------------------- greenness

def zonal_ndvi(C, feats):
    """Mean NDVI per area, over the land pixels the scene classifies as usable."""
    import numpy as np
    cuts = bands(C)

    # Hold every dataset in a name. A gdal.Open() chained straight into a band read is
    # collected the moment the expression ends, and the band it handed back stops working.
    red = gdal.Open(cuts["B04"])
    nir = gdal.Open(cuts["B08"])
    scls = gdal.Open(cuts["SCL"])
    gt = red.GetGeoTransform()
    w, h = red.RasterXSize, red.RasterYSize
    r = red.GetRasterBand(1).ReadAsArray().astype("float64")
    n = nir.GetRasterBand(1).ReadAsArray().astype("float64")
    scl = scls.GetRasterBand(1).ReadAsArray()

    valid = (r > 0) & (n > 0)
    keep = np.zeros(scl.shape, dtype=bool)
    for c in SCL_KEEP:
        keep |= (scl == c)
    valid &= keep

    r = r * S2_SCALE + S2_OFFSET
    n = n * S2_SCALE + S2_OFFSET
    den = n + r
    valid &= (den > 0)
    nd = np.zeros(r.shape)
    nd[valid] = (n[valid] - r[valid]) / den[valid]

    # Burn the area index into a raster on exactly the same grid.
    mem = gdal.GetDriverByName("MEM").Create("", w, h, 1, gdal.GDT_Int32)
    mem.SetGeoTransform(gt)
    mem.SetProjection(red.GetProjection())
    mem.GetRasterBand(1).Fill(-1)
    mem.GetRasterBand(1).SetNoDataValue(-1)
    vds = ogr.GetDriverByName("MEM").CreateDataSource("z")
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(EPSG_OUT)
    vl = vds.CreateLayer("z", srs, ogr.wkbPolygon)
    vl.CreateField(ogr.FieldDefn("ix", ogr.OFTInteger))
    for i, (_, g) in enumerate(feats):
        f = ogr.Feature(vl.GetLayerDefn())
        f.SetGeometry(g)
        f.SetField("ix", i)
        vl.CreateFeature(f)
    gdal.RasterizeLayer(mem, [1], vl, options=["ATTRIBUTE=ix"])
    ix = mem.GetRasterBand(1).ReadAsArray()

    N = len(feats)
    tot = np.zeros(N)
    cnt = np.zeros(N, dtype="int64")
    good = valid & (ix >= 0)
    np.add.at(tot, ix[good], nd[good])
    np.add.at(cnt, ix[good], 1)
    out = [float(tot[i] / cnt[i]) if cnt[i] >= 20 else None for i in range(N)]
    sys.stderr.write("greenness: %d areas measured, %d with too few pixels\n"
                     % (sum(1 for v in out if v is not None),
                        sum(1 for v in out if v is None)))
    return out, [int(c) for c in cnt]


# ---------------------------------------------------------------- census

def profile(zip_path, dauids):
    """Pull three characteristics for the wanted areas out of the profile CSV.

    The published file holds every geography in British Columbia at 2,631 rows each, which
    is 3.6 GB of text. The zip also ships a starting-row index, so the rows wanted here are
    known before a byte is read: the file is streamed once, and only the three lines per
    area are parsed."""
    import csv as _csv
    import io as _io

    ix = {d: i for i, d in enumerate(dauids)}
    got = {k: [None] * len(dauids) for k, _, _ in WANT}

    with zipfile.ZipFile(zip_path) as z:
        starts = {}
        with z.open(PROFILE_INDEX) as fh:
            rd = _csv.reader(_io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace"))
            next(rd)
            for row in rd:
                starts[row[0]] = int(row[2])
        wanted = {}
        for d in dauids:
            s0 = starts.get(DA_DGUID + d)
            if s0 is None:
                raise SystemExit("no starting row published for one of the areas")
            for key, cid, name in WANT:
                wanted[s0 + cid - 1] = (d, key, cid, name)
        last = max(wanted)
        sys.stderr.write("reading %d rows out of %s\n" % (len(wanted), PROFILE_MEMBER))

        with z.open(PROFILE_MEMBER) as fh:
            t = _io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace", newline="")
            rd = _csv.reader(t)
            cols = next(rd)
            ci = {c: i for i, c in enumerate(cols)}
            n = 1
            for row in rd:
                n += 1
                if n > last:
                    break
                w = wanted.get(n)
                if w is None:
                    continue
                d, key, cid, name = w
                # Three assertions, because a row read by position is a claim about the
                # file's shape and the file is not going to complain.
                if row[ci["ALT_GEO_CODE"]] != d or row[ci["GEO_LEVEL"]] != "Dissemination area":
                    raise SystemExit("row %d is not the area it should be (%s)" % (n, row[ci["ALT_GEO_CODE"]]))
                if row[ci["CHARACTERISTIC_ID"]] != str(cid) or row[ci["CHARACTERISTIC_NAME"]].strip() != name:
                    raise SystemExit("row %d is not %r but %r"
                                     % (n, name, row[ci["CHARACTERISTIC_NAME"]].strip()))
                v = row[ci["C1_COUNT_TOTAL"]].strip()
                got[key][ix[d]] = None if v in ("", "..", "...", "F", "x") else float(v)

    for key, _, name in WANT:
        n_have = sum(1 for v in got[key] if v is not None)
        sys.stderr.write("%-4s %-60s %d of %d\n" % (key, name, n_have, len(dauids)))
    return got


# ---------------------------------------------------------------- adjacency

def centres(qrings):
    """The centre of each area's largest ring, flat as x0, y0, x1, y1, ..."""
    out = []
    for rings in qrings:
        best = None
        for pts in rings:
            a = cx = cy = 0.0
            m = len(pts)
            for i in range(m):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % m]
                cr = x1 * y2 - x2 * y1
                a += cr
                cx += (x1 + x2) * cr
                cy += (y1 + y2) * cr
            a *= 0.5
            if a != 0 and (best is None or abs(a) > best[2]):
                best = (cx / (6 * a), cy / (6 * a), abs(a))
        out.append(best[0] if best else 0.0)
        out.append(best[1] if best else 0.0)
    return out


def adjacency(qrings):
    edge = {}
    for i, rs in enumerate(qrings):
        for r in rs:
            for k in range(len(r)):
                a, b = r[k], r[(k + 1) % len(r)]
                key = (a, b) if a < b else (b, a)
                edge.setdefault(key, set()).add(i)
    nbr = [set() for _ in qrings]
    for owners in edge.values():
        o = list(owners)
        for i in range(len(o)):
            for j in range(i + 1, len(o)):
                nbr[o[i]].add(o[j])
                nbr[o[j]].add(o[i])
    return [sorted(s) for s in nbr]


# ---------------------------------------------------------------- the search

def fit(xs, ys):
    """Ordinary least squares of y on x, one point per zone, unweighted."""
    n = len(xs)
    if n < 3:
        return 0.0, 0.0, n
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx <= 0 or syy <= 0:
        return 0.0, 0.0, n
    return sxy / sxx, sxy / math.sqrt(sxx * syy), n


class Sums(object):
    """Running per-zone totals, so moving one area between zones costs O(1) rather than
    a pass over the city. Income is the household-weighted mean of the areas' medians,
    which is the widget's default rule; greenness is the mean over the zone's pixels,
    which is what an area-weighted mean of area means comes to."""

    def __init__(self, zone, k, hh, inc, nd, px):
        self.k = k
        self.hh, self.inc, self.nd, self.px = hh, inc, nd, px
        self.iw = [0.0] * k          # household weight carrying an income
        self.iv = [0.0] * k          # household-weighted income
        self.gw = [0.0] * k          # pixels carrying a greenness
        self.gv = [0.0] * k          # pixel-weighted greenness
        for i, z in enumerate(zone):
            self.add(i, z, +1)

    def add(self, i, z, s):
        h, v, g, p = self.hh[i], self.inc[i], self.nd[i], self.px[i]
        # One inclusion rule, and it is the widget's: an area counts only where income,
        # greenness and a household count all exist. Letting greenness in from an area
        # whose income is suppressed made the search optimise a quantity the page does not
        # show, and the two then disagreed in the third decimal place.
        if not (h and v is not None and g is not None and p):
            return
        self.iw[z] += s * h
        self.iv[z] += s * h * v
        self.gw[z] += s * p
        self.gv[z] += s * p * g

    def points(self):
        xs, ys = [], []
        for z in range(self.k):
            if self.iw[z] > 0 and self.gw[z] > 0:
                xs.append(self.iv[z] / self.iw[z] / 1000.0)
                ys.append(self.gv[z] / self.gw[z])
        return xs, ys

    def fit(self):
        return fit(*self.points())


def grow(nbr, weights, k, seed):
    """k contiguous zones grown from k seeds, always extending whichever holds least.
    Real census units are built to hold similar populations, so a balanced growth is the
    fair starting point: it makes the comparison about where the lines are rather than
    about how uneven the areas are."""
    import heapq
    rnd = random.Random(seed)
    n = len(nbr)
    zone = [-1] * n
    starts = rnd.sample(range(n), k)
    load = [0.0] * k
    heap = []
    for z, s in enumerate(starts):
        zone[s] = z
        load[z] = weights[s]
        for j in nbr[s]:
            if zone[j] < 0:
                heapq.heappush(heap, (load[z], z, j))
    while heap:
        l, z, cell = heapq.heappop(heap)
        if zone[cell] >= 0:
            continue
        if l != load[z]:
            heapq.heappush(heap, (load[z], z, cell))
            continue
        zone[cell] = z
        load[z] += weights[cell]
        for j in nbr[cell]:
            if zone[j] < 0:
                heapq.heappush(heap, (load[z], z, j))
    left = [i for i in range(n) if zone[i] < 0]
    if left:
        done = [i for i in range(n) if zone[i] >= 0]
        for i in left:
            zone[i] = zone[done[0]]
    return zone


def still_connected(nbr, zone, z, drop):
    """Would zone z stay in one piece if this area left it? A zoning whose zones are not
    connected is not a zoning anybody could defend, so the search will not make one."""
    members = [i for i in range(len(zone)) if zone[i] == z and i != drop]
    if not members:
        return False
    want = set(members)
    seen = {members[0]}
    stack = [members[0]]
    while stack:
        c = stack.pop()
        for j in nbr[c]:
            if j in want and j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == len(members)


def wedges(cent, k, turn, cx, cy):
    """k sectors around a centre. A planner's radial districting, and the one family here
    that reliably cuts across a gradient rather than following it."""
    out = []
    for i in range(len(cent) // 2):
        a = math.atan2(cent[i * 2 + 1] - cy, cent[i * 2] - cx) + turn
        out.append(int((a % (2 * math.pi)) / (2 * math.pi) * k) % k)
    return out


def strips(cent, k, angle):
    """k bands of equal width laid across the city at one angle. A plan that splits a place
    along an axis: north from south, or east from west, or anything between."""
    ca, sa = math.cos(angle), math.sin(angle)
    ds = [cent[i * 2] * ca + cent[i * 2 + 1] * sa for i in range(len(cent) // 2)]
    lo, hi = min(ds), max(ds)
    span = (hi - lo) or 1.0
    return [min(k - 1, int((d - lo) / span * k)) for d in ds]


def regroup(parent, npar, nbr, weights, k, seed):
    """Group an existing set of published areas into k contiguous groups of roughly equal
    households. This is how a zoning gets built in practice: from units somebody else
    already drew, not from scratch."""
    import heapq
    pw = [0.0] * npar
    for i, pz in enumerate(parent):
        pw[pz] += weights[i]
    pnbr = [set() for _ in range(npar)]
    for i, ns in enumerate(nbr):
        for j in ns:
            if parent[j] != parent[i]:
                pnbr[parent[i]].add(parent[j])
    pnbr = [sorted(x) for x in pnbr]
    grp = grow(pnbr, pw, k, seed)
    return [grp[pz] for pz in parent]


def relabel(zone, k):
    """Zone numbers in a fixed order, so a rebuild names the same zone the same thing."""
    seen = {}
    for z in zone:
        if z not in seen:
            seen[z] = len(seen)
    return [seen[z] for z in zone], len(seen)


CENTS = []


def farthest_seeds(cent, k, first):
    """k starting areas, each the one furthest from everything already chosen. No random
    numbers anywhere: given the first area, the other seven follow."""
    n = len(cent) // 2
    seeds = [first]
    d = [((cent[i * 2] - cent[first * 2]) ** 2 +
          (cent[i * 2 + 1] - cent[first * 2 + 1]) ** 2) for i in range(n)]
    while len(seeds) < k:
        nxt = max(range(n), key=lambda i: d[i])
        seeds.append(nxt)
        for i in range(n):
            dd = ((cent[i * 2] - cent[nxt * 2]) ** 2 + (cent[i * 2 + 1] - cent[nxt * 2 + 1]) ** 2)
            if dd < d[i]:
                d[i] = dd
    return seeds


def grow_from(nbr, weights, seeds):
    """Grow zones outward from stated seeds, always extending whichever holds least."""
    import heapq
    k = len(seeds)
    n = len(nbr)
    zone = [-1] * n
    load = [0.0] * k
    heap = []
    for z, sd in enumerate(seeds):
        zone[sd] = z
        load[z] = weights[sd]
        for j in nbr[sd]:
            if zone[j] < 0:
                heapq.heappush(heap, (load[z], z, j))
    while heap:
        l, z, cell = heapq.heappop(heap)
        if zone[cell] >= 0:
            continue
        if l != load[z]:
            heapq.heappush(heap, (load[z], z, cell))
            continue
        zone[cell] = z
        load[z] += weights[cell]
        for j in nbr[cell]:
            if zone[j] < 0:
                heapq.heappush(heap, (load[z], z, j))
    # Anything the growth could not reach is on the far side of water. It joins the zone
    # whose nearest member it is; leaving it unassigned would quietly make a ninth zone.
    left = [i for i in range(n) if zone[i] < 0]
    if left:
        done = [i for i in range(n) if zone[i] >= 0]
        for i in left:
            j = min(done, key=lambda t: (CENTS[t * 2] - CENTS[i * 2]) ** 2 +
                                        (CENTS[t * 2 + 1] - CENTS[i * 2 + 1]) ** 2)
            zone[i] = zone[j]
    return zone


def rings(cent, k, cx, cy):
    """k rings of equal area around a point, which is how a plan talks about a core and
    its edges."""
    n = len(cent) // 2
    d = [math.hypot(cent[i * 2] - cx, cent[i * 2 + 1] - cy) for i in range(n)]
    order = sorted(range(n), key=lambda i: d[i])
    out = [0] * n
    for rank, i in enumerate(order):
        out[i] = min(k - 1, rank * k // n)
    return out


def run_split(parent, npar, order, weights, k):
    """Walk somebody else's areas in a stated order and cut the walk into k runs of equal
    households. Nothing is split that they did not split."""
    pw = [0.0] * npar
    for i, pz in enumerate(parent):
        pw[pz] += weights[i]
    total = sum(pw) or 1.0
    grp, run, z = [0] * npar, 0.0, 0
    for pz in order:
        grp[pz] = min(k - 1, z)
        run += pw[pz]
        if run >= total * (z + 1) / k:
            z += 1
    return [grp[pz] for pz in parent]


def parent_order(parent, npar, cent, angle):
    """Somebody else's areas, in order along one direction."""
    sx, sy, c = [0.0] * npar, [0.0] * npar, [0] * npar
    for i, pz in enumerate(parent):
        sx[pz] += cent[i * 2]
        sy[pz] += cent[i * 2 + 1]
        c[pz] += 1
    ca, sa = math.cos(angle), math.sin(angle)
    key = [(sx[z] / c[z] * ca + sy[z] / c[z] * sa) if c[z] else 0.0 for z in range(npar)]
    return sorted(range(npar), key=lambda z: key[z])


# Forty zonings, ten for each of the four things a preset is there to show, each one a
# rule written down before it was run. Nothing here is searched and nothing is random: the
# only inputs are the geometry, the household counts and the published boundaries.
GROUPS = [
    ("across", "cut across the grain of the city",
     "Zones that each reach from one side of the city to the other, so every zone holds "
     "some of everything. A radial plan, or rings around a core."),
    ("follow", "follow published lines",
     "Zones built from whole units somebody else already drew, walked in one direction "
     "and cut into eight runs of equal households."),
    ("along", "follow the grain of the city",
     "Eight bands of equal width laid across the city, at eight angles, plus two grids."),
    ("equal", "equal households, grown outward",
     "Eight zones grown from eight starting areas as far apart as the city allows, each "
     "taking the next area until the households even out."),
]


def candidates(nbr, attrs, ndvi, ndvipx, cent, k):
    """Forty zonings, ten per group, each named for the rule that drew it.

    An earlier version of this generated a hundred-odd zonings from seeded region growing
    and kept the ones that disagreed most. The rules were fair; the seeds were not stated,
    so the answer was reproducible without being explicable, and a student could not be
    told what the preset *is*. These forty can each be described in a sentence."""
    n = len(nbr)
    hh = [attrs["hh"][i] or 0.0 for i in range(n)]
    inc = attrs["inc"]
    ones = [1.0] * n
    xs = [cent[i * 2] for i in range(n)]
    ys = [cent[i * 2 + 1] for i in range(n)]
    cx, cy = sum(xs) / n, sum(ys) / n
    global CENTS
    CENTS = cent
    # Three stated centres: the middle of the city, its north-west corner (the downtown
    # peninsula) and its south-east corner. Named by position, not by place, because the
    # page does not name places.
    centres = [("the middle of the city", cx, cy),
               ("the north-west of the city", min(xs) + (max(xs) - min(xs)) * 0.2,
                max(ys) - (max(ys) - min(ys)) * 0.2),
               ("the south-east of the city", max(xs) - (max(xs) - min(xs)) * 0.2,
                min(ys) + (max(ys) - min(ys)) * 0.2)]
    out = []

    def add(group, label, zone, note):
        z, kk = relabel(tidy(nbr, zone, k), k)
        S = Sums(z, kk, hh, inc, ndvi, ndvipx)
        slope, r, cnt = S.fit()
        out.append({"group": group, "label": label, "zone": z, "k": kk, "note": note,
                    "slope": slope, "r": r, "n": cnt, "pieces": count_pieces(nbr, z)})

    # --- ten that cut across the grain ---------------------------------------
    for name, px, py in centres:
        for t, turn in enumerate([0.0, 1.0 / 3, 2.0 / 3]):
            add("across", "Wedges from %s" % name.split(" of ")[0].replace("the ", ""),
                wedges(cent, k, turn * 2 * math.pi / k, px, py),
                "eight sectors around %s, turned %d degrees" % (name, round(turn * 360.0 / k)))
    add("across", "Rings from the middle", rings(cent, k, cx, cy),
        "eight rings of equal area around the middle of the city, a core and its edges")

    # --- ten that follow published lines --------------------------------------
    # Named for the bands the walk produces rather than for the walk: walking west to east
    # and cutting the walk into runs leaves eight north-south bands, which is what somebody
    # looking at the map sees.
    dirs = [("west to east", 0.0, "North-south groups"),
            ("south to north", math.pi / 2, "East-west groups"),
            ("south-west to north-east", math.pi / 4, "Diagonal groups"),
            ("north-west to south-east", -math.pi / 4, "Diagonal groups"),
            ("along the long axis", math.radians(20), "Cross-city groups")]
    for what, parent, npar, plain in (("census tracts", attrs["ct"], attrs["nct"], True),
                                      ("the city's neighbourhoods", attrs["la"], attrs["nla"], False)):
        for dname, ang, bands in dirs:
            add("follow", bands if plain else "City neighbourhoods",
                run_split(parent, npar, parent_order(parent, npar, cent, ang), hh, k),
                "whole %s walked %s and cut into eight runs of equal households"
                % (what, dname))

    # --- ten that follow the grain --------------------------------------------
    for a in range(8):
        add("along", "Bands across the city", strips(cent, k, a * math.pi / 8),
            "eight bands of equal width at %d degrees" % round(a * 180.0 / 8))
    for rows, cols in ((2, 4), (4, 2)):
        add("along", "A grid of blocks",
            [min(k - 1, (min(rows - 1, int((ys[i] - min(ys)) / ((max(ys) - min(ys)) or 1) * rows))) * cols
                 + min(cols - 1, int((xs[i] - min(xs)) / ((max(xs) - min(xs)) or 1) * cols)))
             for i in range(n)],
            "a %d by %d grid laid over the city" % (rows, cols))

    # --- ten grown to equal households ----------------------------------------
    corners = [(min(xs), min(ys)), (min(xs), max(ys)), (max(xs), min(ys)), (max(xs), max(ys)),
               (cx, min(ys)), (cx, max(ys)), (min(xs), cy), (max(xs), cy), (cx, cy)]
    names = ["south-west", "north-west", "south-east", "north-east", "south", "north",
             "west", "east", "middle"]
    for (px, py), nm in zip(corners, names):
        first = min(range(n), key=lambda i: (xs[i] - px) ** 2 + (ys[i] - py) ** 2)
        add("equal", "Same number of households", grow_from(nbr, hh, farthest_seeds(cent, k, first)),
            "grown from eight starting areas as far apart as possible, the first in the "
            "%s of the city, until the households even out" % nm)
    first = min(range(n), key=lambda i: (xs[i] - cx) ** 2 + (ys[i] - cy) ** 2)
    add("equal", "Compact blocks", grow_from(nbr, ones, farthest_seeds(cent, k, first)),
        "grown from the same eight starting areas at the same rate, so every zone covers "
        "about the same number of areas")
    return out


def tidy(nbr, zone, k):
    """Leave every zone in one piece.

    A rule stated in words rarely comes out contiguous on real ground: a band crosses an
    inlet, a group of neighbourhoods has an outlier. So every candidate is tidied the same
    way, and the tidying is part of the rule rather than a repair hidden from the reader:
    each zone keeps its largest piece, and every other piece joins whichever neighbouring
    zone it shares the most areas with."""
    n = len(zone)
    zone = list(zone)
    for _ in range(12):
        comp = [-1] * n
        comps = []
        for i in range(n):
            if comp[i] >= 0:
                continue
            c = len(comps)
            members = [i]
            comp[i] = c
            stack = [i]
            while stack:
                a = stack.pop()
                for j in nbr[a]:
                    if comp[j] < 0 and zone[j] == zone[a]:
                        comp[j] = c
                        members.append(j)
                        stack.append(j)
            comps.append(members)
        biggest = {}
        for c, m in enumerate(comps):
            z = zone[m[0]]
            if z not in biggest or len(m) > len(comps[biggest[z]]):
                biggest[z] = c
        moved = False
        for c, m in enumerate(comps):
            z = zone[m[0]]
            if biggest.get(z) == c:
                continue
            votes = {}
            for a in m:
                for j in nbr[a]:
                    if zone[j] != z:
                        votes[zone[j]] = votes.get(zone[j], 0) + 1
            if not votes:
                continue                      # an island: nothing to join
            to = max(votes, key=lambda t: (votes[t], -t))
            for a in m:
                zone[a] = to
            moved = True
        if not moved:
            break
    return zone


def count_pieces(nbr, zone):
    seen = [0] * len(zone)
    out = 0
    for i in range(len(zone)):
        if seen[i]:
            continue
        out += 1
        seen[i] = 1
        stack = [i]
        while stack:
            c = stack.pop()
            for j in nbr[c]:
                if not seen[j] and zone[j] == zone[c]:
                    seen[j] = 1
                    stack.append(j)
    return out


def still_connected(nbr, zone, z, drop):
    """Would zone z stay in one piece if this area left it?"""
    members = [i for i in range(len(zone)) if zone[i] == z and i != drop]
    if not members:
        return False
    want = set(members)
    seen = {members[0]}
    stack = [members[0]]
    while stack:
        c = stack.pop()
        for j in nbr[c]:
            if j in want and j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == len(members)


def flattened(nbr, attrs, ndvi, ndvipx, k):
    """One zoning searched for its effect rather than stated as a rule: move boundary areas
    between neighbouring zones, keeping every move that brings the correlation nearer zero
    and leaves the zone they left in one piece.

    It is kept apart from the four above, and the page says what it is. Openshaw called
    this applied gerrymandering and drove an Iowa correlation from -0.99 to +0.99 by
    choosing where the lines went. Without it the page would only be able to show
    aggregation raising the correlation, which is a rule the deck's own slide states and
    which is false."""
    n = len(nbr)
    hh = [attrs["hh"][i] or 0.0 for i in range(n)]
    inc = attrs["inc"]
    best = None
    for seed in SEEDS_SEARCH:
        zone = grow(nbr, hh, k, seed)
        S = Sums(zone, k, hh, inc, ndvi, ndvipx)
        cur = -abs(S.fit()[1])
        for _ in range(40):
            moved = False
            for i in range(n):
                z = zone[i]
                for j in nbr[i]:
                    nz = zone[j]
                    if nz == z:
                        continue
                    S.add(i, z, -1)
                    S.add(i, nz, +1)
                    val = -abs(S.fit()[1])
                    if val > cur + 1e-12 and still_connected(nbr, zone, z, i):
                        zone[i] = nz
                        cur = val
                        z = nz
                        moved = True
                    else:
                        S.add(i, nz, -1)
                        S.add(i, z, +1)
            if not moved:
                break
        if best is None or cur > best[0]:
            best = (cur, list(zone))
    z, kk = relabel(best[1], k)
    S = Sums(z, kk, hh, inc, ndvi, ndvipx)
    slope, r, cnt = S.fit()
    sys.stderr.write("%-26s r %+0.4f  slope %+0.6f  n %d  pieces %d\n"
                     % ("Drawn to flatten the line", r, slope, cnt, count_pieces(nbr, z)))
    return {"zone": z, "k": kk, "label": "Drawn to flatten the line",
            "note": "searched for: areas moved between neighbouring zones, over and over, "
                    "keeping every move that brought the correlation nearer zero",
            "slope": round(slope, 6), "r": round(r, 4), "n": cnt,
            "pieces": count_pieces(nbr, z), "seeds": list(SEEDS_SEARCH)}


def search_zonings(nbr, attrs, ndvi, ndvipx, cent, k):
    """Generate the principled candidates, then keep the four that disagree most.

    An earlier version of this searched for zonings that steepened, flattened or reversed
    the line. It worked, and it taught the wrong thing: a zoning built by a computer told
    to move a statistic is not a zoning anybody would defend, so a student could set the
    whole page aside as a trick. These are rules a census office or a planner states in
    advance, and they still disagree."""
    # The ground itself is in more than one piece: Richmond is across the Fraser from
    # Vancouver and Sea Island is across another arm, so no zoning of this set can have
    # eight zones in eight pieces. A zoning counts as contiguous when it is in as few
    # pieces as the ground allows.
    base = count_pieces(nbr, [0] * len(nbr))
    allowed = k + base - 1
    sys.stderr.write("the ground is in %d pieces, so a contiguous zoning is in %d\n"
                     % (base, allowed))
    cands = candidates(nbr, attrs, ndvi, ndvipx, cent, k)
    for c in cands:
        sys.stderr.write("  %-8s %-30s r %+0.4f  slope %+0.6f  n %d  pieces %d  | %s\n"
                         % (c["group"], c["label"], c["r"], c["slope"], c["n"],
                            c["pieces"], c["note"]))
    # Each group is ten rules aimed at one of the four things a preset is here to show, and
    # the one shipped is the best of its own ten. Where a role cannot be filled - no group
    # here produces a negative slope over this city - the best available stands in and the
    # widget's file says so rather than the page pretending otherwise.
    def choose(group, key):
        same = [c for c in cands if c["group"] == group and c["pieces"] <= allowed
                and c["n"] == c["k"] and c["k"] == k]
        if not same:
            sys.stderr.write("WARNING: no candidate in group %s is eight zones in eight "
                             "pieces; falling back\n" % group)
            same = [c for c in cands if c["group"] == group]
        return sorted(same, key=key)[0]

    best = [
        choose("across", lambda c: c["r"]),                  # the weakest correlation
        choose("along", lambda c: -c["r"]),                  # the strongest
        choose("follow", lambda c: -c["slope"]),             # the steepest line
        choose("equal", lambda c: c["slope"]),               # the shallowest, or a negative one
    ]
    out = {"pieces_allowed": allowed, "ground_pieces": base}
    for c in best:
        sys.stderr.write("SHIPPED %-30s r %+0.4f  slope %+0.6f  n %d  pieces %d\n"
                         % (c["label"], c["r"], c["slope"], c["n"], c["pieces"]))
        out["z" + str(len(out) + 1)] = {"group": c["group"], "zone": c["zone"], "k": c["k"], "label": c["label"],
                            "note": c["note"], "slope": round(c["slope"], 6),
                            "r": round(c["r"], 4), "n": c["n"], "pieces": c["pieces"]}
    return out


if __name__ == "__main__":
    main()
