// Independent check of the pairwise weights widget (web/pairwise/).
// Three criteria, in plain JavaScript with no dependency. Shares no code with
// the widget and no code with pairwise-verify.py: explicit loops and Math.pow
// rather than matrix algebra, so that agreement between the three routes is
// evidence about the arithmetic and not about a shared routine.
//
// Written as ahp_check.js under batch 370-AHP-1, section B; moved here and
// extended with the four presets, the walk and the rounding rule under
// batch 370-AHP-2 on 19 September 2026.
//
//   node tools/pairwise-verify.js
//
// Random index: Saaty's table. RI(3) = 0.58.
// The alternative RI(3) = 0.52 is what 123ahp.com appears to use.

"use strict";

var RI_SAATY = [0, 0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49];
var RI_SITE3 = 0.52;

// Build the reciprocal matrix from the three upper-triangle comparisons.
function build(a12, a13, a23) {
  var A = [[1, a12, a13],
           [1 / a12, 1, a23],
           [1 / a13, 1 / a23, 1]];
  return A;
}

// Principal eigenvector by power iteration, to a maximum absolute change of tol.
function eigenWeights(A, tol) {
  var n = A.length, i, j, k, s, w = [], nw = [], diff;
  for (i = 0; i < n; i++) w.push(1 / n);
  for (k = 0; k < 100000; k++) {
    nw = [];
    for (i = 0; i < n; i++) {
      s = 0;
      for (j = 0; j < n; j++) s += A[i][j] * w[j];
      nw.push(s);
    }
    s = 0;
    for (i = 0; i < n; i++) s += nw[i];
    for (i = 0; i < n; i++) nw[i] = nw[i] / s;
    diff = 0;
    for (i = 0; i < n; i++) diff = Math.max(diff, Math.abs(nw[i] - w[i]));
    w = nw;
    if (diff < tol) return { w: w, iterations: k + 1 };
  }
  throw new Error("power iteration did not converge");
}

// Row geometric mean, normalised.
function geomeanWeights(A) {
  var n = A.length, i, j, p, g = [], s = 0;
  for (i = 0; i < n; i++) {
    p = 1;
    for (j = 0; j < n; j++) p *= A[i][j];
    g.push(Math.pow(p, 1 / n));
    s += g[i];
  }
  for (i = 0; i < n; i++) g[i] = g[i] / s;
  return g;
}

function lambdaMax(A, w) {
  var n = A.length, i, j, s, total = 0;
  for (i = 0; i < n; i++) {
    s = 0;
    for (j = 0; j < n; j++) s += A[i][j] * w[j];
    total += s / w[i];
  }
  return total / n;
}

function consistency(A, w) {
  var n = A.length;
  var lm = lambdaMax(A, w);
  var ci = (lm - n) / (n - 1);
  return { lambdaMax: lm, CI: ci, CR58: ci / RI_SAATY[n], CR52: ci / RI_SITE3 };
}

function f(x, d) { return x.toFixed(d === undefined ? 6 : d); }

function run(label, a12, a13, a23) {
  var A = build(a12, a13, a23);
  var e = eigenWeights(A, 1e-12);
  var g = geomeanWeights(A);
  var ce = consistency(A, e.w), cg = consistency(A, g);
  var d = 0, i;
  for (i = 0; i < 3; i++) d = Math.max(d, Math.abs(e.w[i] - g[i]));
  console.log("-".repeat(78));
  console.log(label);
  console.log("  eigenvector  " + e.w.map(function (x) { return f(x); }).join("  ")
              + "   (" + e.iterations + " iterations)");
  console.log("  geometric    " + g.map(function (x) { return f(x); }).join("  "));
  console.log("  max |eigen - geomean| = " + d.toExponential(3));
  console.log("  lambda_max " + f(ce.lambdaMax) + "   CI " + f(ce.CI)
              + "   CR(RI 0.58) " + f(ce.CR58) + "   CR(RI 0.52) " + f(ce.CR52));
  console.log("  geomean route: lambda_max " + f(cg.lambdaMax)
              + "   CI " + f(cg.CI) + "   CR(0.58) " + f(cg.CR58));
  console.log("  as percentages: "
              + e.w.map(function (x) { return (x * 100).toFixed(2); }).join(" / ")
              + "   rounded: "
              + e.w.map(function (x) { return Math.round(x * 100); }).join(" / "));
  return { w: e.w, c: ce };
}

console.log("=".repeat(78));
console.log("REFERENCE ENCODING: aspect over slope 5, aspect over elevation 3,");
console.log("slope equal to elevation. Order: elevation, slope, aspect.");
console.log("=".repeat(78));
run("reference 5-3-1", 1, 1 / 3, 1 / 5);

console.log("");
console.log("=".repeat(78));
console.log("THE CONTRADICTION: elevation over slope 3, slope over aspect 3,");
console.log("aspect over elevation 3.");
console.log("=".repeat(78));
run("cycle 3-3-3", 3, 1 / 3, 3);

console.log("");
console.log("=".repeat(78));
console.log("ELEVEN READINGS, aspect/slope and aspect/elevation, slope = elevation");
console.log("=".repeat(78));
var readings = [[5, 3], [5, 2], [5, 4], [4, 3], [4, 2], [6, 3],
                [6, 4], [7, 5], [7, 3], [3, 2], [5, 5]];
readings.forEach(function (r) {
  var A = build(1, 1 / r[1], 1 / r[0]);
  var e = eigenWeights(A, 1e-12);
  var c = consistency(A, e.w);
  console.log("aspect/slope " + r[0] + ", aspect/elevation " + r[1]
              + "  ->  " + e.w.map(function (x) { return (x * 100).toFixed(2); }).join("  ")
              + "   CR(0.58) " + f(c.CR58, 4) + "   CR(0.52) " + f(c.CR52, 4));
});

console.log("");
console.log("=".repeat(78));
console.log("AGREEMENT WITH THE SITE (values read off 123ahp.com, 19 Sept 2026)");
console.log("=".repeat(78));
[["reference 5-3-1", 1, 1 / 3, 1 / 5,
  [0.1852, 0.1562, 0.6586], 0.0281, 0.0146, 3.0293],
 ["cycle 3-3-3", 3, 1 / 3, 3,
  [0.3333, 0.3333, 0.3333], 1.2816, 0.6665, 4.3329]
].forEach(function (t) {
  var A = build(t[1], t[2], t[3]);
  var e = eigenWeights(A, 1e-12);
  var c = consistency(A, e.w);
  var i, wd = 0;
  for (i = 0; i < 3; i++) wd = Math.max(wd, Math.abs(Number(e.w[i].toFixed(4)) - t[4][i]));
  console.log(t[0] + ":");
  console.log("  weights, ours rounded to 4 dp vs the site: max difference " + wd);
  console.log("  lambda_max ours " + f(c.lambdaMax) + " vs site " + t[7]
              + "   difference " + f(Math.abs(c.lambdaMax - t[7]), 6));
  console.log("  CI ours " + f(c.CI) + " vs site " + t[6]
              + "   difference " + f(Math.abs(c.CI - t[6]), 6));
  console.log("  CR at RI 0.58 " + f(c.CR58, 4) + " ; at RI 0.52 " + f(c.CR52, 4)
              + " ; site " + t[5]);
  console.log("  RI implied by the site's own CI and CR: "
              + f(t[6] / t[5], 6));
});

console.log("");
console.log("=".repeat(78));
console.log("INVARIANTS");
console.log("=".repeat(78));
var Ac = build(2, 6, 3);
var ec = eigenWeights(Ac, 1e-14);
console.log("consistent 2-6-3: weights " + ec.w.map(function (x) { return f(x, 10); }).join(" ")
            + "  lambda_max " + f(lambdaMax(Ac, ec.w), 12));
var Ae = build(1, 1, 1);
var ee = eigenWeights(Ae, 1e-14);
console.log("all equal: weights " + ee.w.map(function (x) { return f(x, 10); }).join(" ")
            + "  lambda_max " + f(lambdaMax(Ae, ee.w), 12));
console.log("reciprocity holds by construction: A[i][j] * A[j][i] = 1 for every pair.");
var Ar = build(1, 1 / 3, 1 / 5), ok = true;
for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) {
  if (Math.abs(Ar[i][j] * Ar[j][i] - 1) > 1e-15) ok = false;
}
console.log("  checked on the reference matrix: " + ok);

// ---------------------------------------------------------------------------
// Added for batch 370-AHP-2: the widget's own encoding, its four presets, the
// walk, and the rounding rule the page displays under. Everything below reads
// the signed axis the page puts in the URL rather than raw ratios, so a figure
// here can be compared against a figure on screen without a conversion step.
// ---------------------------------------------------------------------------

// Signed comparison to matrix entry. +k means the first of the pair is k times
// as important; -k means the second is; 1 and -1 both mean equal.
function entry(s) {
  if (s === 1 || s === -1) return 1;
  return s > 0 ? s : -1 / s;
}
function fromSigned(c12, c13, c23) {
  return build(entry(c12), entry(c13), entry(c23));
}

// The page's largest-remainder rounding, to hundredths of a per cent.
// Round every share down, then hand the spare hundredths to the largest
// residuals, lowest index first on a tie.
function displayPercents(w) {
  var units = w.map(function (x) { return x * 10000; });
  var floors = units.map(Math.floor);
  var spare = 10000 - floors.reduce(function (a, b) { return a + b; }, 0);
  var order = [0, 1, 2].sort(function (i, j) {
    var d = (units[j] - floors[j]) - (units[i] - floors[i]);
    return d !== 0 ? d : i - j;
  });
  for (var k = 0; k < spare; k++) floors[order[k % 3]] += 1;
  return floors.map(function (u) { return u / 100; });
}

function solve(c12, c13, c23) {
  var A = fromSigned(c12, c13, c23);
  var e = eigenWeights(A, 1e-12);
  var g = geomeanWeights(A);
  var c = consistency(A, e.w);
  var d = 0, i;
  for (i = 0; i < 3; i++) d = Math.max(d, Math.abs(e.w[i] - g[i]));
  return { A: A, w: e.w, g: g, iterations: e.iterations, gap: d,
           lambdaMax: c.lambdaMax, CI: c.CI, CR: c.CR58,
           pct: displayPercents(e.w) };
}

var AXIS = [];                       // the seventeen positions, left to right
for (var p = 0; p <= 16; p++) AXIS.push(p < 8 ? 9 - p : p === 8 ? 1 : -(p - 7));

console.log("");
console.log("=".repeat(78));
console.log("THE FOUR PRESETS  (c12 / c13 / c23 on the signed axis)");
console.log("=".repeat(78));
[["Equal (the opening state)", 1, 1, 1],
 ["One dominates", 9, 9, 1],
 ["A near tie", 1, 2, 2],
 ["A contradiction", 3, -3, 3]].forEach(function (t) {
  var r = solve(t[1], t[2], t[3]);
  console.log(t[0] + "  [" + t[1] + " / " + t[2] + " / " + t[3] + "]");
  console.log("  weights    " + r.w.map(function (x) { return f(x, 10); }).join("  "));
  console.log("  displayed  " + r.pct.map(function (x) { return x.toFixed(2); }).join(" / ")
              + "   sum " + r.pct.reduce(function (a, b) { return a + b; }, 0).toFixed(2));
  console.log("  lambda_max " + f(r.lambdaMax, 12) + "   CI " + f(r.CI, 12)
              + "   CR " + f(r.CR, 6));
  console.log("  |eigen - geomean| " + r.gap.toExponential(3)
              + "   iterations " + r.iterations);
});

console.log("");
console.log("=".repeat(78));
console.log("ONE STEP FROM THE NEAR TIE, on the first comparison");
console.log("=".repeat(78));
[["one step, first over second", 2, 2, 2],
 ["the preset", 1, 2, 2],
 ["one step, second over first", -2, 2, 2]].forEach(function (t) {
  var r = solve(t[1], t[2], t[3]);
  console.log("  " + t[0].padEnd(30) + r.pct.map(function (x) { return x.toFixed(4); }).join(" / ")
              + "   CR " + f(r.CR, 6));
  console.log("    exact weights " + r.w.map(function (x) { return f(x, 10); }).join("  "));
});

console.log("");
console.log("=".repeat(78));
console.log("THE WALK: aspect 5x slope, aspect 3x elevation, c12 across the axis");
console.log("c13 = -3, c23 = -5, c12 runs over all seventeen positions");
console.log("=".repeat(78));
var first = [], minA = 1, maxA = 0;
AXIS.forEach(function (s) {
  var r = solve(s, -3, -5);
  first.push(r.w[2] > r.w[0] && r.w[2] > r.w[1]);
  minA = Math.min(minA, r.w[2]); maxA = Math.max(maxA, r.w[2]);
  console.log("  c12 " + String(s).padStart(3) + "   "
              + r.pct.map(function (x) { return x.toFixed(2).padStart(6); }).join(" / ")
              + "   CR " + f(r.CR, 4) + "   " + (r.CR < 0.10 ? "agree" : "disagree"));
});
console.log("  aspect first in all seventeen: " + first.every(Boolean)
            + ";  aspect from " + (minA * 100).toFixed(2) + " to " + (maxA * 100).toFixed(2) + " per cent");

console.log("");
console.log("=".repeat(78));
console.log("ALL 4,913 CONFIGURATIONS");
console.log("=".repeat(78));
var n = 0, badSum = 0, worstGap = 0, cycles = 0, fails = 0, failsNotCycle = 0, notCycle = 0;
var worstRecip = 0;
AXIS.forEach(function (a) { AXIS.forEach(function (b) { AXIS.forEach(function (c) {
  var r = solve(a, b, c);
  n++;
  var sum = r.pct[0] + r.pct[1] + r.pct[2];
  if (Math.abs(sum - 100) > 1e-9) badSum++;
  worstGap = Math.max(worstGap, r.gap);
  for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) {
    worstRecip = Math.max(worstRecip, Math.abs(r.A[i][j] * r.A[j][i] - 1));
  }
  var e12 = entry(a), e13 = entry(b), e23 = entry(c);
  var cyc = (e12 > 1 && e23 > 1 && e13 < 1) || (e12 < 1 && e23 < 1 && e13 > 1);
  if (cyc) cycles++; else notCycle++;
  if (r.CR >= 0.10) { fails++; if (!cyc) failsNotCycle++; }
}); }); });
console.log("  configurations                        " + n);
console.log("  displayed percentages not summing 100 " + badSum);
console.log("  worst |eigenvector - geometric mean|  " + worstGap.toExponential(3));
console.log("  worst |A[i][j]*A[j][i] - 1|           " + worstRecip.toExponential(3));
console.log("  cycles                                " + cycles
            + "  (" + (100 * cycles / n).toFixed(1) + " per cent)");
console.log("  at or above CR 0.10                   " + fails
            + "  (" + (100 * fails / n).toFixed(1) + " per cent)");
console.log("  not a cycle and still failing         " + failsNotCycle
            + " of " + notCycle);

console.log("");
console.log("=".repeat(78));
console.log("RELABELLING PERMUTES THE WEIGHTS AND CHANGES NOTHING ELSE");
console.log("=".repeat(78));
// Swap criteria 1 and 2. c12 flips sign, c13 and c23 exchange.
var base = solve(1, -3, -5);
var swapped = solve(-1, -5, -3);
console.log("  original  " + base.w.map(function (x) { return f(x, 10); }).join("  ")
            + "   CR " + f(base.CR, 8));
console.log("  swapped   " + swapped.w.map(function (x) { return f(x, 10); }).join("  ")
            + "   CR " + f(swapped.CR, 8));
var perm = 0;
perm = Math.max(Math.abs(swapped.w[0] - base.w[1]), Math.abs(swapped.w[1] - base.w[0]),
                Math.abs(swapped.w[2] - base.w[2]), Math.abs(swapped.CR - base.CR));
console.log("  worst difference after permuting: " + perm.toExponential(3));

console.log("");
console.log("=".repeat(78));
console.log("THE REFERENCE ENCODING ON THE SIGNED AXIS  (c12=1, c13=-3, c23=-5)");
console.log("=".repeat(78));
var ref = solve(1, -3, -5);
console.log("  weights    " + ref.w.map(function (x) { return f(x, 6); }).join("  "));
console.log("  displayed  " + ref.pct.map(function (x) { return x.toFixed(2); }).join(" / "));
console.log("  lambda_max " + f(ref.lambdaMax, 6) + "   CI " + f(ref.CI, 6)
            + "   CR " + f(ref.CR, 6) + "   iterations " + ref.iterations);
