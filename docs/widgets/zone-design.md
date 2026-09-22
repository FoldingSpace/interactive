# Zone design: you help draw the boundaries

`web/zone-design/` &middot; built 22 September 2026, **not deployed**

## The one thing

Whether household income and greenery are related in Vancouver depends on where you put the
boundaries, and there is no boundary in the data.

## What it is

1,342 dissemination areas in and just beyond the City of Vancouver, each with the median
household income published for it and the mean summer greenness measured over it. Four
panels, left to right: the zoning on its own, a map of income by those zones, the same zones
by greenness, and a scatter of one dot per zone with the fitted line, its slope and
R<sup>2</sup> printed live at the head of it. They stack in that order on a narrow screen.
Eight zones, painted by hand, against four zonings drawn by stated rules and against the
published dissemination areas and census tracts.

It is **a separate widget from `maup`**, decided by Luke on 21 September 2026. `maup` is
about police-reported incidents and redraws its zones at random; this one has no crime data
in it, its zonings are drawn rather than sampled, and a student paints them.

### The counter-case is not an extra, it is the finding

The build queue warned that any prediction task here "must carry the counter-case
(O'Sullivan Figs 5.6&ndash;5.7: aggregation can lower r) or it teaches a law". The current
L03 deck states that law in words, on the slide beginning **"MAUP and regression"**: "As a
generalization, as you aggregate units, the correlation gets stronger."

On this ground it is false, and not by a trick. Across the 1,317 areas R<sup>2</sup> is
**0.169**. Of the four zonings drawn by a stated rule, **two land below it** &mdash; 0.001
and 0.097 &mdash; and the second has a line that leans the other way. Same ground, same
records, eight zones in each case, and only the boundaries moved. (Grouping to the 189
published census tracts does raise it, to 0.185, which is the direction the slide expects.)

**The page reports R<sup>2</sup>, not r** (22 September). R<sup>2</sup> has no sign, so the
direction of the relationship is carried by the slope printed beside it, which is where a
reader should be looking anyway. r survives in this file, because the verification record
below is easier to check against an independent implementation in the quantity that
implementation computes.

The queue cites O'Sullivan and Unwin's Figures 5.6 and 5.7 for the counter-case. **That
citation is not on the page.** Nobody on this build had the book, so it could not go through
the adversarial check `principles.md` section 11 requires, and section 11 says an
unconfirmable citation is removed rather than hedged. The page cites Openshaw and Taylor
(1979) instead, already verified in this repository for `maup`, whose Iowa result is the
stronger form of the same claim.

## The slides it answers to

Read from `GEOS 370 2023W2 - Lecture/Lecture03-2026-draft.pptx` on 21 September 2026, by
position in `ppt/presentation.xml`. **The queue's slide numbers are from the 2024 deck and
are out of date; these are the current positions**, each cited by position and first words.

| now | first words | what it carries |
|---|---|---|
| s17 | "Spatial autocorrelation &middot; Moran's I = &minus;1.0" | the grain argument, ending "Consider it might matter whether you choose CTs vs. DAs (in Canada census data)" |
| s36 | "MAUP &middot; The modifiable areal unit problem (MAUP) is possible in any spatially aggregated data" | defines the **scale effect** and the **aggregation or zoning** effect |
| s37 | "MAUP &middot; Scale &middot; Why would the scale effect occur?" | a checkerboard figure, the scale effect as a picture |
| s38 | "DA's &middot; MAUP &middot; CT's" | the two Vancouver maps, dissemination areas against census tracts |
| s39 | "MAUP and regression &middot; As a generalization, as you aggregate units, the correlation gets stronger" | the textbook two-scheme figure: R<sup>2</sup> 0.6902 ungrouped, 0.8151 under scheme 1, 0.8899 under scheme 2 |

The deck was read from the XML rather than from the notes, per the standing rule that the
2024 speaker notes are stale. The figure on s39 was opened as an image and its three
R<sup>2</sup> values confirmed on the slide itself.

## The data

| | |
|---|---|
| Dissemination areas | 1,342 |
| ... with income, greenness and a household count | 1,317 |
| Census tracts touched | 190 |
| City of Vancouver local areas | 22 |
| Vertices after quantising to 5 m | 34,133 |
| Encoded geometry | 69,540 bytes |
| `data.js` | 194095 bytes |
| `ndvi.png` | 144131 bytes |
| `index.html` | 72604 bytes |
| Neighbours per area (sharing an edge) | min 1, mean 5.22, max 20, none isolated |
| Median household income | $23,200 to $222,000, median $88,000 |
| Greenness | 0.0911 to 0.8420, mean 0.4020 |

### Which ground, and by what rule

**The study area is stated in the extraction script and drawn on the page as its own edge.**
It is the City of Vancouver's outline, from the City's own local-area boundaries, joined to
three rectangles in UTM zone 10N:

| | what it takes in | extent |
|---|---|---|
| UBC | the other half of the Point Grey peninsula: the university and the University Endowment Lands, which are a different census subdivision and which the City's outline stops short of | 479,500&ndash;484,500 E, 5,452,500&ndash;5,459,500 N |
| east | Burnaby west of 501,500 E, about two kilometres past Boundary Road | 496,000&ndash;501,500 E, 5,450,000&ndash;5,458,000 N |
| south | Lulu Island north of 5,443,500 N, the northern half of Richmond | 483,000&ndash;501,500 E, 5,443,500&ndash;5,451,500 N |

An area is in if the centre of its **land** lies inside that polygon, or if a third of its
land and at least a square kilometre of it does. Its geometry is then cut to the polygon and
to land, so the data end on a line somebody chose rather than on a ragged fringe.

**Sea Island is why the second clause exists.** One dissemination area covers the whole
island &mdash; the airport, Burkeville and Iona &mdash; and it is 112.6 km<sup>2</sup> as
published, because it runs west across Sturgeon Bank into the Strait of Georgia. Its centre
falls at 482,017 E, out at sea and outside the study area, so the island was missing from the
map while every one of its neighbours was drawn. Taking the centre of its *land* does not
rescue it either: Sturgeon Bank is mudflat, the satellite reads it as ground rather than as
water, and the land centre is still out west. What is true of it is that 19.1 of its
47.6 km<sup>2</sup> of land, 40 per cent, is inside. Measured against every area that
straddles the edge, those two thresholds admit exactly one area, this one; the next nearest
candidate has 0.59 km<sup>2</sup> inside. Iona Island stays out, because it is west of the
483,000 E edge and the clip cuts it &mdash; that is the boundary doing its job.

**Nothing is dropped for a suppressed figure.** 25 of the 1,342 areas have no published
median income; they are drawn, they belong to a zone, and they are shown as no data rather
than removed.
Every rectangle's top edge is south of Burrard Inlet, so **nothing on the North Shore is in**:
no West Vancouver, no North Vancouver.

**New Westminster is not in.** It sits east of the 501,500 E line, and taking it would mean
taking the whole of Burnaby with it, which roughly doubles the file for ground that adds
nothing the widget asks about. That is a judgement, and it is the one thing in the boundary
rule that was decided here rather than instructed.

The clipped set is in **one piece**, so eight zones can be in eight pieces and the widget
says so under the map when they are not.

### Sources and licences

**Boundaries.** Statistics Canada, 2021 Census cartographic boundary files: dissemination
areas (`lda_000a21a_e`) and census tracts (`lct_000a21a_e`). Statistics Canada Open Licence.
An area's census tract is the tract its centroid falls in; the cartographic DA file carries
no parent identifier, and tracts are built from whole dissemination areas, so this is exact.

**Census attributes.** Statistics Canada, Census Profile, 2021, dissemination-area level
(98-401-X2021006). Three characteristics, matched on published name *and* number so a
renumbering fails loudly: "Population, 2021" (1), "Total - Private households by household
size - 100% data" (50), "Median total income of household in 2020 ($)" (243). Statistics
Canada Open Licence, with the *adapted from* wording in the footer. The download is 2.2 GB;
the script reads three rows per area out of it by way of the published starting-row index.

**City of Vancouver local areas.** `local-area-boundary`, Open Government Licence &ndash;
Vancouver. It defines the City, and it is the source of one family of candidate zonings.

**Greenness.** Copernicus Sentinel-2 level-2A, scene `S2C_T10UDV_20260807T191738_L2A`,
7 August 2026, 0.0014% cloud, processing baseline 05.12, from the Earth Search catalogue's
`sentinel-2-c1-l2a` collection. NDVI per 10 m pixel is `(nir - red) / (nir + red)` with each
band turned into reflectance first by the collection's published numbers,
`reflectance = DN * 0.0001 - 0.1`. **The offset is load-bearing**: Collection 1's pixels sit
1,000 counts above the older bucket's, and NDVI from raw digital numbers is wrong by a
visible amount. Pixels count where the scene classification reads 4, 5 or 7; water, cloud,
shadow, snow and saturated pixels are dropped.

**Water, and the clip.** Census areas are published out over English Bay, False Creek,
Burrard Inlet and both arms of the Fraser. A map of them is not recognisable as Vancouver, so
every area is cut back to land before anything else is worked out about it. The water is the
same scene's own: class 6 **and** near-infrared reflectance below 0.12, which excludes the
building shadows the class alone picks up, with patches under two hectares dropped and the
outline simplified to 15 m. 109.3 km<sup>2</sup> in nine patches. It ships with the data and
is drawn pale blue behind all the areas.

**No individual-level data of any kind.** Median household income is published per area and
for no household. Nothing here describes a person, a dwelling or a parcel, and no
dissemination area identifier is anywhere in the page or in the shipped data &mdash; the test
suite asserts both.

### Checked against a second implementation, and against the ground

`tools/zone-design-verify.py` rebuilds every figure from `data.js` in Python by matrix
algebra, sharing no code with the widget's JavaScript, and rebuilds the adjacency from the
shared vertices rather than reading the shipped lists. It agrees.

The NDVI itself was checked against a second implementation on the same scene: GEOS 472's
geoblaze demo, whose nine known-ground clicks are recorded in
`472-2026/review-2026-09-06/batches/review-log-S5.md`. Neighbourhood means agree closely
&mdash; Stanley Park 0.87 against 0.87, English Bay &minus;0.34 against &minus;0.32, downtown
roofs 0.09 against 0.09, Queen Elizabeth Park 0.52 against 0.55. Single 10 m cells differ,
because the two were not clicking the same pixel. That is the check `principles.md` section 11
says recomputation cannot give you.

**Built twice, byte-identical.** Seeds and starting points are written into the script; the
quantising origin is anchored to a round number below the minimum rather than to `floor(min)`.

## Verified numbers

Every figure below comes out of `tools/zone-design-verify.py`. They are the regression suite.

**Across the 1,317 areas themselves: r = +0.410136 (R<sup>2</sup> = 0.168212), slope =
+0.001760 per $1,000.** r is recorded here and R<sup>2</sup> is what the page prints; they
are the same number squared, and nothing but the display changed.

| zoning | zones | rule | r | R<sup>2</sup> | slope per $10,000 |
|---|---|---|---|---|---|
| dissemination areas | 1,317 | any | +0.410136 | 0.1682 | +0.01760 |
| Rings from the middle | 8 | households | &minus;0.3794 | 0.1439 | &minus;0.0295 |
| A grid of blocks | 8 | households | +0.8162 | 0.6662 | +0.0874 |
| North-south groups | 8 | households | +0.1824 | 0.0333 | +0.0600 |
| Same number of households | 8 | households | &minus;0.2987 | 0.0892 | &minus;0.0391 |

Three of the four land below the area level and two of them lean the other way, which is
the counter-case the deck's own slide s39 says cannot happen.

### The two variables aggregate differently, which is why the rule is a control

Greenness is intensive in the strict sense: a value per square metre, so a zone's mean is the
mean over its pixels and comes out identical however the pixels are grouped. Nothing is lost,
and the widget's greenness numbers do not move when the income rule changes. **The test
asserts exactly that.**

Income does not behave. What Statistics Canada publishes is a **median**, and medians do not
add: the middle household of two areas put together is not the average of the two middles,
and it cannot be recovered from them at all. So a zone's income is one of three averages of
the areas' medians &mdash; weighted by households (the default), weighted by people, or a
plain average &mdash; and none of them is the figure Statistics Canada would publish for the
merged zone. The page says so at the control.

**Stanley Park and its like.** An area with very few households still belongs to a zone and
is still drawn; its weight under the default rule is its household count, so it contributes
almost nothing to that zone's income and its full pixel count to that zone's greenness. That
is the honest consequence of weighting income by households, and it is worth naming because
the greenest ground in the city is where nobody lives.

## The four presets, and the forty rules they came from

**No search against r or against the slope.** Forty zonings, ten in each of four groups, each
drawn by a rule that can be stated in a sentence before it is run, and each made contiguous
the same way afterwards (each zone keeps its largest piece; every other piece joins whichever
neighbouring zone it shares the most areas with). Nothing is random: there are no seeds,
because the starting areas are chosen by a stated rule &mdash; the eight areas furthest apart
from each other, beginning from the area nearest a named corner of the city.

The one shipped from each group is the best of its own ten for one role: the weakest
correlation, the strongest, the steepest line, the shallowest. The extremes of the forty are
**not** shipped, so a class has something to beat.

**Budget: 40 candidate zonings.** That is the whole search.

**The table below is from the build of 22 September, before Sea Island was let in, and it
carries the old family names.** The census-tract rules are now named for the bands they
produce rather than for their parent units &mdash; walking tracts west to east and cutting
the walk into runs leaves eight north-south bands &mdash; so "Groups of census tracts" walked
west to east is the preset the page now calls **North-south groups**. The
forty rules are unchanged and so is the method; the figures moved when the ground did, and
they are kept here as the record of what was tried rather than as current values. The four
shipped are current, in the table above.

| group | name | rule | r | slope/$10k | zones | pieces |
|---|---|---|---|---|---|---|
| across | Wedges from middle | eight sectors around the middle of the city, turned 0 degrees | +0.793 | +0.0580 | 8 | 9 |
| across | Wedges from middle | eight sectors around the middle of the city, turned 15 degrees | +0.337 | +0.0484 | 8 | 9 |
| across | Wedges from middle | eight sectors around the middle of the city, turned 30 degrees | +0.869 | +0.0987 | 8 | 9 |
| across | Wedges from north-west | eight sectors around the north-west of the city, turned 0 degrees | -0.843 | -0.1098 | 5 | 6 |
| across | Wedges from north-west | eight sectors around the north-west of the city, turned 15 degrees | +0.184 | +0.0125 | 5 | 6 |
| across | Wedges from north-west | eight sectors around the north-west of the city, turned 30 degrees | -0.112 | -0.0145 | 5 | 6 |
| across | Wedges from south-east | eight sectors around the south-east of the city, turned 0 degrees | +0.532 | +0.0520 | 7 | 8 |
| across | Wedges from south-east | eight sectors around the south-east of the city, turned 15 degrees | +0.175 | +0.0161 | 8 | 9 |
| across | Wedges from south-east | eight sectors around the south-east of the city, turned 30 degrees | +0.686 | +0.0569 | 7 | 8 |
| across | Rings from the middle | eight rings of equal area around the middle of the city, a core and its edges | +0.489 | +0.0720 | 8 | 9 |
| follow | Groups of census tracts | whole census tracts walked west to east and cut into eight runs of equal households | +0.085 | +0.0081 | 8 | 9 |
| follow | Groups of census tracts | whole census tracts walked south to north and cut into eight runs of equal households | -0.189 | -0.0230 | 8 | 9 |
| follow | Groups of census tracts | whole census tracts walked south-west to north-east and cut into eight runs of equal households | -0.047 | -0.0043 | 8 | 9 |
| follow | Groups of census tracts | whole census tracts walked north-west to south-east and cut into eight runs of equal households | +0.255 | +0.0486 | 8 | 9 |
| follow | Groups of census tracts | whole census tracts walked along the long axis and cut into eight runs of equal households | +0.329 | +0.0495 | 8 | 9 |
| follow | Groups of the city's neighbourhoods | whole the city's neighbourhoods walked west to east and cut into eight runs of equal households | -0.447 | -0.0629 | 8 | 9 |
| follow | Groups of the city's neighbourhoods | whole the city's neighbourhoods walked south to north and cut into eight runs of equal households | +0.535 | +0.0388 | 8 | 9 |
| follow | Groups of the city's neighbourhoods | whole the city's neighbourhoods walked south-west to north-east and cut into eight runs of equal households | -0.293 | -0.0302 | 8 | 9 |
| follow | Groups of the city's neighbourhoods | whole the city's neighbourhoods walked north-west to south-east and cut into eight runs of equal households | +0.109 | +0.0144 | 8 | 9 |
| follow | Groups of the city's neighbourhoods | whole the city's neighbourhoods walked along the long axis and cut into eight runs of equal households | -0.197 | -0.0245 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 0 degrees | +0.108 | +0.0085 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 22 degrees | +0.081 | +0.0062 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 45 degrees | -0.148 | -0.0176 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 68 degrees | +0.177 | +0.0154 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 90 degrees | -0.501 | -0.0375 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 112 degrees | +0.361 | +0.0469 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 135 degrees | +0.119 | +0.0201 | 8 | 9 |
| along | Bands across the city | eight bands of equal width at 158 degrees | -0.049 | -0.0050 | 8 | 9 |
| along | A grid of blocks | a 2 by 4 grid laid over the city | +0.504 | +0.0395 | 8 | 9 |
| along | A grid of blocks | a 4 by 2 grid laid over the city | +0.162 | +0.0141 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the south-west of the city, until the households even out | +0.642 | +0.0728 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the north-west of the city, until the households even out | +0.261 | +0.0286 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the south-east of the city, until the households even out | +0.294 | +0.0305 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the north-east of the city, until the households even out | -0.036 | -0.0079 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the south of the city, until the households even out | -0.021 | -0.0079 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the north of the city, until the households even out | +0.081 | +0.0197 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the west of the city, until the households even out | +0.322 | +0.0645 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the east of the city, until the households even out | -0.109 | -0.0235 | 8 | 9 |
| equal | Same number of households | grown from eight starting areas as far apart as possible, the first in the middle of the city, until the households even out | -0.130 | -0.0237 | 8 | 9 |
| equal | Compact blocks | grown from the same eight starting areas at the same rate, so every zone covers about the same number of areas | -0.390 | -0.0648 | 8 | 9 |

The four shipped are **Wedges from north-west** (weakest r), **A grid of blocks** (strongest r), **North-south groups** (steepest line) and
**Same number of households** (shallowest). Each is named for its rule and for nothing else: a name that said
"steeper" or "flatter" would give away the answer to the thing the class is asked to find.

### What was tried and dropped

- **A mode on `maup`.** Ruled out by Luke, 21 September. The crime data is not what this
  teaches and `maup`'s zoning is random rather than drawn.
- **An equity intent**, in which a student drew zones to mix incomes, with a
  between-zone share of income variance as its measure. Built, then removed on Luke's
  instruction: the page has one thing to do. The measure and its readout are gone from the
  code, not hidden.
- **A gerrymandering search** &mdash; hill-climbing to flatten, steepen or reverse the line.
  It worked (r reached 0.000 on an earlier extent) and it taught the wrong thing: a zoning a
  computer built to move a statistic is not one anybody would defend, so a student can set
  the whole page aside as a trick. Replaced by the forty stated rules, which disagree anyway.
- **Two census variables with income only in the equity half.** Replaced by income against
  greenness on Luke's instruction, and it is the better pair, because the two aggregate
  differently.
- **A slider between two intents.** Refused on `principles.md` section 4: the middle of it
  would not be a state.

## Why the rest of the choices are what they are

**It opens on a painted zoning, not on dissemination areas.** `principles.md` section 2 asks
that the default not be a dead end, and painting is the widget's own lesson. A page opening
on 1,241 areas would have its main control disabled on arrival.

**Painting is refused on the published zonings**, and the note under the palette says how to
get back to something paintable rather than leaving a dead control.

**Fixed class breaks**, quantiles into seven from the area-level distribution, and **fixed
scatter axes**. A re-zoning has to read as a change in the data, never as a change in the
palette or in the frame.

**The scatter is drawn for a projector.** Zone dots are at least 6 units of a 320-unit
viewBox, which is about 6 px at the default layout and about 15 on a projector, filled from
the income ramp with a white stroke so overlaps stay countable; the fitted line is 3.5 units;
every piece of type on it is 13 units, above the 11 px floor the course uses for anything
read from the back. The 1,317 areas behind are **not** dots: single points disappear on a
projector, so they are drawn as one flat light-grey field on a 46 by 42 grid, which reads as
a region. The equation, its slope and its r sit at the head of the panel at title size, with
only the slope and r in bold.

**Colours.** ColorBrewer PuBu for income and YlGn for greenness, both from the sets their
authors mark safe for the commonest colour blindness, and two different ramps so the maps
cannot be confused. Zone identity uses eight of Okabe and Ito's qualitative set on the outline
and the paint chip, and the zone's number is spoken rather than drawn, for the reasons above.

**The dots are sized by households.** The fit is unweighted, one dot one zone; sizing the dots
is the only place that disagreement is visible.

**The link is a fragment, not a query string.** A painted zoning is 1,241 numbers under eight,
packed three bits each into base64: about 415 characters, well under any limit, and a fragment
is never sent to a server. It carries the zoning, the name the student typed and the
aggregation rule. **Copy link** puts the whole URL on the clipboard; a paste box takes one
back. No course-specific service is named anywhere on the page.

## Known limits and open threads

**One day in August.** Greenness is one cloud-free scene: that summer's drought, that week's
irrigation, that morning's shadows. It is not tree canopy and it is not parks.

**Greenness is ground, not gardens.** A high value can be a golf course, a cemetery or a
single large lawn. Reading it as a fact about what residents did is the error the income half
is warning about.

**No inference.** No p-value, no standard error, no test. With eight zones chosen by the
reader a p-value would be a lie with a decimal point on it. Whether the page should say that
in so many words is open.

**The regression is unweighted across zones.** Every zone counts once whatever it holds.

**Whose land.** `principles.md`'s open question applies exactly as it does to `maup` and
`least-cost`. This page draws Vancouver, cuts it up and prices it, and says nothing on screen
about territory. Luke's call, not made.

**Three maps, one zoning, all three painted on.** A stroke on any of them moves the same
areas and all four panels redraw. The zone boundaries, the study-area edge and the keyboard
cursor are drawn identically on all three, so any one of them reads as the zoning on its own.

**No zone number is drawn on any map.** A zone can be in several pieces &mdash; that is the
point of letting somebody paint one &mdash; and a number at its centroid then sits in
whichever piece the arithmetic landed in, or in the gap between them on ground belonging to
another zone. Identity is carried by colour on the zones map and by the boundaries on all
three, and **the scatter's dots take the same palette colours**, so a dot can be matched to
the ground it came from by eye. The number survives where it cannot mislead: in what is
announced after a keypress or a stroke, which is the route a screen-reader or keyboard user
has. Colour is therefore doing more work here than `principles.md` section 9 normally allows,
and what pays for it is that it is a label rather than a measurement &mdash; the quantities
are in the two choropleths, each with its own legend, and the eight hues were measured at
3.06 to 5.19:1 against the page.

**The leftmost panel is the zoning and nothing else**: each area filled with its zone's
palette colour, no variable in the way. The two choropleths answer "what is in these zones";
this one answers "what are the zones", which is the question somebody painting is actually
holding. The palette sits under it, so choosing a colour and using it are one movement rather
than two halves of the page. The fill is paired with the zone number printed on it, and drawn
at 0.55 opacity so the area hairlines and the water stay visible through it, and it is the
key the scatter is read against.

**There is a way down to the original data and back.** On a wide screen, and on a projector,
the section is far below the fold and nobody is scrolling. An **Original data** button sits
with the other controls, opens the disclosure, scrolls to it and puts focus on its heading; a
**Back to the maps** control at the foot of the section returns the view and the focus to the
button that sent you. Both are buttons, so both work from the keyboard. The section is no
longer hidden in presentation mode, because hiding it would have broken the button that
reaches it.

**Three sentences were deleted on Luke's instruction** and the suite asserts they stay gone:
the area-level figure repeated under the R<sup>2</sup> card, the same under the slope card,
and the closing note about turning people into areas. The area-level figures survive where
they do work &mdash; in the two explanation panels and in the five-minute activity.

**Painting is one code path for mouse, pen and finger.** `pointerdown` captures the pointer,
`pointermove` finds the area by hit-testing the page rather than by reading the event target
(capture has retargeted it to the map), and `pointerup` or `pointercancel` releases. A press
paints before any move arrives, so a single click or tap paints one area. Both take
`touch-action: none`, so a finger drag paints rather than scrolls; a 2 rem gutter each side
under `pointer: coarse` gives a thumb somewhere to scroll from
(46 px each side at 375 px wide, measured). Verified in the browser with a mouse drag across
the map, 16 areas repainted, and under touch emulation with five touch points, 13 areas
repainted. The suite builds the stroke by hand, because an automated drag helper sends a
press and a release with nothing between.

**Not yet checked:** the lecture machine, a compressed recording, and a screen reader.

## For the classroom &mdash; drafted, not settled

`principles.md` section 16 requires that the activity be settled by interrogation with
whoever teaches it rather than drafted alone. **This one was drafted alone**, and the panel
says so where an instructor will see it. Re-read against section 16 on 22 September and
rewritten once; what it now asks:

- **Commit, one minute.** "Across the 1,317 areas, R<sup>2</sup> between income and greenness
  is 0.17. You are about to group those areas into eight zones. Write down one number: what
  will R<sup>2</sup> be then?" One number, no screen needed, written before anything is
  pressed. **The figure is now asserted by the test suite against what the page
  computes**, because the first draft quoted 0.481 from an earlier extent and nothing caught
  it.
- **Pair, two minutes.** Compare the two numbers and say why they differ. Press each of the
  four rules and read R<sup>2</sup> off each. Then paint, for one of four prizes: the
  steepest positive slope, the steepest negative slope, the highest R<sup>2</sup>, and the
  R<sup>2</sup> nearest zero. Name it, copy the link, hand it on with the slope and the
  R<sup>2</sup>.
- **Room, two minutes.** Take the four prizes in turn and open the winning link at the front.

**Will two reasonable people differ?** Yes, and the spread is written into the data rather
than hoped for: the four rules give R<sup>2</sup> of 0.62, 0.30, 0.10 and 0.00 over the same
eight zones, so any number between 0 and 0.6 is a defensible guess.

**The wrong answers, and what each is made of.** "Above 0.17, because grouping strengthens a
relationship" is what the deck's own slide s39 says in those words, and two of the four rules
are below it. "About 0.17, because a zone is a sample of the city" is the sampling intuition,
and it is wrong because a zone is not a sample, it is a sum. "The line must still lean the
same way" is reasonable if you have seen aggregation demonstrated once, and one of the four
leans the other way.

**What the share-back does with them.** The three positions are named on the panel, and the
instructor settles between them by opening two of the room's own links rather than by
asserting anything. The panel then ends on the question the prizes cannot settle: which of
these zonings would anybody put in a report, and how would a reader tell?

**Five minutes including the share-back**, split one, two, two. Pen and paper carries the
commitment; the page only settles it.

Candidates dropped: guessing a mixing figure (nobody has a prior, so the commitment is a coin
toss); asking which of two zonings is "fairer" (the right shape, but the page cannot settle
it, so the share-back has nowhere to go); asking pairs to reach a target r (turns a lesson
about instability into a puzzle with an answer).

## Picking this up again

Source in `web/zone-design/`. Data rebuilt with

```
python3 tools/zone-design-extract.py --cache /tmp/zone-design --out-dir web/zone-design \
    > web/zone-design/data.js
```

which fetches everything it needs: about 98 MB of boundaries, 10 MB of tracts, 2.2 GB of
census profile, one GeoJSON, and three windows out of a Sentinel-2 scene read over
`/vsicurl`. Run it twice and diff before recording anything against it. Then

```
python3 tools/zone-design-verify.py web/zone-design/data.js
node tools/test/run.js zone
```

Preview with `python3 -m http.server 8791 --directory ~/teaching-interactive/github/web` and
open `http://localhost:8791/zone-design/`.

**Check first:** the area level is r = +0.410136 (R<sup>2</sup> = 0.168) over 1,317 areas;
Rings from the middle gives r = &minus;0.3794; A grid of blocks gives +0.8162; and the point at 486,944 E, 5,449,115 N, which
is the airport terminal on Sea Island, is inside a drawn area. If those four come back, the
boundary rule, the aggregation, the fit and the zonings are all intact.

`window.ZONE_TEST` exposes `state()`, `fitAt(zoning, rule)`, `daFit`, `zoning(id)`,
`groundPieces()`, `setZoning`, `setRule`, `paint(area, zone)`, `zone()`, `pack()`,
`fragment()` and `readFragment()`.

## Review record

```
Widget: zone-design
Reviewed: 2026-09-22 (first build)
```

**Pedagogical critique &mdash; not yet run as an interview.** The build was steered by Luke
through the session rather than critiqued at the end, and the classroom activity was drafted
rather than settled. Both are outstanding.

**Correctness &mdash; pass.** Every shipped figure recomputed by an independent Python route
that shares no code with the widget, agreeing to better than 1e-4 on values recorded at four
decimals. Adjacency rebuilt from the geometry and matched against the shipped lists. The data
file built twice and byte-identical. The NDVI checked against a second implementation on the
same scene and against known ground.

Two claims were written from design intent and **measured false**, then corrected: that the
zoning which sharpens the line also sorts incomes more (it was the opposite), and that
aggregation always raises r here (the published census tracts lower it). Both were caught by
the test suite because the assertions were written before the numbers were read.

**Text &mdash; partial.** Scanned for direction words that would be wrong in one of the three
layouts and rewritten to be position-free. The classroom paragraph re-read against section 16
and rewritten. Not yet read aloud end to end, and not yet scanned against the anti-AI list.

**Accessibility &mdash; measured, two fixes.** Body text 17.8:1, soft labels 7.0:1, the
study-area rim and the zone lines 15.5&ndash;17.8:1 against the palest fill in either ramp.
Two failures, both fixed: the dissemination-area hairline measured **2.67:1** against the
palest income fill, below the 3:1 a graphical object needs, and is darkened to 3.62:1 and
4.09:1; two of the eight zone hues measured **2.25:1 and 2.31:1** against the page, and the
zone's number is drawn in that colour, so both are darkened, taking the whole set to
3.06&ndash;5.19:1. Touch targets 44 px on a phone. Keyboard painting works and its
instructions live in the map's accessible description.

**Two standards knowingly spent**, written here because a standard quietly abandoned is worse
than one deliberately given up (`principles.md` 12b). The water fill is 1.57:1 against the
page and the reference field behind the scatter is 1.29:1. Neither carries information on its
own: the coast is drawn by the study-area rim at 17.8:1 and by the areas' own edges, and the
field is context behind dots that are themselves 3:1 or better. Making either meet 3:1 would
put them in front of the data they sit behind.

**Device and room &mdash; measured.** No horizontal overflow at 988 px, at 375 px, or at
640 px with a 32 px base font, which is the 200% zoom case. On a phone the map is 346 px wide
and the page is 3,195 px tall. In presentation mode at 988 px &mdash; the narrowest width it
would be used at &mdash; the smallest type on the scatter is **12.4 px**, the equation line
and the preset names are 16.9 px and the note under the panel is 15.1 px, all above the 11 px
floor the course uses for anything read from the back. Not yet checked on the lecture machine,
in a compressed recording, or with a screen reader.

