# Libraries

What we use, what worked, what did not, and what is worth trying. Update this every time
a library earns or loses a place. Licences below are recorded from prior knowledge and
must be checked against the project's own repository before anything ships publicly.

Started 2026-08-19. One widget built so far, and it needed no library at all, so the
"in use" table is still empty and everything below it remains a candidate.

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

## Things to test early

1. PMTiles served from GitHub Pages, with MapLibre, on a phone over campus wifi. This
   determines whether we can have real basemaps at all.
2. DuckDB-WASM cold-load time on a mid-range phone.
3. Whether GitHub Pages serves the byte-range requests PMTiles needs, and what the file
   size limits are in practice.
4. How MapLibre's default styles read on a projector, and how much restyling is needed to
   meet the legibility rules.
