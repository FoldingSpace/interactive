#!/usr/bin/env node
"use strict";
// Run every *.test.js here. Exits non-zero on the first failing assertion, so it can gate
// a deploy. No dependencies: see docs/libraries.md.
//
//   node tools/test/run.js            all suites
//   node tools/test/run.js least      only suites whose name contains "least"

var fs = require("fs");
var path = require("path");

var filter = process.argv[2] || "";
var files = fs.readdirSync(__dirname).filter(function (f) {
  return /\.test\.js$/.test(f) && f.indexOf(filter) >= 0;
});

var passed = 0, failed = 0, current = null;
var failures = [];

function assert(ok, msg) {
  if (ok) { passed++; return; }
  failed++;
  failures.push(current + " — " + msg);
}
var a = {
  ok: function (v, msg) { assert(!!v, msg); },
  equal: function (got, want, msg) {
    assert(got === want, msg + (got === want ? "" : "  (got " + JSON.stringify(got) + ", wanted " + JSON.stringify(want) + ")"));
  },
  close: function (got, want, eps, msg) {
    assert(Math.abs(got - want) <= eps, msg + (Math.abs(got - want) <= eps ? "" : "  (got " + got + ", wanted " + want + " ± " + eps + ")"));
  }
};

files.forEach(function (f) {
  process.stdout.write("\n" + f + "\n");
  var suite = require(path.join(__dirname, f));
  suite(function (name, fn) {
    current = name;
    var before = failed;
    try { fn(a); } catch (e) { failed++; failures.push(name + " — threw: " + e.message + "\n" + e.stack.split("\n").slice(0, 4).join("\n")); }
    process.stdout.write((failed === before ? "  ok   " : "  FAIL ") + name + "\n");
  });
});

process.stdout.write("\n" + passed + " passed, " + failed + " failed\n");
if (failed) {
  process.stdout.write("\n" + failures.map(function (s) { return "  " + s; }).join("\n") + "\n\n");
  process.exit(1);
}
