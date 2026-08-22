# Tests

```bash
node tools/test/run.js          # everything
node tools/test/run.js least    # suites whose filename contains "least"
```

Exits non-zero on the first failing assertion. `.github/workflows/pages.yml` runs it and
nothing is published unless it passes.

## What these test, and what they cannot

Each suite loads a widget's **shipped HTML**, parses the markup, and runs the widget's own
script inside a small DOM defined in `dom.js`. Two things get recorded as the widget runs:
every attribute set on an SVG element, and the pixels handed to `putImageData`. A test can
therefore read the map back out of the canvas and the routes back out of the SVG, and
re-cost a drawn route from the values shown on the controls — checking what the page
*draws*, not what it computes. That distinction is the point. A widget whose model is right
and whose drawing is wrong looks entirely fine until someone measures the picture.

What this cannot check: layout, CSS, real pointer behaviour, contrast against real
rendering, and anything about how it feels. Those stay in the manual passes in
`docs/review.md`, and no amount of this replaces opening it on a phone.

## Why no browser and no framework

A headless browser would test more, at the cost of a large dependency and a browser
download in CI. The assertions that matter here are geometry and arithmetic, and those need
the widget's own code against its own data rather than a rendering engine. The stub is
about 250 lines and has caught real defects: a solver that drew fewer alternatives at a
wider tolerance than at a narrower one, and every stale number after a change of
resolution.

The runner is 40 lines for the same reason. `a.ok`, `a.equal`, `a.close`. If a suite ever
needs more than that, write it in the suite.

## What the stub does and does not do

It parses the markup, runs the scripts (following a `<script src>` sibling, which one widget
uses for its data), and gives the page a DOM with events, a canvas that records what was
painted, `getComputedStyle` backed by the real custom properties, animation frames and timers
you drive by hand, and a Worker that runs the widget's own worker source and replies through
the timer queue. `innerHTML` is parsed into nodes and entities are decoded, because widgets
mark values by writing spans and a test asking whether anything is marked needs those spans
to exist.

It does not lay anything out. Every `getBoundingClientRect` is whatever the test sets, so
nothing here can tell you a control is 3 px tall or a column has collapsed.

## Adding a suite

Name it `<widget>.test.js` and export a function taking `t(name, fn)`. `fn` receives the
assertions. `load.js` gives you `{ doc, win, vars, flushFrames, flushTimers, location }`;
animation frames only run when you ask, so a test can look at the state between a click and
its redraw.

Give the canvas and any slider a rectangle before driving pointer events, or their maths
has nothing to work from:

```js
w.doc.getElementById("cv")._rect = { left: 0, top: 0, width: W * 2, height: H * 2 };
```
