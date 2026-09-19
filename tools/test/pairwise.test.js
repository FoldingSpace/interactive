"use strict";
// Tests for web/pairwise. The eight invariants of PROPOSAL-ahp.md section 3, and
// then what the page actually draws: the bar widths, the readout words at every
// one of the seventeen positions, the verdict either side of the 0.10 bar, and
// what the saved picture records.
//
// The bug that would pass a test of the numbers alone: the weights are right and
// the bars are scaled to the largest weight rather than to 100, so the longest
// bar is full width whatever it holds and nothing can be read off the picture.
// Every bar assertion below reads the width off the element for that reason.

var fs = require("fs");
var path = require("path");
var L = require("./load.js");

var FILE = path.join(__dirname, "..", "..", "web", "pairwise", "index.html");

function open(search) {
  var w = L.load(FILE, { slug: "pairwise", search: search || "" });
  w.settle();
  w.T = w.win.PAIRWISE_TEST;
  return w;
}
function set(w, a, b, c) { w.T.set(a, b, c); w.settle(); return w; }
function txt(w, id) { return w.doc.getElementById(id).textContent; }
function pcts(w) {
  return [0, 1, 2].map(function (i) { return txt(w, "wpct" + i); });
}
function bars(w) {
  return [0, 1, 2].map(function (i) { return w.doc.getElementById("wfill" + i).style.width; });
}
function click(w, text) {
  var b = w.doc.querySelectorAll("button").filter(function (e) {
    return e.textContent.trim() === text;
  })[0];
  if (!b) throw new Error("no button reading " + JSON.stringify(text));
  b.click();
  w.settle();
  return b;
}
var AXIS = [9, 8, 7, 6, 5, 4, 3, 2, 1, -2, -3, -4, -5, -6, -7, -8, -9];

module.exports = function (t) {

  // ---- the eight invariants of the proposal, section 3 ---------------------

  t("invariant 1: a coherent set of comparisons scores exactly zero", function (a) {
    var w = open();
    // Elevation twice slope, elevation six times aspect, slope three times aspect.
    var r = w.T.solveAt(2, 6, 3);
    a.close(r.w[0], 0.6, 1e-12, "elevation exactly 0.6");
    a.close(r.w[1], 0.3, 1e-12, "slope exactly 0.3");
    a.close(r.w[2], 0.1, 1e-12, "aspect exactly 0.1");
    a.close(r.lambdaMax, 3, 1e-12, "largest eigenvalue exactly 3");
    a.close(r.CI, 0, 1e-12, "consistency index exactly 0");
    a.close(r.CR, 0, 1e-12, "and the ratio with it");
    // And the same when it is drawn, not only when it is computed.
    set(w, 2, 6, 3);
    a.equal(pcts(w).join(" / "), "60.00% / 30.00% / 10.00%", "as drawn");
    a.equal(txt(w, "cr"), "0.0000", "ratio as drawn");
    a.equal(txt(w, "verdict"), "agree", "verdict as drawn");
  });

  t("invariant 2: all three equal gives a third each and an eigenvalue of 3", function (a) {
    var w = open();
    var r = w.T.solveAt(1, 1, 1);
    [0, 1, 2].forEach(function (i) {
      a.close(r.w[i], 1 / 3, 1e-12, "share " + i + " is a third");
    });
    a.close(r.lambdaMax, 3, 1e-12, "largest eigenvalue exactly 3");
    a.close(r.CR, 0, 1e-12, "ratio exactly 0");
  });

  t("invariant 3: eigenvector and geometric mean agree at three criteria", function (a) {
    // At n = 3 these two estimators are the same to the power iteration's own
    // tolerance, which is why the page never has to explain a method choice.
    // Run over every setting the controls can reach rather than a random sample.
    var w = open();
    var worst = 0, n = 0;
    AXIS.forEach(function (x) { AXIS.forEach(function (y) { AXIS.forEach(function (z) {
      var r = w.T.solveAt(x, y, z);
      n++;
      for (var i = 0; i < 3; i++) worst = Math.max(worst, Math.abs(r.w[i] - r.g[i]));
    }); }); });
    a.equal(n, 4913, "all 4,913 settings visited");
    a.ok(worst < 5e-12, "worst difference " + worst.toExponential(3) + " over the whole range");
  });

  t("invariant 4: the matrix is reciprocal", function (a) {
    var w = open();
    var worst = 0;
    AXIS.forEach(function (x) { AXIS.forEach(function (y) { AXIS.forEach(function (z) {
      var A = w.T.solveAt(x, y, z).A;
      for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) {
        worst = Math.max(worst, Math.abs(A[i][j] * A[j][i] - 1));
      }
    }); }); });
    a.ok(worst <= 1e-15, "worst |A[i][j] * A[j][i] - 1| is " + worst.toExponential(3));
  });

  t("invariant 5: relabelling two criteria permutes the weights and nothing else", function (a) {
    var w = open();
    // The reference encoding, then criteria 1 and 2 exchanged: c12 changes sign,
    // c13 and c23 swap places.
    var base = w.T.solveAt(1, -3, -5);
    var swap = w.T.solveAt(-1, -5, -3);
    a.close(swap.w[0], base.w[1], 1e-14, "the first share is the old second");
    a.close(swap.w[1], base.w[0], 1e-14, "the second is the old first");
    a.close(swap.w[2], base.w[2], 1e-14, "the third does not move");
    a.close(swap.CR, base.CR, 1e-14, "and the ratio does not move");
  });

  t("invariant 6: the three displayed shares sum to 100.00 everywhere", function (a) {
    // This is a claim about the rounding rule, so it belongs here rather than in
    // a sentence. Naive rounding to two decimals misses 100 on four of the eleven
    // readings recorded in the proposal.
    var w = open();
    var bad = 0, n = 0;
    AXIS.forEach(function (x) { AXIS.forEach(function (y) { AXIS.forEach(function (z) {
      var p = w.T.solveAt(x, y, z).pct;
      n++;
      if (Math.abs(p[0] + p[1] + p[2] - 100) > 1e-9) bad++;
      for (var i = 0; i < 3; i++) {
        if (Math.abs(p[i] * 100 - Math.round(p[i] * 100)) > 1e-9) bad++;
      }
    }); }); });
    a.equal(n, 4913, "all 4,913 settings visited");
    a.equal(bad, 0, "every one sums to exactly 100.00 in whole hundredths");
    // Naive rounding really does fail, so the rule is earning its place.
    var naive = 0;
    AXIS.forEach(function (x) { AXIS.forEach(function (y) { AXIS.forEach(function (z) {
      var ws = w.T.solveAt(x, y, z).w;
      var s = ws.reduce(function (acc, v) { return acc + Math.round(v * 10000); }, 0);
      if (s !== 10000) naive++;
    }); }); });
    // The exact count, not "some": a figure quoted in two documents needs a test
    // or it goes stale silently, and this one was written from memory as 1,206
    // before anybody counted it.
    a.equal(naive, 1244, "1,244 of the 4,913 would miss 100.00 under plain rounding");
  });

  t("invariant 7: the reference encoding, to every figure recorded", function (a) {
    var w = open();
    var r = w.T.solveAt(1, -3, -5);
    a.close(r.w[0], 0.185174, 5e-7, "elevation 0.185174");
    a.close(r.w[1], 0.156182, 5e-7, "slope 0.156182");
    a.close(r.w[2], 0.658644, 5e-7, "aspect 0.658644");
    a.close(r.lambdaMax, 3.029064, 5e-7, "largest eigenvalue 3.029064");
    a.close(r.CI, 0.014532, 5e-7, "consistency index 0.014532");
    a.close(r.CR, 0.025055, 5e-7, "consistency ratio 0.025055 at a random index of 0.58");
    a.equal(r.iterations, 13, "thirteen power iterations to 1e-12");
    a.equal(r.pct.join(" / "), "18.52 / 15.62 / 65.86", "displayed shares");
  });

  t("invariant 8: a fourth name in the link is ignored", function (a) {
    var w = open("?n=Shade,View,Quiet,Cost");
    a.equal(w.T.state().names.join(","), "Shade,View,Quiet", "only the first three are used");
    a.equal(txt(w, "wname0"), "Shade", "and the page draws three");
    a.equal(txt(w, "wname2"), "Quiet", "the third is the third name, not the fourth");
    a.equal(w.doc.querySelectorAll(".wrow").length, 3, "three weight rows, whatever the link says");
    a.equal(w.doc.querySelectorAll(".cmp").length, 3, "and three comparisons");
  });

  // ---- what the page draws -------------------------------------------------

  t("the bars are scaled to 100 per cent, not to the largest weight", function (a) {
    var w = open("?c13=-3&c23=-5");
    a.equal(pcts(w).join(" / "), "18.52% / 15.62% / 65.86%", "the reference encoding");
    a.equal(bars(w).join(" / "), "18.52% / 15.62% / 65.86%",
      "and the bar widths are the same numbers");
    a.ok(bars(w)[2] !== "100%", "the largest bar is not full width");
    // Each of the four presets, read off the drawing.
    var want = {
      "All equal":           ["33.34%", "33.33%", "33.33%"],
      "One far ahead":       ["81.82%", "9.09%", "9.09%"],
      "Two tied":            ["40.00%", "40.00%", "20.00%"],
      "Each beats the next": ["33.34%", "33.33%", "33.33%"]
    };
    Object.keys(want).forEach(function (label) {
      click(w, label);
      a.equal(bars(w).join(" / "), want[label].join(" / "), label + ": bar widths");
      a.equal(pcts(w).join(" / "), want[label].map(function (s) { return s.replace("%", "") + "%"; }).join(" / "),
        label + ": printed shares");
    });
  });

  t("the four presets reproduce the recorded table", function (a) {
    var w = open();
    [["All equal", 0, "agree"],
     ["One far ahead", 0, "agree"],
     ["Two tied", 0, "agree"],
     ["Each beats the next", 1.149425, "disagree"]].forEach(function (p) {
      click(w, p[0]);
      a.equal(txt(w, "cr"), p[1].toFixed(4), p[0] + ": ratio on the face");
      a.equal(txt(w, "verdict"), p[2], p[0] + ": verdict on the face");
    });
    // Three of the four have an eigenvalue of exactly 3 rather than about 3.
    [[1, 1, 1], [9, 9, 1], [1, 2, 2]].forEach(function (s) {
      a.close(w.T.solveAt(s[0], s[1], s[2]).lambdaMax, 3, 1e-12,
        s.join("/") + ": largest eigenvalue exactly 3");
    });
    a.close(w.T.solveAt(3, -3, 3).lambdaMax, 13 / 3, 1e-12,
      "the contradiction is exactly 13/3");
    a.close(w.T.solveAt(3, -3, 3).CI, 2 / 3, 1e-12, "and its index exactly 2/3");
  });

  t("the readout says the right thing at all seventeen positions", function (a) {
    var w = open();
    var want = [
      ["Elevation 9 times Slope", "far more important"],
      ["Elevation 8 times Slope", "far more important"],
      ["Elevation 7 times Slope", "much more important"],
      ["Elevation 6 times Slope", "much more important"],
      ["Elevation 5 times Slope", "more important"],
      ["Elevation 4 times Slope", "more important"],
      ["Elevation 3 times Slope", "slightly more important"],
      ["Elevation 2 times Slope", "slightly more important"],
      ["Equal", "both matter the same"],
      ["Slope 2 times Elevation", "slightly more important"],
      ["Slope 3 times Elevation", "slightly more important"],
      ["Slope 4 times Elevation", "more important"],
      ["Slope 5 times Elevation", "more important"],
      ["Slope 6 times Elevation", "much more important"],
      ["Slope 7 times Elevation", "much more important"],
      ["Slope 8 times Elevation", "far more important"],
      ["Slope 9 times Elevation", "far more important"]
    ];
    AXIS.forEach(function (s, i) {
      set(w, s, 1, 1);
      a.equal(txt(w, "num12"), want[i][0], "position " + i + ": the number line");
      a.equal(txt(w, "word12"), want[i][1], "position " + i + ": the words");
      var on = w.doc.getElementById("strip12").children.filter(function (e) {
        return (" " + e.className + " ").indexOf(" on ") >= 0;
      });
      a.equal(on.length, 1, "position " + i + ": one tick is marked");
      a.equal(w.doc.getElementById("strip12").children.indexOf(on[0]), i,
        "position " + i + ": and it is the right one");
    });
    a.equal(w.doc.getElementById("strip12").children.length, 17, "seventeen ticks");
  });

  t("the stepper stops at the ends and reaches both of them", function (a) {
    var w = open();
    set(w, 9, 1, 1);
    a.ok(w.doc.getElementById("dn12").disabled, "at one end the minus button is off");
    a.ok(!w.doc.getElementById("up12").disabled, "and the plus button still works");
    set(w, -9, 1, 1);
    a.ok(w.doc.getElementById("up12").disabled, "at the other end the plus button is off");
  });

  t("the verdict changes on the right side of 0.10", function (a) {
    var w = open();
    // The walk of the proposal's section 3: aspect five times slope, aspect three
    // times elevation, the first comparison moving.
    set(w, 4, -3, -5);
    a.equal(txt(w, "cr"), "0.0739", "just under the bar");
    a.equal(txt(w, "verdict"), "agree", "and the word says agree");
    set(w, 5, -3, -5);
    a.equal(txt(w, "cr"), "0.1169", "one step on, just over it");
    a.equal(txt(w, "verdict"), "disagree", "and the word changes");
    // The bar is a hard edge, so check the arithmetic at it rather than near it.
    a.ok(w.T.solveAt(4, -3, -5).CR < 0.10, "0.0739 is below 0.10");
    a.ok(w.T.solveAt(5, -3, -5).CR >= 0.10, "0.1169 is at or above 0.10");
  });

  t("one step from the near tie decides the tie", function (a) {
    var w = open();
    click(w, "Two tied");
    a.equal(pcts(w).join(" / "), "40.00% / 40.00% / 20.00%", "the preset is an exact tie");
    var step = w.T.solveAt(2, 2, 2);
    a.close(step.w[0] * 100, 49.3386, 5e-5, "one step, first over second: 49.3386");
    a.close(step.w[1] * 100, 31.0814, 5e-5, "31.0814");
    a.close(step.w[2] * 100, 19.5800, 5e-5, "19.5800");
    a.close(step.CR, 0.046225, 5e-7, "at a ratio of 0.046225");
    var back = w.T.solveAt(-2, 2, 2);
    a.close(back.w[0] * 100, 31.0814, 5e-5, "the other way round: 31.0814");
    a.close(back.w[1] * 100, 49.3386, 5e-5, "49.3386");
    a.close(back.w[2] * 100, 19.5800, 5e-5, "and the third barely moves");
    // And the press of one button really does it, through the drawn control.
    w.doc.getElementById("dn12").click();
    w.settle();
    a.equal(pcts(w).join(" / "), "49.34% / 31.08% / 19.58%",
      "one press of the minus button, read off the drawing");
  });

  t("the saved picture says in words what produced it", function (a) {
    // It leaves the page and is read cold, by a student months later and by a marker
    // who was not there. Luke, 19 September: the first version was too terse for a
    // student to know what it meant. So every comparison is a sentence, the weights
    // carry their names and both forms of the number, and the ratio comes with the
    // line saying what it does not measure.
    var w = open("?c13=-3&c23=-5");
    var img = w.T.imageText();
    a.equal(img.title, "Three weights and the comparisons behind them",
      "the title says what the picture is");
    a.equal(img.comparisonsHeading, "What was compared", "and each part is labelled");
    a.equal(img.comparisons[0], "Elevation and Slope matter the same.",
      "an equal comparison reads as a sentence");
    a.equal(img.comparisons[1], "Aspect matters 3 times as much as Elevation.",
      "and so does an unequal one, the right way round");
    a.equal(img.comparisons[2], "Aspect matters 5 times as much as Slope.", "and the third");
    a.equal(img.weightsHeading, "The weights these give", "the weights are labelled");
    a.equal(img.weightsNote,
      "Each one twice: a share of 100 per cent, then the same number as a fraction.",
      "and the two forms of the number are explained rather than left to be guessed");
    a.equal(img.weights[0].name, "Elevation", "each weight carries its name");
    a.equal(img.weights[0].pct, "18.52%", "its percentage");
    a.equal(img.weights[0].frac, "0.1852", "and its fraction");
    a.equal(img.weights[2].name + " " + img.weights[2].pct, "Aspect 65.86%", "the third weight");
    a.equal(img.ratioHeading, "How well the comparisons agree", "the ratio is labelled");
    a.equal(img.ratio,
      "Consistency ratio 0.0251. That is below 0.10, so this page says agree.",
      "the ratio says where it sits against the bar, and who says agree");
    a.equal(img.ratioNote,
      "This measures whether the three comparisons agree with each other. "
      + "It says nothing about whether they are right.",
      "and the picture carries the sentence the page carries");
    a.equal(img.circle, undefined, "no circle line when the comparisons are not a circle");
    a.ok(img.source.indexOf("Made on this page: http") === 0,
      "the address a reader can go back to: " + img.source);
    a.ok(img.source.indexOf("/pairwise/") > 0, "which is this page");
    a.ok(/^Saved on \d{4}-\d{2}-\d{2}$/.test(img.date), "and a dated line: " + img.date);

    // The other side of the bar, and the circle.
    set(w, 5, -3, -5);
    a.equal(w.T.imageText().ratio,
      "Consistency ratio 0.1169. That is 0.10 or above, so this page says disagree.",
      "over the bar it says so in the same shape");
    set(w, 3, -3, 3);
    a.equal(w.T.imageText().circle,
      "These three comparisons run in a circle, so they cannot all be true.",
      "and a circle is named in the picture as it is on the page");

    // Change two inputs, and the record has to follow both. What is saved and what is
    // shown are written by different code and can disagree.
    set(w, 9, 9, 1);
    var img2 = w.T.imageText();
    a.equal(img2.comparisons[0], "Elevation matters 9 times as much as Slope.",
      "the saved comparison follows the control");
    a.equal(img2.weights[0].pct, "81.82%", "and so does the saved weight");
    a.equal(img2.percents.join(" / "), pcts(w).join(" / ").replace(/%/g, ""),
      "the saved shares are the shares on screen");
    a.equal(img2.circle, undefined, "and the circle line went away with the circle");

    var w2 = open("?n=Shade,View,Quiet&c12=-4");
    var img3 = w2.T.imageText();
    a.equal(img3.weights[0].name, "Shade", "renaming reaches the picture");
    a.equal(img3.comparisons[0], "View matters 4 times as much as Shade.",
      "and reaches the sentences, in the right order");
  });

  t("the saved picture draws its bars against 100, like the page", function (a) {
    // The one part of the picture that is a drawing rather than a string. A bar scaled
    // to the largest weight would be full width whatever it held, in the file a marker
    // opens months later, and no assertion about the text would see it. The stub
    // records every fillRect, so the widths can be read back off the picture.
    var w = open("?c13=-3&c23=-5");
    w.T.drawImage();
    var ctx = w.doc.getElementById("shot")._ctx;
    var fills = ctx.rects.filter(function (r) { return r.style === "#1a5fb4"; });
    var tracks = ctx.rects.filter(function (r) { return r.style === "#bcc0c6"; });
    a.equal(fills.length, 3, "three bars are drawn");
    a.equal(tracks.length, 3, "each against its own full-width track");
    var CW = tracks[0].w;
    a.ok(CW > 600, "the track is the content width, " + CW + " px");
    [18.52, 15.62, 65.86].forEach(function (pct, i) {
      a.close(fills[i].w / CW * 100, pct, 0.01,
        "bar " + i + " is " + pct + " per cent of the track");
      a.equal(tracks[i].w, CW, "and every track is the same width");
    });
    a.ok(fills[2].w < CW, "the largest bar is not full width");
    // And it follows the controls rather than a stale copy.
    set(w, 9, 9, 1);
    w.T.drawImage();
    var after = w.doc.getElementById("shot")._ctx.rects.filter(function (r) { return r.style === "#1a5fb4"; });
    a.close(after[after.length - 3].w / CW * 100, 81.82, 0.01, "redrawn at the new setting");
  });

  t("a saved picture does not stay on the page after a control moves", function (a) {
    // Found in the browser rather than here: press Save on the fallback route and
    // then press a stepper, and a picture of the old setting sat under a page
    // showing the new one, looking exactly as current.
    var w = open();
    var box = w.doc.getElementById("saved");
    box.hidden = false;
    w.doc.getElementById("up12").click();
    w.settle();
    a.ok(box.hidden, "one press of a stepper puts it away");
    box.hidden = false;
    click(w, "Two tied");
    a.ok(box.hidden, "so does a preset");
    box.hidden = false;
    click(w, "Reset");
    a.ok(box.hidden, "and so does reset");
  });

  // ---- what is on the face -------------------------------------------------

  t("the opening state says nothing has been said, and stops saying it", function (a) {
    var w = open();
    a.equal(txt(w, "ratio-line"), "Nothing has been said yet. All three comparisons are equal.",
      "the opening line");
    set(w, 2, 1, 1);
    a.equal(txt(w, "ratio-line"),
      "This measures whether your three comparisons agree with each other. "
      + "It says nothing about whether they are right.",
      "one move and the other line takes over");
    a.equal(txt(w, "ratio-line").split(/\s+/).length, 18, "which is eighteen words");
    click(w, "Reset");
    a.equal(txt(w, "ratio-line").indexOf("Nothing has been said yet"), 0,
      "and reset puts the opening line back");
    // The two never share the face.
    a.ok(txt(w, "ratio-line").indexOf("says nothing about whether") < 0,
      "only one of the two lines is ever on screen");
  });

  t("a circle of comparisons is named on screen at the moment it happens", function (a) {
    var w = open();
    a.ok(w.doc.getElementById("cycle-line").hidden, "no such line at rest");
    click(w, "Each beats the next");
    a.ok(!w.doc.getElementById("cycle-line").hidden, "the line appears");
    a.ok(txt(w, "cycle-line").indexOf("run in a circle") > 0, "and says what happened");
    a.ok(txt(w, "cycle-line").indexOf("refusing") > 0,
      "and that equal shares here are the method refusing: " + txt(w, "cycle-line"));
    a.equal(pcts(w).join(" / "), "33.34% / 33.33% / 33.33%",
      "which is the moment three near-identical bars would otherwise read as a finding");
    // Not every failing setting is a circle, and the line must not claim otherwise.
    set(w, 5, -3, -5);
    a.equal(txt(w, "verdict"), "disagree", "this one fails the bar");
    a.ok(w.doc.getElementById("cycle-line").hidden, "and is not a circle, so no circle line");
    // The count the proposal records.
    var cyc = 0, fail = 0;
    AXIS.forEach(function (x) { AXIS.forEach(function (y) { AXIS.forEach(function (z) {
      var r = w.T.solveAt(x, y, z);
      if (r.cycle) cyc++;
      if (r.CR >= 0.10) fail++;
    }); }); });
    a.equal(cyc, 1024, "1,024 of the 4,913 settings are a circle");
    a.equal(fail, 3826, "3,826 of them are at or above 0.10");
  });

  t("the classroom panel holds the three student steps and nothing else", function (a) {
    // It stays on the projector, so whatever is in it is read by the room. Telling a
    // class what the task will produce before it does the task hands over the answer,
    // and a note about our own process is not addressed to a student at all. Both
    // paragraphs moved to docs/widgets/pairwise.md.
    var w = open();
    var ps = w.doc.getElementById("info-classroom").querySelectorAll("p");
    a.equal(ps.length, 3, "three paragraphs, one per step");
    a.ok(ps[0].textContent.indexOf("On your own, one minute, on paper.") === 0,
      "the commitment comes first, on paper, before the page");
    a.ok(ps[1].textContent.indexOf("In pairs, two minutes, one phone between two.") === 0,
      "then the pair");
    a.ok(ps[2].textContent.indexOf("Back to the room, two minutes.") === 0, "then the room");
    var all = w.doc.getElementById("info-classroom").textContent;
    ["running the room", "principles.md", "54.99", "72.48", "candidate", "Two tied"].forEach(function (s) {
      a.equal(all.indexOf(s), -1, "the panel does not carry " + JSON.stringify(s));
    });
    a.equal(w.doc.querySelectorAll(".classroom .note").length, 0,
      "and no note to ourselves is left in it");
  });

  t("nothing can make the layout wider than the viewport", function (a) {
    // The stub lays nothing out, so this cannot measure a right edge. What it can do is
    // assert the three guards that stop the measurement going wrong, each of which was
    // added because the page really did run 14 px past a 320 px phone: one table in one
    // (i) panel, in a grid track sized to its widest min-content.
    // The measurement itself is in the browser, and the numbers are in
    // docs/widgets/pairwise.md: 320, 360 and 375, every panel open, long names, zero
    // elements past the edge and zero clipped.
    var html = fs.readFileSync(FILE, "utf8");
    var style = html.slice(html.indexOf("<style>"), html.indexOf("</style>"));
    a.ok(/grid-template-columns:\s*minmax\(0,\s*1fr\);/.test(style),
      "the one-column track is minmax(0, 1fr), not the default auto");
    ["result", "cmps", "tools"].forEach(function (area) {
      a.ok(new RegExp("\\." + area + "\\s*\\{[^}]*min-width:\\s*0").test(style),
        "." + area + " declares min-width: 0");
    });
    a.ok(/\.matrix-wrap\s*\{[^}]*overflow-x:\s*auto/.test(style),
      "the table scrolls inside its own box");
    var w = open();
    var table = w.doc.getElementById("matrix");
    a.equal(table.parentNode.className, "matrix-wrap",
      "and the table is actually inside that box");
    // No fixed pixel width on anything that holds content: that is the other way a
    // layout stops fitting a narrow phone.
    var fixed = style.match(/[^-]width:\s*\d{3,}px/g);
    a.equal(fixed, null, "no element is given a fixed width of 100 px or more");
  });

  t("nothing on the page is empty", function (a) {
    var w = open();
    w.doc.querySelectorAll(".wrow").forEach(function (row) {
      a.ok(row.querySelector(".wname").textContent.trim().length > 0, "a weight row has a name");
      a.ok(row.querySelector(".wpct").textContent.trim().length > 0, "and a percentage");
      a.ok(row.querySelector(".fill").style.width, "and a drawn bar");
    });
    w.doc.querySelectorAll(".help-panel").forEach(function (p) {
      a.ok(p.textContent.trim().length > 20,
        "the panel " + p.id + " has something in it");
    });
    w.doc.querySelectorAll(".cmp").forEach(function (g) {
      a.ok(g.querySelector(".read-num").textContent.trim().length > 0, "a readout is not blank");
      a.ok(g.querySelector(".read-word").textContent.trim().length > 0, "nor are its words");
    });
    a.ok(w.doc.getElementById("matrix").querySelectorAll("td").length === 9,
      "the working shows all nine entries");
    a.ok(txt(w, "extras").indexOf("Largest eigenvalue") === 0, "and the two spare numbers");
  });

  t("the argument is in the reading flow, not behind a control", function (a) {
    var w = open();
    // Presentation mode removes the (i) panels, so anything living only there is
    // missing from every lecture. principles.md sections 3 and 13.
    a.equal(w.doc.querySelector(".framing").closest(".help-panel"), null,
      "the framing sentence is not inside a panel");
    a.equal(w.doc.getElementById("ratio-line").closest(".help-panel"), null,
      "nor is the line under the ratio");
    a.equal(w.doc.getElementById("cycle-line").closest(".help-panel"), null,
      "nor the line that fires on a circle");
    var html = fs.readFileSync(FILE, "utf8");
    var style = html.slice(html.indexOf("<style>"), html.indexOf("</style>"));
    a.ok(style.indexOf('body[data-present="1"] .framing') < 0,
      "and no rule hides the framing sentence on a projector");
    a.ok(style.indexOf('body[data-present="1"] .help-panel:not(.classroom)') > 0,
      "while the other panels do go");
    a.ok(style.indexOf('.info:not(.classroom-btn)') > 0,
      "and the classroom panel is the one that stays");
  });

  t("presentation mode keeps the numbers and drops the rest", function (a) {
    var w = open("?present=1");
    a.equal(w.doc.body.getAttribute("data-present"), "1", "the page opens in presentation mode");
    a.equal(w.doc.getElementById("present").getAttribute("aria-pressed"), "true",
      "and the button says so");
    ["wpct0", "wpct1", "wpct2", "cr", "verdict", "num12", "num13", "num23"].forEach(function (id) {
      a.ok(txt(w, id).trim().length > 0, id + " still has something in it");
    });
    // The things that go are marked, so the CSS and the test agree about which.
    ["wfrac0", "lesson", "rename", "save", "strip12"].forEach(function (id) {
      a.ok((" " + w.doc.getElementById(id).className + " ").indexOf(" hide-present ") >= 0,
        id + " is marked to go on a projector");
    });
    a.ok((" " + w.doc.getElementById("reset").className + " ").indexOf(" hide-present ") < 0,
      "reset stays, because a student at the front still needs it");
  });

  t("the link carries the setting, and drops what is at its default", function (a) {
    var w = open();
    set(w, 5, -3, -5);
    w.settle();
    a.equal(w.location.search, "?c12=5&c13=-3&c23=-5", "three comparisons, nothing else");
    click(w, "All equal");
    w.settle();
    a.equal(w.location.search, "", "a default setting writes an empty query");
    var w2 = open("?c12=5&c13=-3&c23=-5");
    a.equal(txt(w2, "cr"), "0.1169", "and the link restores the setting it carried");
    a.equal(txt(w2, "num12"), "Elevation 5 times Slope", "including which way round it is");
    var w3 = open("?c12=-5");
    a.equal(txt(w3, "num12"), "Slope 5 times Elevation",
      "a minus sign means the second of the pair, which is half of what a comparison is");
    var w4 = open("?c12=0&c13=99&c23=abc");
    a.equal(w4.T.state().c["12"], 1, "a zero is not a comparison, so it falls back to equal");
    a.equal(w4.T.state().c["13"], 1, "nor is anything past nine");
    a.equal(w4.T.state().c["23"], 1, "nor is a word");
  });

  t("the live region says what changed", function (a) {
    var w = open();
    w.doc.getElementById("up12").click();
    w.settle();
    var said = txt(w, "live");
    a.ok(said.indexOf("Slope 2 times Elevation") === 0, "it names the comparison: " + said);
    a.ok(said.indexOf("Consistency ratio") > 0, "and the ratio");
    a.ok(said.indexOf("per cent") > 0, "and the three shares");
  });

  t("the page ships no unchecked citation and none of the lab's own story", function (a) {
    var html = fs.readFileSync(FILE, "utf8");
    var body = html.slice(html.indexOf("<body>"));
    a.equal(body.indexOf("For more, see"), -1,
      "no (i) panel ends in a citation, because none has been through the check yet");
    ["botanist", "Okanagan", "species", "plant"].forEach(function (word) {
      a.equal(body.toLowerCase().indexOf(word.toLowerCase()), -1,
        "nothing on the page about " + word);
    });
    a.equal(body.indexOf("123ahp"), -1, "and nothing naming another tool");
    a.ok(body.indexOf("Made by Luke Bergmann with Claude") > 0, "the credit line reads as it should");
    a.equal(html.indexOf("<script src"), -1, "one self-contained file, no second request");
  });
};
