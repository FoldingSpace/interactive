# Libraries

What we use, what worked, what did not, and what is worth trying. Update this every time
a library earns or loses a place. Licences below are recorded from prior knowledge and
must be checked against the project's own repository before anything ships publicly.

Started 2026-08-19. Three widgets built so far and none needed a library, so the
"in use" table is still empty and everything below it remains a candidate.

Worth being exact about what that claim now covers, because the third widget uses more of
the browser than the first two did. A Web Worker, `OffscreenCanvas`-free `ImageData`
painting, `Blob` and `URL.createObjectURL`: all platform, none of it imported, none of it a
network request. "No library" means nothing we did not write is downloaded. It has never
meant we only use what a browser could do in 2010, and the line worth watching is whether a
feature is old enough and universal enough that a URL printed on a slide still works in
2031 — which workers are, comfortably.

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

Three widgets in, the streak is holding, and the third was the one most likely to break it.
`web/least-cost` runs Dijkstra over 41,800 cells and repaints a raster on every animation
frame, which sounds like a job for a graph library and a canvas library and is neither. A
binary heap on two typed arrays is about forty lines. Painting the land is one
`ImageData` and one `putImageData`; the browser's own nearest-neighbour upscaling does the
rest, from `image-rendering: pixelated`. Two Dijkstras, a full repaint and a DOM rebuild
settle at about 15 ms.

What it did need was a build-time dependency, which is a different thing and does not go in
the table above: `tools/lab4-extract.py` uses GDAL's Python bindings to fetch and rasterise
Metro Vancouver's land use. That runs on our machine, once, and what ships is a string of
41,800 digits inlined in the HTML. A build-time tool has none of the costs a runtime
dependency has — it cannot break a lecture, and it cannot stop working in 2031 — so the
rule "try it with no dependency first" applies to what the browser loads, not to what makes
the data.

Also worth recording because it was considered and rejected: shipping the grid as a GeoTIFF
and parsing it in the browser. That needs a TIFF reader, which is a runtime dependency, to
save about 30 KB before compression on a file the server already gzips. Digits in the HTML
keep the widget a single file that works from `file://`.

### Shortest paths: a library, or WebGPU?

Both asked, both answered no, and the reasons generalise.

**A graph library.** `ngraph.path` and friends are good and would lose here. They are built
for general graphs with object nodes and hash maps, and the cost of that indirection is
exactly what a grid lets you avoid: the whole state is four typed arrays indexed by
`row * W + col`, and neighbours are arithmetic rather than a lookup. The win available was
never in the library, it was in the queue.

**The queue was the win.** Replacing the binary heap with Dial's buckets took a solve over
167,200 cells from 28.9 ms to 13.5. Constant-time push and pop instead of O(log n), about
thirty lines, exact as long as a bucket is no wider than the smallest possible step. Measure
before reaching for anything larger: the second implementation of the right algorithm beat
every library that was on the table.

**WebGPU.** Tempting and wrong for this. Dijkstra expands in cost order, which is inherently
sequential; the GPU-shaped alternatives are Bellman-Ford relaxation sweeps or a fast
iterative eikonal solve, which do far more total work in the hope of doing it in parallel.
At 167,200 cells the problem is small enough that setup and readback would eat the gain.
Three further objections, any one of which decides it: WebGPU is not available everywhere
and a widget has to run in whatever browser a student already has; a URL printed on a slide
should still work in 2031, and a GPU API is a worse bet than typed arrays for that; and an
eikonal solver would quietly *change the answer*, because it approximates continuous
distance rather than the eight-direction lattice — losing the very artefact the widget
teaches about in its length panel.

**The Web Worker, which was on the table and is now in use.** It does not make anything
faster; it stops the main thread waiting, which is what `principles.md` section 4 asks for.
The trigger was measurable rather than aesthetic: at 376,200 cells a solve is about 35 ms,
which is two frames, and no scheduling on one thread hides that — 12 frames in 83 ran long
and a stroke averaged 52 fps. With the solver in a worker, none do.

Two things worth copying from how it is wired. The worker body is a **function that closes
over nothing**, stringified into a Blob at load, so the widget is still one file that works
from `file://` and there is no second request. And the move had to change no answers, which
is the sort of claim that needs a suite rather than a promise: 194 assertions, every
recorded number identical either side of it.

The cost is that nothing is synchronous any more, and that lands somewhere specific — the
one place that needed an answer matching the numbers beside it rather than the previous
ones. Find that place before moving a solver, not after.

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

## What the fourth widget taught

**Still no dependency, and a street network did not change that.** Reading a 917 KB
`data.js` of delta-coded integers, running Dijkstra over 24,410 junctions and 64,500
directed arcs, and stroking 32,250 polylines onto a canvas is about 500 lines of plain
JavaScript. A routing library would have been more code to integrate than to write, and a
graph library would have brought its own representation to argue with.

**A recompute is 17 to 63 ms, so no worker.** The trigger in `widget-pattern.md` is
measurable rather than aesthetic: the expensive work here happens on a click, not during a
drag, and a click can afford a frame. What runs every frame is the coordinate transform
and the stroking, which is two multiplies and an add per vertex over about 79,000
vertices. Algorithm first, and in this case the algorithm was enough.

**A binary heap was fine.** `least-cost` needed Dial's buckets because its costs were a
small set of integers over 800,000 cells. Here the costs are continuous and the graph is
thirty times smaller, so the heap never showed up in a measurement.

**`Float32Array` is not a free optimisation when a threshold is involved.** A grade stored
as exactly 50 per mille reads back as 0.050000001 and fails `> 0.05`. Keep the integer the
data actually holds and compare integers; use `Float64Array` wherever an independent check
has to agree with you. See `docs/widgets/relative-distance.md`.

**Antialiasing does not add up.** Two clipped shapes sharing an edge are each
antialiased against it, and two half-covered edges do not make one covered edge, so a
pale seam runs down every join. A mesh of them shows as a grid across the whole picture.
Push each shape's corners a fraction of a pixel out from its own centre before clipping.

**`requestAnimationFrame` is not a promise.** A page in a background tab gets no frames at
all, so anything a reader reads must be written before the first one, not in the last one.

### Warping a photograph: three libraries considered, none used

The fourth widget stretches a satellite image by the same rule as its streets, which is a
texture warp, and texture warps are what graphics libraries are for. All three candidates
were measured or reasoned about before being dropped, and the reasons differ.

**Canvas 2D, which is what it uses.** A clipped affine patch per mesh cell. Benchmarked
before anything was built: 1,300 cells in about 13 ms, 6,600 in 55. In the finished widget
a whole frame — photograph, streets, labels — is 10 to 14 ms, because more than half the
mesh is held rather than drawn. Fast enough that nothing else had to be considered
seriously.

**WebGL** does textured triangles natively and would be far faster. It was not needed once
canvas was measured, and it would have traded "runs on anything" for speed the widget does
not want. Same conclusion as WebGPU in `least-cost`, reached the same way: measure the
plain thing first.

**Mapbox's earcut** turns a polygon with holes into triangles, and looked relevant because
the warp has to stop at the edge of the traveller's space — a concave region with the inlet
as a hole. It is the wrong tool twice over. Ear clipping adds no interior points, so it
gives a few large skinny triangles where a texture warp needs many small ones; refining a
mesh is constrained Delaunay's job, not earcut's. And canvas takes an arbitrary path as a
clip region directly, so the crisp boundary needs no triangulation at all.

**Mapbox's Delaunator** was the closer call. A mesh whose vertices are the street junctions
themselves would follow the travel-time field better than a regular grid, because it puts
detail where the data is. 24,410 points gives roughly 48,000 triangles, which is a quarter
of a second a frame: fine for a settled state, too slow for the movement, and the movement
is the thing the widget is for.

## Tools used for extraction, not shipped

**GDAL's Python bindings, again** — `gdal.Warp` to mosaic four 1 m LiDAR tiles down to 4 m,
and `osr` for WGS84 to UTM zone 10N. Same as `least-cost`; nothing new learned except that
`floor()` on a projected minimum is not a stable anchor, because the last bit of a
projection is not stable between runs.

**The Overpass API** — `way["highway"](bbox); out body geom;` over twenty tiles. A regex
over highway values timed the server out every time and a plain tag query returned the
same window in three seconds. Filter locally.

## Things to test early

1. PMTiles served from GitHub Pages, with MapLibre, on a phone over campus wifi. This
   determines whether we can have real basemaps at all.
2. DuckDB-WASM cold-load time on a mid-range phone.
3. Whether GitHub Pages serves the byte-range requests PMTiles needs, and what the file
   size limits are in practice.
4. How MapLibre's default styles read on a projector, and how much restyling is needed to
   meet the legibility rules.
