#!/usr/bin/env python3
"""Turn the Lab 3 geodatabase into the data block the MAUP widget embeds.

Source (not in this repository, course material):
  370 - 2024/Lab3/Lab3/MAUP.gdb

Ships: dissemination-area boundaries and three census attributes (Statistics Canada),
plus a count per DA of reported incidents in several crime categories (City of Vancouver
open data). Does NOT ship the City boundary layer, which is DMTI and not openly licensed,
and does NOT ship residential break and enter, which is the category the lab models.

Geometry is quantised to a 2 m grid in BC Albers (EPSG:3005) and delta-encoded as
base64 varints. Quantising before encoding snaps shared boundaries to identical
vertices, so neighbouring polygons stay coincident and adjacency can be read straight
off the shared vertices.

Usage:  python3 tools/lab3-extract.py <path to MAUP.gdb> > web/maup/data.js
"""
import sys, json, base64
from osgeo import ogr

ogr.UseExceptions()

Q = 2.0                      # quantisation, metres

# Residential break and enter is deliberately NOT among these. It is the category the
# GEOG 370 lab models, and a widget that reproduced the lab's numbers would be an answer
# key. These four are the same records, the same city and the same method, so everything
# the widget teaches still holds, and comparing categories that are reported at very
# different rates is a better lesson than repeating one.
# Order matters: the first is the widget's default. Bicycle theft leads because it is
# mundane, because its under-reporting is well known, and because the result it gives is
# deflationary — a coefficient that looks solid across 996 areas dissolves across 118.
# Mischief is offered but not defaulted to: a negative income coefficient on a category
# whose name sounds like a judgement of people is the single result here most open to
# being misread, so it is reached deliberately rather than met on arrival.
TYPES = [
    ("bicycle",  "Theft of Bicycle"),
    ("vehicle",  "Theft from Vehicle"),
    ("commerc",  "Break and Enter Commercial"),
    ("mischief", "Mischief"),
]


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


def main(gdb):
    ds = ogr.Open(gdb)
    da = ds.GetLayerByName("Van_DA")
    crimes = ds.GetLayerByName("van_crimes")
    totals = {}
    for key, label in TYPES:
        crimes.SetAttributeFilter("TYPE = '%s'" % label)
        totals[key] = crimes.GetFeatureCount()

    # bounding box first, so quantisation is relative to it
    x0, x1, y0, y1 = da.GetExtent()[0], da.GetExtent()[1], da.GetExtent()[2], da.GetExtent()[3]

    feats = []
    da.ResetReading()
    for f in da:
        g = f.GetGeometryRef()
        rings = []
        for i in range(g.GetGeometryCount()):
            poly = g.GetGeometryRef(i)
            for j in range(poly.GetGeometryCount()):
                r = poly.GetGeometryRef(j)
                pts = []
                for k in range(r.GetPointCount()):
                    px, py = r.GetPoint(k)[:2]
                    qx = int(round((px - x0) / Q))
                    qy = int(round((py - y0) / Q))
                    if not pts or pts[-1] != (qx, qy):
                        pts.append((qx, qy))
                if len(pts) > 1 and pts[0] == pts[-1]:
                    pts.pop()
                if len(pts) >= 3:
                    rings.append(pts)
        # count the points of each type inside this DA
        counts = {}
        for key, label in TYPES:
            crimes.SetAttributeFilter("TYPE = '%s'" % label)
            crimes.ResetReading()
            crimes.SetSpatialFilter(g)
            counts[key] = sum(1 for c in crimes if g.Contains(c.GetGeometryRef()))
        feats.append({
            "dauid": f.GetField("DAUID"),
            "ctuid": f.GetField("CTUID"),
            "pop": f.GetField("Pop"),
            "hh": f.GetField("Tot_Private"),
            "inc": f.GetField("MedHHInc"),
            "counts": counts,
            "rings": rings,
        })

    # ---- adjacency from shared quantised vertices (queen contiguity) ----
    at = {}
    for idx, ft in enumerate(feats):
        for ring in ft["rings"]:
            for p in ring:
                at.setdefault(p, set()).add(idx)
    nbr = [set() for _ in feats]
    for owners in at.values():
        if len(owners) > 1:
            for a in owners:
                nbr[a].update(owners)
    for i, s in enumerate(nbr):
        s.discard(i)

    # ---- census tracts, in a stable order ----
    cts = sorted({ft["ctuid"] for ft in feats})
    ct_of = [cts.index(ft["ctuid"]) for ft in feats]

    # ---- encode geometry ----
    buf = bytearray()
    ring_index = []       # per feature: list of ring lengths
    px = py = 0
    for ft in feats:
        lens = []
        for ring in ft["rings"]:
            lens.append(len(ring))
            for (x, y) in ring:
                varint(x - px, buf)
                varint(y - py, buf)
                px, py = x, y
        ring_index.append(lens)

    data = {
        "note": "Lab 3 (GEOG 370) data. See docs/widgets/maup.md.",
        "quant": Q,
        "origin": [round(x0, 2), round(y0, 2)],
        "size": [int(round((x1 - x0) / Q)), int(round((y1 - y0) / Q))],
        "n": len(feats),
        "geom": base64.b64encode(bytes(buf)).decode("ascii"),
        "rings": ring_index,
        "ct": ct_of,
        "ctuid": cts,
        "dauid": [ft["dauid"] for ft in feats],
        "pop": [ft["pop"] for ft in feats],
        "hh": [ft["hh"] for ft in feats],
        "inc": [ft["inc"] for ft in feats],
        "types": [{"key": k, "label": l} for k, l in TYPES],
        "crime": dict((k, [ft["counts"][k] for ft in feats]) for k, l in TYPES),
        "nbr": [sorted(s) for s in nbr],
    }

    sys.stderr.write(
        "DAs %d  CTs %d  vertices %d  geom bytes %d\n"
        % (len(feats), len(cts), sum(sum(l) for l in ring_index), len(buf)))
    for key, label in TYPES:
        sys.stderr.write("  %-8s %-30s %6d in the layer, %6d inside a DA\n"
                         % (key, label, totals[key], sum(data["crime"][key])))
    sys.stderr.write(
        "sum households %d  sum pop %d  DAs with a null attribute %d\n"
        % (sum(v or 0 for v in data["hh"]), sum(v or 0 for v in data["pop"]),
           sum(1 for ft in feats if ft["hh"] is None or ft["inc"] is None)))
    sys.stderr.write(
        "neighbours per DA: min %d  mean %.2f  max %d\n"
        % (min(len(s) for s in nbr), sum(len(s) for s in nbr) / len(nbr),
           max(len(s) for s in nbr)))

    print("var LAB3 = " + json.dumps(data, separators=(",", ":")) + ";")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "MAUP.gdb")
