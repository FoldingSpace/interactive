"use strict";
// Tests for web/maup. The prompt for these was a card that had been empty for months: the
// commit that turned a printed equation into a row of maps deleted the code filling it and
// left the element behind, and nothing noticed. One assertion here would have.

var path = require("path");
var L = require("./load.js");
var dom = require("./dom.js");

var FILE = path.join(__dirname, "..", "..", "web", "maup", "index.html");

function open(search) {
  var w = L.load(FILE, { search: search || "" });
  w.settle();
  return w;
}
function click(w, text) {
  var b = w.doc.querySelectorAll(".opt, .preset, button").filter(function (e) {
    return e.textContent.indexOf(text) >= 0;
  })[0];
  if (!b) throw new Error("no control containing " + JSON.stringify(text));
  b.click();
  w.settle();
  return b;
}
// Sum the five terms against the result, straight out of the widget's own accessor.
function sumError(w) {
  var T = w.win.MAUP_TEST, st = T.state();
  var ids = T.layers.map(function (l) { return l.id; });
  var vals = {}, worst = 0, n = 0, i;
  ids.forEach(function (id) { vals[id] = T.valuesFor(id, st); });
  for (i = 0; i < st.k; i++) {
    if (!st.ag.use[i]) continue;
    var sum = 0;
    ids.forEach(function (id) { if (id !== "be") sum += vals[id][i]; });
    var d = Math.abs(sum - vals.be[i]);
    if (d > worst) worst = d;
    n++;
  }
  return { worst: worst, areas: n };
}

module.exports = function (t) {

  t("opens on the recorded regression", function (a) {
    var w = open();
    a.equal(w.doc.getElementById("r2").textContent, "56%", "R squared at 996 areas");
    a.equal(w.doc.getElementById("moran").textContent, "0.165", "Moran's I of the residuals");
  });

  t("census tracts give the recorded weaker fit", function (a) {
    var w = open();
    click(w, "Census tracts");
    a.equal(w.doc.getElementById("r2").textContent, "53%", "R squared at 118 tracts");
  });

  t("every card on the page has something in it", function (a) {
    // The assertion that would have caught the empty card. A titled box with a collapsed
    // body looks like a rendering glitch and reads as one.
    var w = open();
    w.doc.querySelectorAll(".stat").forEach(function (card) {
      var label = card.querySelector(".label");
      var body = card.querySelectorAll(".big, .sub, .pick-line, .eqrow");
      var text = "";
      body.forEach(function (e) { text += e.textContent.trim(); });
      a.ok(text.length > 0,
        'the "' + label.textContent.trim().replace(/\s+/g, " ").replace(" i", "") + '" card is not empty');
    });
  });

  t("what the crossed-out numbers mean is on the page, not only behind an (i)", function (a) {
    var w = open();
    click(w, "Census tracts");                     // income stops holding up here
    var struck = w.doc.querySelectorAll(".tbeta .dead");
    a.ok(struck.length > 0, "something is crossed out at census tracts");
    var note = w.doc.getElementById("eqnote").textContent;
    a.ok(note.indexOf("Crossed out") >= 0, "the visible card says what crossing out means: " + note);
    a.ok(note.indexOf("income") >= 0, "and names which term it applies to");
    // The (i) panels are removed in presentation mode, so an explanation living only there
    // is missing from every lecture. This body is not a help panel.
    a.equal(w.doc.getElementById("eqnote").closest(".help-panel"), null,
      "the explanation is outside the (i) panel");
  });

  t("the constant is tested like the other terms and printed without a times sign", function (a) {
    var w = open();
    var c = w.doc.getElementById("constval").textContent;
    a.ok(c.indexOf("×") < 0, "the constant multiplies nothing, so no times sign: " + c);
    a.ok(/±/.test(c), "and it carries its standard error: " + c);
    var T = w.win.MAUP_TEST, st = T.state();
    a.ok(st.model.p.length === 3 && isFinite(st.model.p[0]),
      "the constant has a p-value, which is why it can be tested");
  });

  t("the row reads the five terms in order, constant third", function (a) {
    var w = open();
    // The titles carry the operators too, so the top of the row reads as the equation.
    var titles = w.doc.getElementById("eqrow").querySelectorAll(".tname").map(function (e) {
      return e.textContent.replace(/\s+/g, " ").trim();
    });
    a.equal(titles[0], "household size contribution +", "first term, and a plus after it");
    a.equal(titles[1], "income contribution +", "second term");
    a.equal(titles[2], "the model\u2019s constant term +",
      "the constant sits third, left of the spatial error");
    a.equal(titles[3], "spatial error we account for +", "fourth term");
    a.equal(titles[4], "residual error", "fifth term, and no plus: an equals comes next");
    a.ok(/^=\s/.test(titles[5]), "and the result is introduced by the equals: " + titles[5]);
    // Read straight across, the titles are the equation.
    a.equal(titles.join(" "),
      "household size contribution + income contribution + the model\u2019s constant term + "
      + "spatial error we account for + residual error = " + titles[5].replace(/^=\s*/, ""),
      "the title line scans left to right as the equation");
    a.equal(w.win.MAUP_TEST.layers.map(function (l) { return l.id; }).join(","),
      "hh,inc,const,sperr,res,be", "and the layer list says the same");
  });

  t("the five terms add up to the reported counts", function (a) {
    var w = open();
    var d = sumError(w);
    a.equal(d.areas, 995, "995 areas carry a model");
    a.ok(d.worst < 1e-13, "worst sum error " + d.worst.toExponential(2) + " across dissemination areas");
    click(w, "Census tracts");
    var c = sumError(w);
    a.equal(c.areas, 118, "118 census tracts");
    a.ok(c.worst < 1e-13, "worst sum error " + c.worst.toExponential(2) + " across census tracts");
  });

  t("the spatial error map is empty when the model is aspatial", function (a) {
    var w = open();
    click(w, "Aspatial OLS");
    var T = w.win.MAUP_TEST, st = T.state();
    // Two different claims, and only one of them is "exactly zero". The values carry
    // floating-point noise, because the term is a subtraction of two quantities computed by
    // different routes. What is drawn is nothing at all, and that is the claim on the page.
    var v = T.valuesFor("sperr", st), i, worst = 0;
    for (i = 0; i < st.k; i++) if (st.ag.use[i]) worst = Math.max(worst, Math.abs(v[i]));
    a.ok(worst < 1e-13, "spatial error is " + worst.toExponential(2) + ", which is noise not signal");
    a.equal(w.doc.getElementById("m-sperr").querySelectorAll("circle").length, 0,
      "and nothing is drawn: not small circles, none");
    a.equal(w.doc.getElementById("b-sperr").textContent, "nothing: this model assumes none",
      "and the panel says so rather than going blank");
    click(w, "Spatial error model");
    a.equal(w.doc.getElementById("b-sperr").textContent, "neighbourhood effects of unknown origin",
      "the spatial model names what the term stands in for");
    a.ok(w.doc.getElementById("m-sperr").querySelectorAll("circle").length > 900,
      "and the spatial model does draw the term");
  });

  t("the symbol key puts each number beside its own circle, and the two divide", function (a) {
    var w = open();
    ["Dissemination areas", "Census tracts"].forEach(function (z) {
      click(w, z);
      var svg = w.doc.getElementById("symkey").querySelector("svg");
      var texts = svg.querySelectorAll("text"), circles = svg.querySelectorAll("circle");
      a.equal(texts.length, 2, z + ": two labelled sizes");
      var big = +texts[0].textContent, small = +texts[1].textContent;
      a.equal(small * 4, big, z + ": the smaller circle is a quarter of the bigger, " + big + " and " + small);
      a.equal(big % 4, 0, z + ": the bigger is a multiple of four so the quarter is whole (" + big + ")");
      // each label sits immediately to the right of the circle it belongs to, which is the
      // whole point: the numbers used to be a trailing list you had to pair off by guessing
      var r0 = +circles[0].getAttribute("r"), r1 = +circles[1].getAttribute("r");
      var gap0 = +texts[0].getAttribute("x") - (+circles[0].getAttribute("cx") + r0);
      var gap1 = +texts[1].getAttribute("x") - (+circles[1].getAttribute("cx") + r1);
      a.ok(gap0 > 0 && gap0 < 8, z + ": the big number sits just right of its circle (gap " + gap0.toFixed(1) + ")");
      a.ok(gap1 > 0 && gap1 < 8, z + ": the small number sits just right of its circle (gap " + gap1.toFixed(1) + ")");
      a.ok(+circles[1].getAttribute("cx") - r1 > +texts[0].getAttribute("x"),
        z + ": and the second pair starts after the first number, not on top of it");
      // area goes with the value, so the radius goes with its square root: half for a quarter
      a.ok(Math.abs(r1 * 2 - r0) < 0.02, z + ": a quarter of the value is half the radius (" + r0 + ", " + r1 + ")");
      a.equal(circles[0].getAttribute("cy"), circles[1].getAttribute("cy"),
        z + ": both circles sit on one midline");
      a.equal(texts[0].getAttribute("y"), texts[1].getAttribute("y"),
        z + ": and both numbers with them");
    });
  });

  t("the page still refuses the category its lab asks about", function (a) {
    var fs = require("fs");
    var html = fs.readFileSync(FILE, "utf8");
    var body = html.slice(html.indexOf("<body>"));
    a.equal(body.indexOf("Break and Enter Residential"), -1,
      "residential break and enter is not offered");
    a.ok(body.indexOf("missing on purpose") > 0, "and the page says that is deliberate");
  });
};
