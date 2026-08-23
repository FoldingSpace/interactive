# Vancouver, measured in minutes

**Live:** https://foldingspace.github.io/interactive/relative-distance/
**Code:** `web/relative-distance/index.html` and `data.js`
**Data:** `tools/relative-distance-extract.py`
**Check:** `tools/relative-distance-verify.py`
**Tests:** `tools/test/relative-distance.test.js`

Started 2026-08-22. Built from row 3 of the widget build queue in the GEOS 370 course
audit, which asked for a relative-distance map after O'Sullivan's Figure 6.14.

## The one thing it teaches

How far away a place is depends on who is going and which end they start from, so a map
of distance is a map of one person's trip rather than a fact about the ground.

## What is on the screen

A street network for Vancouver and the North Shore, a start, and two pins. Press
**Minutes** and every street slides along the line running out from the start, to a
distance set by how long the trip takes. Direction never changes; only distance does.

Four travellers: on foot, on foot avoiding steep ground and steps, by bike, by car. Four
starting points as buttons, or tap anywhere on the map. A button swaps the start with the
blue pin, which is the test that matters: if getting there and getting back took the same
time the two maps would be the same map, and they are not.

Two sets of rings, in kilometres and in minutes, each always meaning what it says and
cross-fading as the map moves between them.

## Verified numbers

Every figure below was produced twice: once by the widget in a browser, once by
`tools/relative-distance-verify.py`, which reads the shipped `data.js` and rebuilds the
speed models and the routing from the written description in
`tools/relative-distance-extract.py`, sharing no code with either the widget or the
extractor. The two agreed to six decimal places on every value.

Data, as shipped 2026-08-22:

| | |
|---|---|
| Window | 49.25–49.36 N, 123.22–123.00 W |
| Ways in the window | 61,441 |
| Dropped as separately mapped sidewalks and crossings | 25,043 |
| Routable ways after every filter | 24,635 |
| Junctions before pruning / after | 31,919 / **24,410** |
| Street segments before pruning / after | 38,503 / **32,250** |
| Shape points between junctions | 7,557 |
| Junctions off the LiDAR mosaic, on CDEM instead | 94 |
| Coordinate origin, UTM zone 10N | 483000 E, 5453100 N, 2 m per unit |
| `data.js` | 916,878 bytes, 234,262 gzipped |
| `basemap.jpg` | 166,877 bytes, 1150 x 1131, 16 m |
| Mesh over the photograph | 92 x 91 cells, 200 m |
| Mesh cells with no travel time behind them | about 54% on foot, 84% avoiding steep ground |
| Whole frame, fine mesh | 10–14 ms |

**Checked against independent routers.** Valhalla's pedestrian profile walks Waterfront to
Lonsdale Quay in 130.2 minutes over 10.74 km, against this widget's 132.16 minutes over
11.04 km — 1.5% apart, and both cross Lions Gate on land. That the widget comes out
slightly *slower* is worth noting: the free-flow assumption should make it faster, and
Tobler's hill penalty on the causeway climb cancels it. By car, Valhalla gives 17.87
minutes and OSRM 16.8 against this widget's 12.05, which is the right direction and about
the right size for posted limits with no signals and no queues. Public OSRM's foot profile
returns 17.6 minutes because it routes over the SeaBus, which is not a comparison.

Travel times from Waterfront Station, in minutes. "Back" is the same trip in reverse.

| Traveller | Lonsdale Quay there / back | Commercial & Hastings there / back |
|---|---|---|
| On foot | 132.158528 / 129.498085 | 37.667 / 38.049 |
| On foot, avoiding steep ground | unreachable | 37.667 / 38.049 |
| By bike | 33.643006 / 31.495512 | 9.264 / 9.207 |
| By car | 12.051 / 12.441 | 3.847 / 3.928 |

Straight-line distances: Lonsdale Quay 3.47 km, Commercial & Hastings 3.06 km. That pair
is the widget's opening case and the whole argument: 13% apart on the ground, four times
apart on foot.

The steepest asymmetry in the default set is by bike up to Upper Lonsdale — **43.125902
minutes out, 33.023574 back**. That is the climb, and it is a climb rather than a detour,
which took a correction to be true of: see below.

How much of the city each traveller can use, and how much of that they can reach from
Waterfront Station:

| Traveller | Junctions usable | Reachable | Out of reach |
|---|---|---|---|
| On foot | 22,828 | 22,337 | 2% |
| On foot, avoiding steep ground | 19,401 | 7,407 | **62%** |
| By bike | 18,935 | 18,213 | 4% |
| By car | 12,738 | 12,654 | 1% |

Slopes, measured on the shipped graph. Roads only, excluding bridges and tunnels, 16,099
segments across the window: median 2.1%, ninetieth percentile 7.3%, and **20.8% of road
segments are steeper than 5%**.

**These numbers move if the coordinate anchor moves.** They depend on which junction is
nearest to each named place and on which junctions fall within 150 m of it, and those are
computed from quantised coordinates. An early rebuild shifted the origin by one metre and
walked Park Royal from 83.19 to 85.08 minutes, because the pin snapped to a different
junction in a car park. The origin is now anchored to a round 100 m for exactly this
reason — see the note in `pack()`. If these figures shift on a rebuild, check the anchor
before suspecting the model.

## Why the choices are what they are

### The city, and why it can be this one

Burrard Inlet. Lonsdale Quay is three and a half kilometres from Waterfront Station and
two hours and twelve minutes away on foot. Nothing else in the region makes the point so
plainly, and it is the students' own city.

Nothing here can serve as an answer key, and that was checked rather than assumed, twice:
no GEOG 370 lab asks for anything on a network. Lab 1 is linguistic diversity, Lab 2 is
terrain and multi-criteria evaluation in the Okanagan, Lab 3 is the modifiable areal unit
problem, Lab 4 is least-cost paths — which is cost distance over a raster of land-use
frictions, not a network. See `principles.md` section 15; this is the first widget here
that is not built beside an assessment at all.

The one place to keep an eye on: Lab 4's third question asks students to compare a
straight-line distance with a least-cost path distance, which is conceptually the move
this widget makes. Different city, different data model, no time in it, and nothing the
widget produces goes anywhere near the answer — but it is the nearest thing to an overlap
and it is worth knowing about rather than being surprised by.

### The deformation, and what it cannot say

Each place is drawn in its true direction from the start, at a distance set by its travel
time. That is O'Sullivan's Figure 6.14 construction: the network redrawn from a central
location. It is exact, it is fast enough to animate, and moving the start redraws
everything, which is what makes the asymmetry visible rather than merely reported.

The cost is severe and it is stated on the page. **The map is true along the lines
running out from the start and nowhere else.** The gap between two places that are not
the start is not their travel time, and nothing in this construction can show it. That is
the trade a map projection makes, and saying so is better teaching than hiding it.

Multidimensional scaling on the full matrix of pairwise travel times was the alternative.
It would make distances readable everywhere on the map rather than only along the rays.
It was not built, for three reasons. All-pairs shortest paths over 24,410 junctions is not
a thing to do in a browser while someone waits. The result would have no single origin, so
the swap that demonstrates asymmetry would have nothing to swap. And classical MDS takes a
symmetric matrix, so the asymmetry — the thing this widget exists to show — would have to
be averaged away before the standard algorithm could run. There are asymmetric MDS models
that would not require that; they are a real literature and a much larger build than this
one, and they would still cost the single origin.

### The scale, and why the map stays the same size

The time map is scaled so that the median drawn radius matches the median radius of the
metre map. If it were not, walking would produce a map four times the size of the driving
one and the frame would have to zoom, so the *shape* change — which is the lesson — would
be lost inside a size change. What carries the magnitude instead is the ring labels and
the table: the same map, drawn at 30-minute rings for a walker and 5-minute rings for a
driver.

The frame is fitted to the union of both the metre and the minute extent, so it does not
move while the transition runs. That costs a little empty margin at the metre end and it
is worth it.

### Two states and no dial

This was a slider from metres to minutes for its first hour. Luke asked what a value in
the middle was supposed to mean, and the honest answer is nothing: half a distance added
to half a scaled time is not a way of measuring anything. The two buttons sitting under
the slider, both at the ends, were the design already admitting it.

What the slider was really buying was the movement — watching Lonsdale Quay travel
outward past Commercial Drive is how a reader does the comparison, and a cut between two
still maps makes them do it from memory instead. So the movement stayed and the dial
went: two states, animated between, with `prefers-reduced-motion` snapping straight
across.

**The state changes at the start of the animation, not at the end.** That is not a
preference. Animation frames do not always arrive — a page in a background tab gets none
at all — and the first version wrote the settled state in the last frame, so the widget
sat half way between its two maps with a readout describing neither. Found by pressing a
button in a browser pane that reports itself hidden. A timer now snaps the drawing into
place if the frames never come, and a test asserts that everything readable is right
before any frame has run.

### The travellers

A traveller is a speed and a set of permissions, and the two are deliberately kept apart.
Someone on foot and someone on foot avoiding steep ground move at **exactly the same
speed**; only what they will use differs. So whatever changes between those two maps is
the ground refusing rather than the walker slowing down. This is `principles.md` section
5: hold constant everything that is not the lesson.

*On foot* uses Tobler's hiking function, W = 6 exp(−3.5 |S + 0.05|) km/h with S the rise
over the run, giving 5 km/h on the level and a maximum on a slight downhill. Steps are a
flat 1.5 km/h, which is a stated assumption and not from anywhere.

*Avoiding steep ground* refuses steps and anything over 5 in 100. That threshold is where
an accessible route stops being a walking surface and has to be built as a ramp. The page
said "the slope an accessible route is built to" until the citation check refused it: 5%
is a ceiling, not a target, and a ramp may reach 1:12.

*By bike* solves the cycling power equation for speed: 150 watts, 90 kg of rider and bike,
rolling resistance 0.005, drag area 0.40 m², air at 1.226 kg/m³, capped at 22 km/h and
floored at walking speed. The cap is the rider's own choice rather than physics, and it
means that on the flat the speed is chosen while on a hill it is calculated — which is
about right, and is said in the panel. A grade lookup table of 701 entries stands in for
the bisection at run time.

*By car* uses the posted speed limit from OpenStreetMap's `maxspeed`, or a default by
road class, and respects one-way streets.

Walking ignores one-way. Both pedestrian crossings of Burrard Inlet are tagged as one-way
cycleways carrying `foot=designated`, because the roadway itself is `foot=no` or a
motorway, and `oneway` on those ways means the bike direction.

This file said, until the second adversarial round measured it, that treating `oneway` as
binding on foot would lose Vancouver its bridges for walkers. **That was a story, not a
finding.** Each bridge is mapped as a *pair* of one-way ways, so a walker obeying `oneway`
just uses the correctly directed side. Measured on the shipped graph: nothing becomes
unreachable in either direction, the northbound times do not move at all, and the largest
southbound cost is Park Royal to Stanley Park going from 40.8 to 52.7 minutes. The rule is
still right, because a pedestrian is not bound by a one-way street. It is not right for
the reason I gave, and I had not run the counterfactual before writing it down.

### The correction that verification could not have found

The bike map was wrong, and both implementations agreed it was right.

OpenStreetMap maps the Lions Gate crossing, and the Stanley Park Causeway approach to it,
as a pair of one-way cycleways, one for each side. Taken literally that sends a cyclist
heading north the long way round, and the widget reported **Park Royal at 57.7 minutes out
against 20.0 back** — a thirty-eight minute asymmetry that this file confidently explained
as the causeway climb. It was a detour. Corrected, it is 22.2 out and 20.0 back.

Luke, who cycles the city, said the bridge takes bikes both ways.

**The number had been verified.** `relative-distance-verify.py` reproduced 57.788652 to
six decimals, because it reads the same `data.js`. Checking by recomputation tests the
arithmetic and cannot see a wrong input, and this is the plainest instance of that in the
repository: two implementations, perfect agreement, wrong about the world. What caught it
was somebody who has ridden the bridge.

The rule that replaced it is narrow and general at the same time: **a path that pedestrians
are designated to use is a shared footway, and the direction written on it is a
recommendation rather than a restriction.** In this window there are 984 one-way cycleways.
It frees 42 — the bridge and causeway sidewalks — and leaves 942 alone, those being
contraflow bike lanes on real streets like the Burrard Street Cycleway and the 10th Avenue
Bikeway, which are genuinely one-way. The Stanley Park Seawall bike path also stays
one-way, correctly, because it is tagged `foot=no`: it is cycle-only and it really does
run one direction.

### Free-flow, which is the missing control

The build queue asked for a departure-hour control. There is none, and the reason is a
licence rather than an oversight. No openly licensed record of Vancouver traffic by time
of day exists, and inventing a congestion model would put a fabricated claim on a page
whose entire subject is that the assumptions make the map.

What is there instead is consistency: every traveller moves as though the way were clear.
Posted limits with no traffic, cycling with no stop signs, walking with no crossings.
Held constant across all four, so comparisons between them stay honest, and stated on the
page in the traveller panel. Nobody's trip is this fast; what the map shows is how the
ground and the network shape a trip, not how long it takes.

### A trip ends within 150 m

Time to a pin is time to any junction within 150 m of it — you park, or you walk the last
bit. Without this rule a pin dropped in a park is unreachable by car, which is true and
useless. With it, "cannot get there" means something: the whole North Shore is genuinely
out of reach for the traveller avoiding steep ground, and Jericho Beach is genuinely not
somewhere you can drive.

A marked place is *drawn* at the radius of the time that is *reported* for it, not at the
time of its own junction. The two disagree by a little, and if the drawing used one while
the table used the other, a reader measuring a pin against the rings would get a different
answer from the one printed beside the map.

### The photograph, and where it stops

Luke asked for the satellite image to be warped along with the streets. It is, and the
interesting part is where it refuses.

The image is Sentinel-2, two tiles from the same satellite on the same cloud-free day so
there is no seam of date or sensor across the window, at 10 m, already in UTM zone 10N so
nothing is reprojected. A regular mesh of 92 by 91 cells is laid over it; each mesh node
takes the same treatment as a street — moved out along its own line from the start, to a
distance set by travel time — and each cell is drawn as one affine patch clipped to its
true deformed quad.

**The travel time at a mesh node is an inverse-distance mean of the reachable junctions
within 260 m. Where there are none, the cell is held where it is and faded out rather
than stretched.** This is the whole reason the feature is defensible. The network has a
travel time at every point *on it*; the ground between streets does not, and Burrard
Inlet certainly does not. Interpolating a time across the water and letting it stretch
like everything else would say the sea is merely slow. It is not slow. It is not there.
About 54% of the mesh is held on foot, 84% for the traveller avoiding steep ground.

Two things had to be fixed before it looked like anything.

*Seams.* Two clipped quads sharing an edge are each antialiased against it, and two
half-covered edges do not add back up to one, so a pale grid ran across the whole
photograph. Each corner is now pushed 0.6 px out from its own cell's centre before
clipping, so neighbours overlap.

*Spikes.* A cell whose four corners have very different travel times is lying across a
tear — one corner a minute from the start, the next half an hour, because the way between
them goes the long way round. A quadrilateral cannot draw that, and letting it try
produced long shards reaching across the map that read as a broken renderer. A cell that
would be stretched to more than six times its own width is now held as well. On foot that
costs 20 cells out of 8,372.

**And the cost that is not a bug.** Measured against the shipped image, the plain
palette's pale path colour sits at **1.6:1** over the darkest land in the photograph,
under the 3:1 a drawn line needs, and lightening the image far enough to fix it leaves no
photograph. So turning the ground on switches the streets to a darker set: **5.16, 4.03
and 3.09** to one against that same darkest land.

The strength of the photograph and the darkness of the streets are one negotiation, and
both ends of it were measured. Washed harder, the streets are comfortable and the ground
is a rumour; washed less, the ground reads and the paths stop being lines. What ships is
the strongest photograph the palette can carry — land at a fifth-percentile relative
luminance of 0.318 — with the paths thinned from 0.6 px to 0.40 and darkened rather than
paled, because paling is what breaks the standard and a thin dark line recedes perfectly
well anyway. The three clear steps of lightness compress to two and a bit, and width takes
up the slack. That is a real loss, and it is why the photograph can be turned off, which
is also the right answer on a projector, where dark tones crush.

### Colour and drawing

The map keeps a light palette in both page themes, because pale ground under dark streets
survives a projector and inverting cartography for dark mode does not. Three street
weights: major, minor, path. The two pins differ in hue *and* shape — a filled circle and
a filled square — and an unreachable pin is hollow with a dashed edge and a caption saying
so, never a silent gap.

Labels are placed in priority order, the start and the pins first, and anything that would
collide is dropped. The first version drew all twelve at once and at the minutes end they
piled into an unreadable knot at the centre, because everything close in time collapses
there.

## What the correctness pass found

**The bug that would have passed every test I had run.** The slope threshold was compared
against a `Float32Array`. A grade stored as exactly 50 per mille comes back from float32
as 0.050000001, so `> 0.05` was true and 93 street segments at exactly five in a hundred
were excluded from the traveller defined by that threshold. Every recorded travel time was
still correct, so reproducing known values would never have caught it. What caught it was
running the independent Python check and finding the *counts* disagreed — 7,433 against
7,360 reachable — while every time matched.

The fix keeps the integer per mille in an `Int16Array` and compares integers, so the
boundary cannot round at all, and the arrays that feed the arithmetic are `Float64Array`
so the widget and the checker agree bit for bit. There is now a test that finds a real
segment at 50 and one at 51 and asserts the first is allowed and the second is not.

**The rebuild was not reproducible.** The coordinate origin was `floor(min)`, and two runs
over identical input put the southernmost junction either side of a whole metre — a
sub-millimetre wobble in the projection, which `floor` turned into a one-metre shift and
so into a different delta for half the nodes in the file. The origin is now anchored to a
round 100 m. Two consecutive runs now produce byte-identical output.

**Three gaps in the shared test stub**, each fixed there rather than worked around:
`removeChild`, `insertBefore` and `cancelAnimationFrame` were missing, and the canvas
context could not record a stroked path. It records them now, which is what lets the test
"the drawing separates two places the ground does not" read the picture instead of the
model.

## Known limits and open threads

**No transit, and it is the biggest thing missing.** The SeaBus crosses Burrard Inlet in
about twelve minutes, which would turn the North Shore from the furthest part of the map
into one of the nearest, and no other single addition would make the "different traveller,
different city" point so hard.

The reason given here at first was that TransLink's terms might not permit redistributing
a derived extract. **They do.** The Open API Terms of Use grant "a limited, revocable and
non-exclusive license to use, reproduce, and redistribute the Data", and expressly
contemplate modifications, while retaining ownership of them. What actually stands in the
way is the shape of that permission rather than its absence: it is revocable, gated on a
written application naming who will use the data and where it will be distributed, capped
at a thousand requests a day, terminable on ten days' notice, and not sublicensable. So a
`data.js` built from it could be published here and could not be picked up and reused by
anyone else, which is the thing `principles.md` section 10 is protecting. A required
disclaimer would also have to go on the page.

**Still open:** whether the *static* GTFS download is governed by that same instrument —
the Terms define "the Data" as "any Open API", and the checker could not establish that
the timetable ZIP falls under the quoted grant. Somebody would have to ask TransLink.

**Departure hour.** The page says there is no open record of Vancouver traffic. Narrowly
that is right — there is nothing openly licensed giving speeds street by street and hour
by hour. The City of Vancouver's two traffic datasets are location layers with no counts
attached, the BC catalogue has no travel-time product, and Uber Movement is gone and was
non-commercial anyway.

What does exist, and what the page's earlier and broader wording got wrong, is Statistics
Canada tables 98-10-0504-01 and 98-10-0457-01: commuting duration by mode and by time of
departure and arrival, for the Vancouver census metropolitan area, under the Statistics
Canada Open Licence. That is an openly licensed record of travel by hour of day. It would
buy one coarse peak factor over the whole city and nothing finer, which is not a
departure-hour control, but it is not nothing and the claim should not have been stated as
though it were.

**The bike model's parameters are assumptions, not measurements.** 150 watts and 22 km/h
are stated on the page, which is the honest move, but nobody has checked them against
anything. Somebody who cycles Vancouver could look at the numbers and say.

**Steps at 1.5 km/h** comes from nowhere. It is a guess, marked as a guess here, and it
matters only for the walking map.

**Stanley Park by car looks broken, and is reporting something real.** Way 49426723, a
90 m piece of Stanley Park Drive by Second Beach, carries `motor_vehicle=no` in
OpenStreetMap — stable across four edits and last touched in January 2025, so not a stale
accident. Stanley Park Drive is a one-way loop, and cutting a one-way loop at one point
puts everything behind the cut a full lap away. So the west side of the park sits at 9.8
minutes by car where its neighbours are at 4, and in the time map that little cluster is
flung out over where the water used to be. It reads as a rendering fault and it is
arithmetic. Whether the tag is *right* is a question for somebody who has driven it
lately; the widget is not overruling a specific access tag on a hunch. If it should go,
the fix belongs upstream in OSM, not in a special case here.

**The window edge.** Routes that would leave the window and come back cannot. Nothing in
the default set does, but a start placed at the eastern edge will see a city that stops.

**What the drawing cannot say**, restated because it is the thing most likely to be
misread: distances between two places that are not the start mean nothing on the minutes
map. The (i) panel says so; whether that is enough, and whether it should be on the face
of the page rather than behind a button, is worth a look after the first time it is used
in a room.

## Picking it up again

Preview with `python3 -m http.server 8791 --directory ~/teaching-interactive/github/web`,
then `http://localhost:8791/relative-distance/`. Presentation mode is `?present=1` or the
`p` key. `?m=1` opens on the traveller avoiding steep ground, which is the most striking
state; `?s=0` opens in metres.

**Check first:** run `node tools/test/run.js relative`. If the counts fail but the times
pass, suspect the slope threshold. If everything shifts by a small amount, check `x0` and
`y0` in `data.js` against the test — the anchor moved.

**To rebuild the data:** `python3 tools/relative-distance-extract.py`. It caches under
`tools/rd-cache`; the first run downloads about a gigabyte of LiDAR. Then run
`python3 tools/relative-distance-verify.py` and compare against the table above.

`window.__rd` on the page exposes `state()`, `timeTo(node, "out"|"back")`, `node(name)`,
`set({...})` and `relayout()`, which is how both the tests and the browser checks drive it.

## Review record

```
Widget: relative-distance — Vancouver, measured in minutes
Reviewed: 2026-08-22

Pedagogical critique: changes requested, made.
  The slider from metres to minutes was removed. Its middle was half a distance
  added to half a scaled time, which is not a way of measuring anything, and the
  two buttons sitting under it at the ends were the design admitting it. Two
  states now, with the change drawn as a movement, which is what the slider was
  really for.
  The default was checked against principles.md section 2 by turning on each
  control in turn. "On foot, no steep hills or steps" removes 62% of the city and
  puts the blue pin out of reach — a limit arrived at rather than started inside,
  which is where a limit belongs.
  Two cases a student will compare — on foot, and on foot avoiding steep ground —
  differ in exactly one thing, because both use the same speeds. That was designed
  in rather than discovered.

Correctness: pass, after two real defects.
  A Float32Array threshold silently excluded 93 street segments at exactly five in
  a hundred while every recorded travel time stayed correct. Caught by an
  independent Python implementation disagreeing about counts, not about times.
  The rebuild was not reproducible: floor() on a projected minimum moved the
  coordinate origin by a metre between runs. Anchored to 100 m; two runs now give
  byte-identical output.
  Every figure in this file was produced twice, by routes sharing no code.

Text: changes requested, made.
  The claim that 5 in 100 is "the slope an accessible route is built to" was wrong
  — it is a ceiling above which a ramp is required, not a target — and was caught
  by the adversarial citation check, not by re-reading. Rewritten.
  Tobler's function is now scoped on the page: he fitted it for paths in hilly
  country, and what it lends a city map is the shape of the curve.
  Bicycling Science credits three people; the citation now does too.

Accessibility: changes requested, made.
  The path line colour was at 2.01:1 against the map ground, under the 3:1 a
  graphical object needs. All three street weights re-measured and spread across
  lightness: 10.7, 5.2, 3.1.
  The canvas had no text alternative. It now carries one that says where the map
  is drawn from, what the rings mean, and how much of the city is missing.
  Controls raised to 44 px in both layouts rather than only under pointer: coarse.
  Checked: keyboard reaches all 18 controls and every one is named; no horizontal
  scrolling at 380 px or at 200% text; dark mode leaves the cartography alone.

Device and room: partly checked.
  Phone at 375 and 380 px: labels ran off the right edge and two collided. Labels
  are now placed in priority order and measured with getBBox rather than estimated
  from character counts, and anything that would collide is dropped.
  Presentation mode: map lettering scales past the page multiplier, because it is
  read at fifteen metres. (i) panels and the footer drop; the sentence the widget
  is for stays in the reading flow.

Outstanding, and all of it needs a real device or a real room:
  - The transition has never been seen running. The browser pane used for checking
    reports the page hidden, so requestAnimationFrame never fires in it. The
    transition is driven and asserted in the test suite instead, and the settled
    state is written before the first frame rather than after the last, so a
    reader is never looking at a half-finished map. Watch it once on a real
    machine.
  - Dragging a pin, and tapping the map to move the start, have been exercised
    through code but not by hand on a touch screen.
  - Not yet seen on a projector, or in a compressed recording.
  - Colour-blindness simulation not run. The two pins differ in shape as well as
    hue, and the street classes differ in width as well as lightness, so nothing
    rests on hue alone — but that is an argument, not a measurement.
```
