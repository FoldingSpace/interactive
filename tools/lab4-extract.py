#!/usr/bin/env python3
"""Build the land use grid for the least-cost path widget.

Source: Metro Vancouver Land Use 2016, "Landuse 2016 - Code Description", published on
the Metro Vancouver Open Data Portal under the Metro Vancouver Open Government Licence.
Polygons arrive in NAD83 / UTM zone 10N (EPSG:26910), which is the projection the grid
uses, so nothing is reprojected.

Needs GDAL's Python bindings and network access. Writes the block of JavaScript that
goes into web/least-cost/index.html.

    python3 tools/lab4-extract.py > /tmp/grid.js

Why these choices, since none of them are forced:

  Window   504000-526000 E, 5428500-5447500 N. Holds the Surrey substation at 124 St
           and 86 Ave, the Campbell Heights industrial district, and enough room either
           side for a route to wander. Entirely inside Metro Vancouver, so there are no
           holes, and clear of every reserve and treaty boundary in the region's
           Jurisdiction field.
  Cells    22 2/9 m, chosen so that 990 cells is exactly the 22 km width. It began at
           100 m, which was fine for blocks of housing and farmland and wrong for
           everything linear: road allowances, rail and watercourses are narrower than
           that, so they rasterised into dotted lines and a route could not follow one.
           50 m joined up the main grid, 33 1/3 m most of the rural lanes, and 22 2/9 m
           the rest. 846450 cells, and the solver runs in a worker to keep up.
  Classes  Metro Vancouver's 29 codes grouped into 8. The grouping is a claim and is
           printed in the widget.
"""

import json, os, sys, urllib.parse, urllib.request, time
import numpy as np
from osgeo import gdal, ogr
gdal.UseExceptions(); ogr.UseExceptions()

SERVICE = ("https://services6.arcgis.com/56eqCzQ5SZhBaDST/arcgis/rest/services/"
           "Landuse_2016___Code_Description_No_Outlines/FeatureServer/1/query")

X0, Y1, W, H = 504000, 5447500, 990, 855
CELL = 200.0 / 9          # 22 2/9 m: 990 cells is exactly the 22 km window

# Class 0 is unused: it means "no land use polygon here", and the window has none.
CLASSES = [
    (1, "Farmland",            ["A500"]),
    (2, "Houses",              ["S100", "S110", "S120", "S130", "S131", "S135",
                                "S410", "S230", "S235"]),
    (3, "Shops and offices",   ["S200", "S202", "S204"]),
    (4, "Industry",            ["S300", "M300", "S600", "T400"]),
    (5, "Schools and civic",   ["S400", "S420", "S450", "S460"]),
    (6, "Parks and protected", ["R100", "W400"]),
    (7, "Water",               ["R200"]),
    (8, "Open land",           ["U100"]),
    (9, "Road and rail",       ["S500", "T100", "T200", "T300"]),
]

# Burn order. Later classes overwrite earlier ones where polygons overlap, so the
# narrow and the specific go last: a school inside a park should read as a school.
BURN_ORDER = [8, 9, 1, 6, 7, 2, 3, 5, 4]


def fetch(path):
    env = "%d,%d,%d,%d" % (X0, Y1 - H * CELL, X0 + W * CELL, Y1)
    feats, off = [], 0
    while True:
        q = urllib.parse.urlencode(dict(
            where="1=1", geometry=env, geometryType="esriGeometryEnvelope",
            inSR="26910", outSR="26910", outFields="LU_Code", returnGeometry="true",
            geometryPrecision="1", f="geojson",
            resultOffset=str(off), resultRecordCount="2000"))
        for attempt in range(4):
            try:
                with urllib.request.urlopen(SERVICE + "?" + q, timeout=120) as r:
                    d = json.load(r)
                break
            except Exception as e:
                sys.stderr.write("retry %d: %s\n" % (attempt, e)); time.sleep(3)
        else:
            raise SystemExit("could not reach the feature service")
        got = d.get("features", [])
        feats += got
        sys.stderr.write("  %d features\n" % len(feats))
        if len(got) < 2000:
            break
        off += 2000
    json.dump({"type": "FeatureCollection", "features": feats}, open(path, "w"))


def main():
    src_json = "/tmp/mv-landuse-window.geojson"
    src_gpkg = "/tmp/mv-landuse-window.gpkg"
    if os.path.exists(src_json) and "--refetch" not in sys.argv:
        sys.stderr.write("reusing %s (pass --refetch to download again)\n" % src_json)
    else:
        sys.stderr.write("fetching Metro Vancouver Land Use 2016...\n")
        fetch(src_json)
    # GeoJSON is assumed to be lon/lat by OGR whatever its contents, so the CRS is
    # attached on the way into a container that can hold one. Without this GDAL tries
    # to reproject UTM metres as degrees and rasterising fails.
    gdal.VectorTranslate(src_gpkg, src_json, dstSRS="EPSG:26910",
                         reproject=False, layerName="lu")

    mem = gdal.GetDriverByName("MEM").Create("", W, H, 1, gdal.GDT_Byte)
    mem.SetGeoTransform((X0, CELL, 0, Y1, 0, -CELL))
    # Hold the data source in a name. If only the layer is kept, Python collects the
    # data source out from under it and every later call fails with a type error.
    vec = ogr.Open(src_gpkg)
    lyr = vec.GetLayer()
    by_code = {c: codes for c, _, codes in CLASSES}
    for c in BURN_ORDER:
        lyr.SetAttributeFilter(" OR ".join("LU_Code='%s'" % k for k in by_code[c]))
        gdal.RasterizeLayer(mem, [1], lyr, burn_values=[c])
        lyr.SetAttributeFilter(None)

    a = mem.GetRasterBand(1).ReadAsArray()

    # Adjacent polygons in the source do not tile perfectly, so at fine cell sizes the
    # occasional cell centre lands in a sliver between two of them. Those get filled from
    # whatever surrounds them. A real hole -- a window reaching outside Metro Vancouver --
    # would be a contiguous region, not a scattering of single cells, so the count is what
    # tells the two apart and a run says which happened.
    holes = int((a == 0).sum())
    limit = max(16, a.size // 10000)
    if holes > limit:
        raise SystemExit("%d cells have no land use polygon, over the %d allowed for "
                         "sliver gaps; the window is probably wrong" % (holes, limit))
    filled = 0
    while holes:
        rs, cs = np.where(a == 0)
        for r, c in zip(rs, cs):
            near = a[max(0, r - 1):r + 2, max(0, c - 1):c + 2]
            near = near[near > 0]
            if near.size:
                a[r, c] = np.bincount(near).argmax()
                filled += 1
        if int((a == 0).sum()) == holes:
            raise SystemExit("%d cells have no land use polygon and no neighbour to take "
                             "one from" % holes)
        holes = int((a == 0).sum())
    if filled:
        sys.stderr.write("  filled %d sliver cell(s) from their neighbours\n" % filled)

    counts = {c: int((a == c).sum()) for c, _, _ in CLASSES}
    for c, name, _ in CLASSES:
        sys.stderr.write("  %-20s %6d  %5.1f%%\n" % (name, counts[c], 100 * counts[c] / a.size))

    # One digit per cell, row-major from the north-west. 41800 characters; the server
    # gzips it to a few kilobytes, which is smaller than any hand-rolled run-length
    # scheme that also has to ship its decoder.
    flat = "".join(str(int(v)) for v in a.ravel())
    print("// Metro Vancouver Land Use 2016, Metro Vancouver Open Government Licence.")
    print("// Built by tools/lab4-extract.py. %d x %d cells of %d m, NAD83 / UTM 10N," % (W, H, CELL))
    print("// north-west corner %d E %d N. One digit per cell, row-major." % (X0, Y1))
    print('var GRID = "%s";' % flat)


if __name__ == "__main__":
    main()
