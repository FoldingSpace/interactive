# Building a widget

One widget is one folder under `web/`, holding one self-contained HTML file, showing one
idea. The folder name becomes the URL, so keep it short and name it for the subject:
students read it off a slide and it goes into QR codes.

Start by copying `template/` to `web/<name>/`. The template is a working page, not a
sketch: it opens showing something, it has both layouts, presentation mode, the (i)
explanation machinery, URL state, a live region for screen readers, and the credit line.
Copying it means a new widget begins with several of the non-negotiables already met.

`template/` sits outside `web/` so it is not published. Preview it with the `repo`
configuration in `.claude/launch.json`, which serves the repository root on port 8792.

## The template is copied, not imported

The template is a starting point you edit, not a library you depend on. That is a
deliberate choice with a cost on both sides.

Copying means a widget shipped last term cannot break when the template changes, and each
widget stays a single file that works from an `iframe`, from a `file://` URL, and with no
second request. It also means a fix made in one place does not reach the others, so when
you fix something in a widget, ask whether the template has the same bug.

There is no `web/shared/`. There should not be one until a second widget needs the same
code, and probably not until a third. Duplication between two files is cheap and visible;
a shared file is a thing that can break a widget nobody is currently looking at. If a
shared file is ever added, every widget that uses it has to re-pass the verified numbers
in its own file in `docs/widgets/` before the change is pushed.

The three pieces most likely to earn sharing eventually: the colour tokens with their
dark-mode block, the `[data-info]` panel handler, and the presentation-mode toggle.

## The shape of the code

Read state from the URL, render, write the URL back. One `render()` function, called after
every change, that draws the whole view from the current state. Nothing else touches the
DOM. This is slower than patching individual elements and it is worth it: two code paths
writing the same pixels is how a readout ends up one edit behind, which happened here
once already and took a while to see.

Keep the URL clean by omitting parameters that hold their default value, so the link a
student gets is short and the link from a slide carries only what it changed.

Announce changes in the live region. A student using a screen reader gets nothing from a
redrawn grid.

**If `render()` is batched into an animation frame, state can be one frame behind, and
something will read it.** Batching is right — a brush stroke should never wait on a solve —
but it means anything reading the result synchronously gets the previous frame's answer. In
`least-cost` that filed the current cost table against the previous route, so two kept
proposals showed identical statistics under visibly different numbers. Keep a `flush()` that
does the work now, and call it wherever a settled answer is read rather than drawn. The same
argument applies to a control's own `aria-valuenow`: redraw the control synchronously and let
the expensive part wait.

**Debounce the URL write.** `history.replaceState` on every frame of a drag is both wasteful
and, in Safari, throttled — about a hundred calls in thirty seconds, after which it throws.
A few seconds of painting reaches that. Write the URL a third of a second after things
settle.

**Anything overlaid on an interactive canvas must not be inside the element you measure
against.** A drawing banner placed inside the map box made the box taller than the canvas,
so a press near the top mapped to a negative row and silently did nothing. Put the chrome
beside the canvas, not around it, and the pointer arithmetic stays one subtraction.

## What changes with the sort of widget

The first widget was pure computation with no data and no dependencies. Most of what it
established still holds, but not all of it, and the parts that will not hold are worth
naming before they are discovered mid-build.

**Computation only.** Statistics on made-up data, sampling, distance and area on a grid.
No files, no network, no libraries so far. The thing to watch is speed: keep the main
thread free, and prefer an exact answer to a simulated one wherever a closed form exists
(`principles.md` section 7).

**Maps and geometry.** A basemap, vector tiles, a real projection. This is where "no
dependency" most likely ends, and where two current claims need revisiting: the README
says each widget makes no network calls after load, which is false the moment tiles are
fetched, and a widget that depends on a tile server can fail in a lecture room with bad
wifi. Decide deliberately between bundling a small extract and fetching tiles, write the
decision in the widget's own file, and put every source in `docs/attributions.md` at the
moment it is added.

**Data that ships with the widget.** A file in the widget folder. Keep it small enough to
load over classroom wifi and over a student's phone data, record its licence, and prefer
an extract you can describe exactly over a download whose provenance is vague.

**Time and animation.** Respect `prefers-reduced-motion`, give the reader a control rather
than an animation that runs on its own, and never let motion carry a cue that is not also
carried by something still. A projector recording destroys smooth movement.

**Drawing and direct input.** Pointer events with `setPointerCapture`, and interpolation
between pointer positions so a fast drag does not leave gaps. The touch case is not the
narrow-window case: ask about the pointer, not the viewport.

## Layout: what splits on what

Width decides the column count, because whether two panels fit side by side is a question
about width. Pointer type decides control shape and target size, because whether a slider
is usable is a question about the pointer. A narrow desktop window is not a phone.

Targets are sized for touch everywhere rather than only under `pointer: coarse`, which is
simpler and costs a desktop user nothing.

Presentation mode is the third context and it cannot be detected, so it is a choice:
`?present=1`, a button, and the `p` key. One custom property, `--ui`, multiplies every
size through `calc()`.

## Adding a widget

1. Copy `template/` to `web/<name>/` and start replacing.
2. Open `docs/widgets/<name>.md` at the same time and write it as you go. Written
   afterwards it becomes a summary; written alongside it becomes the record of why.
3. Make the opening state show something, and check that every control leads somewhere
   from it.
4. Give every control that embodies a choice an (i) explanation. Any citation in it goes
   to an adversarial check before it ships, and is removed rather than hedged if the check
   cannot confirm it.
5. Record verified numbers in the widget's file, checked by a route that shares no code
   with the widget.
6. Add the widget to `web/index.html` and to the list in `README.md`.
7. Log anything borrowed in `docs/attributions.md`, and anything tried, used, or ruled out
   in `docs/libraries.md`.
8. Run all five passes in `docs/review.md`.

## What goes where

Four documents, and they answer different questions. `principles.md` is why we build these
and what a widget must be. This file is how one is put together in code. `visual-forms.md`
is what to draw once you know what you are showing. `review.md` is how any of it gets
checked. When a lesson turns up, the question is which of those four it belongs to; a lesson
recorded in two places goes stale in one of them.

`libraries.md`, `attributions.md` and `deployment.md` are registers rather than guidance:
what we tried, what we borrowed, how it ships.

## What the first build taught that carries over

Measure rather than eyeball, for layout, for speed, and for what a control demonstrates.
Almost every real defect found so far was invisible until something was measured, and one
control turned out to teach the opposite of its design intent.

Check a statistic by a route that shares no code with the widget, in a different language
if possible. Reproducing a known case is necessary and never sufficient: ask what bug
would pass the test you just ran.

Check anything touching the random number generator by running the widget's own source,
not a reimplementation of it. A port that diverges silently costs an afternoon, twice.

CSS specificity and source order caused three separate bugs, all of them looking like
JavaScript failures. An author rule beats `[hidden]`; a rule later in the file beats an
identical-specificity rule inside a media query.

Documentation goes stale exactly like code. When a feature changes, grep the docs for the
numbers and for the words "every", "always" and "all".
