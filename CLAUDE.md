# interactive

Interactive widgets for cartography and geographic information science. They are
built to explain things — in lectures, in talks, in writing, and to anyone who
follows a link — so teaching is the main use but not the only one.

This repository is the `github/` subfolder of a larger local working folder;
anything outside it is local-only and never pushed.

```
CLAUDE.md      this file
docs/          principles, libraries, attributions, review — documentation for us
web/           the published site
  shared/      stylesheets and scripts common to several widgets
  <widget>/    one folder per widget, named for what it shows
```

Widgets are named for their subject, not for a course. A widget only carries a
course label when it is genuinely specific to one course. Keep the folder names
short: they become the URL, and the URL goes on slides and into QR codes.

`docs/` is documentation for us and is not published. `web/` is the site.

## Read first

- `docs/principles.md` — the standing rules for everything built here.
- `docs/libraries.md` — what we use, what we have rejected, what we want to try.
- `docs/attributions.md` — register of every borrowed dataset, basemap, image, and library.
- `docs/review.md` — the passes a widget must survive before it goes in front of students.
- `docs/deployment.md` — how the repository is published, and the credential setup.
- `docs/widgets/` — one file per widget: what it teaches, how it works, its review record.

## Non-negotiables

1. Static files only. Everything runs from GitHub Pages with no server, no build step
   the browser can see, and no software a student has to install.
2. Two layouts from one file: a touch layout and a desktop layout, split on pointer
   type rather than width. The desktop layout serves both a laptop at reading distance
   and a projector seen from the back, so every widget has a presentation mode reached
   by `?present=1`.
3. It opens showing something. No blank canvas, no "click here to begin".
4. Every widget is embeddable in an `<iframe>` and reachable by a plain URL that can be
   pasted into a PowerPoint slide.
5. Student-facing text obeys `~/claude scratch/anti-ai-writing-style.md` and is written
   for readers with little technical background, many of whom read English as a second
   language.
6. Nothing ships without going through `docs/review.md`.

## Working notes

- Keep `docs/libraries.md` current. Every time a library works, fails, or is ruled out,
  write down which and why. That file is the point of not relearning this each term.
- Every external thing gets a line in `docs/attributions.md` at the moment it is added,
  not later.
