# Libraries

What we use, what worked, what did not, and what is worth trying. Update this every time
a library earns or loses a place. Licences below are recorded from prior knowledge and
must be checked against the project's own repository before anything ships publicly.

Started 2026-08-19. Two widgets built so far and neither needed a library, so the
"in use" table is still empty and everything below it remains a candidate.

The empty table is a result about one kind of widget, not about the repository. A widget
that computes something over made-up data has nothing to import. A widget that draws a
real basemap, reprojects real coordinates, or queries a real file almost certainly does,
and the first one that does will change two claims made elsewhere: that no widget needs a
dependency, and that no widget makes a network call after it loads. Change the claims when
that happens rather than contorting the widget to keep them true. See section 13 of
`principles.md` and `widget-pattern.md`.

---

## In use

| Library | Version | What we use it for | Notes |
|---|---|---|---|
| _(none)_ | | | Spatial autocorrelation needed no dependency at all. Worth trying that first each time. |

## Platform features we do rely on

No libraries, but the widgets are not written in 2005 either. These are the browser
features the first widget leans on, all of them long-standing and universally supported:

| Feature | Used for |
|---|---|
| `Worker` from a `Blob` URL | heavy computation off the main thread, without a second file |
| Typed arrays | `Int32Array`, `Float64Array` in hot loops |
| CSS grid, `grid-template-areas` | the layout, including the presentation rearrangement |
| Pointer events, `setPointerCapture` | drag-to-paint, with mouse and touch distinguished |
| `aspect-ratio`, `min()` in CSS | square grids that size themselves to the viewport |
| `history.replaceState`, `URLSearchParams` | configuration in the URL |
| `prefers-color-scheme`, `prefers-reduced-motion` | respecting the reader's settings |

The worker trick is worth remembering: put the worker's source in a
`<script type="javascript/worker">` tag, read its `textContent`, and construct a `Blob`
URL. The page stays a single self-contained file, there is one copy of the code, and if
`Worker` is unavailable the same source can be compiled on the main thread with
`new Function`.

## Ruled out

| Library | Why | Date |
|---|---|---|
| Any dense matrix library | Considered for the permutation test in the spatial autocorrelation widget. It would have been *slower*: the weights are sparse, about 4,800 non-zeros in a 225 × 225 matrix, and a dense routine does ten times the arithmetic to earn its vectorisation. The wins came from the algorithm and from exploiting binary data, neither of which a general library could have found. | 2026-08-19 |

---

## Candidates

Grouped by the job they do. None of these have been tested in this repository yet.

### Slippy maps and vector tiles

- **MapLibre GL JS** — BSD-3. WebGL vector tiles, client-side styling, good on mobile.
  The obvious default for anything that needs a pannable map with a real cartographic
  style. Heavier than Leaflet; check the load on an older phone.
- **Leaflet** — BSD-2. Small, raster tiles, very forgiving. Right choice when the map is
  a backdrop and the teaching point is somewhere else.
- **OpenLayers** — BSD-2. The most capable on projections and on mixed raster/vector
  sources. Larger and more verbose; worth it when the lesson is about projections or
  about WMS/WMTS services.
- **PMTiles / Protomaps** — BSD-3. Single-file tile archives served over plain HTTPS with
  range requests. This is the piece that makes real basemaps possible on GitHub Pages
  with no tile server. High priority to test.

### Projections and geometry

- **proj4js** — MIT. The projection lesson in a box. Pairs with EPSG definitions.
- **d3-geo** and **d3-geo-projection** — ISC. Projection animation, graticules, and the
  whole family of world projections drawn as SVG or canvas. Best available tool for
  teaching what a projection does to shape and area.
- **Turf.js** — MIT. Buffers, overlays, centroids, distance. Modular, so import only the
  functions used.
- **h3-js** — Apache-2.0. Hexagonal indexing, if we teach aggregation over grids.

### Charts and non-map graphics

- **Observable Plot** — ISC. Fast to write, sensible defaults, good for the chart that
  sits beside a map. Check its output against the legibility rules in
  `principles.md`; defaults are tuned for a laptop screen, not a projector.
- **D3** — ISC. When the graphic is the lesson and nothing off the shelf will do.

### Data in the browser

- **DuckDB-WASM** — MIT. SQL over Parquet and CSV in the browser, including spatial
  functions through its spatial extension. Would let us teach querying without a
  database server. Test the download size first; it is not small.
- **Apache Arrow JS** — Apache-2.0. Efficient columnar data transfer; usually arrives as
  a dependency of something else rather than a direct choice.
- **GeoTIFF.js** — MIT. Reads Cloud-Optimized GeoTIFFs in the browser, including partial
  reads. The route to teaching raster analysis without a server.
- **gdal3.js** (GDAL compiled to WebAssembly) — check licence. Format conversion and
  warping in the browser. Powerful and large; only where the lesson needs it.

### Colour

- **ColorBrewer** — Apache-2.0. The schemes and the reasoning behind them. Our default
  source for cartographic ramps.
- **d3-scale-chromatic** — ISC. ColorBrewer plus viridis and friends, ready to use.
- **chroma.js** — check licence (BSD/Apache). Colour interpolation, contrast ratios, and
  colour-blindness simulation. Useful in a widget that teaches colour choice.
- **viridis / cividis** — public domain. Perceptually uniform, and cividis is designed
  specifically for colour vision deficiency. Good defaults for sequential data.

### Accessibility and checking

- **axe-core** — MPL-2.0. Automated accessibility checking. Runs as a dev-time check, not
  shipped.
- Manual checks still matter more: keyboard, zoom to 200%, greyscale, and looking at it
  on a real projector.

### Basemap and tile sources

Anything that needs a key or has a usage cap is a poor fit for a class of students all
clicking at once. Prefer self-hosted PMTiles built from OpenStreetMap or Natural Earth.
The OSM tile servers are not for classroom load; read their usage policy before pointing
anything at them.

---

## What the first widget taught

**Try it with nothing first.** Moran's I, local Moran's I, a permutation test,
Benjamini-Hochberg, a seeded random number generator, a smoothed-field pattern generator,
colour ramp interpolation and drag painting with line interpolation came to a few dozen
lines each. Every one of them would have been more work to integrate as a dependency than
to write. That will not hold for a real basemap, but it held for everything so far.

**The cost that matters is rarely the arithmetic.** In the permutation test the bottleneck
was the random number generator, not the multiply-adds, and the biggest single win in the
whole widget came from not writing to DOM nodes whose value had not changed. Profile
before reaching for anything.

## Tools used to build, not to ship

Neither of these is a dependency — nothing they touch reaches the browser.

**Node** for offline verification: syntax-checking the widget's scripts after every edit,
and running searches against a copy of the widget's own generator. Copying the real source
rather than reimplementing it matters; see the correctness pass in `review.md`.

**Python with numpy** for independent recomputation of every statistic, by a different
route from the widget's own — matrix algebra against its loops. This is what has caught
things, and it is worth the small cost of writing the check twice.

## What the second widget taught

**A data-backed widget still needed no library.** The MAUP widget ships 996 polygons,
their contiguity, an ordinary least squares fit with exact p-values, and a permutation
test, in plain JavaScript. What replaced a geometry library was a choice about the data
format: quantising coordinates to a 2 m grid *before* encoding makes touching polygons
share exact vertices, so contiguity is a hash of shared points rather than a topology
computation, and simplification cannot open slivers between neighbours. Deciding how the
data is written is often the cheaper half of deciding what code to run over it.

**Exact inference beat simulation twice.** Coefficient p-values come from the regularised
incomplete beta function in about sixty lines, checked against three closed forms. Moran's I
uses the exact randomisation moments rather than a permutation test — which was not only
tidier but necessary, since one of the weight matrices on offer is dense and 999 shuffles of
it would have been a billion operations.

**Two files, not one.** This is the first widget with a separate `data.js`, at 130 KB.
The single-file rule was about having no external dependency, and a sibling file in the
same folder does not break that. Inlining it would only have made the source unreadable.

**Do not time code in a harness.** Slicing the widget's maths into a Node script to
measure it reported 208 ms where the page takes 57 ms, and blamed the random number
generator, which was not the problem. Top-level script code is not optimised the way code
inside a function is. Verify *values* in a harness; measure *time* in the page.

## What each sort of widget is likely to need

A rough map, to be corrected as widgets get built. The point is to know before starting
which of the project's habits are about to be tested.

| Sort | Likely dependencies | What to watch |
|---|---|---|
| Computation on made-up data | none so far | Speed and exactness. Prefer a closed form; keep the main thread free. |
| Vector polygons with attributes | none so far | Quantise coordinates before encoding, and adjacency comes free. Watch the file size and the licence. |
| Spatial statistics on irregular areas | none so far | Dense weight matrices rule out simulation; use exact moments. Estimators that need a determinant do not fit in a browser, ones built on moment conditions do. |
| Maps and basemaps | MapLibre, PMTiles | Network calls after load, tile licensing, default styles that fail on a projector. |
| Projections and geometry | proj4js, turf, d3-geo | Which definition of a projection is being used, and whether it matches what students are taught. |
| Data-backed | possibly none; DuckDB-WASM only if genuinely large | File size over classroom wifi and phone data. Licence and provenance of the extract. |
| Charts and non-map graphics | none, or d3 pieces | A whole charting library is rarely worth it for one figure that has to be legible from the back of a room. |
| Time and animation | none | `prefers-reduced-motion`, and never letting motion carry a cue on its own. |

## Things to test early

1. PMTiles served from GitHub Pages, with MapLibre, on a phone over campus wifi. This
   determines whether we can have real basemaps at all.
2. DuckDB-WASM cold-load time on a mid-range phone.
3. Whether GitHub Pages serves the byte-range requests PMTiles needs, and what the file
   size limits are in practice.
4. How MapLibre's default styles read on a projector, and how much restyling is needed to
   meet the legibility rules.
