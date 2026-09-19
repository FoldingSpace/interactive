"""Independent check of the pairwise weights widget (web/pairwise/).

Three criteria, checked independently of the widget and of
pairwise-verify.js, which implements the same arithmetic by a different route
in plain JavaScript.

Written as ahp_check.py under batch 370-AHP-1, section B; moved here and
extended with the four presets, the walk and the rounding rule under batch
370-AHP-2 on 19 September 2026. Run it with a Python that has numpy:

    /opt/homebrew/bin/python3 tools/pairwise-verify.py

Here the priority vector comes from matrix algebra: repeated multiplication of
the whole matrix by a vector (power iteration), and a row-wise geometric mean
taken with numpy's product over an axis. The JavaScript file uses explicit
loops and Math.pow. Neither file reads the other.

Random index: Saaty's table, reported in T.L. Saaty (1990) "How to make a
decision: the analytic hierarchy process", European Journal of Operational
Research 48(1), 9-26, Table 2, and in Saaty (1980) The Analytic Hierarchy
Process (New York: McGraw-Hill). RI(3) = 0.58.
The competing figure RI(3) = 0.52 comes from later re-simulations; Alonso and
Lamata (2006) report 0.5245 for n = 3.
"""

import numpy as np

RI_SAATY = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24,
            7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
RI_ALT = {3: 0.52}          # the value 123ahp.com appears to use
RI_ALONSO_LAMATA = {3: 0.5245}


def matrix(a12, a13, a23):
    """Reciprocal 3x3 from three comparisons.

    a12 is how many times as important criterion 1 is as criterion 2.
    A value below 1 (e.g. 1/3) means criterion 2 dominates.
    """
    return np.array([[1.0, a12, a13],
                     [1.0 / a12, 1.0, a23],
                     [1.0 / a13, 1.0 / a23, 1.0]], dtype=np.float64)


def eigen_weights(A, tol=1e-12, max_iter=100000):
    """Principal eigenvector by power iteration, normalised to sum 1."""
    n = A.shape[0]
    w = np.full(n, 1.0 / n, dtype=np.float64)
    for _ in range(max_iter):
        nw = A.dot(w)
        nw = nw / nw.sum()
        if np.max(np.abs(nw - w)) < tol:
            return nw, _ + 1
        w = nw
    raise RuntimeError("power iteration did not converge")


def geomean_weights(A):
    """Row geometric mean, normalised. Crawford and Williams' estimator."""
    g = np.prod(A, axis=1) ** (1.0 / A.shape[0])
    return g / g.sum()


def lambda_max(A, w):
    """Rayleigh-style estimate: mean over rows of (Aw)_i / w_i."""
    return float(np.mean(A.dot(w) / w))


def report(A, w):
    n = A.shape[0]
    lm = lambda_max(A, w)
    ci = (lm - n) / (n - 1)
    return {
        "w": w,
        "lambda_max": lm,
        "CI": ci,
        "CR_058": ci / RI_SAATY[n],
        "CR_052": ci / RI_ALT[n],
        "CR_05245": ci / RI_ALONSO_LAMATA[n],
    }


def fmt(x, d=6):
    return ("%." + str(d) + "f") % x


def show(label, a12, a13, a23, note=""):
    A = matrix(a12, a13, a23)
    we, iters = eigen_weights(A)
    wg = geomean_weights(A)
    re_, rg = report(A, we), report(A, wg)
    print("-" * 78)
    print("%s   (Elev:Slope %s, Elev:Aspect %s, Slope:Aspect %s)%s"
          % (label, frac(a12), frac(a13), frac(a23),
             ("  -- " + note) if note else ""))
    print("  eigenvector   w = [%s]   (%d iterations to 1e-12)"
          % (", ".join(fmt(x) for x in we), iters))
    print("  geometric     w = [%s]" % ", ".join(fmt(x) for x in wg))
    print("  max |eigen - geomean| = %s" % fmt(float(np.max(np.abs(we - wg))), 9))
    print("  eigen:    lambda_max %s  CI %s  CR(0.58) %s  CR(0.52) %s  CR(0.5245) %s"
          % (fmt(re_["lambda_max"]), fmt(re_["CI"]), fmt(re_["CR_058"]),
             fmt(re_["CR_052"]), fmt(re_["CR_05245"])))
    print("  geomean:  lambda_max %s  CI %s  CR(0.58) %s  CR(0.52) %s  CR(0.5245) %s"
          % (fmt(rg["lambda_max"]), fmt(rg["CI"]), fmt(rg["CR_058"]),
             fmt(rg["CR_052"]), fmt(rg["CR_05245"])))
    print("  percentages (eigen, rounded to whole): %s"
          % " / ".join(str(int(round(x * 100))) for x in we))
    return we, re_


def frac(v):
    if abs(v - round(v)) < 1e-12:
        return str(int(round(v)))
    inv = 1.0 / v
    if abs(inv - round(inv)) < 1e-9:
        return "1/%d" % int(round(inv))
    return "%.4f" % v


print("=" * 78)
print("THE REFERENCE ENCODING (audit row 15, critical review M4)")
print("aspect over slope 5, aspect over elevation 3, slope equal to elevation")
print("=" * 78)
show("reference 5-3-1", 1.0, 1.0 / 3.0, 1.0 / 5.0)

print()
print("=" * 78)
print("THE CONTRADICTION: A over B 3, B over C 3, C over A 3")
print("Elevation over Slope 3, Slope over Aspect 3, Aspect over Elevation 3")
print("=" * 78)
show("cycle 3-3-3", 3.0, 1.0 / 3.0, 3.0)

print()
print("=" * 78)
print("ELEVEN READINGS OF THE BOTANIST'S THREE SENTENCES")
print("Cell 74: aspect significantly (but not very) more important than slope;")
print("aspect slightly (but not very) more important than elevation;")
print("slope equally important as elevation.")
print("Each row fixes slope = elevation and varies the two aspect numbers.")
print("=" * 78)
rows = []
for asp_slope, asp_elev, tag in [
    (5, 3, "the reference: significantly 5, slightly 3"),
    (5, 2, "slightly read as 2"),
    (5, 4, "slightly read as 4"),
    (4, 3, "significantly read as 4"),
    (4, 2, "both read one step down"),
    (6, 3, "significantly read as 6"),
    (6, 4, "significantly 6, slightly 4"),
    (7, 5, "significantly read as 7, slightly as 5"),
    (7, 3, "significantly 7, slightly 3"),
    (3, 2, "the whole reading damped"),
    (5, 5, "the two statements read as the same strength"),
]:
    A = matrix(1.0, 1.0 / asp_elev, 1.0 / asp_slope)
    we, _ = eigen_weights(A)
    r = report(A, we)
    rows.append((asp_slope, asp_elev, we, r, tag))
    print("aspect/slope %d, aspect/elevation %d  ->  elevation %s  slope %s  "
          "aspect %s  |  CR(0.58) %s  CR(0.52) %s   [%s]"
          % (asp_slope, asp_elev, fmt(we[0] * 100, 2), fmt(we[1] * 100, 2),
             fmt(we[2] * 100, 2), fmt(r["CR_058"], 4), fmt(r["CR_052"], 4), tag))

print()
print("All eleven put aspect first: %s"
      % all(w[2] > w[0] and w[2] > w[1] for _, _, w, _, _ in rows))
print("Aspect ranges from %s to %s per cent."
      % (fmt(min(w[2] for _, _, w, _, _ in rows) * 100, 2),
         fmt(max(w[2] for _, _, w, _, _ in rows) * 100, 2)))
print("Largest CR at RI 0.58: %s; at RI 0.52: %s. The bar is 0.10."
      % (fmt(max(r["CR_058"] for _, _, _, r, _ in rows), 4),
         fmt(max(r["CR_052"] for _, _, _, r, _ in rows), 4)))

print()
print("=" * 78)
print("WHICH RI THE SITE USES")
print("=" * 78)
for label, a12, a13, a23, site_cr, site_ci, site_lm in [
    ("reference 5-3-1", 1.0, 1.0 / 3.0, 1.0 / 5.0, 0.0281, 0.0146, 3.0293),
    ("cycle 3-3-3", 3.0, 1.0 / 3.0, 3.0, 1.2816, 0.6665, 4.3329),
]:
    A = matrix(a12, a13, a23)
    we, _ = eigen_weights(A)
    r = report(A, we)
    implied = r["CI"] / site_cr
    print("%s: site CR %s, our CI %s  ->  implied RI %s"
          % (label, fmt(site_cr, 4), fmt(r["CI"], 8), fmt(implied, 6)))
    print("    site CI %s vs ours %s ; site lambda %s vs ours %s"
          % (fmt(site_ci, 4), fmt(r["CI"], 4), fmt(site_lm, 4),
             fmt(r["lambda_max"], 4)))
    print("    site CR against ours at RI 0.52: %s vs %s (difference %s)"
          % (fmt(site_cr, 4), fmt(r["CR_052"], 4),
             fmt(abs(site_cr - r["CR_052"]), 6)))
    print("    rounding the CI to 4 dp first, then dividing by 0.52: %s"
          % fmt(round(r["CI"], 4) / 0.52, 6))

print()
print("=" * 78)
print("EXACT VALUES, DERIVED BY HAND, FOR THE CYCLE")
print("=" * 78)
print("For the cycle with every off-diagonal ratio k = 3 the matrix is")
print("  [[1, k, 1/k], [1/k, 1, k], [k, 1/k, 1]].")
print("Every row has product 1, so the geometric mean is 1 in each row and the")
print("geometric-mean weights are exactly 1/3, 1/3, 1/3.")
print("The characteristic polynomial is  l^3 - 3l^2 + (3 - k^3 - 1/k^3) = 0,")
print("so with w = (1/3, 1/3, 1/3), lambda_max = 1 + (k + 1/k)/... check below.")
k = 3.0
A = matrix(k, 1.0 / k, k)
w = np.array([1 / 3.0, 1 / 3.0, 1 / 3.0])
print("  A w / w componentwise: %s" % np.round(A.dot(w) / w, 12))
print("  closed form 1 + (k + 1/k)/3 * ... ; measured lambda_max = %s"
      % fmt(lambda_max(A, w), 10))
print("  hand check: (1 + 3 + 1/3)/3 * 3 = %s" % fmt((1 + 3 + 1 / 3.0), 10))
print("  numpy eigenvalues: %s" % np.round(np.linalg.eigvals(A), 10))

print()
print("=" * 78)
print("INVARIANTS")
print("=" * 78)
A = matrix(1.0, 1.0 / 3.0, 1.0 / 5.0)
we, _ = eigen_weights(A)
print("1. A perfectly consistent matrix gives CR exactly 0.")
Ac = matrix(2.0, 6.0, 3.0)          # a13 = a12 * a23
wc, _ = eigen_weights(Ac)
print("   consistent 2-6-3: lambda_max %s, CI %s"
      % (fmt(lambda_max(Ac, wc), 12), fmt((lambda_max(Ac, wc) - 3) / 2, 12)))
print("   eigenvector %s, geometric mean %s, max difference %s"
      % (np.round(wc, 10), np.round(geomean_weights(Ac), 10),
         fmt(float(np.max(np.abs(wc - geomean_weights(Ac)))), 14)))
print("2. All comparisons equal gives 1/3 each and CR 0.")
Ae = matrix(1.0, 1.0, 1.0)
wee, _ = eigen_weights(Ae)
print("   %s, lambda_max %s" % (np.round(wee, 12), fmt(lambda_max(Ae, wee), 12)))
print("3. Swapping the labels of two criteria permutes the weights, nothing else.")
Aswap = matrix(1.0 / 3.0, 1.0, 1.0 / 5.0 * 3.0)   # elevation and aspect exchanged
print("   original weights            %s" % np.round(we, 6))
Asw = matrix(1.0 / (1.0 / 3.0), 1.0, 5.0)
print("   relabelled (aspect first)   %s" % np.round(eigen_weights(
    np.array([[1.0, 3.0, 5.0], [1 / 3.0, 1.0, 1.0], [1 / 5.0, 1.0, 1.0]]))[0], 6))
print("4. Scaling every entry of a row and its reciprocal column is not a")
print("   legal operation on a reciprocal matrix, so there is no scale")
print("   invariance to test here. What there is: the weights are unchanged")
print("   by normalising the eigenvector differently.")
print("   sum of weights = %s" % fmt(float(we.sum()), 15))


# ---------------------------------------------------------------------------
# Added for batch 370-AHP-2: the widget's own signed axis, its four presets,
# the walk, and the rounding rule the page displays under. Reading the signed
# axis here rather than raw ratios means a figure in this file can be compared
# against a figure on screen with no conversion step in between.
# ---------------------------------------------------------------------------

def entry(s):
    """Signed comparison to matrix entry.

    +k means the first of the pair is k times as important, -k means the
    second is, and 1 and -1 both mean equal.
    """
    if s in (1, -1):
        return 1.0
    return float(s) if s > 0 else -1.0 / s


def from_signed(c12, c13, c23):
    return matrix(entry(c12), entry(c13), entry(c23))


def display_percents(w):
    """The page's largest-remainder rounding, to hundredths of a per cent.

    Round every share down, then hand the spare hundredths to the largest
    residuals, lowest index first on a tie.
    """
    units = [x * 10000.0 for x in w]
    floors = [int(np.floor(u)) for u in units]
    spare = 10000 - sum(floors)
    order = sorted(range(3), key=lambda i: (-(units[i] - floors[i]), i))
    for k in range(spare):
        floors[order[k % 3]] += 1
    return [u / 100.0 for u in floors]


def solve(c12, c13, c23):
    A = from_signed(c12, c13, c23)
    we, iters = eigen_weights(A)
    wg = geomean_weights(A)
    r = report(A, we)
    return {"A": A, "w": we, "g": wg, "iterations": iters,
            "gap": float(np.max(np.abs(we - wg))),
            "lambda_max": r["lambda_max"], "CI": r["CI"], "CR": r["CR_058"],
            "pct": display_percents(we)}


AXIS = [(9 - p) if p < 8 else (1 if p == 8 else -(p - 7)) for p in range(17)]

print()
print("=" * 78)
print("THE FOUR PRESETS  (c12 / c13 / c23 on the signed axis)")
print("=" * 78)
for label, c12, c13, c23 in [("Equal (the opening state)", 1, 1, 1),
                             ("One dominates", 9, 9, 1),
                             ("A near tie", 1, 2, 2),
                             ("A contradiction", 3, -3, 3)]:
    r = solve(c12, c13, c23)
    print("%s  [%d / %d / %d]" % (label, c12, c13, c23))
    print("  weights    %s" % "  ".join(fmt(x, 10) for x in r["w"]))
    print("  displayed  %s   sum %.2f"
          % (" / ".join("%.2f" % x for x in r["pct"]), sum(r["pct"])))
    print("  lambda_max %s   CI %s   CR %s"
          % (fmt(r["lambda_max"], 12), fmt(r["CI"], 12), fmt(r["CR"], 6)))
    print("  |eigen - geomean| %.3e   iterations %d" % (r["gap"], r["iterations"]))

print()
print("=" * 78)
print("ONE STEP FROM THE NEAR TIE, on the first comparison")
print("=" * 78)
for label, c12, c13, c23 in [("one step, first over second", 2, 2, 2),
                             ("the preset", 1, 2, 2),
                             ("one step, second over first", -2, 2, 2)]:
    r = solve(c12, c13, c23)
    print("  %-30s %s   CR %s"
          % (label, " / ".join("%.4f" % (x * 100) for x in r["w"]), fmt(r["CR"], 6)))
    print("    displayed %s" % " / ".join("%.2f" % x for x in r["pct"]))

print()
print("=" * 78)
print("THE WALK: aspect 5x slope, aspect 3x elevation, c12 across the axis")
print("=" * 78)
asp = []
for s in AXIS:
    r = solve(s, -3, -5)
    asp.append(r["w"][2])
    print("  c12 %3d   %s   CR %s   %s"
          % (s, " / ".join("%6.2f" % x for x in r["pct"]), fmt(r["CR"], 4),
             "agree" if r["CR"] < 0.10 else "disagree"))
print("  aspect first in all seventeen: %s; aspect from %.2f to %.2f per cent"
      % (all(solve(s, -3, -5)["w"][2] > max(solve(s, -3, -5)["w"][0],
                                            solve(s, -3, -5)["w"][1]) for s in AXIS),
         min(asp) * 100, max(asp) * 100))

print()
print("=" * 78)
print("ALL 4,913 CONFIGURATIONS")
print("=" * 78)
n = bad_sum = cycles = fails = fails_not_cycle = not_cycle = 0
worst_gap = worst_recip = 0.0
for a in AXIS:
    for b in AXIS:
        for c in AXIS:
            r = solve(a, b, c)
            n += 1
            if abs(sum(r["pct"]) - 100.0) > 1e-9:
                bad_sum += 1
            worst_gap = max(worst_gap, r["gap"])
            A = r["A"]
            worst_recip = max(worst_recip,
                              float(np.max(np.abs(A * A.T - 1.0))))
            e12, e13, e23 = entry(a), entry(b), entry(c)
            cyc = (e12 > 1 and e23 > 1 and e13 < 1) or (e12 < 1 and e23 < 1 and e13 > 1)
            if cyc:
                cycles += 1
            else:
                not_cycle += 1
            if r["CR"] >= 0.10:
                fails += 1
                if not cyc:
                    fails_not_cycle += 1
print("  configurations                        %d" % n)
print("  displayed percentages not summing 100 %d" % bad_sum)
print("  worst |eigenvector - geometric mean|  %.3e" % worst_gap)
print("  worst |A[i][j]*A[j][i] - 1|           %.3e" % worst_recip)
print("  cycles                                %d  (%.1f per cent)" % (cycles, 100.0 * cycles / n))
print("  at or above CR 0.10                   %d  (%.1f per cent)" % (fails, 100.0 * fails / n))
print("  not a cycle and still failing         %d of %d" % (fails_not_cycle, not_cycle))

print()
print("=" * 78)
print("RELABELLING PERMUTES THE WEIGHTS AND CHANGES NOTHING ELSE")
print("=" * 78)
base, swapped = solve(1, -3, -5), solve(-1, -5, -3)
print("  original  %s   CR %s" % ("  ".join(fmt(x, 10) for x in base["w"]), fmt(base["CR"], 8)))
print("  swapped   %s   CR %s" % ("  ".join(fmt(x, 10) for x in swapped["w"]), fmt(swapped["CR"], 8)))
print("  worst difference after permuting: %.3e"
      % max(abs(swapped["w"][0] - base["w"][1]), abs(swapped["w"][1] - base["w"][0]),
            abs(swapped["w"][2] - base["w"][2]), abs(swapped["CR"] - base["CR"])))
