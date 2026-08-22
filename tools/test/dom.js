"use strict";
// A small DOM, enough to run a widget from this repository inside Node.
//
// Why not a headless browser: the assertions we care about are geometry and arithmetic —
// is this drawn line a real path, does it cost what the page says — and those need the
// widget's own code running against its own data, not a rendering engine. A stub keeps the
// suite dependency-free, which is the same rule the widgets follow. What it deliberately
// cannot check is layout, CSS and real pointer behaviour; those stay in the manual passes
// in docs/review.md.
//
// The stub records two things the tests read back: every attribute set on an SVG element,
// and the pixels handed to putImageData. Between them a test can check what was drawn
// rather than what was computed.

function makeEvent(type, props) {
  var e = { type: type, bubbles: true, defaultPrevented: false };
  for (var k in props) if (Object.prototype.hasOwnProperty.call(props, k)) e[k] = props[k];
  e.preventDefault = function () { e.defaultPrevented = true; };
  e.stopPropagation = function () { e._stopped = true; };
  return e;
}

function matches(node, sel) {
  // The attribute part is split off first. Checking for a leading "." before that made
  // ".swatch[data-k=\"1\"]" look for a class literally called swatch[data-k="1"].
  var br = sel.indexOf("[");
  if (br > 0) return matches(node, sel.slice(0, br)) && matches(node, sel.slice(br));
  if (sel.charAt(0) === "#") return node.id === sel.slice(1);
  if (sel.charAt(0) === ".") return (" " + (node.className || "") + " ").indexOf(" " + sel.slice(1) + " ") >= 0;
  var m = sel.match(/^([a-zA-Z]*)\[([^\]=]+)(?:=["']?([^"'\]]*)["']?)?\]$/);
  if (m) {
    if (m[1] && node.tagName !== m[1].toUpperCase()) return false;
    var v = node.getAttribute(m[2]);
    if (v === null) return false;
    return m[3] === undefined || String(v) === m[3];
  }
  return node.tagName === sel.toUpperCase();
}

function Node(tag, ns) {
  this.tagName = String(tag).toUpperCase();
  this.ns = ns || null;
  this.children = [];
  this.parentNode = null;
  this.attrs = {};
  this.dataset = {};
  this.style = { setProperty: function () {}, cssText: "" };
  this.className = "";
  this.id = "";
  this._text = "";
  this.listeners = {};
  this.hidden = false;
}
Node.prototype.appendChild = function (c) {
  if (c && c._fragment) { c.children.forEach(function (x) { this.appendChild(x); }, this); return c; }
  c.parentNode = this; this.children.push(c); return c;
};
Node.prototype.setAttribute = function (k, v) {
  this.attrs[k] = String(v);
  if (k === "id") this.id = String(v);
  if (k === "class") this.className = String(v);
  if (k === "hidden") this.hidden = true;
  if (k.indexOf("data-") === 0) this.dataset[k.slice(5).replace(/-(\w)/g, function (_, c) { return c.toUpperCase(); })] = String(v);
};
Node.prototype.getAttribute = function (k) {
  if (k === "class") return this.className || null;
  if (k === "id") return this.id || null;
  if (k.indexOf("data-") === 0) {
    var d = this.dataset[k.slice(5).replace(/-(\w)/g, function (_, c) { return c.toUpperCase(); })];
    return d === undefined ? null : String(d);
  }
  return Object.prototype.hasOwnProperty.call(this.attrs, k) ? this.attrs[k] : null;
};
Node.prototype.removeAttribute = function (k) { delete this.attrs[k]; };
Object.defineProperty(Node.prototype, "textContent", {
  get: function () {
    if (this.children.length === 0) return this._text;
    return this.children.map(function (c) { return c.textContent; }).join("");
  },
  set: function (v) { this.children = []; this._text = String(v); }
});
Object.defineProperty(Node.prototype, "innerHTML", {
  get: function () { return this._text; },
  set: function (v) { this.children = []; this._text = String(v).replace(/&times;/g, "x").replace(/<[^>]*>/g, ""); }
});
Object.defineProperty(Node.prototype, "firstChild", {
  get: function () { return this.children[0] || null; }
});
Node.prototype.addEventListener = function (t, fn) {
  (this.listeners[t] = this.listeners[t] || []).push(fn);
};
Node.prototype.removeEventListener = function (t, fn) {
  var a = this.listeners[t] || [];
  var i = a.indexOf(fn); if (i >= 0) a.splice(i, 1);
};
Node.prototype.dispatchEvent = function (e) {
  e.target = e.target || this;
  var n = this;
  while (n) {
    (n.listeners[e.type] || []).slice().forEach(function (fn) { if (!e._stopped) fn.call(n, e); });
    if (!e.bubbles) break;
    n = n.parentNode;
  }
  return !e.defaultPrevented;
};
Node.prototype.click = function () {
  this.dispatchEvent(makeEvent("click", { target: this, detail: 1 }));
};
Node.prototype.focus = function () { this.ownerDoc && (this.ownerDoc.activeElement = this); };
Node.prototype.select = function () {};
Node.prototype.setPointerCapture = function () {};
Node.prototype.releasePointerCapture = function () {};
Node.prototype.closest = function (sel) {
  var n = this;
  while (n) { if (n.tagName && matches(n, sel)) return n; n = n.parentNode; }
  return null;
};
Node.prototype.getBoundingClientRect = function () {
  return this._rect || { left: 0, top: 0, width: 100, height: 20, right: 100, bottom: 20 };
};
Node.prototype._walk = function (out) {
  this.children.forEach(function (c) { out.push(c); c._walk(out); });
  return out;
};
Node.prototype.querySelectorAll = function (sel) {
  var parts = sel.split(",").map(function (s) { return s.trim(); });
  return this._walk([]).filter(function (n) {
    return parts.some(function (p) {
      var seg = p.split(/\s+/);
      var last = seg[seg.length - 1];
      if (!matches(n, last)) return false;
      var anc = n.parentNode, i = seg.length - 2;
      while (i >= 0) {
        var found = false;
        while (anc) { if (matches(anc, seg[i])) { found = true; anc = anc.parentNode; break; } anc = anc.parentNode; }
        if (!found) return false;
        i--;
      }
      return true;
    });
  });
};
Node.prototype.querySelector = function (sel) { return this.querySelectorAll(sel)[0] || null; };

function build(doc, spec) {
  var el = doc.createElement(spec.tag || "div");
  if (spec.id) el.setAttribute("id", spec.id);
  if (spec.cls) el.className = spec.cls;
  if (spec.attrs) for (var k in spec.attrs) el.setAttribute(k, spec.attrs[k]);
  if (spec.text) el.textContent = spec.text;
  (spec.kids || []).forEach(function (s) { el.appendChild(build(doc, s)); });
  return el;
}

function makeDocument(vars) {
  var doc = new Node("document");
  doc.documentElement = new Node("html");
  doc.body = new Node("body");
  doc.documentElement.appendChild(doc.body);
  doc.appendChild(doc.documentElement);
  doc.activeElement = doc.body;
  doc.createElement = function (t) {
    var n = new Node(t); n.ownerDoc = doc;
    if (t === "canvas") {
      n.getContext = function () {
        return {
          createImageData: function (w, h) { return { width: w, height: h, data: new Uint8ClampedArray(w * h * 4) }; },
          putImageData: function (img) { n.painted = img; },
          getImageData: function () { return n.painted; }
        };
      };
    }
    return n;
  };
  doc.createElementNS = function (ns, t) { var n = new Node(t, ns); n.ownerDoc = doc; return n; };
  doc.createDocumentFragment = function () { var f = new Node("#fragment"); f._fragment = true; return f; };
  doc.createTextNode = function (t) { var n = new Node("#text"); n._text = String(t); return n; };
  doc.getElementById = function (id) { return doc.querySelectorAll("#" + id)[0] || null; };
  return doc;
}

module.exports = { Node: Node, makeDocument: makeDocument, makeEvent: makeEvent, build: build };
