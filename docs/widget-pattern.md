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

### When the work stops fitting in a frame

Four things in the order they are worth doing, learned taking one widget from 41,800 cells
to 809,820 without losing sixty frames a second.

**Change the algorithm before anything else.** A binary heap became Dial's buckets and a
solve more than halved, in about thirty lines and with the answers bit-identical. Measure the
alternative rather than assuming the library or the GPU is the answer; `libraries.md` records
why neither was, here.

**Separate the cheap redraw from the expensive computation.** Repainting a raster is about a
millisecond and solving over it was thirty-five, so the land can follow the brush every frame
while the result arrives a few times a second. What settles at the end is never stale,
because the stroke ends with a flush.

**Cache derived state against a version counter.** Bump the counter wherever the model
actually changes and record it on the derived thing. Keeping a proposal changed nothing about
the model and was paying for two solves anyway: 180 ms became 19.

**Then a worker, and only then.** The trigger is measurable, not aesthetic: a solve reached
two frames and no scheduling on one thread hides that. Build the worker body as a function
that closes over nothing and stringify it into a Blob at load, so the widget stays one file
with no second request. Two things to expect. Nothing is synchronous any more, so find the
place that needs a settled answer *before* you move the solver — here it was the moment a
proposal is kept, which must file the current numbers against the current route and not the
previous one. And the first frame now paints before any result exists, so whatever reads the
result has to tolerate its absence; showing the map with the number blank beats showing
nothing.

**Then stop sending it the whole world.** Copying an 809,820-cell array into every message
was the last thing on the main thread big enough to cost a frame, and it cost four in
ninety-one. Send the cells that changed, and fall back to the whole array when the list grows
long or the data is reset.

**Anything overlaid on an interactive canvas must not be inside the element you measure
against.** A drawing banner placed inside the map box made the box taller than the canvas,
so a press near the top mapped to a negative row and silently did nothing. Put the chrome
beside the canvas, not around it, and the pointer arithmetic stays one subtraction.

## What the fourth widget added

A street network, a warped photograph and two kinds of animated transition. Six things
that will be true of the next one too.

**A typed array is not a free optimisation when a threshold is involved.** `Float32Array`
stores a grade of exactly 50 per mille as 0.050000001, so `> 0.05` was true and 93 streets
were quietly excluded from the one traveller defined by that threshold. Every recorded
travel time stayed correct, so no worked example could have caught it. Keep the integer the
data actually holds and compare integers; use `Float64Array` anywhere an independent check
has to agree with you to more than six figures.

**`requestAnimationFrame` is not a promise.** A page in a background tab gets no frames at
all. Anything a reader reads — a readout, a control's pressed state, the URL — must be
written before the first frame, not in the last one, or the widget can sit half way through
a transition describing neither end. Keep a timer as a backstop that snaps the drawing into
place if the frames never come.

**`floor(min)` is not a stable anchor.** Quantised coordinates need an origin, and taking
it from the minimum of a projected extent means the last bit of a projection decides it:
two runs over identical input put the southernmost point either side of a whole metre, and
half the deltas in the file changed. Anchor to a round number below the minimum. Then build
the data twice and diff it — a data file that cannot be reproduced cannot be checked.

**To move between two models, find the state they agree on and go through it.** There is no
half-way point between "on foot" and "by car": the costs, the scale and the frame all
change at once, and an average of two answers is an answer to nothing. But an undeformed
map is the same map for every traveller, so a change can collapse to it, swap the model
where both sides agree, and rebuild the other way. The join is exact rather than blended.
The first half has to be played back from a snapshot, because by then the model is gone.

**Two questions that look like one are usually two.** How far the map was deformed and how
much of the hidden ground was allowed to show were the same variable, which was fine until
a transition passed through the undeformed state and unclipped everything for a frame.
Separating them was the whole fix. When an animation does something ugly only in the middle,
suspect a variable that is answering two questions.

**A comment that states an intent is a claim, and it can be false.** One here read *"does
this traveller have any way to leave the start?"* above code that marked a junction usable
if a usable arc *touched* it, in either direction. Being able to arrive somewhere is not
being able to leave it, and the gap between the comment and the code shipped a blank map.
Read the comment as an assertion and check the code against it, the same way a citation
gets checked against its claim.

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
8. Design the **For the classroom** activity with whoever will teach it, by interrogation
   rather than by drafting — `principles.md` section 16 — and write it, and the candidates
   dropped, into the widget's file.
9. Run all five passes in `docs/review.md`.

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
