"use strict";
// Tests for web/least-cost. The point of these is not that the widget computes a route —
// that is easy to see. It is that the route it *draws* is a real path from the substation
// to the plant, and that the alternatives it draws really do cost what the page says they
// cost, after the map has been drawn on and the numbers have been changed.

var path = require("path");
var L = require("./load.js");
var dom = require("./dom.js");

var FILE = path.join(__dirname, "..", "..", "web", "least-cost", "index.html");
var W = 660, H = 570, CELL = 100 / 3, SUB = "73,154", DST = "450,540";
var SCALE = 1;   // pixels per cell for the pretend canvas, so pointer maths is exact

function open(search) {
  var w = L.load(FILE, { search: search || "" });
  w.doc.getElementById("cv")._rect = { left: 0, top: 0, width: W * SCALE, height: H * SCALE };
  w.doc.querySelectorAll(".bar").forEach(function (b) {
    b._rect = { left: 0, top: 0, width: 200, height: 24 };
  });
  w.settle();
  return w;
}
function hex(s) {
  s = String(s).trim().replace("#", "");
  return [parseInt(s.slice(0, 2), 16), parseInt(s.slice(2, 4), 16), parseInt(s.slice(4, 6), 16)];
}

// Read the map back out of the pixels the widget painted, and the routes back out of the
// SVG it built. Nothing here looks at the widget's own variables.
function readDrawing(w) {
  var pal = [], dim = hex(w.vars["--dim"]), i;
  for (i = 1; i <= 9; i++) {
    var c = hex(w.vars["--c" + i]);
    pal.push({ k: i, full: c, faded: c.map(function (v, j) { return v + (dim[j] - v) * 0.62; }) });
  }
  var img = w.doc.getElementById("cv").painted;
  var land = new Uint8Array(W * H), inBand = new Uint8Array(W * H);
  for (i = 0; i < W * H; i++) {
    var r = img.data[i * 4], g = img.data[i * 4 + 1], b = img.data[i * 4 + 2];
    var bk = -1, bd = Infinity, faded = false;
    pal.forEach(function (p) {
      var e1 = Math.hypot(r - p.full[0], g - p.full[1], b - p.full[2]);
      var e2 = Math.hypot(r - p.faded[0], g - p.faded[1], b - p.faded[2]);
      if (e1 < bd) { bd = e1; bk = p.k; faded = false; }
      if (e2 < bd) { bd = e2; bk = p.k; faded = true; }
    });
    land[i] = bk; inBand[i] = faded ? 0 : 1;
  }
  var cost = {};
  w.doc.querySelectorAll(".bar").forEach(function (b) {
    cost[+b.getAttribute("data-k")] = +b.getAttribute("aria-valuenow");
  });
  var lines = w.doc.getElementById("ov").querySelectorAll("polyline");
  function pts(p) {
    return p.getAttribute("points").trim().split(/\s+/).map(function (s) {
      var a = s.split(","); return { c: Math.floor(+a[0]), r: Math.floor(+a[1]) };
    });
  }
  function evaluate(P) {
    var total = 0, metres = 0, illegal = 0;
    for (var i = 0; i < P.length - 1; i++) {
      var dr = P[i + 1].r - P[i].r, dc = P[i + 1].c - P[i].c;
      if (Math.abs(dr) > 1 || Math.abs(dc) > 1 || (!dr && !dc)) illegal++;
      var d = CELL * ((dr && dc) ? Math.SQRT2 : 1);
      total += (cost[land[P[i].r * W + P[i].c]] + cost[land[P[i + 1].r * W + P[i + 1].c]]) * 0.5 * d;
      metres += d;
    }
    return {
      cost: total, km: metres / 1000, cells: P.length, illegal: illegal,
      from: P[0].r + "," + P[0].c, to: P[P.length - 1].r + "," + P[P.length - 1].c,
      whollyInBand: P.every(function (q) { return inBand[q.r * W + q.c] === 1; })
    };
  }
  var heavy = lines.filter(function (p) { return p.getAttribute("stroke-width") === "5.7"; });
  var thin = lines.filter(function (p) { return p.getAttribute("stroke-width") === "2.7"; });
  return {
    cells: heavy.length ? pts(heavy[0]).map(function (q) { return q.r * W + q.c; }) : [],
    best: heavy.length ? evaluate(pts(heavy[0])) : null,
    alts: thin.map(function (p) { return evaluate(pts(p)); }),
    bandCells: Array.prototype.reduce.call(inBand, function (a, v) { return a + v; }, 0)
  };
}

// --- driving the widget --------------------------------------------------------------
function press(el, key) { el.dispatchEvent(dom.makeEvent("keydown", { key: key, target: el })); }
function setValue(w, k, want) {
  var bar = w.doc.querySelector('.bar[data-k="' + k + '"]'), guard = 0;
  press(bar, "Home");
  while (+bar.getAttribute("aria-valuenow") !== want && guard++ < 600) {
    press(bar, +bar.getAttribute("aria-valuenow") < want ? "ArrowRight" : "ArrowLeft");
  }
  w.settle();
  return +bar.getAttribute("aria-valuenow");
}
function stroke(w, k, brush, x0, y0, x1, y1, steps) {
  w.doc.querySelector('.swatch[data-k="' + k + '"]').click();
  w.doc.querySelector('[data-brush="' + brush + '"]').click();
  var mb = w.doc.getElementById("mapbox");
  function ev(t, f) {
    return dom.makeEvent(t, {
      clientX: (x0 + (x1 - x0) * f) * W * SCALE, clientY: (y0 + (y1 - y0) * f) * H * SCALE,
      pointerId: 1, target: mb
    });
  }
  mb.dispatchEvent(ev("pointerdown", 0));
  for (var i = 1; i <= steps; i++) mb.dispatchEvent(ev("pointermove", i / steps));
  mb.dispatchEvent(ev("pointerup", 1));
  w.settle();
}
function bandOn(w, tol) {
  var btn = w.doc.getElementById("band");
  if (btn.getAttribute("aria-pressed") !== "true") btn.click();
  w.doc.querySelector('[data-tol="' + tol + '"]').click();
  w.settle();
}

// --- the tests -------------------------------------------------------------------------
module.exports = function (t) {

  // The composition assertions below are deliberately exact, and they are the most
  // fragile thing in this file — on purpose. Changing the queue inside the solver from a
  // binary heap to buckets left the accumulated cost bit-identical and moved half the
  // route, because the two routes tie. Any change that moves the line should have to come
  // and re-record these, and read this comment while doing it.
  t("opens showing a route, and it is the recorded one", function (a) {
    var w = open();
    a.equal(w.doc.getElementById("len").textContent, "20.4", "opening length");
    a.equal(w.doc.getElementById("mix").textContent,
      "Crosses 57% farmland, 23% industry, 9% open land.", "opening composition");
    var d = readDrawing(w);
    a.equal(d.best.from, SUB, "route starts at the substation");
    a.equal(d.best.to, DST, "route ends at the plant");
    a.equal(d.best.illegal, 0, "every step is an eight-neighbour move");
    a.close(d.best.km, 20.44, 0.02, "drawn length matches the model");
    a.close(d.best.cost, 316031.87, 0.5, "drawn route re-costs to the recorded optimum");
  });

  t("the three presets give the recorded routes", function (a) {
    var w = open();
    var want = [
      ["Protect farmland", "24.3", "Crosses 35% road and rail, 33% open land, 28% industry."],
      ["Follow what is built", "24.5", "Crosses 84% road and rail, 14% open land, 2% industry."],
      ["Keep away from homes", "22.9", "Crosses 33% farmland, 29% open land, 26% industry."]
    ];
    var buttons = w.doc.querySelectorAll("#presets .act");
    a.equal(buttons.length, 3, "three presets, and none of them a cost claim");
    want.forEach(function (row, i) {
      a.equal(buttons[i].textContent, row[0], "preset " + i + " name");
      buttons[i].click(); w.settle();
      a.equal(w.doc.getElementById("len").textContent, row[1], row[0] + " length");
      a.equal(w.doc.getElementById("mix").textContent, row[2], row[0] + " composition");
    });
  });

  ["0.001", "0.01", "0.05"].forEach(function (tol) {
    t("every alternative drawn at " + (tol * 100) + "% is a real route within " + (tol * 100) + "%", function (a) {
      var w = open();
      bandOn(w, tol);
      var d = readDrawing(w);
      a.ok(d.alts.length > 0, "at least one alternative is drawn");
      d.alts.forEach(function (p, i) {
        a.equal(p.from, SUB, "alternative " + i + " starts at the substation");
        a.equal(p.to, DST, "alternative " + i + " ends at the plant");
        a.equal(p.illegal, 0, "alternative " + i + " is contiguous");
        a.ok(p.whollyInBand, "alternative " + i + " lies inside the shading");
        a.ok(p.cost <= d.best.cost * (1 + (+tol)) + 1e-6,
          "alternative " + i + " costs " + (100 * (p.cost / d.best.cost - 1)).toFixed(3) + "%, within " + (tol * 100) + "%");
      });
    });
  });

  t("a wider tolerance never draws fewer alternatives", function (a) {
    var counts = ["0.001", "0.01", "0.05"].map(function (tol) {
      var w = open(); bandOn(w, tol); return readDrawing(w).alts.length;
    });
    a.ok(counts[1] >= counts[0], "1% draws at least as many as 0.1% (" + counts.join(", ") + ")");
    a.ok(counts[2] >= counts[1], "5% draws at least as many as 1% (" + counts.join(", ") + ")");
  });

  t("the shaded area grows with the tolerance", function (a) {
    var areas = ["0.001", "0.01", "0.05"].map(function (tol) {
      var w = open(); bandOn(w, tol); return readDrawing(w).bandCells;
    });
    a.ok(areas[0] < areas[1] && areas[1] < areas[2], "band areas increase: " + areas.join(" < "));
  });

  t("routes and alternatives still hold up after drawing and after changing the numbers",
    function (a) {
      var w = open();
      stroke(w, 7, 11, 0.02, 0.55, 0.98, 0.42, 30);   // a water barrier across the corridor
      stroke(w, 6, 11, 0.30, 0.10, 0.55, 0.95, 30);   // a long park
      stroke(w, 4, 5,  0.60, 0.20, 0.95, 0.80, 30);   // an industrial wedge
      stroke(w, 2, 11, 0.05, 0.20, 0.45, 0.30, 20);   // more housing
      w.doc.getElementById("disarm").click();
      [[1, 93], [2, 40], [6, 30], [9, 7], [7, 161]].forEach(function (p) { setValue(w, p[0], p[1]); });
      ["0.001", "0.01", "0.05"].forEach(function (tol) {
        bandOn(w, tol);
        var d = readDrawing(w);
        a.equal(d.best.from, SUB, tol + ": route still starts at the substation");
        a.equal(d.best.to, DST, tol + ": route still ends at the plant");
        a.equal(d.best.illegal, 0, tol + ": route still contiguous");
        a.close(+w.doc.getElementById("len").textContent, d.best.km, 0.06,
          tol + ": the printed length matches the drawn line");
        a.ok(d.alts.length > 0, tol + ": alternatives are still drawn");
        d.alts.forEach(function (p, i) {
          a.equal(p.illegal, 0, tol + ": alternative " + i + " contiguous after editing");
          a.equal(p.from + ">" + p.to, SUB + ">" + DST, tol + ": alternative " + i + " runs end to end");
          a.ok(p.whollyInBand, tol + ": alternative " + i + " inside the shading");
          a.ok(p.cost <= d.best.cost * (1 + (+tol)) + 1e-6,
            tol + ": alternative " + i + " within tolerance after editing ("
            + (100 * (p.cost / d.best.cost - 1)).toFixed(3) + "%)");
        });
      });
    });

  t("the two positions that use existing corridors stay distinguishable", function (a) {
    // "Protect farmland" prices road and rail low, because a group keeping fields whole has
    // no reason to avoid ground that is already a corridor. Priced too low it stops being
    // about farmland and becomes "follow what is built"; at 5 the two shared 92% of their
    // cells. This guards the gap.
    function routeOf(i) {
      var w = open();
      w.doc.querySelectorAll("#presets .act")[i].click(); w.settle();
      return readDrawing(w).cells;
    }
    var farm = routeOf(0), follow = routeOf(1);
    var f = {}, shared = 0;
    follow.forEach(function (u) { f[u] = 1; });
    farm.forEach(function (u) { if (f[u]) shared++; });
    var pct = Math.round(100 * shared / farm.length);
    a.ok(pct < 60, "the two routes share " + pct + "% of their cells, which is under 60");
    a.ok(pct > 5, "and more than 5%, so farmland is still using corridors where they help");
  });

  t("a kept proposal records the route that matches the numbers beside it", function (a) {
    var w = open();
    w.doc.querySelectorAll("#presets .act")[0].click(); w.settle();
    w.doc.getElementById("pin").click(); w.settle();
    var first = w.doc.querySelector(".pin .stats").textContent;
    a.ok(/^24\.3 km/.test(first), "the kept card carries the route it was kept from: " + first);
    w.doc.querySelectorAll("#presets .act")[1].click(); w.settle();
    w.doc.getElementById("pin").click(); w.settle();
    var cards = w.doc.querySelectorAll(".pin .stats").map(function (e) { return e.textContent; });
    a.ok(/^24\.3 km/.test(cards[0]) && /^24\.5 km/.test(cards[1]),
      "two kept proposals stay distinct: " + cards.join(" | "));
    var names = w.doc.querySelectorAll(".pin input").map(function (e) { return e.getAttribute("value") || e.value; });
    a.equal(names[0], "Protect farmland", "a preset supplies the name it was loaded under");
  });

  t("a link carries the numbers and the kept proposals", function (a) {
    var w = open();
    w.doc.querySelectorAll("#presets .act")[0].click(); w.settle();
    w.doc.getElementById("pin").click(); w.settle();
    w.settle();
    var url = w.location.search;
    a.ok(url.indexOf("c=120.60.20.10.40.125.200.1.20") > 0, "the numbers are in the link");
    a.ok(url.indexOf("k=") > 0, "the kept proposal is in the link");
    var back = open(url);
    a.equal(back.doc.getElementById("len").textContent, "24.3", "reopening restores the route");
    a.equal(back.doc.querySelectorAll(".pin").length, 1, "reopening restores the kept proposal");
    a.equal(back.doc.querySelector(".pin .stats").textContent.slice(0, 7), "24.3 km",
      "the restored proposal carries its route");
  });

  t("drawing is offered before it is armed, and reset offers it again", function (a) {
    var w = open();
    a.equal(w.doc.body.dataset.hinting, "1", "the hint is on at the start");
    a.equal(w.doc.getElementById("mapbox").dataset.armed, "0", "nothing is armed at the start");
    a.ok(w.doc.getElementById("drawhint").textContent.indexOf("draw more of it onto the map") > 0,
      "the hint says what to do");
    w.doc.querySelector('.swatch[data-k="1"]').click();
    a.equal(w.doc.body.dataset.hinting, "0", "the hint goes once anything is armed");
    a.equal(w.doc.getElementById("mapbox").dataset.armed, "1", "arming a class arms the map");
    w.doc.getElementById("reset").click(); w.settle();
    a.equal(w.doc.body.dataset.hinting, "1", "reset offers it again");
    a.equal(w.doc.getElementById("mapbox").dataset.armed, "0", "reset disarms");
    a.equal(w.doc.getElementById("len").textContent, "20.4", "reset returns the opening route");
  });

  t("nothing on the page claims these numbers were measured", function (a) {
    var fs = require("fs");
    var html = fs.readFileSync(FILE, "utf8");
    var body = html.slice(html.indexOf("<body>"));
    ["Cheapest to build", "near tie", "Near ties", "Nobody measured"].forEach(function (bad) {
      a.equal(body.indexOf(bad), -1, 'the page no longer says "' + bad + '"');
    });
    a.ok(body.indexOf("Values are complex and vary by perspective") > 0,
      "the page says the values are contested rather than absent");
    a.ok(body.indexOf("nobody looked up any land prices") > 0,
      "the costs panel still says plainly what these numbers are not");
  });
};
