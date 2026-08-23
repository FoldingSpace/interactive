# Review before shipping

Five passes. A widget is not finished until it has been through all of them. Record the
result as a section of the widget's own file in `docs/widgets/` so we can see what was
checked and when.

The passes are ordered so that the expensive one comes first. There is no point polishing
the contrast on a widget that teaches the wrong thing.

---

## 1. Pedagogical critique

This pass can send the work back for redesign. It is not a polish pass.

The critic is given the widget and the teaching context, and is asked, in this order:

**What is the one thing a student should understand after using this?** State it in a
sentence. If it takes more than a sentence, the widget is doing too much and should be
split.

**Does the interaction teach that thing, or does it only illustrate it?** A student
should learn something by moving a control that they could not learn by looking at a
static figure. If a screenshot would do the same work, the interactivity is decoration.

**What will a student do first, and what will they conclude from it?** Trace the likely
first three actions. Novices poke at the biggest control and drag it to the extremes.
What do the extremes show? If the extreme cases are degenerate or misleading, fix the
ranges.

**Do the cases a student will compare differ in only the thing being taught?** Take the
presets and defaults two at a time and name every way they differ. If two cases differ in
more than the lesson, a student cannot tell which difference produced the result, and the
widget will teach the wrong cause convincingly. This is `principles.md` section 5, and it
is the failure that is hardest to spot once you already know what the widget is for.

**Where can a student form a wrong idea?** Name the specific misconception the widget
might create or reinforce. Defaults, ranges, and colour choices all carry implications
that students read as claims.

**Is the vocabulary the students' or the software's?** Every label should be a word the
course has already taught or a word in ordinary use.

**Is there a way to be wrong that the widget does not reveal?** If students can reach a
nonsensical configuration, does the widget show them that it is nonsense, or does it
draw it as though it were fine?

**Does the control demonstrate what you think it demonstrates? Measure it.** Do not write
the explanation from the design intent. The extent toggle in the autocorrelation grid was
built to show that more observations buy statistical power; measured, it showed the
opposite, because the smaller extent is a window that happens to sit over a more clustered
part of the surface. The boundary effect beat the power effect outright. That turned out to
be the better lesson, but only because it was measured before the panel was written rather
than after. **An explanation written from intention rather than evidence will be wrong
about a third of the time, and confidently.**

**Where does the method fail, and does the widget say so?** Find the inputs that make the
result empty, undefined, zero, or unmoved. Then check what appears on screen at that
moment. Silence is a failure: a blank result reads as a statement about the data when it is
a statement about the method. This is `principles.md` section 6, and the failing cases
should be reachable from the presets in one click.

**What should the instructor say while this is on screen?** If that is not obvious, the
widget probably needs a caption or a clearer default.

The critique produces requested changes, in priority order. Changes that affect what
students learn come before changes that affect how it looks.

## 2. Correctness

Only for widgets that compute something. The question is not "does it work on the case I
tried" but **"what is the bug that would pass the test I just ran?"**

Name it out loud. In the first widget the answer was: any coercion treating a non-zero
weight as 1 would reproduce the rook and queen weightings *exactly* while computing every
distance-decay kernel as though it were uniform, and nothing about the obvious test would
have caught it. Once named, the checks follow.

**Reproduce known values.** Cases whose answers are fixed by theory or previously recorded
— the exact −1, the exact 0. Necessary, never sufficient.

**Check the invariants.** Things that must hold whatever the input: a statistic unchanged
when all weights are scaled by a constant; a mean of parts equal to the whole; a weight of
2 giving the same answer as two contributions of 1. These catch what worked examples do
not.

**Check that different inputs give different answers.** If two settings that should differ
return the same number, something is being ignored. Three distinct decay kernels returning
three distinct values is a stronger test than any one of them being right.

**Recompute independently.** A second implementation, ideally in another language and by
another route — a matrix formulation against a loop. Agreement to several decimals across
every combination, not one.

**And know which parts it can agree about.** Where a problem has ties, an independent
implementation will match every scalar and differ on which of the tied answers it picked. A
Python check of `least-cost` agrees with the widget on cost to four decimals, on length to
the metre and on the count of cells exactly, and disagrees on *which* cells — because the two
break ties differently, and so did the same widget before and after its queue changed. Read
the scalars as claims about the world and the rest as a regression test on this
implementation, and say which is which where you record them. If ties are possible at all,
that is itself worth putting on the page: which answer you are shown is a property of the
software, not of the subject.

**Compare the counts, not only the values.** A `Float32Array` threshold in
`relative-distance` excluded 93 streets at exactly five in a hundred from the one traveller
defined by that threshold. Every recorded travel time stayed correct to six decimals,
because none of the recorded routes used one of those 93. The independent check agreed on
every *number* and disagreed about how many junctions were reachable — 7,433 against 7,360
— and that is the only place it showed. Have the independent route report cardinalities as
well as quantities, and diff those too.

**Build the data twice and diff it.** A generated data file that cannot be reproduced
cannot be regression-checked, and the failure is silent: the origin of a quantised grid was
`floor(min)`, so the last bit of a projection moved it a whole metre between runs and half
the deltas in the file changed. Two runs, byte-identical, before anything is recorded
against it.

**A probe has to read the same state the drawing reads.** While an animation runs there are
two answers to "where is this drawn" — the settled one and the one on screen — and a test
helper that reads the wrong one reports the widget broken while it is fine, or fine while
it is broken. Here the markers really *were* reading the settled value and jumping while
the streets travelled, and the probe read it too, so the two agreed and the bug looked like
a test artefact. Route everything through one accessor.

**But when the thing being checked is generated data, run the real code.** A
reimplementation is right for checking a *formula*, where a second route is the whole
point. It is wrong for checking a *generator*, where any drift makes the two disagree about
the input rather than the answer. A hand-port of the widget's random number generator
silently diverged and cost a round of confusion; the later seed search ran in Node against
a copy of the widget's own source and matched exactly. Rule of thumb: verify formulas by
reimplementing, verify generated inputs by executing.

**Check that what was recorded matches what was shown.** Where a widget saves, pins, or
exports a result, the saved copy and the thing on screen are written by different code and
can disagree. Change two inputs, save after each, and confirm the two saved records differ
in the way the inputs did. This is where batched rendering shows up as a data bug rather
than a visual one.

**Verify what the page asserts against what the page ships.** The least-cost widget nearly
said its line starts at a named company's substation. That came from the licensed dataset
the widget had been designed around and does not use, and nothing it ships could have
supported it. What the wording rests on instead is Metro Vancouver's own classification of
that exact cell — a utility yard — which a reader can check from the same source the map
comes from. The rule: if a claim on screen cannot be checked from the data in the page, it
is either cited to something else or it goes.

**Derive one case by hand.** Slow, and worth it once per statistic. It is the only check
that tests your understanding rather than your code.

**Ask whether a closed form exists before reaching for a simulation.** If one does, it is
both the better implementation and the better check — exact, instant, and free of the
error a simulation carries. "Simulation is used because closed forms are hard" is true of
some cases and assumed of many more; test it rather than inherit it. Where a simulation is
genuinely needed, know the floor of what it can resolve, and never report a value below
that floor as a finding.

**Assert that the things you build have something in them.** A titled card whose body is
empty renders as a label over a collapsed div and reads as a rendering glitch. One in the
MAUP widget had been empty for months, since the commit that removed the code filling it and
left the element behind. `for each card: its body has text` would have caught it the day it
broke, and is now the first thing that file asserts.

### Some of this can be a suite, and the part that can should be

`tools/test/` runs before every deploy and is where anything repeatable belongs: recorded
values, the invariants a drawing has to satisfy, and every regression already found. It
loads a widget's shipped HTML, runs the widget's own script against a stub DOM, and reads
the routes back off the SVG and the map back off the canvas pixels — so it checks the
picture, not the model. Writing the checks down turned three of the passes below from
something to remember into something that fails.

What it cannot do is the rest of this file. Layout, contrast against real rendering, how a
drag feels, whether the argument lands. Do not let a green suite stand in for opening it on
a phone.

### Testing an interface is not the same as using one

Three rounds of confusing results here came from the harness rather than the widget, and all
three look like bugs until you check.

**A synchronous read after triggering a change reads the previous state.** If renders are
batched into an animation frame — and they should be, so a drag never waits on a solve — then
asserting straight after a click tests the frame before it. Wait a frame, or call the
widget's own flush. Two attempts at checking the cost bars here spun on a stale
`aria-valuenow` and concluded, wrongly, that the control was broken.

**Automated pointer drags are not strokes.** The browser tool's drag helper sends a press and
a release with nothing in between, so a painting stroke that works perfectly by hand drew a
single dot and looked like a dead feature. Build the pointer events yourself when you are
testing interpolation, and keep the hand test for whether it feels right.

**A stub DOM disagrees with a browser in specific ways, and each disagreement is a bug in
the stub.** Three turned up here, all found because an assertion contradicted what the page
visibly does: HTML entities left raw so a test saw `&rsquo;` where a reader sees an
apostrophe; `innerHTML` stripped to text instead of parsed, so spans a widget writes to mark
a value never became nodes and "is anything marked?" always answered no; and whitespace-only
text between two inline elements dropped, turning "= Theft of Bicycle" into
"=Theft of Bicycle". Fix the stub. A test that passes against a stub the browser does not
match is worse than no test.

**A test that fails because it describes the layout you just replaced is the suite working.**
Two did. Re-record rather than loosen.

**A scripted edit that matches nothing changes nothing, and says nothing.** Editing files
with `str.replace` from a script is fast and it fails silently: the suite went green here on
a test that had not been replaced, because the search string said "real map" where the file
said "metre map". Assert the match count before writing, and make the whole batch atomic so
a later mismatch does not leave earlier edits half-applied.

**A console keeps its errors across reloads.** A fixed error goes on being reported until the
tab is replaced, which is a fast way to spend twenty minutes re-fixing something. Read the
console in a fresh tab before believing it.

Record the resulting values in the widget's file in `docs/widgets/`, so a future rebuild
has something to fail against.

**And audit what the documentation itself claims.** Documentation makes factual assertions
that go stale exactly like code, and nothing tests them. This file once said every control
was at least 44 px, which was never true of the ? button; the widget's own file carried
power figures from an experiment the shipped control no longer performs. When a feature
changes, grep the docs for numbers and superlatives — "every", "always", "all" — and check
each one still holds.

## 3. Text

Read every string in the widget: titles, labels, tooltips, instructions, error messages,
legend text, captions.

- Would a first-year student with no technical background understand this sentence on
  first reading?
- Would someone reading English as an additional language understand it? Idiom, phrasal
  verbs, and metaphor are the usual failures.
- Is any technical term used before it is defined?
- Does anything read as machine-written? Check against
  `~/claude scratch/anti-ai-writing-style.md`.
- Can any sentence be shorter without losing its meaning?
- Read it aloud. Anything that trips the tongue gets rewritten.

**Every source cited must have been through an adversarial check.** Not a look-over: a
separate agent briefed to falsify each entry — does the work exist, are the details exact,
and does it actually support the claim it is attached to? The third is the one that
matters, because a real paper attached to a claim it never made survives casual reading.
Anything wrong is corrected or removed; anything that cannot be confirmed is removed. See
`principles.md` section 11.

## 4. Accessibility

- Keyboard only: reach every control, operate every control, see where focus is.
- Zoom the page to 200%. Nothing overlaps, nothing is cut off, nothing scrolls sideways.
- Screen reader: does every control announce what it is and what its value is? Does the
  graphic have a text alternative that conveys the same information?
- Colour: view in greyscale, and simulate deuteranopia and protanopia. Is any distinction
  now lost? If so, add a second cue.
- Contrast: check text and control graphics against their actual backgrounds, including
  over map tiles. 4.5:1 for body text, 3:1 for large text and control parts.
- Motion: check `prefers-reduced-motion`. Nothing flashes, nothing is on a timer.
- Touch targets at least 44x44 CSS pixels, with space between.

## 5. Device and room check

Three contexts, checked separately. See `docs/principles.md` section 3.

**Phone.** Open it in portrait on a real phone, over a slow connection, and use it for a
minute. Every control reachable by thumb. Nothing that needs hover. Nothing that needs a
precise drag. No horizontal scrolling. Reload with the network off after the first load
and see what it says.

**Laptop at reading distance.** Mouse and keyboard. Hover readouts work. Keyboard
shortcuts work. Nothing is comically oversized — this is the ordinary student URL and it
should look like a normal web page.

**Projected.** Open the presentation URL (`?present=1`) on the machine used in the
lecture room, put it on the projector in a lit room, and walk to the back. Read the
controls, the current values, and the legend from there, not just the graphic. Then look
at it in a compressed recording at medium resolution and check that thin lines and small
type have survived.

**Responsiveness.** Drag, paint, or scrub every continuous control and watch for stutter.
Time a redraw. If anything expensive runs on the main thread, move it to a worker; if a
redraw rewrites nodes that have not changed, stop it doing that. Check on a mid-range phone,
not only on the laptop.

**Measure the layout, do not eyeball it.** Two real bugs in the first widget were invisible
to the eye and obvious to a measurement: a single long sentence stretched its grid column
and pushed the controls off screen, and a stale rule outranked its replacement on CSS
specificity. Read back the actual widths, heights, and computed styles when something looks
even slightly wrong, and compare `document.documentElement.scrollWidth` against the
viewport.

**Embedding and links.** Open it in an `<iframe>` at the sizes we actually embed at.
Click the URL from a PowerPoint slide on the lecture machine. Confirm that a URL carrying
a particular configuration restores that configuration.

---

### The picture, not only the numbers

Check what was rendered, not what was computed. Read attributes back off the output and
confirm the drawing makes the same claim the model does — a widget here had correct values
drawn as circles that were wrong by up to 21 per cent, because of a clamp that looked like
a tidiness fix.

Then: is any quantity on an area a count shaded into a polygon? Does every panel in a row of
small multiples share one scale? Does a control still control something, after whatever was
changed? Do the captions, the footer and the licence line still describe what is modelled?

### What a reader sees with everything closed

List it. Title, labels, any text not behind an (i), at every screen size and in presentation
mode as well as normal. Then ask whether someone reading only that would know what the
widget is about and why it matters. If the answer lives in an explanation panel, and
presentation mode hides those panels, then the lecture version of the widget is missing its
argument. See `principles.md` section 13.

## Before the push

Three things that are not a pass but are part of shipping, and all three have been
forgotten at least once.

The widget is listed on `web/index.html` with a one-line description. A widget missing
from the front page is reachable only by people who were handed the URL.

Its file exists in `docs/widgets/` and has the five required parts listed in
`docs/widgets/README.md`, the verified numbers among them.

If a bug was fixed in the widget, `template/` was checked for the same bug. Copying is
what keeps the widgets independent, and it is also what lets one mistake live in several
places.

## Sign-off

```
Widget:
Reviewed: YYYY-MM-DD

Pedagogical critique: pass / changes requested — summary
Correctness: pass / changes requested — summary
Text: pass / changes requested — summary
Accessibility: pass / changes requested — summary
Device and room: pass / changes requested — summary

Outstanding:
```
