# Least cost, whose cost?

**Live:** https://foldingspace.github.io/interactive/least-cost/
**Source:** `web/least-cost/index.html` (one file, grid data inlined, no dependencies)
**Data tool:** `tools/lab4-extract.py`
**Built:** 2026-08-21

## The one thing it teaches

A least-cost route is a proposal made by whoever chose the numbers, not a fact found in
the landscape — so the honest output of the analysis is a set of routes, each carrying the
table that produced it.

Two mechanisms carry that. The bars change what each kind of land costs. The brush changes
what kind of land is there. Between them they cover the two places a value can enter the
analysis: what you price, and what you decide the thing is.

## Where it came from

GEOG 370 Lab 4 routes a power line across Langley over DMTI land use, using a friction
table the lab itself describes as carrying "an urban-centered bias". The lab is worked in
full in `lab4-worked.md` in the **local** working folder, outside this repository, because
that file is the answer key.

**This widget is deliberately not that lab.** Different city, different destination,
different classification, and — decisively — a different set of classes. The lab's DMTI
data has no agricultural class at all, so Langley's Agricultural Land Reserve is filed
under "Open Area" and priced at the base cost of 1. Metro Vancouver's land use has
Agriculture as its own class. Nothing a student does here can reproduce the lab's surface.

The finding that shaped the widget: the lab asks students to argue for protecting
farmland, and the classification has no word for it. The value cannot be expressed
whatever numbers you choose. That is why the widget lets you draw as well as price.

## The data

**Metro Vancouver Land Use 2016** ("Landuse 2016 - Code Description"), Metro Vancouver Open
Government Licence. Already in NAD83 / UTM zone 10N, so nothing is reprojected.

DMTI CanMap Route Logistics, which the lab uses, is licensed data and cannot go on a public
site. That constraint turned out to improve the widget rather than limit it.

**Window:** 504000–526000 E, 5428500–5447500 N. 220 × 190 cells of 100 m. Entirely inside
Metro Vancouver, so there are no holes, and clear of every reserve and treaty boundary in
the region's own `Jurisdiction` field — checked, not assumed. An earlier plan ran to Roberts
Bank; the causeway's shore end sits inside Tsawwassen First Nation lands, and a cost surface
that assigns treaty land a friction number is making a category error. The corridor was
moved rather than the question fudged. This does not make the land it does cross
uncontested.

**Endpoints.** The start is a real utility site at 124 St and 86 Ave in Surrey, cell
(row 24, col 51). Metro Vancouver's own data classifies that exact cell **T400, "Utility,
Communication and Work Yards"**, which is what the widget's wording rests on — checked
against the open dataset rather than inherited from the licensed one, and stated as a
utility site rather than as a named company's substation, because the open data does not
say whose it is. The plant is not real: it stands in for something that would be proposed
at Campbell Heights, cell (row 150, col 180), where the industrial district's expansion
into farmland is a live argument.

**Classes.** Twenty-nine Metro Vancouver codes grouped into eight, plus roads. The grouping
is ours and the widget says so. Shares of the window:

| Class | Codes | Share |
|---|---|---|
| Houses | S100, S110, S120, S130, S131, S135, S410, S230, S235 | 28.5% |
| Farmland | A500 | 21.8% |
| Water | R200 | 14.1% |
| Parks and protected | R100, W400 | 12.9% |
| Road and rail | S500, T100, T200, T300 | 12.4% |
| Industry | S300, M300, S600, T400 | 3.8% |
| Open land | U100 | 3.3% |
| Shops and offices | S200, S202, S204 | 1.9% |
| Schools and civic | S400, S420, S450, S460 | 1.2% |

## How it computes

Eight-neighbour Dijkstra. Stepping between two cells costs the mean of their two values
times the distance between their centres — 100 m orthogonally, 100√2 m diagonally — which is
what ArcGIS's Distance Accumulation does with a cost raster, and what the lab's numbers
assume.

The near-tie band runs the same solve twice, outward from the substation and outward from
the plant, and adds the surfaces. Each cell then holds the cost of the cheapest route that
passes through it; cells within the tolerance of the optimum are the band. This is Pinto and
Keitt's Conditional Minimum Transit Cost.

A binary heap on typed arrays, with a settled flag rather than a decrease-key. A cell can be
pushed more than once; the flag is what stops it being expanded twice. Reading the key off
the heap entry instead would use a stale distance.

## Verified numbers

Every figure below was produced by the widget in the browser **and** by an independent
Python implementation (GDAL for the raster, `heapq` for the search) that shares no code with
it. They agree to the displayed precision in every case.

**The four presets**, on the unedited map:

| Preset | Length | Route composition |
|---|---|---|
| Cheapest to build | 19.9 km | 56% farmland, 25% industry, 8% open land |
| Protect farmland | 26.3 km | 32% open land, 30% industry, 21% houses |
| Follow what is built | 28.1 km | 65% road and rail, 21% open land, 8% industry |
| Keep away from homes | 20.1 km | 50% farmland, 29% industry, 11% open land |

Tables, in the order farmland, houses, shops, industry, civic, parks, water, open, roads:

```
Cheapest to build      1  150  50  10  70  125  200  1  130     (also the opening state)
Protect farmland     120   60  20  10  40  125  200  1  130
Follow what is built  40  150  50  10  70  125  200  1    2
Keep away from homes  10  200  60   5  80  100  150  1   60
```

**Other checked cases**, all against Python:

```
farmland 120, rest at start        24.9 km   36% open land, 30% industry
roads 2, rest at start             23.2 km   59% farmland, 32% road and rail
houses 20, rest at start           19.7 km   57% farmland, 21% industry
accumulated cost, opening state    300320.8
```

**Near-tie band**, opening state:

```
within 0.1% of the optimum    1322 cells    13.2 km²
within 1%                     4198 cells    42.0 km²
within 5%                     7625 cells    76.3 km²   (Python prints 76.2; same 7625 cells,
                                                         the two languages round 76.25 apart)
```

**Grid bias.** The straight line between the two endpoints is 18032.5 m. The same line
measured eight-connected on this grid is 18119.1 m, an overstatement of **0.480%**. The
worst case, for a route running at 22.5° to the grid, is **8.239%**. This corridor runs
close to 45°, where the error is smallest — which is itself the point, since the error is a
property of the direction, not of the landscape.

**Timing**, measured in the page, not in a harness. A full flush — two Dijkstras over 41800
cells, a repaint of the whole canvas, and a DOM rebuild — settles at about 15 ms after the
JIT warms up; the first two calls are 22 to 43 ms. During a brush stroke the band solve is
skipped and the median frame is 16.7 ms, so painting holds 60 frames per second.

## Why the choices are what they are

**Log axis on the bars.** The route depends only on the ratios between the numbers, so a
doubling should move the bar the same distance whether it is 1 to 2 or 100 to 200. On a
linear axis everything under 20 collapses into a stub against a 200 bar and half the table
stops being editable by drag. The cost is one sentence of explanation, which the (i) carries.

Arrow keys step by a ratio of 1.15 rather than by 1, to match the axis. A consequence: not
every integer is reachable from the keyboard — from 1 the steps run 1, 2, 3 … 93, 107, 123,
so exactly 100 cannot be typed in. Dragging reaches any value. This is a deliberate trade and
it fits the widget's own argument that the exact number is not the interesting part.

**A value cap at the end of each bar.** Measured, every fill sits between 1.11:1 and 2.04:1
against the track, so on the pale classes the end of the bar — the only thing carrying the
value — was invisible. The cap is drawn in `--ink`, which is over 15:1, so the value reads at
full contrast whatever the hue is doing and the colour is left to carry identity alone.

**Road and rail priced high at the start.** In trial runs at 250 m that class carried half of
every route, because road allowances form a connected cheap network and real transmission
lines do follow them. Cheap by default, the opening state would teach "follow the roads"
before it taught anything about farmland against houses, and the other seven rows would look
inert. High by default, lowering it is a discovery: the route snaps onto Surrey's section-line
grid and runs 28.1 km in right angles.

**Farmland starts at 1.** This is the position the lab's own classification takes, and it is
what makes the opening route run 56% through the Serpentine and Nicomekl farmland. Defaults
are claims (principles §5), and this one is a claim the widget wants a student to argue with.
The (i) panel says where the numbers came from.

**"Keep away from homes" barely moves the line.** 20.1 km against 20.0. That is not a broken
preset, it is the best thing in the set: the cheapest route was already avoiding houses, so
a value stated loudly changes nothing. Whether an assertion has consequences depends on the
land, not on how strongly it is held. The preset (i) says so.

**Endpoints are fixed.** The disagreement this widget is about is over values, not over where
the line runs from. Holding everything else constant is principles §5.

**Drawing is a mode you arm.** The first widget refused to drag-paint on touch, because the
grid filled the screen and capturing drags would have taken away page scrolling. Here drawing
is half the point, so the trade is made — but explicitly. Nothing is armed on arrival, the
map takes no pointer events until a class is tapped, and a banner says drawing is on and how
to stop. The brush starts at 11 cells under `pointer: coarse`, because 5 cells is about 16 px
on a phone, well under a fingertip.

**Keyboard drawing exists.** Arrow keys move a cursor, shift moves it five at a time, space
draws. Without it the whole left half of the widget is unreachable without a pointer, and
principles §9 does not have an exception for the hard case.

**Colour is never the only cue for a route.** Every route has a white casing so one colour
reads over pale farmland and over dark industry alike; the live route is the thickest; each
kept route repeats its colour beside its name and its numbers; and pointing at a card brings
its route forward and fades the rest.

**Pin colours are split into a line colour and a label colour.** The map keeps its pale land
palette in dark mode, because inverting cartography for a page theme makes the land
unreadable — so on a dark page the line and the label need different values of the same hue
to both clear 4.5:1. Measured: on the light card the orange was at 4.23:1 and was darkened to
#b83800 for 5.24:1.

**Painting does not travel in the URL.** Costs, kept proposals and the toggles do. A kept
proposal carries its own route as a string of eight-direction characters, because it cannot
be recomputed once the land underneath it has been drawn over — about 200 characters per
proposal. Paint edits can run to thousands of cells and would make the link unusable, so they
are session-only.

## Known limits and open threads

**100 m cells are far too coarse for a power line corridor and far too fine to be free.**
The number on screen is a property of the grid as much as of the ground. The length (i)
says so for direction; nothing on screen yet says it for cell size. Letting the resolution
change would show it directly and would cost another data file per resolution.

**No topography.** The lab includes a DEM and, worked through, it changes the answer by
0.066% and does not move the entry cell at all — so leaving it out is defensible and is
recorded rather than hidden. But it means the widget cannot show that a surface raster makes
uphill and downhill cost the same, which is a real misconception the lab's own text creates.

**The route is a line with no width.** A corridor is tens of metres across and would take
land either side of the centreline. Nothing here represents that.

**Only ratios matter, and the widget does not say so on its face.** It is in the costs (i).
A student who never opens it may spend effort arguing about whether houses should be 150 or
200 while leaving everything else alone, which is an argument about a ratio, not a number.

**No demographic data.** The widget can say a route crosses 21% houses; it cannot say whose.
That is the distributive question and it is the one students will ask first. Adding census
data would answer it and would double the widget.

**Nothing on screen says whose land this is.** The corridor was chosen partly to keep clear
of a jurisdiction the method cannot represent, which is recorded above and makes the page's
silence about territory louder rather than quieter. Adding a line to the footer is the
obvious move and is close to the failure `principles.md` section 6 describes. Open question
there; not this file's to settle.

**Whether the framing lands.** The pin cards and the naming prompt are the whole argument
that a route is a proposal. Untested with students.

**Nine categorical colours is more than principles §9 wants.** The mitigations are that the
chart doubles as the legend, that the composition is given in words, and that pointing or
tapping names the class under the pointer. Not yet checked under a deuteranopia simulation.

## Picking it up again

Preview with the `widgets` configuration in `.claude/launch.json`, then open
`http://localhost:8791/least-cost/`.

To rebuild the grid: `python3 tools/lab4-extract.py > /tmp/grid.js`, then replace the
`var GRID = "..."` line in the first `<script>` block. The tool caches the download at
`/tmp/mv-landuse-window.geojson`; pass `--refetch` to go back to the service.

**Check these first after any change.** The four preset lengths — 19.9, 26.3, 28.1, 20.1 km
— and their compositions. Then the near-tie areas at the three tolerances. Then that keeping
a proposal records the route that matches the table beside it, which is the bug that was
hardest to see: `render()` batches into an animation frame, so `solved` can be one frame
behind the table, and `addPin` calls `flush()` for exactly that reason.

## Review record

```
Widget:   Least cost, whose cost?
Reviewed: 2026-08-21
```

**Pedagogical critique — pass, after two redesigns.** The destination moved twice. The first
plan routed to Roberts Bank; the causeway's shore end is inside Tsawwassen First Nation
lands, and there is no honest way for a cost surface to price a jurisdiction, so the
corridor moved rather than the question being fudged. The framing was going to be
"categories before numbers"; it became "many tables, many publics", which made keeping
proposals the spine of the widget rather than a convenience, and made the naming prompt
part of the argument instead of a label.

Four presets were added so that the failing case is one click away rather than something a
student has to stumble into. "Keep away from homes" is the failing case: it moves the line
by 0.2 km, because the cheapest route was already avoiding houses.

**Correctness — pass.** Every figure in "Verified numbers" was produced twice, once by the
widget in the browser and once by a Python implementation sharing no code with it, and they
agree to the displayed precision.

*The bug that would have passed the obvious test*: a heap that trusts the key it popped
rather than the current best distance. It gives correct answers on most inputs and silently
wrong ones where a cell is pushed several times, which is exactly the case a single spot
check does not produce. The implementation carries a settled flag instead, and the four
presets exercise routes of 157 to 262 cells over tables spanning a factor of 200.

*What the test caught*: keeping a proposal filed the current table against the previous
frame's route, because `render()` batches into an animation frame and `solved` was one frame
behind. Two pins in a row recorded identical statistics under visibly different tables. The
fix is `flush()`, called wherever a settled answer has to be read synchronously.

**Text — pass, with two claims corrected by the adversarial check.** Four citations went
out; two came back needing the *claim* changed rather than the citation. Goodchild compares
several move sets, so the eight-neighbour rule is an instance of his argument and not its
premise, and the panel now separates our grid from his general point. Sieber treats
"GIS broadens participation" as the field's contested question and reports at length the
objection that such software "lends the illusion of control over decision making when actual
control remains within the governing class" — so the widget now cites the argument rather
than one side of it, and says on screen that five proposals side by side can look like a
debate and change nothing about who signs. That paragraph is better than the one it
replaced.

**Accessibility — pass, after two fixes.**

Measured, every bar fill sat between 1.11:1 and 2.04:1 against its track, so on the pale
classes the end of the bar — the only thing carrying the value — was invisible. Each fill
now ends in a cap drawn in `--ink`, over 15:1.

The palette was searched rather than chosen. The first one had six pairs colliding under
simulated deuteranopia, including farmland against houses at a colour distance of 20 and a
lightness difference of 2 — the two largest classes on the map, half its area between them.
The replacement was found by scoring candidates under both deuteranopia and protanopia,
weighted by how much ground each class covers. One pair is still marginal under protanopia:
shops against roads, at colour distance 23 and lightness difference 8. Shops is 1.9% of the
map, roads are thin lines, and both are named when you point at or tap them.

Every text and control colour passes 4.5:1 against its actual background, checked in the
page. The route reads 4.41:1 against the darkest land colour and its white casing 4.28:1,
both above the 3:1 a graphical object needs. Thirty-six focusable elements in a sensible
order. At a 32 px root font — 200% — nothing overflows and nothing scrolls sideways.
Drawing works from the keyboard: arrows move a cursor, shift moves it five at a time, space
draws.

**Device and room — pass.** No horizontal overflow at 375 px, at 600 px, or at 1280 px.
Every control at least 24 px and every primary control 44 px under `pointer: coarse`. The
brush starts at 11 cells on a touch screen, because 5 cells is about 16 px there. During a
brush stroke the median frame is 16.7 ms.

**Outstanding:** the phone layout is a 2238 px scroll, which is long but has no better
answer while the map, nine bars and the kept proposals all have to be on one page. Not
checked on a real phone or on a projector yet — both are in the list above the sign-off.
