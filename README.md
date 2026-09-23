# interactive

Small pages that show ideas from cartography or geographic information science. They allow
you to interact and explore the ideas. They run in a browser with nothing to install, on a
phone or on a projector. They are built for explaining: in lectures, in talks, and to
anyone who follows a link.

*Note that this page and the widgets linked to here should be assumed to have been made in
close conversation with Claude Code, mostly for classroom purposes.*

**Live site: https://foldingspace.github.io/interactive/**

## What is here

- [**Spatial autocorrelation on a
  grid**](https://foldingspace.github.io/interactive/spatial-autocorrelation/) — Explore
  spatial autocorrelation. Pattern lives in arrangement, not in amounts: the same number of
  grey squares, rearranged, gives a different answer. Who counts as a neighbour is a choice.
  Some things Moran’s I cannot see at all, such as direction. Paint a grid of black and white squares and watch
  Moran's I respond. The weights are an editable picture rather than a fixed choice; a
  second grid shows where the global number comes from, square by square; and an optional
  test against chance can be run corrected or uncorrected, so the cost of asking hundreds of
  questions at once is visible rather than asserted.

- [**Drawing the lines**](https://foldingspace.github.io/interactive/maup/) — Explore the
  Modifiable Areal Unit Problem. Cut Vancouver into areas one way, then another: the records
  stay the same and the answer does not. The records are made by institutions. Their
  categories decide what can be said. Does who lives in an area predict where incidents get
  reported to police? Three choices move the answer and none of them is in the data: how
  many areas you cut the city into, where the boundaries go, and what counts as *near*. A
  coefficient can be significant across 996 areas, absent across 118, and absent in every
  one of twenty other ways of drawing 118. A spatial error model is there to deal with the
  clustered errors. Taking space seriously helps, but no technical fix can settle the
  question of which aggregations and scales to rely upon in a given situation.

- [**Zone design: you help draw the
  boundaries**](https://foldingspace.github.io/interactive/zone-design/) — An exploration of
  the Modifiable Areal Unit Problem (MAUP). Boundaries are drawn by someone. Whoever draws
  the shapes shapes what the data will say. Is there a relationship between what households
  earn and how green the ground is? The page holds 1,342 dissemination areas across the City
  of Vancouver, UBC, western Burnaby and northern Richmond, what households in them earn,
  and how green the ground was on one August morning. Paint eight zones over the areas, on
  any of three maps, and the line between income and greenness moves, with its slope and R²
  printed live. Four zonings anybody could defend disagree. One turns the line over
  altogether. Each of the four is drawn by a rule somebody could state in advance. Greenness
  aggregates exactly whatever you do to it; income arrives as a median per area, medians do
  not add, and the three ways of averaging them disagree, so the averaging rule is a control
  rather than a footnote. A link carries any zoning you paint.

- [**Vancouver, measured in
  minutes**](https://foldingspace.github.io/interactive/relative-distance/) — Explore
  relative space. Distance is not only a property of the ground. It is made by how people
  move. Lonsdale Quay is 3.47 km from Waterfront Station and Commercial Drive is 3.06 km. On
  foot one is two and a quarter hours away and the other is thirty-eight minutes. Press
  Minutes and the street network slides outward until distance from the start *is* travel
  time, so two places the ground puts side by side end up nowhere near each other. A
  satellite photograph is stretched by the same rule, but only where the streets can say how
  long it takes to get there, so Burrard Inlet fades out rather than stretching. Four
  travellers, and the one who avoids steep ground loses 62% of the city, including the whole
  North Shore. Getting there and getting back are different trips, so swapping the two ends
  redraws everything.

- [**Three criteria, three weights**](https://foldingspace.github.io/interactive/pairwise/) —
  Explore the Analytical Hierarchy Process for decision-making. Every weight in a model is a
  choice somebody made. Here, judgements about what matters more are turned into numbers.
  Say in words how much more one thing matters than another, three times over, and the page
  turns the words into firm weights. A second number says how consistent your comparisons
  are. Consistent is not the same as right. Move the words and watch what survives: the
  order of the weights holds up to disagreement about how strong the words are, and gives
  way to disagreement about which way they point.

- [**Least cost, whose cost?**](https://foldingspace.github.io/interactive/least-cost/) —
  Explore least-cost path analysis for routing. An optimal route is only optimal for
  somebody: its costs are values, not measurements. A power line has to reach a new plant,
  and the route it takes is decided by nine numbers. Say what crossing farmland, houses,
  parks or water is worth avoiding and the line moves; draw a park where there was none and
  it moves again. Keep a route and it carries the table that produced it, so a set of
  proposals can be compared with their reasons attached. One control draws six more routes
  the same numbers score almost the same, because the single confident line is the method's
  most misleading habit — and swapping the queue inside the solver, a detail with nothing
  geographic in it, moves half the answer onto different ground at exactly the same cost.

## How they are built

Static HTML, CSS and JavaScript, with **no libraries, no build step the browser can see,
and no network calls after the page loads**. No server, no accounts. Three of the six are a
single self-contained file; the other three keep their data in a sibling `data.js` (and, for
two of them, one image) in the same folder, which is the same thing as far as a reader or an
`iframe` is concerned. Where data
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
