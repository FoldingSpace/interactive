# interactive

Interactive widgets for cartography and geographic information science. They are
built to explain things — in lectures, in talks, in writing, and to anyone who
follows a link — so teaching is the main use but not the only one.

This repository is the `github/` subfolder of a larger local working folder;
anything outside it is local-only and never pushed.

```
CLAUDE.md      this file
docs/          principles, libraries, attributions, review — documentation for us
  widgets/     one file per widget: what it teaches, the verified numbers, the review record
template/      a working skeleton to copy when starting a widget; not published
tools/         data extraction, and the test suite that gates the deploy
web/           the published site
  index.html   the list of widgets
  <widget>/    one folder per widget, named for what it shows
```

Run `node tools/test/run.js` before pushing. CI runs it too and nothing publishes if it
fails. The suite loads a widget's shipped HTML, runs its own script in a small stub DOM, and
checks what the page **draws** — routes read back off the SVG, land read back off the canvas
pixels — rather than what it computes. See `tools/test/README.md`.

There is no `web/shared/`. Each widget is a single self-contained file, and shared code
waits until a second widget needs the same thing — see `docs/widget-pattern.md`.

Widgets are named for their subject, not for a course. A widget only carries a
course label when it is genuinely specific to one course. Keep the folder names
short: they become the URL, and the URL goes on slides and into QR codes.

`docs/` is documentation for us and is not published. `web/` is the site.

## Read first

- `docs/principles.md` — the standing rules for everything built here.
- `docs/visual-forms.md` — what to draw: quantities on areas, small multiples, decomposition, colour.
- `docs/libraries.md` — what we use, what we have rejected, what we want to try.
- `docs/attributions.md` — register of every borrowed dataset, basemap, image, and library.
- `docs/review.md` — the passes a widget must survive before it goes in front of students.
- `docs/deployment.md` — how the repository is published, and the credential setup.
- `docs/widget-pattern.md` — how a widget is put together, and what to do when starting one.
- `docs/widgets/` — one file per widget: what it teaches, how it works, its review record.

## Non-negotiables

1. Static files only. Everything runs from GitHub Pages with no server, no build step
   the browser can see, and no software a student has to install.
2. Two layouts from one file: a touch layout and a desktop layout. Width decides the
   column count; pointer type decides control shape and target size. The desktop layout
   serves both a laptop at reading distance and a projector seen from the back, so every
   widget has a presentation mode reached by `?present=1`.
3. It opens showing something, and the opening state is not a dead end — every control a
   student might reach for must lead somewhere from the default.
4. Every widget is embeddable in an `<iframe>` and reachable by a plain URL that can be
   pasted into a PowerPoint slide.
5. Student-facing text obeys `~/claude scratch/anti-ai-writing-style.md`, is written for
   readers with little technical background and for readers of English as a second
   language, and there is as little of it on screen as the widget can manage.
6. Try it with no dependency first. So far nothing has needed one.
7. Where the method fails, say so on screen. A blank result reads as a fact about the
   data when it is a fact about the method.
8. Every control that embodies a choice carries an (i) explanation. Where it cites, it
   ends in `For more, see:` with real sources; where there is nothing verified worth
   citing, it cites nothing. The claim decides the citation, never the reverse.
9. **No citation ships unchecked.** A separate adversarial agent must confirm each source
   exists, that its details are exact, and that it supports the claim attached to it.
   Unconfirmable citations are removed, not hedged.
10. Nothing ships without going through `docs/review.md`, including its correctness pass.
11. Every widget carries a **For the classroom** panel: one five-minute pair activity, doable
    on one phone between two or on paper, starting from an answer each student commits to
    before anything is revealed. It is designed in conversation with whoever teaches it, not
    drafted, and it is the one (i) panel that stays visible in presentation mode.
    `principles.md` section 16.

## Where things stand

Four widgets, deployed and live:
[spatial autocorrelation on a grid](https://foldingspace.github.io/interactive/spatial-autocorrelation/);
[drawing the lines](https://foldingspace.github.io/interactive/maup/), on the modifiable
areal unit problem, from GEOG 370's Lab 3;
[least cost, whose cost?](https://foldingspace.github.io/interactive/least-cost/), on
least-cost paths, from Lab 4; and
[Vancouver, measured in minutes](https://foldingspace.github.io/interactive/relative-distance/),
on relative space, which is the first one here not built beside an assessment at all. Each
has a file in `docs/widgets/` carrying its verified
numbers, review record, open threads and a "picking this up again" section. **Read that
before changing one** — the recorded values are the regression suite.

None of the four carries a **For the classroom** panel yet — the requirement post-dates
them. Each one needs its own grilling session with Luke before it is written; see
`principles.md` section 16, and the note at the end of each widget's file.

Neither lab widget is an answer key, and each refuses structurally rather than by asking
students not to look — see `principles.md` section 15, which is the working order both
followed. Both labs are worked through in full in `lab3-worked.md` and `lab4-worked.md` in
the **local** working folder, outside this repository, because those files are the answer
keys and this repository is public. Keep it that way.

`template/` is a working skeleton to copy; `docs/widget-pattern.md` says what to keep and
what changes when a widget needs a map, a data file, or an animation instead of pure
computation.

Repository is `FoldingSpace/interactive`, pushed over an SSH deploy key; see
`docs/deployment.md` for the credential setup and the local preview command.

## Working notes

Nineteen of these accumulated as a flat list over three builds, which is past the point
where anyone reads past the fifth. Grouped now. Every one was paid for.

### Before building

- **Settle the licence before the subject.** It decides what the widget can be about, and it
  has already improved one of these rather than limiting it. `principles.md` section 10.
- **Work the lab in full first** if the widget comes from one, keep the worked version out
  of this repository, and make the widget structurally unable to answer the questions.
  `principles.md` section 15.
- **Prefer an exact answer to a simulated one** wherever a closed form exists, and know the
  floor of what a simulation can resolve. `principles.md` section 7.

### What breaks, and what it looks like when it does

- **Replacing a block of CSS or code wholesale silently takes everything else in it.** List
  what was in the block first; a layout rewrite here deleted an entire stylesheet.
- **Duplicate rules are why a fix does not take.** Two identical `.readout` declarations
  survived two attempts at the same bug.
- **An author `display` rule beats the browser's `[hidden]`.** Caught three widgets here;
  `template/` now declares `[hidden] { display: none !important; }` once, globally.
- **Batching a redraw into an animation frame leaves state one frame behind**, and it fools
  a test harness before it fools a user. Keep a `flush()` for wherever a settled answer is
  read rather than drawn. `widget-pattern.md`.

### What to check

- **Measure before optimising, and measure the alternative too.** Swapping a binary heap for
  a bucket queue more than halved a solve; a graph library and WebGPU were both considered
  and both would have been slower or less portable. See `libraries.md`.
- **A worker is for when scheduling can no longer hide the work**, not for anything that
  fits in a frame. It costs you every synchronous read, so find the place that needs a
  settled answer before you move the solver, not after. Algorithm, then decoupling, then
  caching, then the worker — in that order. See `widget-pattern.md`.
- **A stub DOM that disagrees with a browser is a bug in the stub.** Entities, `innerHTML`,
  whitespace between inline elements: three found here, each because an assertion contradicted
  what the page visibly does.
- **Assert that the things you build are not empty.** A titled card with a collapsed body sat
  live for months. One assertion catches that class of bug on the day it happens.
- **A class name is a claim, and the class defined by absence is where it goes wrong.**
  `least-cost` called U100 "Open land" and priced it at 1, the cheapest thing on its map;
  the class is "Undeveloped and Unclassified", it is defined by what the land is not, and it
  included part of an Indian reserve. Read the publisher's **long** definition — the
  paragraph in the service metadata, not the one-line description field — before writing any
  label. Skipping it caused the mislabel and then caused the correction to invent an example
  belonging to a different code.
- **Never quote a figure measured with the reference implementation as a figure about the
  widget.** They agree on cost, length and composition and disagree about which cells,
  because the routes tie. A "two thirds of the route is unchanged" claim went on the
  least-cost page at 63%; on the widget it is 32%, and the file three sections away already
  said that this exact quantity is a property of the queue. Quote what both agree on.
- **A window is a claim about what is inside it, and it needs the same check as a citation.**
  The least-cost file said its window was clear of every reserve, with the word "checked" in
  the sentence, and one query of the `Jurisdiction` field refuted it. Query the field, print
  the distinct values, and put the extent in a test — it lives as one number in three files
  and a rebuild is where it comes back.
- **A sentence that states a measurement needs a test, or it goes stale silently.** Three
  claims on the least-cost page and in its file were measured on grids two resolutions old
  and had been carried forward as current — one of them in an (i) panel telling students
  something the widget no longer did. Grep the prose for numbers whenever the model moves,
  and put the load-bearing ones in the suite.
- **Measure rather than eyeball** — layout, speed, and what a control actually demonstrates.
  Most real defects here were invisible until something was measured, and one control turned
  out to teach the opposite of its design intent.
- **Check the rendered output, not only the numbers behind it.** Read attributes back off
  the SVG and confirm the picture makes the claim the model does.
- **Measure the mark, not the box it sits in.** An element's rect is the slot; a `Range` over
  its text node gives the line. Comparing boxes said "aligned" while the sign floated eleven
  pixels below the words. See `visual-forms.md`.
- **An independent check agrees about scalars and not about ties.** Cost, length and counts
  will match; which of several tied answers got picked will not. Say which is which.
- **Record verified numbers** in the widget's file in `docs/widgets/`, so a rebuild has
  something to fail against. Reproducing a known case is necessary and never sufficient: ask
  what bug would pass the test you just ran.
- **After changing what is displayed**, audit every control for whether it still controls
  something, and grep the captions, footer and licence line for claims that went stale.
- **Documentation goes stale exactly like code.** When a feature changes, grep the docs for
  the numbers and for "every", "always" and "all". The README's "single self-contained file
  with no build step" survived two builds that had already broken it.

### What goes on the page

- **What a widget is *for* goes in the reading flow**, not behind an (i) and not in the
  footer. Presentation mode hides (i) panels, so anything only there is missing from every
  lecture.
- **A count is not a rate.** Never shade a polygon by a count; use graduated symbols or
  divide by something, and know the denominator is itself a claim. `visual-forms.md`.
- **A palette of more than about six categories has to be searched** under simulated colour
  blindness, weighted by how much ground each class covers, not chosen by eye.
  `visual-forms.md`.
- **A citation is not checked until you have read the thing.** An adversarial agent
  fabricated a full set of verifications for this repository, complete with quotations and
  catalogue records, and then retracted them. Get the paper.
- **An independent implementation cannot see a wrong input.** Two routes agreed to six
  decimals on a cycling time that was wrong about Vancouver, and the widget's own file
  explained the error as a hill when it was a detour. Recomputation tests the arithmetic;
  the input needs a second source, an independent tool, or somebody who knows the place.
  `principles.md` section 11.
- **A number you can explain is not thereby a number you have checked.** The wrong figure
  above survived because it came with a story that fitted. Same failure as reaching for a
  citation because it fits a claim.
- **A comment that states an intent is a claim.** One here said "does this traveller have
  any way to leave the start?" over code that asked something else, and shipped a blank map.
  Check the code against the comment the way you check a source against its claim.
- **The citation most likely to be attached to a claim it does not make** is the one
  supporting a framing rather than a method. Cite the argument, objection included.
  `principles.md` section 11.

### Bookkeeping

- Keep `docs/libraries.md` current. Every time a library works, fails, or is ruled out,
  write down which and why. That file is the point of not relearning this each term.
- Every external thing gets a line in `docs/attributions.md` at the moment it is added.
- Credit reads "Made by Luke Bergmann with Claude" wherever a page carries a credit.
  Copyright notices read "Copyright (c) 2026 Luke Bergmann, where applicable" and stay that
  way — credit and copyright are not the same thing. See `docs/attributions.md`.
