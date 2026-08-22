# Drawing the lines: MAUP in Vancouver

`web/maup/` &middot; live at <https://foldingspace.github.io/interactive/maup/>

## The one thing

A statistical result about places can be an artefact of the boxes. Three choices move the
answer and none of them is in the data: how many areas you cut the city into, where you put
the boundaries, and what you decide counts as *near*.

## What it is

Incidents reported to Vancouver police in 2015 and 2016, against the number of private
households in an area and the median household income there. Two maps, three numbers, and
four controls that each change the answer without changing a single record.

The question on screen is deliberately not "what explains incidents". It is **does who
lives in an area predict where incidents get reported?** — which is all the model does, and
naming it that way makes the mismatch the subject rather than a caveat. Most of these
incidents happen where people are, not where they sleep.

It comes out of GEOG 370's Lab 3, which compares dissemination areas with census tracts.
The lab shows the scale half of the modifiable areal unit problem and describes the zoning
half in its introduction without ever demonstrating it. This does both, and adds a third
thing the lab never raises at all.

The lab worked through in full is in `lab3-worked.md` in the local working folder — **not
in this repository**, because that file is an answer key and this repository is public.

### It deliberately will not do the lab

Residential break and enter is not offered. It is what the lab asks students to model, and
a page printing its regression, its R<sup>2</sup> and its residual Moran's I would be an
answer key on the open web. Bicycle theft, theft from vehicle, commercial break and enter
and mischief are offered instead: same city, same census data, same method, nothing to copy.

The substitution teaches better than duplication would have. Reporting rates differ sharply
between those categories, which is the point the lab's own reference list makes and its
exercises never reach.

**Bicycle theft is the default and mischief is not.** A negative income coefficient on a
category whose name sounds like a judgement of people is the single result here most open
to being read as a claim about who lives where. It is reached deliberately rather than met
on arrival. Bicycle theft also gives the more useful lesson: a coefficient that looks solid
across 996 areas dissolves across 118.

### The critical literature is used as method, not as claims

Lally and Jefferson are cited for how they work, not for findings transplanted onto data
they never touched. Lally's claim is scoped to *minor*, officer-initiated offences; these
four categories are mostly citizen-reported, so his marijuana finding does not carry over
and is not made to.

What carries over is the approach. Interrogate what the data records about the institution
that made it. Interrogate the categories themselves, because the schema decides what can be
said at all. Refuse the idea that a technical improvement settles anything. Then use the
records anyway.

So the schema interrogation lives at the category control, where a student practises the
move rather than reading about someone who made it: these headings were written by an
institution for its own purposes, change one and the city changes shape, and some of what
moves is how each kind of incident comes to be written down. Jefferson's charge that people
become interchangeable objects in reductive categories, and space an invariant coordinate
system, describes this page too. It says so once, in a line, and the 996 smallest areas stay
drawn under every grouping so what aggregation discards is never quite off the screen.

### The way in

A bare URL shows a splash first: 127 words on why the page exists, before any of it moves.
It carries three things and one sentence each. That a map is a standpoint rather than a
view from nowhere, and that whoever chose the areas chose what could be seen. That three
choices here move the answer and none of them is in the data. And that the records are a
standpoint too — they mark where officers were, what someone reported, how it was written
down — so a crime map describes a city and also shapes what can be said about it. It ends
with the two questions the page is built around: what does the model say, and what had to
happen for these numbers to exist?

Any query string skips it. A link from a slide, an `iframe` with a configuration, a shared
state, `?present=1` — all of those are someone being sent somewhere specific, and they land
on it. The page behind the splash is already drawn and live, so nothing about this makes the
opening state a dead end. Escape closes it, and focus moves into the controls.

Nothing is remembered between visits, because this repository stores nothing.

## The data

996 dissemination areas with households, median household income, population, census tract,
and counts of reported incidents in four categories. Census tracts are not shipped: all 996
DAs nest exactly inside the 118 tracts, so a tract is drawn by filling its member DAs, and
every other set of areas is built the same way.

Generated by `tools/lab3-extract.py` from the lab's `MAUP.gdb`, which is course material and
is not in this repository. Geometry is quantised to a 2 m grid in BC Albers and delta-encoded
as base64 varints. Quantising before encoding snaps shared boundaries to identical vertices,
which does two jobs: neighbouring polygons stay coincident with no slivers, and contiguity
falls out of the shared vertices instead of needing a geometry library. Area centres for the
distance weights are computed in the browser from the same rings, so nothing extra ships.

| | |
|---|---|
| Dissemination areas | 996, of which 995 have published figures |
| Census tracts | 118 |
| Vertices after quantising | 22,779 |
| Encoded geometry | 49,488 bytes |
| `data.js` | 137 KB |
| Neighbours per DA (touching) | min 1, mean 6.40, max 17 |
| Households, all DAs | 310,033 |

| category | in the layer | inside a DA |
|---|---|---|
| Theft of Bicycle | 5,698 | 5,698 |
| Theft from Vehicle | 23,357 | 23,351 |
| Break and Enter Commercial | 5,143 | 5,143 |
| Mischief | 8,791 | 8,789 |

**Two files, not one.** `data.js` sits beside `index.html`. Same folder, same request chain,
no external host; inlining 137 KB would only have made the source unreadable.
`widget-pattern.md` anticipated this — the rule bending rather than breaking.

## Verified values

Computed twice: once by the widget's own code sliced out of `index.html` and run in Node,
once in Python with numpy by matrix algebra. **All 36 combinations of category, areas,
neighbour definition and model agree to within 2e-12.** These are the regression suite.

### Ordinary least squares, touching neighbours

Coefficients are households and income, income per $1,000.

| category / areas | n | R<sup>2</sup> | households (p) | income (p) | Moran's I | z |
|---|---|---|---|---|---|---|
| bicycle / DA | 995 | 0.559979 | 0.05761 (4.4e-178) | 0.0614 (8.1e-4) | 0.164995 | 9.60 |
| bicycle / CT | 118 | 0.530771 | 0.05370 (2.8e-20) | 0.1926 (0.51) | 0.170231 | 3.50 |
| bicycle / random 118, seed 7 | 118 | 0.551529 | 0.04857 (2.1e-21) | 0.2032 (0.55) | 0.374657 | 7.39 |
| vehicle / DA | 995 | 0.338375 | 0.15203 (1.1e-89) | 0.0780 (0.31) | 0.223855 | 15.78 |
| vehicle / CT | 118 | 0.315180 | 0.14550 (2.5e-10) | −0.8333 (0.51) | 0.285025 | 6.90 |
| vehicle / random 118, seed 7 | 118 | 0.433684 | 0.13825 (1.0e-14) | −1.4245 (0.26) | 0.373125 | 7.90 |
| commercial / DA | 995 | 0.486442 | 0.03938 (2.0e-140) | −0.0188 (0.20) | 0.300142 | 17.40 |
| commercial / CT | 118 | 0.531708 | 0.04401 (9.5e-19) | −0.4696 (0.064) | 0.287483 | 5.86 |
| commercial / random 118, seed 7 | 118 | 0.513828 | 0.03769 (1.2e-17) | −0.6462 (0.035) | 0.399286 | 7.90 |
| mischief / DA | 995 | 0.341322 | 0.05350 (3.1e-87) | −0.0453 (0.098) | 0.219791 | 15.30 |
| mischief / CT | 118 | 0.320115 | 0.04865 (5.9e-9) | −1.1130 (0.019) | 0.311799 | 6.84 |
| mischief / random 118, seed 7 | 118 | 0.403973 | 0.05030 (6.4e-12) | −1.4463 (0.0079) | 0.307055 | 6.59 |

### What counts as a neighbour, bicycle theft, same residuals throughout

| areas | neighbours | Moran's I | z | p |
|---|---|---|---|---|
| DA | touching | 0.164995 | 9.60 | <0.0001 |
| DA | touching, and theirs | 0.082913 | 8.85 | <0.0001 |
| DA | all, by 1/distance | 0.012499 | 8.09 | <0.0001 |
| CT | touching | 0.170231 | 3.50 | 0.0005 |
| CT | touching, and theirs | 0.059665 | 2.38 | 0.0174 |
| CT | all, by 1/distance | 0.017131 | 2.55 | 0.0109 |

**Read the two columns against each other.** The size falls by more than a factor of ten
as the circle widens, and the test never stops rejecting. Widening dilutes — adding distant
pairs with nothing to do with each other waters down what the near pairs showed — but with
995 areas even a faint pattern is easy to detect. So the neighbour control cannot be used
to make the problem go away, and the widget says so where a student might try.

This closes an open thread from the first widget, which recorded the experiment as unrun
and my guess about it as a guess. The guess was right about the drift and wrong to imply it
would reach "no autocorrelation".

### The error model

Kelejian and Prucha's generalised moments estimator: lambda from the residuals, then the
equation refitted with that structure removed. No determinant, so it runs in a browser.

| category / areas | lambda | R<sup>2</sup> | income | Moran's I | z after |
|---|---|---|---|---|---|
| bicycle / DA | 0.373 | 0.5600 → 0.5185 | 0.0614 → 0.0688 | 0.1650 → −0.1151 | −6.61 |
| bicycle / CT | 0.399 | 0.5308 → 0.4097 | 0.1926 → 0.3224 | 0.1702 → 0.0642 | 1.46 |
| bicycle / random 118, seed 7 | 0.784 | 0.5515 → 0.5008 | 0.2032 → 0.6819 | 0.3747 → 0.0091 | 0.34 |
| mischief / DA | 0.443 | 0.3413 → 0.2825 | −0.0453 → −0.0029 | 0.2198 → −0.0551 | −4.09 |
| mischief / CT | 0.563 | 0.3201 → 0.2308 | −1.1130 → −0.5453 | 0.3118 → −0.0294 | −0.47 |
| mischief / random 118, seed 7 | 0.623 | 0.4040 → 0.2645 | −1.4463 → −1.1428 | 0.3071 → −0.0112 | −0.06 |

Three things here are worth more than the fact that it works.

**The coefficients move, sometimes a lot.** The textbook account is that ordinary least
squares stays unbiased under this model and only its standard errors are wrong. Mischief
across census tracts halves its income coefficient; across dissemination areas it goes to
essentially nothing. That is spatial confounding: the equation cannot tell income apart
from everything else smooth over the same parts of the city, which is where the statistical
reading and the critical reading arrive at the same sentence from opposite directions.

**It overshoots.** Across 996 areas the repair pushes the clustering past zero to −0.115,
z = −6.61. A different problem, not a solved one.

**Lambda hits the ceiling.** With 1/distance weights the estimate runs to 0.950, the edge
of the search. The widget says so on screen and tells the reader not to trust it, rather
than printing a number that looks like an estimate.

The lag model was built, verified, and removed. Its coefficients are not marginal effects —
feedback through neighbours means reading them that way is wrong without a direct and
indirect impact decomposition — and printing them beside ordinary ones would teach something
false. The same clustering admits both stories and the data cannot choose; making the choice,
and saying why, is the move a student has to learn.

### The range across zonings

Twenty other ways of drawing the same number of areas, R<sup>2</sup> sorted:

| category | areas | min | median | max | income |
|---|---|---|---|---|---|
| bicycle | 118 | 0.3735 | 0.5362 | 0.6364 | significant in 0 of 20 |
| bicycle | 40 | 0.1664 | 0.5760 | 0.7450 | significant in 1 of 20 |
| mischief | 118 | 0.2713 | 0.3993 | 0.5054 | significant in 13 of 20 |
| mischief | 40 | 0.2231 | 0.5470 | 0.7199 | significant in 12 of 20 |

Bicycle theft is the sharpest case in the whole widget. Income is significant across 996
dissemination areas at p = 0.0008, is not across the real 118 census tracts, and is not
significant in a single one of twenty arbitrary 118-area partitions. The finding does not
survive the boxes.

Fotheringham and Wong end their 1991 paper by asking for "a technology that will allow the
user to rezone data, to aggregate it in a specified number of ways, and to report a summary
of calibration results for each of the different zoning systems". That is the strip, thirty
years late.

### Exact inference, checked against closed forms

Coefficient p-values come from the regularised incomplete beta function. Checked against
I<sub>0.5</sub>(0.5, 0.5) = 0.5, I<sub>x</sub>(1,1) = x, the Cauchy form for one degree of
freedom and the two-degree form; all agree to ten decimal places, and t = 1.959964 at a
million degrees of freedom returns 0.050000.

Moran's I uses the exact randomisation moments rather than a permutation test. That is
faster, identical across all three neighbour definitions, and follows the repository's rule
about preferring the closed form. It also had to be: 1/distance is a dense matrix of about a
million weights, and 999 shuffles of it would be a billion operations.

The residual caveat stands and is on screen. These residuals come from a model already
fitted to this data, so the ordinary null is not quite right; Cliff and Ord derived the
corrected moments in 1972. At z ≈ 10 the conclusion is not in doubt.

## Design decisions worth keeping

**Random areas are grown to equal household counts.** Free growth gave R<sup>2</sup> far
above the real tracts for the wrong reason: uneven areas manufacture correlation when both
counts scale with size. Balanced growth reproduces how census units are actually built and
lands the real tracts among the random ones rather than outside them.

**Census tracts are built from the DAs rather than read from the census.** Income for a
grouped area is the household-weighted mean of its DAs' medians. Against the published tract
figures: correlation 0.988, median difference $857. Using published figures for tracts and
aggregates for random areas would confound "different boundaries" with "different definition
of income", which is the entire comparison.

**The strip runs 0 to 100 per cent.** Stretching the axis to the observed spread would make
any spread look total.

**R<sup>2</sup> is shown as a whole percentage.** "53%" is readable by someone meeting the
idea for the first time; "0.531" is not. Two arrangements a few tenths of a point apart both
read as 53%, which is a fair trade at the back of a room. The values recorded here stay as
fractions, so the regression suite keeps its precision.

**Colours.** ColorBrewer YlGn for quantities, RdBu for the residuals, both from the set the
scheme's authors mark as safe for the commonest colour blindness.

## Layout notes

Narrow: two maps side by side rather than stacked, which took the page from 2,255 px to
about 1,800.

Presenting: the width cap comes off, content centres vertically, controls run as one wide row
beneath everything, and the (i) buttons hide. Things then drop out in order of how little a
lecturer drives them — the left map's own view, then the hover readout, then the category,
which is normally set in the URL on the slide. Below 820 px of height the readout pairs its
two headline numbers, because the readout and not the maps sets the height of the top row.
Verified with nothing clipped and no overflow at 375×812, 1280×900, 1280×720 and 1920×1080.

## Performance

Measured in the page, never in a harness — the same code timed at top level in Node ran
several times slower and sent me optimising something that was not slow.

| view | full redraw |
|---|---|
| 996 areas, touching | 14 ms |
| 118 areas, cached strip | 10 ms |
| 118 areas, cold strip (20 fits) | 63 ms |
| 996 areas, 1/distance | 47 ms |
| 996 areas, 1/distance, error model | 148 ms |

The last of those is the worst case: a dense million-weight matrix, a moment estimator and a
refit. The weight sums are cached on the matrix, because Moran's I and the estimator both
want them.

## Known limits and open threads

**The maps are not keyboard navigable.** Pointing at an area shows its numbers; there is no
keyboard route to the same thing. Making 996 polygons tabbable is not the answer — a list, or
arrow-key movement between areas, would be. The strip's dots *are* buttons and are reachable.

**No geographically weighted regression.** The widget handles spatial dependence globally.
GWR fits an equation at every area, and the lab's second half does exactly that; it is
computed and recorded in the local worked-lab file. A second map view of local coefficients
would parallel the first widget's local Moran's I.

**The zoning is random, not adversarial.** Openshaw's sharper point was that boundaries can
be drawn *deliberately* to produce a wanted answer — he called it applied gerrymandering and
drove an Iowa correlation anywhere from −0.99 to +0.99. Random draws show the answer is
unstable. A "draw the boundaries that maximise R<sup>2</sup>" button would show it is
steerable, which is worse and more useful.

**Whether the critical framing lands.** It is in the question the page asks, the captions,
the equation, the category panel and the residual panel rather than in a footer. Whether a
student who came to press buttons takes it in is not something this build can tell us, and
it is the first thing to ask in a classroom.

**The crime layer has no `B_E_Resid`, `Mischief` or `Auto_Theft` columns**, though the lab
says three such columns were added. Counts come from the `TYPE` string instead. For
residential break and enter that gives 6,114 against the 6,116 the lab's location-quotient
formula divides by. It changes nothing and is worth fixing before the lab runs again.

## Picking this up again

Live: <https://foldingspace.github.io/interactive/maup/>. Source in `web/maup/`, data
regenerated by `python3 tools/lab3-extract.py <path to MAUP.gdb> > web/maup/data.js`.

Preview with the `widgets` server in `.claude/launch.json`, or
`python3 -m http.server 8791 --directory ~/teaching-interactive/github/web` and open
`http://localhost:8791/maup/`.

Check first: bicycle theft across dissemination areas gives R<sup>2</sup> = 0.559979 and
Moran's I = 0.164995. Switch to census tracts and income moves from p = 0.0008 to p = 0.51.
Switch neighbours to 1/distance and I falls to 0.012499 with z still 8.09. Switch the model
on at census tracts and lambda reads 0.399 with I at 0.0642. If those four come back, the
model, the aggregation, the weights and the estimator are all intact.

`window.MAUP_TEST` exposes `compute()`, `state()` and `setZoning(id, seed)`.

To check against something sharing no code with the widget, slice the maths out of
`index.html` — everything between `decodeGeom` and the colour section is self-contained
given `D` and `N` — run it in Node against `data.js`, and compare with numpy. That is how
every number above was checked.

## Review record

```
Widget: maup
Reviewed: 2026-08-21
```

**Pedagogical critique — changes requested, and made.** Run as a full interview rather than
a read-through, and it changed the build four times. The widget originally modelled
residential break and enter and so published the answers to three graded questions; the
category was removed. The crime-data critique was a footer disclaimer; it became the
question the page asks. Mischief was the default and is no longer. A spatial lag model was
built and then removed once it was clear its coefficients cannot be read as ordinary
effects. The neighbours control and the range strip were both added because the literature
being taught asks for them.

**Correctness — pass.** 36 combinations verified against numpy by an independent route, all
within 2e-12; p-values checked against three closed forms. One error was caught in the
documentation rather than the code: a spread of R<sup>2</sup> values was written down before
it was computed, and the computed range is wider than the invented one.

**Text — changes requested, and made twice.** The splash was written last, scanned clean
against the anti-AI list, 127 words over 15 sentences averaging 8.5 words each.

**Text — changes requested, and made.** Scanned against the anti-AI list, then read again
for plainness, then audited for whether the stakes were actually on screen. They were not.
Everything visible before opening an (i) was a title, a methods question, four control
labels and two grey lines in the footer — and presentation mode hides the (i) buttons, so
a lecture would have shown the statistics and none of the argument. The word Vancouver did
not appear anywhere on the face of the page.

Fixed by putting 47 words above the maps, in the reading flow rather than the footer, and
keeping them in presentation mode: counts like these send officers somewhere and leave them
elsewhere, they are how a neighbourhood gets described when money is handed out, the areas
were drawn by an agency for its own reasons, and every number is a record rather than an
event. The compact-projector threshold moved from 820 px to 960 px to pay for the height.

The same audit caught a live error: the footer still credited "Residential break and enter
incidents", the one category the widget refuses to model.

**Accessibility — pass, with one fix.** Contrast measured: body text 17.8:1, soft labels
6.3:1, captions 7.0:1, buttons 17.8:1, area outlines 17.8:1. The dissemination-area hairline
measured 2.6:1, below the 3:1 minimum, and it matters because the palest fill is within
1.1:1 of the page — the line is what shows where a low-valued area ends. Darkened to 3.18:1
light, 3.03:1 dark. Touch targets 44px, (i) buttons 25px, strip dots 18px on touch. Both
ramps colourblind-safe. Live region announces every change.

**Device and room — pass.** No overflow and nothing clipped at four viewport sizes in both
modes, light and dark. Every control exercised in sequence on a phone with every resulting
fit finite. Not yet checked on the lecture machine or in a compressed recording.
