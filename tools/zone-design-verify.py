#!/usr/bin/env python3
"""Recompute everything the zone-design widget reports, from its shipped data file, by a
route that shares no code with it.

The widget's numbers come out of JavaScript in `web/zone-design/index.html`. These come out
of Python, written from the description in `docs/widgets/zone-design.md` rather than from
that source, and by matrix algebra where the widget uses loops. Agreement is the check;
disagreement is a finding either way round.

    python3 tools/zone-design-verify.py web/zone-design/data.js

Prints a table of r, slope, n and separation for every zoning under every income rule, the
area-level fit, and the counts the widget's file records. Nothing here reads the widget.
"""
import base64
import json
import math
import re
import sys

import numpy as np


def load(path):
    src = open(path, encoding="utf-8").read()
    i = src.index("{")
    j = src.rindex("}")
    return json.loads(src[i:j + 1])


def decode_geom(D):
    raw = base64.b64decode(D["geom"])
    p = 0
    out = []
    x = y = 0
    for lens in D["rings"]:
        rings = []
        for ln in lens:
            pts = []
            for _ in range(ln):
                for axis in (0, 1):
                    shift = 0
                    result = 0
                    while True:
                        b = raw[p]
                        p += 1
                        result |= (b & 0x7F) << shift
                        shift += 7
                        if not (b & 0x80):
                            break
                    v = (result >> 1) ^ -(result & 1)
                    if axis == 0:
                        x += v
                    else:
                        y += v
                pts.append((x, y))
            rings.append(pts)
        out.append(rings)
    assert p == len(raw), "geometry stream has %d bytes left over" % (len(raw) - p)
    return out


def fit(x, y):
    """Least squares of y on x, one point per zone, by the normal equations rather than by
    the covariance shortcut the widget uses."""
    n = len(x)
    if n < 3:
        return None
    X = np.column_stack([np.ones(n), np.asarray(x, dtype=float)])
    yv = np.asarray(y, dtype=float)
    beta = np.linalg.solve(X.T @ X, X.T @ yv)
    pred = X @ beta
    ss_res = float(((yv - pred) ** 2).sum())
    ss_tot = float(((yv - yv.mean()) ** 2).sum())
    r2 = 0.0 if ss_tot == 0 else 1 - ss_res / ss_tot
    r = math.copysign(math.sqrt(max(r2, 0.0)), beta[1])
    return {"a": float(beta[0]), "b": float(beta[1]), "r": r, "n": n}


def zone_points(D, zone, k, weight):
    inc = np.array([np.nan if v is None else v for v in D["inc"]], dtype=float)
    nd = np.array([np.nan if v is None else v for v in D["ndvi"]], dtype=float)
    px = np.array(D["ndvipx"], dtype=float)
    hh = np.array([0.0 if v is None else v for v in D["hh"]], dtype=float)
    pop = np.array([0.0 if v is None else v for v in D["pop"]], dtype=float)
    ok = np.isfinite(inc) & np.isfinite(nd) & (hh > 0)
    w = {"hh": hh, "pop": pop, "plain": np.ones_like(hh)}[weight]
    z = np.asarray(zone)
    xs, ys = [], []
    for zz in range(k):
        m = ok & (z == zz)
        wm = w[m]
        if wm.sum() > 0 and px[m].sum() > 0:
            xs.append(float((wm * inc[m]).sum() / wm.sum() / 1000.0))
            ys.append(float((px[m] * nd[m]).sum() / px[m].sum()))
    return xs, ys


def separation(D, zone, k, weight):
    inc = np.array([np.nan if v is None else v for v in D["inc"]], dtype=float)
    nd = np.array([np.nan if v is None else v for v in D["ndvi"]], dtype=float)
    hh = np.array([0.0 if v is None else v for v in D["hh"]], dtype=float)
    pop = np.array([0.0 if v is None else v for v in D["pop"]], dtype=float)
    ok = np.isfinite(inc) & np.isfinite(nd) & (hh > 0)
    w = {"hh": hh, "pop": pop, "plain": np.ones_like(hh)}[weight].copy()
    w[~ok] = 0.0
    if w.sum() <= 0:
        return None
    gm = float((w * np.nan_to_num(inc)).sum() / w.sum())
    tot = float((w * (np.nan_to_num(inc) - gm) ** 2).sum())
    z = np.asarray(zone)
    between = 0.0
    for zz in range(k):
        m = (z == zz) & (w > 0)
        if not m.any():
            continue
        ww = w[m].sum()
        mean = float((w[m] * inc[m]).sum() / ww)
        between += ww * (mean - gm) ** 2
    return None if tot <= 0 else between / tot


def zonings(D):
    out = [("da", list(range(D["n"])), D["n"]),
           ("ct", D["ct"], D["nct"]),
           ("la", D["la"], len(D["laname"]))]
    for name in sorted(D["zonings"]):
        z = D["zonings"][name]
        if isinstance(z, dict):
            out.append((name, z["zone"], z["k"]))
    return out


def main(path):
    D = load(path)
    geom = decode_geom(D)
    verts = sum(len(r) for f in geom for r in f)

    # Adjacency, rebuilt from the shared quantised vertices rather than read from the file.
    edge = {}
    for i, rings in enumerate(geom):
        for r in rings:
            for k in range(len(r)):
                a, b = r[k], r[(k + 1) % len(r)]
                key = (a, b) if a < b else (b, a)
                edge.setdefault(key, set()).add(i)
    nbr = [set() for _ in geom]
    for owners in edge.values():
        o = sorted(owners)
        for i in range(len(o)):
            for j in range(i + 1, len(o)):
                nbr[o[i]].add(o[j])
                nbr[o[j]].add(o[i])
    shipped = [set(x) for x in D["nbr"]]
    same = all(a == b for a, b in zip(nbr, shipped))
    degs = [len(s) for s in nbr]

    inc = [v for v in D["inc"] if v is not None]
    nd = [v for v in D["ndvi"] if v is not None]
    ok = sum(1 for i in range(D["n"])
             if D["inc"][i] is not None and D["ndvi"][i] is not None
             and D["hh"][i] not in (None, 0))

    print("areas                 %d" % D["n"])
    print("with both figures     %d" % ok)
    print("vertices              %d" % verts)
    print("encoded geometry      %d bytes" % len(base64.b64decode(D["geom"])))
    print("neighbours            min %d  mean %.2f  max %d  isolated %d"
          % (min(degs), sum(degs) / len(degs), max(degs), sum(1 for d in degs if d == 0)))
    print("shipped adjacency     %s" % ("matches" if same else "DIFFERS"))
    print("census tracts         %d" % D["nct"])
    print("local areas           %d" % len(D["laname"]))
    print("income                min %d  median %d  max %d"
          % (min(inc), sorted(inc)[len(inc) // 2], max(inc)))
    print("greenness             min %.4f  mean %.4f  max %.4f"
          % (min(nd), sum(nd) / len(nd), max(nd)))
    print("scene                 %s  %s" % (D["scene"], D["scenedate"]))
    print()

    da_x = [D["inc"][i] / 1000.0 for i in range(D["n"])
            if D["inc"][i] is not None and D["ndvi"][i] is not None and D["hh"][i]]
    da_y = [D["ndvi"][i] for i in range(D["n"])
            if D["inc"][i] is not None and D["ndvi"][i] is not None and D["hh"][i]]
    f = fit(da_x, da_y)
    print("area level            r %+0.6f  slope %+0.6f  n %d" % (f["r"], f["b"], f["n"]))
    print()
    print("%-10s %-6s %10s %12s %10s %10s" % ("zoning", "rule", "r", "slope", "n", "separation"))
    for name, zone, k in zonings(D):
        for rule in ("hh", "pop", "plain"):
            xs, ys = zone_points(D, zone, k, rule)
            ff = fit(xs, ys)
            sep = separation(D, zone, k, rule)
            if ff is None:
                print("%-10s %-6s %10s" % (name, rule, "too few"))
                continue
            print("%-10s %-6s %+10.6f %+12.6f %10d %9.2f%%"
                  % (name, rule, ff["r"], ff["b"], ff["n"], 100 * sep))

    # What the extraction recorded for the searched zonings, against what comes back here.
    print()
    for name in sorted(k for k in D["zonings"] if isinstance(D["zonings"][k], dict)):
        z = D["zonings"][name]
        xs, ys = zone_points(D, z["zone"], z["k"], "hh")
        ff = fit(xs, ys)
        dr = abs(ff["r"] - z["r"])
        db = abs(ff["b"] - z["slope"])
        print("%-10s recorded r %+0.4f slope %+0.6f ; recomputed %+0.6f %+0.6f ; "
              "differs by %.2e and %.2e" % (name, z["r"], z["slope"], ff["r"], ff["b"], dr, db))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "web/zone-design/data.js")
