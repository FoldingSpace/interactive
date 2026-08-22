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
web/           the published site
  index.html   the list of widgets
  <widget>/    one folder per widget, named for what it shows
```

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

## Where things stand

Three widgets, deployed and live:
[spatial autocorrelation on a grid](https://foldingspace.github.io/interactive/spatial-autocorrelation/);
[drawing the lines](https://foldingspace.github.io/interactive/maup/), on the modifiable
areal unit problem, from GEOG 370's Lab 3; and
[least cost, whose cost?](https://foldingspace.github.io/interactive/least-cost/), on
least-cost paths, from Lab 4. Each has a file in `docs/widgets/` carrying its verified
numbers, review record, open threads and a "picking this up again" section. **Read that
before changing one** — the recorded values are the regression suite.

Neither lab widget is an answer key, and each refuses in a different way. The MAUP widget
refuses the crime category the lab asks students to model. The least-cost widget uses a
different city, a different destination and a different classification — Metro Vancouver's
open land use, which has an agricultural class where the lab's licensed DMTI data has none,
so nothing a student does there can reproduce the lab's surface. Both labs are worked
through in full in `lab3-worked.md` and `lab4-worked.md` in the **local** working folder,
outside this repository, because those files are the answer keys and this repository is
public. Keep it that way.

`template/` is a working skeleton to copy; `docs/widget-pattern.md` says what to keep and
what changes when a widget needs a map, a data file, or an animation instead of pure
computation.

Repository is `FoldingSpace/interactive`, pushed over an SSH deploy key; see
`docs/deployment.md` for the credential setup and the local preview command.

## Working notes

- Keep `docs/libraries.md` current. Every time a library works, fails, or is ruled out,
  write down which and why. That file is the point of not relearning this each term.
- Every external thing gets a line in `docs/attributions.md` at the moment it is added,
  not later.
- Credit reads "Made by Luke Bergmann with Claude" wherever a page carries a credit.
  Copyright notices read "Copyright (c) 2026 Luke Bergmann, where applicable" and stay
  that way — credit and copyright are not the same thing. See `docs/attributions.md`.
- Record verified numbers in the widget's file in `docs/widgets/`, so a rebuild has
  something to fail against. Reproducing a known case is necessary and never sufficient:
  ask what bug would pass the test you just ran.
- Measure rather than eyeball, for layout, for speed, and for what a control actually
  demonstrates. Most of the real defects found so far were invisible until something was
  measured, and one control turned out to teach the opposite of its design intent.
- Documentation makes claims that go stale exactly like code. When a feature changes,
  grep the docs for the numbers and the words "every", "always" and "all".
- Prefer an exact answer to a simulated one wherever a closed form exists, and know the
  floor of what a simulation can resolve. See `principles.md` section 7.
- A citation is not checked until you have read the thing. An adversarial agent fabricated
  a full set of verifications for this repository, complete with quotations and catalogue
  records, and then retracted them. Get the paper.
- What a widget is *for* goes in the reading flow, not behind an (i) and not in the footer.
  Presentation mode hides (i) panels, so anything only in them is missing from every lecture.
- A count is not a rate. Never shade a polygon by a count; use graduated symbols or divide
  by something, and know that the denominator is itself a claim. See `visual-forms.md`.
- Check the rendered output, not only the numbers behind it. Read attributes back off the
  SVG and verify the picture makes the claim the model does.
- After changing what is displayed, audit each control for whether it still controls
  something, and grep the captions, footer and licence line for claims that went stale.
- Replacing a block of CSS or code wholesale silently takes everything else in it. List what
  was in the block before replacing it; a layout rewrite here deleted an entire stylesheet.
- Duplicate rules are why a fix does not take. Two identical `.readout` declarations
  survived two attempts at the same bug.
- An author `display` rule beats the browser's `[hidden]`, and it has caught three widgets
  here. `template/` now declares `[hidden] { display: none !important; }` once, globally.
- A palette of more than about six categories has to be searched under simulated colour
  blindness, weighted by how much ground each class covers, not chosen by eye. See
  `visual-forms.md`.
- Batching a redraw into an animation frame means something will read state one frame
  behind. Keep a `flush()` for wherever a settled answer is read rather than drawn.
- Data licences decide what a widget can be. DMTI cannot be redistributed; going to Metro
  Vancouver's open land use produced a *better* widget, because its classes include the
  one the lab's own argument needs. Check the licence before the design, not after.
