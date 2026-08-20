# interactive

Interactive widgets for cartography and geographic information science.

Each widget is a small web page that does one thing: it shows an idea and lets you
change something to see what happens. They are built for explaining — in lectures, in
talks, and to anyone who follows a link — and they run in a browser with nothing to
install.

**Live site: https://foldingspace.github.io/interactive/**

## How they are built

Static HTML, CSS, JavaScript, and WebAssembly. No server, no accounts, no build step
the browser can see. Every widget opens with defaults already set and something already
drawn, works on a phone and on a projector, can be embedded in an `iframe`, and can be
linked by a plain URL that carries its configuration.

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

## Licence

Code is [MIT](LICENSE). Text, figures, and other non-code materials are
[CC BY 4.0](LICENSE-CC-BY-4.0). Borrowed material keeps its own licence, recorded in
[docs/attributions.md](docs/attributions.md).

Reuse and adapt these freely. If you teach with them, a credit is enough.
