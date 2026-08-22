"use strict";
// Load a widget's shipped HTML into the stub DOM and run its script, so a test drives the
// same file the browser gets. The markup is parsed rather than hand-built: a test that
// builds its own DOM stops noticing when the real markup changes.

var fs = require("fs");
var path = require("path");
var vm = require("vm");
var dom = require("./dom.js");

var VOID = { br: 1, hr: 1, img: 1, input: 1, meta: 1, link: 1, source: 1, area: 1, col: 1 };

function parseHTML(html, doc) {
  var body = html.slice(html.indexOf("<body>") + 6, html.lastIndexOf("</body>") + 7);
  var stack = [doc.body], i = 0;
  var re = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][-a-zA-Z0-9]*)((?:\s+[-a-zA-Z0-9_:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*(\/?)>/g;
  var m;
  while ((m = re.exec(body)) !== null) {
    var text = body.slice(i, m.index);
    i = re.lastIndex;
    if (text.trim() && stack.length) {
      var t = doc.createTextNode(text.replace(/\s+/g, " "));
      stack[stack.length - 1].appendChild(t);
    }
    if (m[0].indexOf("<!--") === 0) continue;
    var closing = m[1], tag = m[2].toLowerCase(), attrs = m[3] || "", selfClose = m[4];
    if (tag === "script" || tag === "style") {
      var end = body.indexOf("</" + tag + ">", i);
      i = end < 0 ? body.length : end + tag.length + 3;
      re.lastIndex = i;
      continue;
    }
    if (closing) {
      for (var s = stack.length - 1; s > 0; s--) {
        if (stack[s].tagName === tag.toUpperCase()) { stack.length = s; break; }
      }
      continue;
    }
    var el = doc.createElement(tag);
    var ar = /([-a-zA-Z0-9_:]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g, a;
    while ((a = ar.exec(attrs)) !== null) {
      var val = a[2] !== undefined ? a[2] : a[3] !== undefined ? a[3] : a[4] !== undefined ? a[4] : "";
      el.setAttribute(a[1], val);
    }
    stack[stack.length - 1].appendChild(el);
    if (!VOID[tag] && !selfClose) stack.push(el);
  }
  return doc;
}

function cssVars(html) {
  var out = {};
  var re = /(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);/g, m;
  var head = html.slice(0, html.indexOf("</style>"));
  var rootBlock = head.slice(head.indexOf(":root {"), head.indexOf("@media"));
  while ((m = re.exec(rootBlock)) !== null) out[m[1]] = m[2].trim();
  return out;
}

function widgetScript(html) {
  // The last script block is the widget; earlier ones hold inlined data.
  var parts = html.split("<script>");
  return parts.slice(1).map(function (p) { return p.split("</script>")[0]; }).join("\n");
}

function load(file, opts) {
  opts = opts || {};
  var html = fs.readFileSync(file, "utf8");
  var doc = dom.makeDocument();
  parseHTML(html, doc);
  var vars = cssVars(html);

  var frames = [];
  var timers = [];
  var loc = { search: opts.search || "", pathname: "/least-cost/", href: "http://test/least-cost/" };
  Object.defineProperty(loc, "toString", { value: function () { return this.href; } });

  var win = {
    document: doc,
    location: loc,
    history: { replaceState: function (a, b, url) { loc.href = "http://test" + url; loc.search = url.indexOf("?") >= 0 ? url.slice(url.indexOf("?")) : ""; } },
    getComputedStyle: function () {
      return { getPropertyValue: function (k) { return vars[k] || ""; }, borderStyle: "", content: "" };
    },
    requestAnimationFrame: function (fn) { frames.push(fn); return frames.length; },
    matchMedia: function () { return { matches: false, addEventListener: function () {}, addListener: function () {} }; },
    setTimeout: function (fn, ms) { timers.push(fn); return timers.length; },
    clearTimeout: function () {},
    URLSearchParams: URLSearchParams,
    // A worker that runs the widget's real solver source, but delivers its replies through
    // the same queue as setTimeout. Tests therefore have to flush to see a route, which is
    // what a browser makes them wait a tick for too — the async ordering gets exercised
    // rather than papered over.
    Blob: function (parts) { this.source = parts.join(""); },
    URL: { createObjectURL: function (b) { return b; }, revokeObjectURL: function () {} },
    Worker: function (blob) {
      var outer = this;
      var scope = { onmessage: null, postMessage: function (d) { timers.push(function () { if (outer.onmessage) outer.onmessage({ data: d }); }); } };
      vm.runInContext("(function(self){" + blob.source + "})", win)(scope);
      this.postMessage = function (d) { scope.onmessage({ data: d }); };
      this.terminate = function () {};
    },
    PointerEvent: function (t, p) { return dom.makeEvent(t, p); },
    KeyboardEvent: function (t, p) { return dom.makeEvent(t, p); },
    Event: function (t, p) { return dom.makeEvent(t, p); },
    console: console,
    Math: Math, JSON: JSON, Object: Object, Array: Array, Number: Number, String: String,
    Uint8Array: Uint8Array, Uint8ClampedArray: Uint8ClampedArray,
    Int32Array: Int32Array, Float64Array: Float64Array,
    decodeURIComponent: decodeURIComponent, encodeURIComponent: encodeURIComponent,
    parseInt: parseInt, parseFloat: parseFloat, isNaN: isNaN, Infinity: Infinity
  };
  win.window = win;
  doc.defaultView = win;

  vm.createContext(win);
  vm.runInContext(widgetScript(html), win, { filename: file });

  // Animation frames only run when a test asks for them, so a test can look at the state
  // between a click and its redraw if it wants to.
  function flushFrames(n) {
    for (var i = 0; i < (n || 8); i++) {
      var due = frames; frames = [];
      if (!due.length) break;
      due.forEach(function (fn) { fn(0); });
    }
  }
  function flushTimers() { var due = timers; timers = []; due.forEach(function (fn) { fn(); }); }

  // Run frames and timers alternately until neither has anything left. Worker replies and
  // the debounced URL write both arrive as timers, and a reply schedules a repaint, so a
  // single pass of either is not enough.
  function settle(limit) {
    for (var i = 0; i < (limit || 40); i++) {
      if (!frames.length && !timers.length) return;
      flushFrames(1);
      flushTimers();
    }
  }

  return { doc: doc, win: win, vars: vars, flushFrames: flushFrames, flushTimers: flushTimers,
           settle: settle, location: loc };
}

module.exports = { load: load, parseHTML: parseHTML, cssVars: cssVars };
