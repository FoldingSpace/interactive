# interactive

Interactive widgets for cartography and geographic information science.

Each widget is a small web page that does one thing: it shows an idea and lets you
change something to see what happens. They are built for explaining — in lectures, in
talks, and to anyone who follows a link — and they run in a browser with nothing to
install.

**Live site: https://foldingspace.github.io/interactive/**

## What is here

- [**Spatial autocorrelation on a grid**](https://foldingspace.github.io/interactive/spatial-autocorrelation/)
  — paint a grid of black and white squares and watch Moran's I respond. The weights are an
  editable picture rather than a fixed choice; a second grid shows where the global number
  comes from, square by square; and an optional test against chance can be run corrected or
  uncorrected, so the cost of asking hundreds of questions at once is visible rather than
  asserted.

- [**Drawing the lines: MAUP in Vancouver**](https://foldingspace.github.io/interactive/maup/)
  — does who lives in an area predict where incidents get reported to police? Three choices
  move the answer and none of them is in the data: how many areas you cut the city into,
  where the boundaries go, and what counts as *near*. A coefficient can be significant across
  996 areas, absent across 118, and absent in every one of twenty other ways of drawing 118.
  A spatial error model is there to deal with the clustered errors, and the page is candid
  about what dealing with them does not fix.

- [**Vancouver, measured in minutes**](https://foldingspace.github.io/interactive/relative-distance/)
  — Lonsdale Quay is 3.47 km from Waterfront Station and Commercial Drive is 3.06 km. On foot
  one is two and a quarter hours away and the other is thirty-eight minutes. Press Minutes and
  the street network slides outward until distance from the start *is* travel time, so two
  places the ground puts side by side end up nowhere near each other. A satellite photograph
  is stretched by the same rule, but only where the streets can say how long it takes to get
  there, so Burrard Inlet fades out rather than stretching. Four travellers, and the one who
  avoids steep ground loses 62% of the city, including the whole North Shore. Getting there
  and getting back are different trips, so swapping the two ends redraws everything.

- [**Least cost, whose cost?**](https://foldingspace.github.io/interactive/least-cost/)
  — a power line has to reach a new plant, and the route it takes is decided by nine numbers
  that are somebody's values rather than anybody's measurements. Say what crossing farmland,
  houses, parks or water is worth avoiding and the line moves; draw a park where there was
  none and it moves again. Keep a route and it
  carries the table that produced it, so a set of proposals can be compared with their reasons
  attached. One control draws six more routes the same numbers score almost the same, because
  the single confident line is the method's most misleading habit — and swapping the queue
  inside the solver, a detail with nothing geographic in it, moves half the answer onto
  different ground at exactly the same cost.

## How they are built

Static HTML, CSS and JavaScript, with **no libraries, no build step the browser can see,
and no network calls after the page loads**. No server, no accounts. Two of the three are a
single self-contained file; the third keeps its data in a sibling `data.js` in the same
folder, which is the same thing as far as a reader or an `iframe` is concerned. Where data
has to be prepared, that happens once on our machine — see `tools/` — and what ships is the
result. Every widget opens with defaults already set and something already drawn, works
on a phone and on a projector, can be embedded in an `iframe`, and can be linked by a
plain URL that carries its configuration.

`node tools/test/run.js` runs before anything is published, and gates the deploy. It loads
each widget's shipped HTML, runs its own script, and checks what the page draws rather than
what it computes.

A new widget starts by copying `template/`, a working skeleton that already meets several
of those requirements. What to keep and what to replace is in
[docs/widget-pattern.md](docs/widget-pattern.md).

The rules we hold ourselves to are written down in [docs/principles.md](docs/principles.md),
and nothing goes out without the checks in [docs/review.md](docs/review.md).

## Documentation

| File | What is in it |
|---|---|
| [docs/principles.md](docs/principles.md) | Standing rules: delivery, layout, text, accessibility |
| [docs/libraries.md](docs/libraries.md) | Libraries we use, rejected, or want to try |
| [docs/attributions.md](docs/attributions.md) | Every borrowed dataset, basemap, and library |
| [docs/review.md](docs/review.md) | The passes a widget must survive before release |
| [docs/deployment.md](docs/deployment.md) | How this repository is published, and why |
| [docs/visual-forms.md](docs/visual-forms.md) | What to draw: quantities on areas, small multiples, decomposition, colour |
| [docs/widget-pattern.md](docs/widget-pattern.md) | How a widget is put together, and how to start a new one |
| [docs/widgets/](docs/widgets/) | One file per widget: what it teaches, how it works, the verified numbers, and its review record |

## Who made it

Luke Bergmann with Claude. The widgets were built in conversation: the
teaching judgement, the decisions and the direction are Luke's; Claude wrote the code,
ran the checks and argued back.

## Licence

Code is [MIT](LICENSE). Text, figures, and other non-code materials are
[CC BY 4.0](LICENSE-CC-BY-4.0). Copyright (c) 2026 Luke Bergmann, where applicable.
Borrowed material keeps its own licence, recorded in
[docs/attributions.md](docs/attributions.md).

Reuse and adapt these freely. If you teach with them, a credit is enough.
