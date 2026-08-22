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

**Window:** 504000–526000 E, 5429322–5447500 N. 990 × 818 cells of 22²⁄₉ m, that size chosen so 990 cells is exactly the 22 km width. Entirely inside
Metro Vancouver, so there are no holes. An earlier plan ran to Roberts Bank; the causeway's
shore end sits inside Tsawwassen First Nation lands, and a cost surface that assigns treaty
land a friction number is making a category error. The corridor was moved rather than the
question fudged. This does not make the land it does cross uncontested.

**It was 855 rows deep until 2026-08-22, and this file used to claim it was "clear of every
reserve and treaty boundary in the region's own `Jurisdiction` field — checked, not
assumed". That claim was false**, and it carried the word "checked" while being wrong, which
is the worst way to be wrong. Querying the field says so in one line: the old window held 21
features whose `Jurisdiction` is `Indian Reserve - SEMIAHMOO`. The northern part of
Semiahmoo Indian Reserve sat in the bottom 37 rows — 2260 cells, 112 ha, rows 818–854 and
columns 511–618, the rest of the reserve running south past the window edge.

It was not found by re-reading the claim. It was found because a reader looked at the map
and did not believe the class name, which is the check that actually works.

No route and no alternative had ever run there. Measured over all four tables, at both the
old and the new price for class 8, at all three tolerances — 24 combinations — the number of
band cells falling on the reserve was **zero**, and so was the number of route cells; the
corridor turns east well north of it. That was luck, not design. What was not luck: 1621 of
those 2260 cells were class 8, which the widget called **"Open land" and priced at 1**, the
cheapest thing on the map, so the page was inviting a reader to route through it and would
have obliged.

**The window now stops at 818 rows**, with its southern edge at 5429322 N. The reserve's
northernmost point is 5429314 N and row 817's centre is 5429333 N, so no cell of it is left.
Renaming and repricing class 8 stops the page treating that land as free; moving the edge is
the part that matches the position this widget already took when it moved off Roberts Bank,
because the objection was never that the number was too low. It was that there should be no
number.

What the trim cost, measured before it was made and confirmed after:

- **No route figure moved at all.** All four preset costs, cell counts and lengths are
  bit-identical before and after, because the removed rows were never on any optimal path.
  361735.3709 over 790 cells is the same number in both grids.
- **One recorded figure moved**: the opening 5% band, 66.0 km² to **65.3 km²**. The 0.1% and
  1% bands are unchanged at 8.7 and 34.7 km².
- **4.3% of the map**, 36,630 cells, and the strip was 56% sea. Rows 800–819 are already
  half water, so the Boundary Bay shoreline that orients a reader is well inside the grid
  that remains.
- Class shares shifted with the sea removed: water 14.1% → 12.3%, houses 28.9% → 30.0%.

The trim is asserted in the suite, on the shipped file, because it lives as one number in
three places and a rebuild is exactly where it would come back.

**Endpoints.** The start is a real utility site at 124 St and 86 Ave in Surrey, cell
(row 109, col 231). Metro Vancouver's own data classifies that exact cell **T400, "Utility,
Communication and Work Yards"**, which is what the widget's wording rests on — checked
against the open dataset rather than inherited from the licensed one, and stated as a
utility site rather than as a named company's substation, because the open data does not
say whose it is. The plant is not real: it stands in for something that would be proposed
at Campbell Heights, cell (row 675, col 810), where the industrial district's expansion
into farmland is a live argument.

**Classes.** Twenty-nine Metro Vancouver codes grouped into eight, plus roads. The grouping
is ours and the widget says so. Shares of the window:

| Class | Codes | Share |
|---|---|---|
| Houses | S100, S110, S120, S130, S131, S135, S410, S230, S235 | 30.0% |
| Farmland | A500 | 22.3% |
| Parks and protected | R100, W400 | 13.2% |
| Water | R200 | 12.3% |
| Road and rail | S500, T100, T200, T300 | 11.8% |
| Industry | S300, M300, S600, T400 | 4.0% |
| Other | U100 | 3.2% |
| Shops and offices | S200, S202, S204 | 2.0% |
| Schools and civic | S400, S420, S450, S460 | 1.3% |

**"Other" was called "Open land" and that was a mistake in the grouping.** U100's own
description in the source is **"Undeveloped and Unclassified"**, and the service's layer
metadata carries a longer definition that the first version of this file never read:

> includes lands outside the provincial Agricultural Land Reserve with no visible
> development, vacant urban land, and forested or vegetated areas not identified as
> recreation, open space and protected natural areas or agriculture.

So it is not, as this file first said, the bin for ground the survey could not identify. It
is a positive finding — no visible development — plus everything vegetated that did not
qualify as park or as farm. The class is defined by what the land is **not**, which is why
no attribute splits it: `Description` is one-to-one with `LU_Code`, and the only other
fields are administrative geography.

Calling it "Open land" made a class defined by absence sound like a landscape, and the
opening table then priced that landscape at 1.

**Read the publisher's own long definitions before writing a class label.** Getting this
wrong produced a second error downstream: the first correction described "Other" as holding
"a gravel working". Gravel pits are **M300, "Industrial – Extractive"** — peat extraction,
gravel pits, landfill, quarries — which this very file groups under *Industry*. The example
was invented, and it contradicted our own grouping four lines further up.

It now reads **Other** and starts at **100** in the opening state and in all three presets.
A low number was the page asserting that land nobody has built on, and nobody has given a
name to, is land nobody minds losing. A high one is the opposite assertion. Both are
positions; neither is neutral, and the (i) panel says so.

Repricing it improved three things that had nothing to do with the reason for doing it.
"Protect farmland" now crosses **0.2% farmland** instead of detouring through unclassified
land, so the preset finally does what it is named for. "Follow what is built" reaches 98.5%
road and rail. And "keep away from homes" went back to being the widget's best teaching
case: it runs **20.5 km against the opening 20.9**, where at Other = 1 it had drifted to
23.2 km, quietly falsifying the sentence in its own (i) panel. The detours were all through
the class the page was giving away.

The colour is unchanged: `--c8` is a near-white, which is the right convention for
unclassified ground and was already searched against the rest of the palette. It does read as
cheap, which the number now contradicts. The chart doubles as the legend, so the number is
never far from the colour, but this is the one place in the palette where hue and value
disagree on purpose.

**Cells went 100 → 50 → 33⅓ → 22²⁄₉, every time for the same reason.** Blocks of housing
and farmland rasterise fine at any of these; everything linear does not. Road allowances,
rail and watercourses are narrower than 100 m, so at that size they came out as dotted lines
and a route could not follow one — which mattered, because "follow what is built" is one of
the three positions the widget offers. 50 m joined up the main grid, 33⅓ m most of the rural
lanes, and 22²⁄₉ m the rest.

809,820 cells, nineteen times the first attempt. The answer was never a coarser map; it was a
faster queue, then a worker, then sending the worker changes instead of the map.

**One cell needed filling.** At this size a cell centre can land in a sliver where two
source polygons fail to meet — one did, at row 268, col 478 in the 33⅓ m grid, deep inside
the window and ringed by shops, roads and civic land. `tools/lab4-extract.py` fills holes
like that from their neighbours and says how many it filled, and still refuses to build a
grid with more than one in ten thousand missing, because a genuine hole would be a
contiguous region rather than a scattering of single cells.

## How it computes

Eight-neighbour Dijkstra. Stepping between two cells costs the mean of their two values
times the distance between their centres — 22²⁄₉ m orthogonally, 22²⁄₉√2 m diagonally — which is
what ArcGIS's Distance Accumulation does with a cost raster, and what the lab's numbers
assume.

The similar proposals run the same solve twice, outward from the substation and outward from
the plant, and add the surfaces. Each cell then holds the cost of the cheapest route that
passes through it; cells within the tolerance of the optimum are the band. This is Pinto and
Keitt's Conditional Minimum Transit Cost. Because both solves keep their back-pointers, any
band cell also *names* a route — the cheapest way in, then the cheapest way out — so drawing
an alternative costs nothing beyond a trace.

**Choosing which alternatives to draw took two attempts, and the first was wrong.** Taking
the six band cells furthest from the best route gave six versions of the same bulge, because
the band is much wider in one place than anywhere else and every pick landed there; rendered
at full size they hugged the answer and taught nothing. The second attempt spreads outward
from the best route carrying *which point of it* each cell is nearest to, then takes one
alternative per sixth of the journey. Each one then departs at a different stage.

A wrong turn worth recording: the first version of that staged the journey by accumulated
*cost*, `accA / accA[DST]`. That fails badly here. Cost accumulates fast through the
expensive industrial edge near the plant, so nine tenths of the cost is spent on a short
stretch and the entire wide part of the band falls into the last tenth. Measured by tenths
of cost, the furthest cell from the route ran 4, 5, 1, 1, 0, 0, 0, 0, 0 and then 24. Stage by
position along the route, not by cost spent.

A candidate is rejected if more than 85% of its cells are already covered by something drawn,
and the next candidate in that stage is tried. Without that, two routes at the 5% setting
overlapped by 99% and drew as one line.

**The whole solver runs in a worker**, built from a Blob at load out of a function that
closes over nothing, so the widget stays one file. The main thread keeps the land, the
numbers and the drawing, and never solves; it sends a cost table and, when the land has
changed, a copy of it, and gets back a route and optionally a band. Moving it was the only
way to keep a brush stroke at 60 frames a second once a solve reached 35 ms, which is two
frames. The rule is `principles.md` section 4 and it took three resolutions to actually
need it.

The move had to change no answers, and the suite is what says it did not: 194 assertions,
every recorded number identical before and after.

**The queue is Dial's buckets, not a binary heap**, which is where the speed came from when
the grid first got finer. Each cell is filed in the bucket for its distance and the
buckets are emptied in order, so a push and a pop are constant-time array operations rather
than O(log n). Measured over 167,200 cells at the time: 28.9 ms with the heap, 13.5 ms with buckets.

Buckets are exact only while a bucket is no wider than the smallest possible step, which
here is one cell of the cheapest land to the next: `VMIN × CELL`, and `VMIN` is 1, so one
bucket per cell width is safe whatever a reader sets. Checked rather than assumed — against the heap, over five
tables including all-equal and alternating extremes, all 167,200 accumulated costs came out
identical. At twice that width, 42,528 cells disagreed.

A settled flag rather than a decrease-key. A cell can be queued more than once; the flag is
what stops it being expanded twice, and reading the key off the queue entry instead would
use a stale distance.

## Verified numbers

Every figure below was produced by the widget in the browser **and** by an independent
Python implementation (GDAL for the raster, `heapq` for the search) that shares no code with
it. They agree to the displayed precision in every case.

**The opening state and the three presets**, on the unedited map:

| Numbers | Length | Route composition |
|---|---|---|
| The opening state | 20.9 km | 62% farmland, 26% industry, 4% road and rail |
| Protect farmland | 22.1 km | 64% road and rail, 33% industry, 2% shops and offices |
| Follow what is built | 23.2 km | 99% road and rail, 1% industry, 0% other |
| Keep away from homes | 20.5 km | 57% farmland, 27% industry, 13% road and rail |

Tables, in the order farmland, houses, shops, industry, civic, parks, water, other, roads:

```
The opening state      1  150  50  10  70  125  200  100  130
Protect farmland     120   60  20  10  40  125  200  100   20
Follow what is built  40  150  50  10  70  125  200  100    2
Keep away from homes  10  200  60   5  80  100  150  100   60
```

Full compositions, since the widget only prints the top three:

```
The opening state      farmland 61.5  industry 25.6  road+rail  3.9  shops 3.0  houses 2.4  parks 2.2  other 0.8  civic 0.6
Protect farmland       road+rail 64.0  industry 32.7  shops 2.4  other 0.5  farmland 0.2  water 0.1
Follow what is built   road+rail 98.5  industry  0.8  other 0.4  farmland 0.2
Keep away from homes   farmland 57.3  industry 27.3  road+rail 13.3  shops 1.6  other 0.4
```

**"Protect farmland" prices road and rail at 20, not 130, and that was a correction.** A
group trying to keep fields whole has no reason to avoid ground that is already a corridor
and every reason to prefer it, so pricing corridors high was incoherent as a position. The
number is a balance rather than a preference: pushing it lower stops the route being about
farmland at all and turns it into "follow what is built". Measured overlap between the two
routes as that number falls — 130: 1%, 60: 4%, 40: 6%, 20: **12%**, 10: 60%, 5: 79%. The
collapse is sudden and it sits between 20 and 10. There is a test guarding the gap.

(Those overlaps were re-measured after "Other" was repriced; at Other = 1 the same sweep ran
2%, 3%, 31%, 34%, 76%, 92%. The shape is the same and the cliff is in the same place.)

The opening state used to be a fourth preset called "Cheapest to build" and is not one any
more. Nothing here is a construction cost and no land prices were looked up, so a button
offering the cheapest build claimed something the widget cannot support. "Numbers back to the
start" restores those numbers without naming them as a position anybody holds.

**Accumulated cost at the plant, opening state: 361735.3709**, over a 790-cell route
measuring 20.884 km. That figure is the anchor and a rebuild should reproduce it first. A
Python implementation sharing no code with the widget agrees on all three to every printed
digit, and re-costing the widget's *drawn* polyline in Python gives 361735.3709 as well.

**The two agree on every number and disagree about 45% of the ground.** Python uses a binary
heap, the widget uses Dial's buckets. Same cost to four decimals, same 790 cells, same
20.884 km — and only 434 of those 790 cells are the same cells. They even report the same
composition, 62% farmland, 26% industry, 4% road and rail, which is the sharpest form this
result has taken yet: two routes over different ground, scoring identically and *summarising*
identically. Read cost, length and composition as claims about the world here, and the choice
of cells as a property of the queue.

**Similar proposals**, opening state. The band areas:

```
within 0.1% of the optimum     8.7 km²    3 routes drawn, longest 21.2 km   (+2%)
within 1%                     34.7 km²    6 routes drawn, longest 24.5 km   (+17%)
within 5%                     65.3 km²    6 routes drawn, longest 32.2 km   (+54%)
```

The "+" figures are how much further the longest alternative runs **on the ground** for that
much more cost. At 5% a reader can see a route 54% longer that the numbers score within a
twentieth of the answer.

**How little the tightest setting has to overlap.** Of the three alternatives at 0.1%, the
least overlapping shares **46%** of its cells with the heavy line; at 1% it is 27% and at 5%
26%. The page used to say "barely a third" of a length at 0.1%, which was true of an earlier
table and is not true of this one. It now says the route "runs over different ground for more
than half its way", and there is a test asserting that, because a sentence which is a
measurement should fail when the measurement changes rather than sit there being wrong.

Note which unit the page uses. These are shares of **cells**, not of length, and the two are
not the same on an eight-connected grid where a diagonal step is 1.41 times an orthogonal
one. The page says "way" rather than "length" for that reason.

**Swapping the queue moved half the route at identical cost, and that is the widget's own
thesis arriving uninvited.** Heap and buckets both give accumulated cost 361735.3709 at the
plant — a difference of exactly zero — and both give a 790-cell route of 20.884 km. The two
routes share 434 of those 790 cells. **55%.** An implementation detail with nothing
geographic in it decides 45% of where the line goes, because the two are tied. This is on
the page now, in the similar-proposals panel.

(Measured again on the current grid and the current table. The figure in this file used to
be 49% of a 386-cell route at cost 342042.506987, which was measured on a coarser grid two
resolutions ago and had been carried forward as though it were current. The effect is
unchanged; the numbers were not.)

It also means the composition figures in this file are the most fragile thing in it, and
deliberately so: the test suite asserts them exactly, so anything that moves the line has to
come and re-record them.

**These were checked as drawings, not as numbers.** The polylines were read back out of the
rendered SVG; the land classes were read back off the painted canvas by matching pixels to
the palette and to the palette faded by 0.62; the nine values were read off the controls'
`aria-valuenow`. Every route was then re-costed from those three. At all three tolerances:
every step is an eight-neighbour move, every route runs cell (109,231) to cell (675,810),
every route lies wholly inside the shaded band, and every route is inside the selected
tolerance.

The suite asserts this at all three tolerances, on the unedited map and again after four
brush strokes and five changed values. The check is in `tools/test/least-cost.test.js`; it
runs in CI and nothing publishes without it.

**Grid bias.** The straight line between the two endpoints is 18032.5 m. The same line
measured eight-connected on this grid is 18119.1 m, an overstatement of **0.480%**. The
worst case, for a route running at 22.5° to the grid, is **8.239%**. This corridor runs
close to 45°, where the error is smallest — which is itself the point, since the error is a
property of the direction, not of the landscape.

**Timing**, measured in the page, not in a harness. During a brush stroke over 809,820
cells: median frame 16.7 ms, 99th percentile 20.4, longest 21.6, **zero frames over 25 ms in
120**. A flat 60 frames a second for the whole stroke. (Re-measured after the trim; at
846,450 cells it was median 16.7, 99th 19.7, zero over 25 in 96.) Turning the similar
proposals on, with nothing cached, takes about 230 ms,
which is off the main thread but long enough that the readout says "Working out the
others…" rather than sitting silent.

Five things got it there, in the order they mattered.

**The queue**, binary heap to Dial's buckets, better than 2× and exact.

**Painting was separated from solving.** Repainting the land is about a millisecond and
solving is thirty-five, so the land follows the brush on every frame regardless.

**The band caches against a model version.** Keeping a proposal changes nothing about the
model and was paying for two solves anyway; that alone took it from 180 ms to 19.

**Then the worker**, once a solve reached two frames and no amount of scheduling on one
thread would hide it. Before the worker, at this resolution, 12 frames in 83 ran over 25 ms
and a stroke averaged 52 fps. After it, none do.

**And then sending the worker changes rather than the map.** A brush stroke alters a few
hundred cells; copying all 809,820 into every message was the last thing on the main thread
big enough to cost a frame, and it cost four in 91. The widget keeps a list of changed cells
and sends that instead, falling back to the whole map when the list gets long or the map is
reset. Zero slow frames after.

The cost of the worker is that nothing is synchronous any more. `whenSettled` replaced
`flush`, and keeping a proposal now waits — usually for nothing, because the answer is
already in — for a route that matches the numbers beside it rather than the previous ones.
The first frame paints the land with the length still blank, which is better than a blank
page and is noted in `drawReadout`.

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
inert. High by default, lowering it is a discovery: at 130 the route puts 3.9% of itself on
road and rail, and at 1 it puts **57.6%**, running 19.7 km instead of 20.9.

This paragraph used to say the route "snaps onto Surrey's section-line grid and runs 28.1 km
in right angles". Re-measured on the current grid, both halves are wrong and the second is
backwards: the length is 19.7 km, and lowering the number makes the route *less* orthogonal,
not more — 53.9% of its steps are orthogonal at 130 and 32.2% at 1. It follows the corridors,
and this corridor's corridors run diagonally. Another measurement carried forward from a
coarser grid without being taken again.

**Farmland starts at 1.** This is the position the lab's own classification takes, and it is
what makes the opening route run 61.5% through the Serpentine and Nicomekl farmland. Defaults
are claims (principles §5), and this one is a claim the widget wants a student to argue with.
The (i) panel says where the numbers came from.

**"Keep away from homes" hardly changes the answer.** 20.5 km against 20.9. That is not a
broken preset, it is the best thing in the set: the cheapest route was already avoiding
houses, so a value stated loudly changes almost nothing. Whether an assertion has consequences depends on the land, not on how strongly it
is held. The preset (i) says so.

This is also the claim that went stale without anyone noticing. It was recorded as "20.1 km
against 20.0" from a coarser grid; by the time the grid reached 22²⁄₉ m the preset was
running 23.2 km against 20.9, so the sentence in the (i) panel was simply false, and had been
through two resolutions. Pricing "Other" properly is what brought it back, because the detour
it had been taking ran through unclassified land the page was giving away at 1. Text that states a measurement needs a test, or it needs re-reading
every time the measurement moves; this one now has a test.

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

**One kind of land is marked on arrival, and nothing is armed.** Drawing is the half of the
widget nobody would find on their own — a chart of numbers does not look like a palette. A
line above the rows says so, and the parks row carries a dashed outline and the word "draw"
until the first time anything is armed. It is marked, not armed: arming on load would make
the map swallow pointer events before anyone asked, which on a phone means the page stops
scrolling. Parks because "what if this were protected?" is the move a reader is most likely
to want, and because a park drawn across the corridor moves the route visibly.

**Keeping a proposal and looking at the alternatives are separated by a rule.** Sitting in
one row they read as four equal buttons, when one is an act on this route and the others
change what you are looking at.

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

**The page does not say what used to be in the "Other" class.** It gives the source's own
definition of U100 and says the class is named for what the land is not; it does not say
that until this week the class included part of a reserve. That is deliberate. Naming a First
Nation on a page that prices land is the question section 6 leaves open, and it should not
get answered by accident inside a class label. The window no longer contains the reserve, so
the page is not being silent about something it is currently doing — but it is silent about
territory in general, which is the open question one paragraph up.

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

**Check these first after any change.** The opening length and the three preset lengths —
20.9, 22.1, 23.2, 20.5 km — and their compositions. Then the similar-proposal band areas and
route lengths at the three tolerances, re-costed off the drawing rather than off the model.
Then that keeping a proposal records the route matching the table beside it, which is the bug
that was hardest to see: `render()` batches into an animation frame, so `solved` can be one
frame behind the table, and `addPin` calls `flush()` for exactly that reason.

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

Three presets were added so that the failing case is one click away rather than something a
student has to stumble into. "Keep away from homes" is the failing case: it changes the
answer by 0.4 km, because the cheapest route was already avoiding houses.

**Correctness — pass.** Every figure in "Verified numbers" was produced twice, once by the
widget in the browser and once by a Python implementation sharing no code with it, and they
agree to the displayed precision.

**Classification — fail, then fixed, 2026-08-22.** Class 8 was labelled "Open land" and
priced at 1. The source calls it "Undeveloped and Unclassified" and defines it by what the
land is not — no visible development, vacant urban land, vegetation that is neither park nor
farm — so the label turned a category of absence into a landscape, and the price then made
that landscape the cheapest ground on the map. 1621 of the class's cells were on Semiahmoo Indian
Reserve. Three things changed: the class is "Other" at 100 in every table; the window was
trimmed from 855 rows to 818 so it holds no reserve cell at all; and this file's claim that
the window was clear of every reserve — which carried the word "checked" — has been
corrected. No route or alternative had ever crossed those cells, at any tolerance under any
preset, which is luck rather than design. The trim moved no route figure and one band figure.

**Text — two claims corrected by the adversarial check, 2026-08-22.** The check refuted the
framing of the "Other" class (see the classes section: the source defines U100 positively,
and the "gravel working" example belongs to a code we file under Industry), and refuted the
figure in the "keep away from homes" panel — see below. It also caught the page saying a tie
cost "a thousandth of one per cent" more when the measured excess is 0.0967%, a hundredfold
overstatement that had been on the page since the panel was written.

**A measurement compared across two implementations, 2026-08-22 — the worst thing found in
this pass, and it was mine.** The "keep away from homes" panel was given the sentence "about
two thirds of the route runs over the same ground as the numbers you started with". The
figure, 63.3%, was measured Python-route against Python-route. On the widget the same overlap
is **31.7%** — because the widget's *opening* route shares only 54.9% of its cells with
Python's. So the number described a pair of routes no student ever sees.

Two rules were broken at once, both written down in this very file. Cell overlap between tied
routes is the quantity recorded three sections up as a property of the queue rather than of
the land, and it was then asserted to students as a fact about land. And a figure produced by
the reference implementation was printed as a figure about the widget. The panel now quotes
length, which both implementations agree on to the metre, and a test asserts that the two
lengths in the panel are the two lengths the widget produces.

**Stale text — three found, 2026-08-22.** The 0.1% tie was described as "barely a third" of a
length when the measurement had moved to 46%; the "keep away from homes" (i) said the preset
barely moved the line when it was running 2.3 km longer over different ground; the
alternatives (i) promised "six more routes" where the tightest setting draws three. All three
were measurements written as prose and left behind by later changes to the grid and the
table. Each is now either a test or a hedge that stays true.

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
