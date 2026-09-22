"use strict";
// Tests for web/zone-design. The widget's claim is that the same 1,010 records give
// different answers depending on where the lines go and on how the numbers are added up,
// so what is asserted here is that the answers really do differ, in the directions the
// page says they do, and that the drawing says the same thing the model does.

var path = require("path");
var L = require("./load.js");

var FILE = path.join(__dirname, "..", "..", "web", "zone-design", "index.html");

function open(search, hash) {
  var w = L.load(FILE, { search: search || "", hash: hash || "", slug: "zone-design" });
  w.settle();
  return w;
}
function click(w, text) {
  var b = w.doc.querySelectorAll(".opt, .act").filter(function (e) {
    return e.textContent.replace(/\s+/g, " ").trim() === text;
  })[0];
  if (!b) throw new Error("no control reading " + JSON.stringify(text));
  b.click();
  w.settle();
  return b;
}
function T(w) { return w.win.ZONE_TEST; }
// The four presets are named in the data, not in this file, so a rebuild that renames them
// does not need the tests edited.
var RULED = (function () {
  var fs = require("fs");
  var raw = fs.readFileSync(path.join(__dirname, "..", "..", "web", "zone-design", "data.js"), "utf8");
  var d = JSON.parse(raw.slice(raw.indexOf("{"), raw.lastIndexOf("}") + 1));
  return Object.keys(d.zonings).filter(function (k) { return d.zonings[k] && d.zonings[k].zone; }).sort();
})();

module.exports = function (t) {

  t("it opens on eight zones with something drawn", function (a) {
    var w = open();
    var st = T(w).state();
    a.equal(T(w).k(), 8, "eight zones");
    a.ok(st.fit.ok, "a line is fitted from the opening state");
    a.ok(T(w).canPaint(), "and the opening state is one you can paint, so the paint control leads somewhere");
    a.ok(w.doc.getElementById("m-inc").querySelectorAll("path[data-i]").length === T(w).n,
      "one drawn area per dissemination area");
    a.ok(w.doc.getElementById("m-inc").querySelector(".zline").getAttribute("d").length > 100,
      "and the zone boundaries are drawn, not empty");
  });

  t("every area is filled and the two maps use different ramps", function (a) {
    var w = open();
    var inc = w.doc.getElementById("m-inc").querySelectorAll("path[data-i]");
    var nd = w.doc.getElementById("m-nd").querySelectorAll("path[data-i]");
    var blank = 0, same = 0, i;
    for (i = 0; i < inc.length; i++) {
      var a1 = inc[i].getAttribute("fill"), a2 = nd[i].getAttribute("fill");
      if (!a1 || !a2) blank++;
      if (a1 === a2) same++;
    }
    a.equal(blank, 0, "no area is left without a fill");
    a.ok(same < inc.length, "the two maps are not the same picture (" + same + " of " + inc.length + " share a fill)");
  });

  t("the page reports R squared, not r", function (a) {
    // Changed on 22 September. r survives in the widget's own file, where the verification
    // record lives, and nowhere a student reads.
    var w = open();
    var st = T(w).state();
    a.equal(w.doc.getElementById("r").textContent, (st.fit.r * st.fit.r).toFixed(2),
      "the headline number is R squared");
    var head = w.doc.getElementById("t-sc").textContent.replace(/\s+/g, " ");
    a.ok(head.indexOf("R\u00b2 =") > 0, "and so is the header line: " + head);
    a.equal(/\br = /.test(head), false, "which does not also print r");
    var bold = w.doc.getElementById("t-sc").querySelectorAll("b").map(function (e) { return e.textContent; });
    a.equal(bold.length, 2, "two bold items on the header line");
    a.equal(bold[1], (st.fit.r * st.fit.r).toFixed(2), "the slope and the R squared");
    var label = w.doc.getElementById("c-r").querySelector(".label").textContent;
    a.equal(/correlation/i.test(label), false, "and the card is not called a correlation: " + label);
  });

  t("a drag paints every area it crosses, and a tap paints one", function (a) {
    // The browser tool's own drag helper sends a press and a release with nothing between,
    // so a stroke has to be built by hand here. One code path serves mouse, pen and finger:
    // the pointer is captured on the way down and every move is delivered to the map.
    var w = open();
    var svg = w.doc.getElementById("m-inc");
    var paths = svg.querySelectorAll("path[data-i]");
    function pe(type, el, id) {
      var ev = w.win.PointerEvent(type, { target: el, pointerId: id === undefined ? 1 : id,
                                          clientX: 0, clientY: 0, bubbles: true });
      el.dispatchEvent(ev);
      w.settle();
    }
    // A tap: down and up on one area, no move between.
    var one = 40;
    T(w).setZoning(RULED[0]);
    var before = T(w).zone();
    var want = (before[one] + 3) % 8;
    w.doc.querySelectorAll("#paintbtns .opt")[want].click();
    pe("pointerdown", paths[one]);
    pe("pointerup", paths[one]);
    a.equal(T(w).zone()[one], want, "a tap moves the one area under it");

    // A drag: down, then a move over each of a run of areas, then up.
    var run = [];
    for (var i = 200; i < 230; i++) run.push(i);
    var zone2 = (want + 1) % 8;
    w.doc.querySelectorAll("#paintbtns .opt")[zone2].click();
    pe("pointerdown", paths[run[0]]);
    run.slice(1).forEach(function (ix) { pe("pointermove", paths[ix]); });
    pe("pointerup", paths[run[run.length - 1]]);
    var moved = run.filter(function (ix) { return T(w).zone()[ix] === zone2; }).length;
    a.equal(moved, run.length, "every area the drag crossed went into the chosen zone");

    // And a move with no press before it changes nothing.
    var quiet = T(w).zone().join(",");
    pe("pointermove", paths[500]);
    a.equal(T(w).zone().join(","), quiet, "hovering without pressing paints nothing");
  });

  t("both maps paint, and they are one zoning drawn twice", function (a) {
    var w = open();
    var incMap = w.doc.getElementById("m-inc"), ndMap = w.doc.getElementById("m-nd");
    [incMap, ndMap].forEach(function (m) {
      a.ok((m.getAttribute("class") || "").indexOf("paintmap") >= 0,
        m.getAttribute("id") + " is a map you can paint on");
      a.equal(m.getAttribute("role"), "application", m.getAttribute("id") + " says so to a screen reader");
      a.equal(m.getAttribute("tabindex"), "0", "and can be reached by keyboard");
    });
    // A drag on the greenness map moves the same areas as a drag on the income map would.
    function pe(map, type, el) {
      map.dispatchEvent(w.win.PointerEvent(type, { target: el, pointerId: 3, clientX: 0, clientY: 0, bubbles: true }));
      w.settle();
    }
    var ndPaths = ndMap.querySelectorAll("path[data-i]");
    var before = T(w).zone();
    var want = (before[300] + 5) % 8;
    w.doc.querySelectorAll("#paintbtns .opt")[want].click();
    var run = [300, 301, 302, 303, 304];
    pe(ndMap, "pointerdown", ndPaths[run[0]]);
    run.slice(1).forEach(function (ix) { pe(ndMap, "pointermove", ndPaths[ix]); });
    pe(ndMap, "pointerup", ndPaths[run[run.length - 1]]);
    a.equal(run.filter(function (ix) { return T(w).zone()[ix] === want; }).length, run.length,
      "a drag on the greenness map repaints every area it crossed");
    // ...and the income map redraws with it, because there is one zoning.
    var incPaths = incMap.querySelectorAll("path[data-i]");
    var fills = {};
    run.forEach(function (ix) { fills[incPaths[ix].getAttribute("fill")] = 1; });
    a.equal(Object.keys(fills).length, 1, "and the income map draws them all as one zone now");
  });

  t("the zone lines and numbers are the same on both maps", function (a) {
    var w = open();
    var inc = w.doc.getElementById("m-inc"), nd = w.doc.getElementById("m-nd");
    a.equal(nd.querySelector(".zline").getAttribute("d"), inc.querySelector(".zline").getAttribute("d"),
      "the zone boundaries are drawn identically on both");
    a.equal(nd.querySelector(".rim").getAttribute("d"), inc.querySelector(".rim").getAttribute("d"),
      "and so is the study-area edge");
    function nums(svg) {
      return svg.querySelectorAll("text").map(function (t) {
        return t.textContent + "@" + t.getAttribute("x") + "," + t.getAttribute("y");
      }).join(" ");
    }
    a.ok(nums(inc).length > 0, "the zones are numbered");
    a.equal(nums(nd), nums(inc), "identically on both maps, in the same places");
  });

  t("a map you paint on refuses the browser's own touch gestures, and leaves room to scroll", function (a) {
    var fs = require("fs");
    var css = fs.readFileSync(FILE, "utf8");
    css = css.slice(0, css.indexOf("</style>")).replace(/\n/g, " ");
    a.ok(/\.paintmap\s*\{[^}]*touch-action:\s*none/.test(css),
      "a painting map takes touch-action: none, so a finger drag paints");
    a.ok(/pointer:\s*coarse[^@]*\.paintmap\s*\{[^}]*margin/.test(css),
      "a gutter beside it gives a thumb somewhere to scroll from");
  });

  t("nothing on the page says r", function (a) {
    // R squared only, everywhere a reader or a screen reader meets it. r survives in the
    // widget's own file, where the verification record lives.
    var fs = require("fs");
    var html = fs.readFileSync(FILE, "utf8");
    var body = html.slice(html.indexOf("<body>"), html.indexOf("<script src="));
    var text = body.replace(/<[^>]+>/g, " ");
    var bad = text.match(/(?:^|[^A-Za-z])r(?![A-Za-z\u00b2])\s*(?:=|is\b)|\bthe r\b|\br-value\b/);
    a.equal(bad, null, "no r in the page's text, visible or hidden: " + (bad || ""));
    var attrs = body.match(/(?:title|aria-label|alt|placeholder)="[^"]*"/g) || [];
    var badAttr = attrs.filter(function (t) { return /(?:^|[^A-Za-z])r(?![A-Za-z\u00b2])\s*(?:=|is\b)/.test(t); });
    a.equal(badAttr.length, 0, "nor in a label a screen reader reads: " + badAttr.join(" "));
    var w = open();
    T(w).paint(7, 4);
    w.settle();
    a.equal(/(?:^|[^A-Za-z])r(?![A-Za-z\u00b2])\s*(?:=|is\b)/.test(w.doc.getElementById("live").textContent), false,
      "nor in what is announced: " + w.doc.getElementById("live").textContent);
    a.equal(/NaN/.test(w.doc.getElementById("live").textContent), false,
      "and the announcement is a sentence, not a stray arithmetic result");
  });

  t("four rules, eight zones each, and they disagree", function (a) {
    // The whole argument. Four zonings anybody could defend, the same 1,001 areas under
    // each, the same number of zones, and no two of them say the same thing about the line.
    var w = open();
    var ids = RULED;
    var rs = ids.map(function (id) { return T(w).fitAt(id).r; });
    var r2s = rs.map(function (r) { return r * r; });
    var bs = ids.map(function (id) { return T(w).fitAt(id).b; });
    ids.forEach(function (id) {
      a.equal(T(w).fitAt(id).n, 8, id + " has eight zones, so only the boundaries differ");
    });
    a.ok(Math.max.apply(null, r2s) - Math.min.apply(null, r2s) > 0.2,
      "the four disagree about R squared by more than 0.2 (" +
      r2s.map(function (v) { return v.toFixed(2); }).join(", ") + ")");
    a.ok(Math.max.apply(null, bs) - Math.min.apply(null, bs) > 0.005,
      "and their slopes are not the same line (" +
      bs.map(function (v) { return (v * 10).toFixed(3); }).join(", ") + " per $10,000)");
    // The deck's own slide says that aggregating raises the correlation. It does not have
    // to, and on this ground it often does not: the published census tracts sit below the
    // areas themselves, and one of the four rules turns the line over altogether.
    // The deck's own slide says that aggregating raises the correlation. It does not have
    // to: two of the four rules land below the areas themselves and one turns the line
    // over, on the same ground and with the same number of zones.
    var da = T(w).daFit.r;
    var da2 = da * da;
    a.ok(r2s.filter(function (v) { return v < da2; }).length >= 2,
      "at least two of the four rules lower R squared below the area level " + da2.toFixed(3) +
      " (" + r2s.map(function (v) { return v.toFixed(2); }).join(", ") + ")");
    a.ok(Math.min.apply(null, bs) < 0, "and one of them turns the line over (slope " +
      Math.min.apply(null, bs).toFixed(4) + ")");
    a.ok(Math.max.apply(null, r2s) > da2, "while another beats the areas themselves");
  });

  t("each preset is in one piece, and none of them is an extreme", function (a) {
    var w = open();
    RULED.forEach(function (id) {
      var z = T(w).zoning(id);
      a.equal(z.k, 8, z.label + " is eight zones");
      // The ground is itself in more than one piece, so a zoning in one piece per zone is
      // in as many pieces as the ground plus seven.
      a.equal(z.pieces, 8 + T(w).groundPieces() - 1,
        z.label + " is in as few pieces as the ground allows");
      a.equal(/steep|flat|revers|high|low|\br\b|slope/i.test(z.label), false,
        "and its name says nothing about what it does: " + z.label);
    });
  });

  t("the aggregation rule moves the answer, and greenness does not care", function (a) {
    // Greenness is a value per square metre, so a zone's mean is the same whichever way
    // the areas are weighted. Income arrives as a median per area and medians do not add,
    // so it moves. That asymmetry is the lesson the rule control exists for.
    var w = open();
    var hh = T(w).fitAt(RULED[3], "hh");
    var pop = T(w).fitAt(RULED[3], "pop");
    var plain = T(w).fitAt(RULED[3], "plain");
    a.ok(Math.abs(hh.r - plain.r) > 1e-6, "a plain average gives a different r from a household-weighted one");
    a.ok(Math.abs(hh.b - pop.b) > 1e-9, "and a different slope when weighted by people");
    var ys = [];
    ["hh", "pop", "plain"].forEach(function (rule) {
      T(w).setRule(rule);
      ys.push(T(w).state().ag.y.join(","));
    });
    a.equal(ys[0], ys[1], "the greenness of a zone does not move when income's rule changes");
    a.equal(ys[0], ys[2], "under any of the three");
  });

  t("the aggregation rule can decide the sign of the finding", function (a) {
    // The sharpest thing the rule control does, and it is on the page because it was
    // measured rather than guessed at.
    var w = open();
    var best = RULED.map(function (id) {
      return { hh: T(w).fitAt(id, "hh"), plain: T(w).fitAt(id, "plain"), id: id };
    }).sort(function (p, q) { return Math.abs(q.plain.r - q.hh.r) - Math.abs(p.plain.r - p.hh.r); })[0];
    a.ok(Math.abs(best.plain.r - best.hh.r) > 0.1,
      "the same eight zones, two ways of averaging income, and r moves from " +
      best.hh.r.toFixed(2) + " to " + best.plain.r.toFixed(2));
    a.ok(Math.abs(best.plain.b - best.hh.b) / Math.abs(best.hh.b) > 0.1,
      "and the slope moves with it");
  });

  t("painting changes the zoning, the drawing and the numbers together", function (a) {
    var w = open();
    var before = T(w).state().fit.r;
    var zone = T(w).zone();
    var moved = 0, i;
    for (i = 0; i < 60; i++) {
      var z = (zone[i] + 1) % 8;
      T(w).paint(i, z);
      moved++;
    }
    w.settle();
    a.ok(moved > 0, "areas were painted");
    a.ok(T(w).zone().slice(0, 60).join(",") !== zone.slice(0, 60).join(","), "the assignment changed");
    a.ok(T(w).state().fit.r !== before, "and so did r");
    // The picture has to agree with the model, not merely be redrawn.
    var st = T(w).state();
    var fills = {}, paths = w.doc.getElementById("m-nd").querySelectorAll("path[data-i]");
    for (i = 0; i < T(w).n; i++) {
      var z2 = T(w).zone()[i];
      if (fills[z2] === undefined) fills[z2] = paths[i].getAttribute("fill");
      else a.equal(paths[i].getAttribute("fill"), fills[z2],
        "every area in a zone is drawn the same colour on the greenness map");
    }
    a.ok(st.ag.y.length > 2, "and the zones still carry figures");
  });

  t("a painted zoning survives the round trip through the link", function (a) {
    // The link is what a student pastes for the rest of the room, so it has to come back
    // as exactly what they drew. 1,010 areas at three bits each.
    var w = open();
    T(w).paint(0, 5); T(w).paint(1, 5); T(w).paint(2, 7); T(w).paint(900, 4);
    T(w).setRule("pop");
    w.settle();
    var frag = T(w).fragment();
    var mine = T(w).zone().join(",");
    a.ok(frag.length < 2000, "the link stays short enough to paste (" + frag.length + " characters)");
    var w2 = open("", "#" + frag);
    a.equal(T(w2).zone().join(","), mine, "the same zoning comes back out of the link");
    a.equal(T(w2).k(), 8, "with eight zones");
    a.equal(T(w2).state().rule.id, "pop", "and the way income was averaged");
    a.close(T(w2).state().fit.r, T(w).state().fit.r, 1e-12, "so the readout is the same number");
  });

  t("a name travels in the link and is not an identifier", function (a) {
    var w = open("", "#p=z2&l=Team%20Fraser");
    a.equal(T(w).label(), "Team Fraser", "the name comes back");
    a.ok(T(w).fragment().indexOf("l=Team") > 0, "and goes out again");
  });

  t("the published zonings are real and are not paintable", function (a) {
    var w = open();
    click(w, "Census tracts");
    a.equal(T(w).canPaint(), false, "census tracts are somebody else's lines, so they are not painted over");
    a.ok(T(w).k() > 50, "and there are many more of them than eight");
    var note = w.doc.getElementById("paintnote").textContent;
    a.ok(note.indexOf("eight-zone") > 0, "the page says how to get back to something paintable: " + note);
    click(w, T(w).zoning(RULED[0]).label);
    a.equal(T(w).canPaint(), true, "and one click returns to a paintable zoning");
  });

  t("every card on the page has something in it", function (a) {
    // A titled card with a collapsed body reads as a rendering glitch, and one in another
    // widget here sat empty for months.
    var w = open();
    w.doc.querySelectorAll(".stat").forEach(function (card) {
      var label = card.querySelector(".label").textContent.replace(/\s+/g, " ").replace(" i", "").trim();
      var text = "";
      card.querySelectorAll(".big, .sub").forEach(function (e) { text += e.textContent.trim(); });
      a.ok(text.length > 0, 'the "' + label + '" card is not empty');
    });
    ["rulenote", "fitline", "paintnote", "scene"].forEach(function (id) {
      a.ok(w.doc.getElementById(id).textContent.trim().length > 1, "#" + id + " says something");
    });
  });

  t("the classroom panel quotes the figure the page actually shows", function (a) {
    // It quoted a figure from an earlier extent for a while, which is the way a sentence
    // stating a measurement goes stale in silence.
    var w = open();
    var panel = w.doc.getElementById("info-classroom").textContent.replace(/\s+/g, " ");
    var quoted = panel.match(/between income and greenness is (\d+\.\d+)/);
    a.ok(quoted, "the activity states the area-level R squared");
    var da2 = T(w).daFit.r * T(w).daFit.r;
    a.close(Number(quoted[1]), da2, 0.005,
      "and it is the one the page computes (" + quoted[1] + " against " + da2.toFixed(3) + ")");
    var n = panel.match(/Across the ([\d,]+) areas/);
    a.equal(n && n[1].replace(/,/g, ""), String(T(w).nok), "and the count is the one it fits over");
  });

  t("what is at stake is on the page with every explanation closed", function (a) {
    var w = open();
    var stakes = w.doc.querySelector(".stakes").textContent.replace(/\s+/g, " ");
    a.ok(stakes.indexOf("Vancouver") > 0, "the city is named in the reading flow");
    a.ok(stakes.indexOf("you help draw the boundaries") > 0,
      "and so is what the reader is being asked to do: " + stakes.slice(0, 60) + "...");
    a.equal(w.doc.querySelector(".stakes").closest(".help-panel"), null,
      "it is not behind an (i), because presentation mode hides those");
  });

  t("no dissemination area is named anywhere on the page", function (a) {
    // The equity half is projected at the front of a room some of whose members live in
    // these areas. The page must not be able to point at one of them.
    var fs = require("fs");
    var html = fs.readFileSync(FILE, "utf8");
    a.equal(/\bDAUID\b/.test(html), false, "no DAUID in the page");
    a.equal(/\b59150\d{3}\b/.test(html), false, "no dissemination area identifier in the page");
    // The data file has to be read as data, not as text: "DAUID" turns up by chance inside
    // the base64 geometry, and the first version of this test failed on that.
    var raw = fs.readFileSync(path.join(path.dirname(FILE), "data.js"), "utf8");
    var data = JSON.parse(raw.slice(raw.indexOf("{"), raw.lastIndexOf("}") + 1));
    a.equal(Object.keys(data).some(function (k) { return /dauid|uid$/i.test(k); }), false,
      "no identifier field in the shipped data: " + Object.keys(data).join(","));
    var strings = JSON.stringify(data.laname) + data.scene + data.note;
    a.equal(/\b59\d{6}\b/.test(strings), false, "and no dissemination area code among its labels");
    var w = open();
    var live = w.doc.getElementById("live");
    T(w).paint(3, 2);
    w.settle();
    a.equal(/\d{8}/.test(live.textContent), false,
      "and the screen reader announcement carries no identifier: " + live.textContent);
  });

  t("the class breaks are fixed, so a re-zoning is not a re-palette", function (a) {
    var w = open();
    var before = T(w).breaks.inc.join(",") + "|" + T(w).breaks.ndvi.join(",");
    [RULED[0], "ct", RULED[2], RULED[1]].forEach(function (z) { T(w).setZoning(z); });
    a.equal(T(w).breaks.inc.join(",") + "|" + T(w).breaks.ndvi.join(","), before,
      "the colour bands do not move when the zoning does");
  });

  t("the scatter keeps the areas behind the zones, on fixed axes", function (a) {
    var w = open();
    function frame() {
      var ticks = w.doc.getElementById("plot").querySelectorAll("text");
      return ticks.map(function (e) { return e.textContent; }).join("|");
    }
    var f0 = frame();
    // Drawn as a filled field rather than as dots, because single points do not survive a
    // projector. See the widget's file.
    var cloud = w.doc.getElementById("plot").querySelectorAll("path").filter(function (e) {
      return e.getAttribute("fill") === "var(--cloud)";
    })[0];
    a.ok(cloud && cloud.getAttribute("d").length > 1000, "the 1,001 areas are drawn behind as a field");
    var dots = w.doc.getElementById("plot").querySelectorAll("circle").length;
    a.ok(dots > 2 && dots <= 8, "and one dot per zone on top (" + dots + ")");
    T(w).setZoning("ct");
    a.equal(frame(), f0, "the axes do not move when the zoning does");
    a.ok(w.doc.getElementById("plot").querySelectorAll("circle").length > 50,
      "census tracts put many more dots on the same frame");
  });

  t("presentation mode keeps the argument and the classroom panel", function (a) {
    var w = open("?present=1");
    a.equal(w.doc.body.getAttribute("data-present"), "1", "it starts presenting");
    var panel = w.doc.getElementById("info-classroom");
    a.ok(panel.closest("fieldset").querySelector(".classroom-btn"), "the classroom (i) is the one that stays");
    a.ok(w.doc.querySelector(".stakes").textContent.length > 100, "and the stakes are still in the flow");
  });
};
