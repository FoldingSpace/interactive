"use strict";
// Tests for web/relative-distance. Two of these exist because of specific bugs.
//
// The slope threshold was compared against a Float32Array, where a grade stored as
// exactly 50 per mille reads back as 0.050000001 and fails "> 0.05". That quietly
// dropped 93 streets from the traveller who avoids steep ground, and every recorded
// travel time still came out right, so reproducing a known value would not have caught
// it. The counts below would have.
//
// The pins are checked against the drawn SVG rather than against the model, because the
// whole claim of this page is about a picture: two places the same distance apart on the
// ground, drawn far apart once the map measures minutes.

var path = require("path");
var L = require("./load.js");

var FILE = path.join(__dirname, "..", "..", "web", "relative-distance", "index.html");

function open(search) {
  var w = L.load(FILE, { search: search || "", slug: "relative-distance" });
  // The canvas is sized from its container, and nothing has a size here until we say so.
  var box = w.doc.getElementById("mapbox");
  box._rect = { left: 0, top: 0, width: 900, height: 720, right: 900, bottom: 720 };
  w.settle();
  w.win.__rd.relayout();
  w.settle();
  return w;
}
function rd(w) { return w.win.__rd; }
function text(w, id) { return w.doc.getElementById(id).textContent; }
function click(w, label) {
  var b = w.doc.querySelectorAll("button").filter(function (e) {
    return e.textContent.trim() === label;
  })[0];
  if (!b) throw new Error("no button labelled " + JSON.stringify(label));
  b.click(); w.settle();
  return b;
}
function minutes(w, place, dir) {
  return rd(w).timeTo(rd(w).node(place), dir) / 60;
}
function strokedPoints(w) {
  var ctx = w.doc.getElementById("map").getContext("2d");
  var n = 0;
  ctx.strokes.forEach(function (s) {
    s.paths.forEach(function (p) { n += p.length; });
  });
  return n;
}

module.exports = function (t) {

  t("the data is the extent it claims to be", function (a) {
    // An extent is a claim about what is inside it. It lives in three files and a
    // rebuild is where it comes back, so it is asserted here.
    var w = open();
    var D = w.win.RD;
    a.equal(D.n, 24410, "junctions");
    a.equal(D.m, 32250, "street segments");
    a.equal(D.x0, 483000, "west edge, UTM zone 10N easting");
    a.equal(D.y0, 5453100, "south edge, UTM zone 10N northing");
    a.equal(D.places.length, 12, "named places");
  });

  t("it opens with a map drawn and both places named", function (a) {
    var w = open();
    a.ok(strokedPoints(w) > 20000, "streets are actually stroked on the canvas");
    a.equal(text(w, "nameA"), "Lonsdale Quay", "blue pin");
    a.equal(text(w, "nameB"), "Commercial & Hastings", "orange pin");
    a.equal(text(w, "fromline"), "From Waterfront Station", "the start is named");
    a.ok(text(w, "kmA").indexOf("3.47 km") === 0, "straight line to the quay");
    a.ok(text(w, "outA").indexOf("2 h 12") === 0, "and the walk there");
  });

  t("each traveller explains its own speeds, and none of them is empty", function (a) {
    // The panel used to carry all four at once and ran to 2,293 px, which nobody reads.
    // It now shows the traveller you actually chose. That means four separate strings
    // that can each go missing on their own, which is the empty-card failure again.
    var w = open();
    var seen = {};
    ["On foot", "On foot, no steep hills or steps", "By bike", "By car"].forEach(function (label) {
      click(w, label);
      var txt = w.doc.getElementById("modehelp").textContent.trim();
      a.ok(txt.length > 120, label + " has a real explanation");
      a.ok(!seen[txt], label + " has its own, not the last one over again");
      seen[txt] = 1;
    });
    click(w, "By bike");
    var bike = w.doc.getElementById("modehelp").textContent;
    a.ok(bike.indexOf("150 watts") > 0, "the cycling model says where its speed comes from");
    click(w, "On foot");
    a.ok(w.doc.getElementById("modehelp").textContent.indexOf("Tobler") > 0,
         "and the walking model names the rule it uses");
  });

  t("the times column says what it counts as arriving", function (a) {
    // The 150 m rule decides what a dash means, and it was explained nowhere on the page.
    var w = open();
    var p = w.doc.getElementById("info-times");
    a.ok(p, "there is a panel on the two times");
    a.ok(p.textContent.indexOf("150 metres") > 0, "and it gives the rule");
  });

  t("every box on the page has something in it", function (a) {
    // A titled card with a collapsed body reads as a rendering glitch. One of these
    // sat live in another widget here for months.
    var w = open();
    ["fromline", "nameA", "nameB", "kmA", "kmB", "outA", "outB", "backA", "backB",
     "verdict", "mapnote"].forEach(function (id) {
      a.ok(text(w, id).trim().length > 0, id + " is not empty");
    });
  });

  t("the four travellers give the recorded times to Lonsdale Quay", function (a) {
    // Checked against tools/relative-distance-verify.py, which reads the shipped
    // data.js and rebuilds the routing from the written description, sharing no code
    // with the page. Every figure below agreed to six decimal places.
    var w = open();
    a.close(minutes(w, "Lonsdale Quay", "out"), 132.158528, 1e-4, "on foot, there");
    a.close(minutes(w, "Lonsdale Quay", "back"), 129.498085, 1e-4, "on foot, back");
    click(w, "By bike");
    a.close(minutes(w, "Lonsdale Quay", "out"), 33.643006, 1e-4, "by bike, there");
    a.close(minutes(w, "Lonsdale Quay", "back"), 31.495512, 1e-4, "by bike, back");
    click(w, "By car");
    a.close(minutes(w, "Lonsdale Quay", "out"), 12.050535, 1e-4, "by car, there");
    a.close(minutes(w, "Lonsdale Quay", "back"), 12.441450, 1e-4, "by car, back");
  });

  t("there and back are not the same trip", function (a) {
    // If they were, the widget would have nothing to say about one-way streets or
    // hills, and the swap button would be dead.
    var w = open("?m=2");
    var there = minutes(w, "Park Royal", "out"), back = minutes(w, "Park Royal", "back");
    a.close(there, 22.175340, 1e-4, "by bike to Park Royal");
    a.close(back, 19.958891, 1e-4, "and back from it");
    var up = minutes(w, "Upper Lonsdale", "out"), down = minutes(w, "Upper Lonsdale", "back");
    a.close(up, 43.125902, 1e-4, "by bike up to Upper Lonsdale");
    a.close(down, 33.023574, 1e-4, "and rather less coming down");
    a.ok(up - down > 9, "the climb is worth ten minutes, and it is a climb and not a detour");
  });

  t("the count of streets each traveller can use, and can reach", function (a) {
    // This is the assertion the Float32 bug would have failed. The travel times were
    // all still right while 93 segments at exactly five in a hundred were excluded.
    var w = open();
    var want = { 0: [22337, 22828], 1: [7407, 19401], 2: [18213, 18935], 3: [12654, 12738] };
    [0, 1, 2, 3].forEach(function (m) {
      rd(w).set({ mode: m });
      var st = rd(w).state();
      a.equal(st.reach, want[m][0], "mode " + m + ": reachable");
      a.equal(st.usable, want[m][1], "mode " + m + ": usable at all");
    });
  });

  t("a street at exactly five in a hundred is not a steep hill", function (a) {
    // The boundary itself, named. Anything strictly over 50 per mille is refused.
    var w = open("?m=1");
    var D = w.win.RD, at50 = -1, at51 = -1;
    for (var e = 0; e < D.m && (at50 < 0 || at51 < 0); e++) {
      var g = rd(w).gradeMilli(e);
      if (g === 50 && at50 < 0 && (D.ef[e] & 1)) at50 = e;
      if (g === 51 && at51 < 0 && (D.ef[e] & 1)) at51 = e;
    }
    a.ok(at50 >= 0 && at51 >= 0, "the data holds a segment at each side of the line");
    a.ok(rd(w).arcUsable(at50, true), "exactly 50 per mille is allowed");
    a.ok(!rd(w).arcUsable(at51, true), "51 per mille is refused");
  });

  t("a start you cannot set off from is moved to one you can", function (a) {
    // The URL a reader sent in. It snapped the origin onto the far end of a one-way
    // street, where every arc points inwards. Nothing was reachable, no edges were
    // drawn, and the frame collapsed onto an empty extent, so the page showed a blank
    // rectangle with the reason buried in the readout.
    //
    // The cause was a comment that described the intent and code that did not implement
    // it: a junction counted as usable if an arc the traveller can travel *touched* it,
    // in either direction. Being able to arrive somewhere is not being able to leave.
    var w = open("?m=2&o=1100,882&a=270,308");
    var st = rd(w).state();
    a.ok(st.reach > st.usable * 0.5,
         "most of what this traveller could use is reachable from where they were put");
    a.ok(text(w, "cannot").indexOf("100%") < 0, "not a map of nothing");
    a.ok(strokedPoints(w) > 20000, "and there are streets on the canvas");
    var box = rd(w).state().R98;
    a.ok(box > 1000 && box < 40000, "the frame is a sane size rather than collapsed");
  });

  t("a place that cannot be reached says so rather than going blank", function (a) {
    var w = open("?m=1");
    a.equal(text(w, "outA"), "—", "no time to the quay");
    a.equal(text(w, "backA"), "—", "and none coming back");
    a.ok(text(w, "verdict").indexOf("cannot get there at all") > 0, "the readout says why");
    var dashed = w.doc.querySelectorAll("[data-pin] circle").filter(function (e) {
      return e.getAttribute("stroke-dasharray");
    });
    a.ok(dashed.length === 1, "the pin itself is drawn hollow and dashed");
    a.ok(text(w, "cannot").indexOf("62%") === 0, "and how much of the city goes with it");
  });

  t("there is no map between the two maps", function (a) {
    // The control used to be a slider, and half way along it was half a distance added
    // to half a time, which is not a way of measuring anything. Two states now, with
    // the change shown as a movement. This asserts the dial did not come back.
    var w = open();
    a.equal(w.doc.querySelectorAll("input[type=range]").length, 0, "no slider");
    var ends = w.doc.querySelectorAll("[data-s]").map(function (b) { return b.dataset.s; });
    a.equal(ends.join(" "), "0 100", "two states, and only two");
    click(w, "Metres");
    a.equal(rd(w).state().s, 0, "and pressing one lands on it exactly");
    // Nothing a reader reads may wait on an animation frame. A background tab gets
    // none, and this page once sat between its two maps describing neither.
    a.ok(text(w, "mapnote").indexOf("distance in metres") > 0,
         "the note under the map is right before any frame has run");
    a.ok(text(w, "outA").indexOf("2 h 12") === 0, "and so is the table");
  });

  t("the change is drawn as a movement, and it lands exactly", function (a) {
    // The transition is the widget's main gesture now that the slider is gone, so it
    // gets driven here rather than trusted. Frames arrive with a rising clock.
    var w = open();
    var quay = rd(w).node("Lonsdale Quay");
    function radius() {
      var o = rd(w).drawnXY(rd(w).state().start), p = rd(w).drawnXY(quay);
      return Math.hypot(p[0] - o[0], p[1] - o[1]);
    }
    var minutes = radius();
    click(w, "Metres");
    var metres = radius();
    // 3.47 km on the ground against 132 minutes on foot: at this scale the quay is
    // drawn about twice as far out once the map measures the trip.
    a.close(minutes / metres, 2.07, 0.12, "the quay moves about twice as far out");

    var btn = w.doc.querySelectorAll("[data-s]").filter(function (b) { return b.dataset.s === "100"; })[0];
    btn.click();
    w.flushFrames(3);
    var mid = radius();
    a.ok(mid > metres && mid < minutes, "part way through, it is part way there");
    w.flushFrames(200);
    a.close(radius(), minutes, 0.01, "and it arrives exactly where it started from");
  });

  t("changing the traveller goes through the true map", function (a) {
    // There is no half-way state between "on foot" and "by car" — the times, the scale
    // and the frame all change at once. What there is, is a state every one of these
    // maps agrees on: at the metres end the drawing is just Vancouver. So the change
    // collapses to it, swaps the model there, and deforms again. This checks the middle
    // really is the true map and not an average of two deformed ones.
    var w = open();
    var quay = rd(w).node("Lonsdale Quay"), comm = rd(w).node("Commercial & Hastings");
    function ratio() {
      var o = rd(w).drawnXY(rd(w).state().start);
      var p = rd(w).drawnXY(quay), q = rd(w).drawnXY(comm);
      return Math.hypot(p[0] - o[0], p[1] - o[1]) / Math.hypot(q[0] - o[0], q[1] - o[1]);
    }
    var onFoot = ratio();
    a.ok(onFoot > 3, "on foot the quay is drawn more than three times further out");

    var btn = w.doc.querySelectorAll("[data-mode]").filter(function (b) { return b.dataset.mode === "3"; })[0];
    btn.click();
    // The readout is the new traveller's before a single frame has run.
    a.ok(text(w, "outA").indexOf("12 min") === 0, "the numbers are the car's immediately");
    // Sample the whole morph rather than guessing which frame the middle lands on. The
    // ratio has to come down through the metre ratio on its way from one shape to the
    // other; if the change were a cross-fade it would pass through an average instead,
    // and 3.47/3.06 is nowhere near the average of 3.5 and 3.13.
    var seen = [ratio()];
    for (var f = 0; f < 90; f++) { w.flushFrames(1); seen.push(ratio()); }
    var low = Math.min.apply(null, seen);
    a.close(low, 3.47 / 3.06, 0.06, "it passes through the real map, not through an average");
    w.flushFrames(300);
    a.close(ratio(), 12.050535 / 3.847020, 0.05, "and arrives at the car's shape");
  });

  t("moving the start does not flash the whole city on the way", function (a) {
    // Moving the start takes the direct route, not the one through the real map. At the
    // real map nothing is held back, so the water and everything else the traveller
    // cannot speak for snaps to full strength for an instant. That flash reads as an
    // error in the middle of a re-centring, so the drawing stays at the minutes end the
    // whole way across and only the positions travel.
    var w = open();
    click(w, "Lonsdale Quay");
    a.equal(text(w, "fromline"), "From Lonsdale Quay", "the readout moves at once");
    var low = 1;
    for (var f = 0; f < 90; f++) { w.flushFrames(1); low = Math.min(low, rd(w).drawS()); }
    a.ok(low > 0.98, "it never drops back towards the metre map");
    w.flushFrames(300);
    a.equal(rd(w).state().start, rd(w).node("Lonsdale Quay"), "and the start lands where it was sent");
    a.close(rd(w).drawS(), 1, 1e-9, "settled at minutes");
  });

  t("changing the traveller goes through the real map without unclipping it", function (a) {
    // The shape still collapses to the true map, which is the thing worth watching. What
    // does not happen on the way is the water and every other held patch returning to
    // full strength for a frame. Two probes, because these are two different things: the
    // geometry passes through metres, the clipping does not.
    var w = open();
    var btn = w.doc.querySelectorAll("[data-mode]").filter(function (b) { return b.dataset.mode === "3"; })[0];
    btn.click();
    var lowS = 1, highFade = 0;
    for (var f = 0; f < 90; f++) {
      w.flushFrames(1);
      lowS = Math.min(lowS, rd(w).drawS());
      highFade = Math.max(highFade, rd(w).groundFade());
    }
    a.ok(lowS < 0.02, "the shape passes through the real map");
    a.ok(highFade < 0.01, "and the held ground stays held the whole way across");
  });

  t("at rest the metre map is still complete", function (a) {
    // The clipping is held only while something is moving. Standing at metres, the
    // photograph is whole — that is what an ordinary map of Vancouver looks like.
    var w = open();
    a.close(rd(w).groundFade(), 0, 1e-9, "at minutes, the held ground is hidden");
    click(w, "Metres");
    w.flushFrames(300);
    a.close(rd(w).groundFade(), 1, 1e-9, "at metres, all of it shows");
  });

  t("the drawing separates two places the ground does not", function (a) {
    // The picture, not the model. On the ground the two pins are within 12% of the
    // same distance from the start. Drawn in minutes they must be far apart, and in
    // the same proportion as their travel times.
    var w = open("?s=0");
    var o = rd(w).drawnXY(rd(w).state().start);
    function drawnR(node) {
      var p = rd(w).drawnXY(node);
      return Math.hypot(p[0] - o[0], p[1] - o[1]);
    }
    var qa = rd(w).node("Lonsdale Quay"), qb = rd(w).node("Commercial & Hastings");
    var metreRatio = drawnR(qa) / drawnR(qb);
    a.close(metreRatio, 3.47 / 3.06, 0.03, "in metres the two are drawn about alike");

    rd(w).set({ s: 100 });
    var o2 = rd(w).drawnXY(rd(w).state().start);
    function drawnR2(node) {
      var p = rd(w).drawnXY(node);
      return Math.hypot(p[0] - o2[0], p[1] - o2[1]);
    }
    var timeRatio = drawnR2(qa) / drawnR2(qb);
    a.close(timeRatio, minutes(w, "Lonsdale Quay", "out") / minutes(w, "Commercial & Hastings", "out"),
            0.02, "in minutes the drawing matches the times");
    a.ok(timeRatio > 3, "and the quay is more than three times further out");
  });

  t("every control changes the picture", function (a) {
    // Dead interface is worse than missing interface, because a reader assumes it works.
    var w = open();
    var base = strokedPoints(w);
    click(w, "On foot, no steep hills or steps");
    var easy = strokedPoints(w);
    a.ok(easy < base * 0.6, "refusing hills removes most of the map");
    click(w, "By car");
    a.ok(strokedPoints(w) !== easy, "and driving is a different map again");
  });

  t("the swap button turns the map around", function (a) {
    var w = open();
    var before = rd(w).state();
    click(w, "Start from the blue pin instead");
    var after = rd(w).state();
    a.equal(after.start, before.a, "the start is where the blue pin was");
    a.equal(after.a, before.start, "and the blue pin is where the start was");
    a.equal(text(w, "fromline"), "From Lonsdale Quay", "the readout follows");
  });

  t("a link carries its configuration and hands it back", function (a) {
    var w = open("?m=3&s=0");
    a.equal(rd(w).state().mode, 3, "traveller from the URL");
    a.equal(rd(w).state().s, 0, "and the slider");
    click(w, "On foot");
    a.ok(w.location.search.indexOf("m=") < 0, "the default traveller leaves the URL clean");
    a.ok(w.location.search.indexOf("s=0") >= 0, "a moved slider stays in it");
  });

  t("presentation mode drops the panels and keeps the argument", function (a) {
    // Whatever the widget is for has to survive the projector. Hiding it behind an (i)
    // that presentation mode then removes is how a lecture loses the point.
    var w = open();
    click(w, "Big screen");
    a.equal(w.doc.body.getAttribute("data-present"), "1", "presentation mode is on");
    var intro = w.doc.querySelector(".intro");
    a.ok(intro.textContent.indexOf("different city") > 0, "the sentence it is for is in the flow");
    a.ok(text(w, "fromline").length > 0 && text(w, "outA").length > 0, "and so are the numbers");
    // How to move the start is the main thing a reader does, so it cannot live behind
    // an (i) that presentation mode then removes.
    var hint = w.doc.querySelector(".hint");
    a.ok(hint && hint.textContent.indexOf("tap the map") > 0, "and so is how to move the start");
  });

  t("the photograph is only stretched where the streets can speak for it", function (a) {
    // The point of the whole ground layer. Interpolating a travel time across Burrard
    // Inlet would stretch the water like everything else, which would say the sea is
    // merely slow. Cells with no reachable junction within 260 m are held where they
    // are and faded out instead, and there have to be a lot of them.
    var w = open();
    var g = rd(w).ground();
    a.equal(g.on, 1, "the photograph is on by default");
    a.equal(g.cells, 8372, "the fine mesh");
    a.ok(g.held > 3500 && g.held < 6000,
         "about half the mesh has no travel time behind it — water, and mountainside");
    rd(w).set({ mode: 3 });
    var car = rd(w).ground();
    a.ok(car.held > g.held, "driving can speak for less of the ground than walking can");
  });

  t("turning the photograph off changes the street palette", function (a) {
    // Measured against the washed image, the pale end of the plain palette sits at
    // 1.9:1, under the 3:1 a drawn line needs. The photograph brings a darker set with
    // it; if that ever silently stops happening, the lines stop being readable.
    var w = open();
    a.equal(w.doc.body.getAttribute("data-basemap"), "1", "photograph on");
    click(w, "Plain");
    a.equal(w.doc.body.getAttribute("data-basemap"), "0", "and off");
    a.equal(rd(w).ground().on, 0, "the mesh is not built when it is not drawn");
    a.equal(rd(w).ground().cells, 0, "and costs nothing");
    a.ok(w.location.search.indexOf("g=0") >= 0, "the choice travels in the URL");
  });

  t("nothing is fetched from anywhere", function (a) {
    var fs = require("fs");
    var html = fs.readFileSync(FILE, "utf8");
    a.ok(!/fetch\(|XMLHttpRequest|https?:\/\/[^"']*\.(js|css)/.test(html),
         "no script, stylesheet or request goes off the page");
    a.ok(/<script src="data\.js">/.test(html), "the data ships beside it");
    a.ok(/img\.src = "basemap\.jpg"/.test(html), "and so does the photograph");
    a.ok(!/img\.src = "https?:/.test(html), "no tile server, so no lecture room wifi");
  });

};
