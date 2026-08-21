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

## How they are built

Static HTML, CSS and JavaScript. Every widget so far is a single self-contained file with
**no libraries, no build step, and no network calls after the page loads**. No server, no
accounts. Every widget opens with defaults already set and something already drawn, works
on a phone and on a projector, can be embedded in an `iframe`, and can be linked by a
plain URL that carries its configuration.

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
