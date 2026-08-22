# Showing a quantity

The other documents cover why we build these (`principles.md`), how a widget is put
together (`widget-pattern.md`), and how it gets checked (`review.md`). This one covers what
to draw, and it exists because the graphical decisions recur across widgets while the
subjects do not.

Written from three builds. Expect it to be wrong somewhere by the fifth — and it already
has been once: the boundary rule below replaced an earlier one that was recorded here as a
finding. When that happens, say which won and why rather than quietly deleting the loser.

---

## Quantities on areas

**A count is not a rate, and a choropleth needs a rate.** Shading a polygon by a count
shades big areas dark for being big. This is the oldest mistake in thematic cartography and
it is easy to make in code, because the count is the column you have.

Two ways out, and they are not equivalent.

*Divide by something.* Per square kilometre, per thousand people, per household. The result
is a rate and a choropleth is right for it. But the denominator is a claim: crime per
resident says something different from crime per person present, and the MAUP widget carries
a note about exactly that, because most incidents happen where people are rather than where
they sleep.

*Draw graduated symbols.* A circle at each area's centre, area proportional to the value.
No denominator is needed, so no claim is smuggled in, and the count stays a count. This is
usually the better answer when the quantity really is a count.

**Symbols: area proportional to value, radius to its square root.** Anything else misleads,
including sizing by radius, which exaggerates large values by squaring them.

**Never clamp the radius.** A cap on the largest circles looks tidier and breaks the
proportionality, which is the only reason the symbols mean anything. If the largest circle
is too big, the scale is wrong, not the value.

**Size the biggest circle against the spacing between areas, not against the map.** Half the
mean spacing — `sqrt(mapWidth * mapHeight / areaCount) * 0.5` — leaves the largest touching
its neighbours and everything smaller clear of them. A fraction of the map width works at
118 areas and turns 996 into a single blob.

**A little transparency, no outline.** Overlapping circles have to read as overlapping, and
at these sizes a stroke is most of the symbol. About 0.68 opacity works.

**Draw big circles first.** Otherwise the small ones are buried and the map looks emptier
than the data is.

---

## How fine the grid has to be

**The narrowest thing that has to stay connected decides the cell size.** Not the file size,
not what looks smooth. `least-cost` went 100 m, 50, 33⅓, 22²⁄₉, every step for the same
reason: road allowances, rail and watercourses are narrower than the cell, so they rasterised
into dotted lines and a route could not follow one — which mattered, because following
existing corridors is one of the positions the widget exists to let a reader take. Blocks of
housing and farmland were fine at every size. Ask what the finest *linear* feature is and
whether anything depends on it being continuous.

The cost is quadratic and the answer to it is never a coarser map. Twenty times the cells
took a faster queue, then a worker, then sending the worker changes instead of the map — all
of which are in `widget-pattern.md` and `libraries.md`, and all of which were cheaper than
giving up the thing the resolution was for.

**Source polygons do not tile perfectly.** At a fine enough cell, a centre lands in a sliver
where two of them fail to meet. Fill those from their neighbours and print how many were
filled; keep a hard failure for more than a trivial count, because a real hole — a window
reaching outside the data — is a contiguous region rather than a scattering of single cells.
Do this in the extraction tool, so it fails the build rather than shipping a gap.

## Small multiples

**One scale across all of them, or they are unrelated pictures.** This is the whole
difference between a row that can be read across and a row that cannot. Pool the values from
every panel, take a high percentile of the absolute values, and scale everything to that.

**Same size, including the answer.** Making the result panel larger than the inputs says the
result is the important one and stops the areas being comparable straight across. The MAUP
widget had its result at 2.1 times the width of the terms and lost both.

**Equal heights make the alignment free.** Hold titles and labels to the same number of
lines and the operators between panels can simply centre; otherwise you end up guessing a
padding that is wrong at the next screen size.

---

## Showing that something decomposes

If a model says `y = a + b·x1 + c·x2 + e`, the row of maps can *be* that equation rather
than illustrate it. Each panel is a term, all in the same units, and with proportional
symbols the signed areas add the way the numbers do.

**Then check that they do.** Read the radii and fills back out of the rendered output and
sum the signed areas. The claim is about what a reader sees, so checking the model's
arithmetic is not enough. In the MAUP widget this caught the radius clamp: the values were
right and the circles were wrong by up to 21 per cent.

**Include the terms that are zero.** The spatial error term is exactly zero under an
aspatial model, and its panel stays in the row, empty. An absent panel hides an assumption;
an empty one shows the model declining to use something. Absence is a result.

**Include the constant, even though it is the same everywhere.** Mapping one repeated value
looks wasteful until you notice that without it the areas do not add up.

**Pick the model whose coefficients can be read.** A spatial lag model's coefficients are
not marginal effects — feedback through neighbours means interpreting them requires a direct
and indirect impact decomposition — so printing them beside ordinary ones teaches something
false. Choosing between models is a substantive claim, and the honest move is to make the
choice, show one, and say why.

---

## Colour

Sequential for quantities that run one way, diverging for quantities with a meaningful
middle, and the middle has to be the actual middle. ColorBrewer schemes marked safe for the
commonest colour blindness, every time, and the scheme named in the widget's own file.

For symbols carrying a sign, two colours is enough: one for above, one for below. A seven
class ramp on top of a size encoding is two variables doing one job.

**A categorical scheme with more than about six classes has to be searched, not chosen.**
Nine land use classes were picked by eye once and six pairs collided under simulated
deuteranopia, farmland against houses among them — the two largest classes on the map, half
its area between them, at a colour distance of 20 and a lightness difference of 2. Simulate
both deuteranopia and protanopia, score every pair on colour distance *and* lightness
difference, and weight the pairs by how much ground each class covers: confusing two classes
that are 1% of the map costs almost nothing, and confusing the two that are half of it costs
everything. Then accept that a residual collision among the small classes is the price of
nine categories, and give those classes a second cue — naming what is under the pointer does
it.

**Lightness is the cue that survives everything.** It survives both common forms of colour
blindness, greyscale, a projector, and a compressed recording. If the big classes are spread
across the lightness range, the map still works when the hue does not.

**A pale fill against a pale track has no visible edge, and the edge is the value.** A bar
chart coloured by category inherits whatever the category colour is, and measured, every
fill in one widget sat between 1.11:1 and 2.04:1 against its track. The fix is to stop
asking the fill to do two jobs: cap the end of the bar in the text colour, where it reads at
15:1, and let the hue carry identity alone.

**A page theme is not a map theme.** Dark mode should not invert cartography — pale land
under dark routes is right in both themes, and flipping it makes the land unreadable. What
does have to change is anything that has to pass a contrast ratio against the *page*: a
route's line colour and its label colour are then two different values of the same hue, and
they need separate variables.

**To show a region without recolouring it, turn everything else down.** Washing a
translucent tint over a set of cells fights whatever is underneath, and a tint that reads
over pale farmland goes muddy over water. Fading the cells *outside* the region towards the
page background leaves the region at full strength and its own colours, which is what a
reader wants to look at anyway.

**Measure the mark, not the box it sits in.** Reading `getBoundingClientRect()` on the
element gives you the slot, not the ink. A sign sitting in a 40 px column and a title line
17 px tall have different centres, so comparing element boxes reported perfect alignment
while the sign floated eleven pixels below the words. Put a `Range` over the text node and
take `getClientRects()[0]` — that is the line, and the line is what a reader sees. The same
mistake in a different costume as trusting the values behind a drawing instead of the
drawing.

**Repeated marks go in their own column, not at the end of a phrase.** An operator written
after each title lands wherever that phrase happens to end, so no two agree with each other.
Put the mark in its own grid item and draw it as many times as it has to appear; then
alignment is a property of the structure rather than a measurement to redo each time a label
changes length. In the MAUP row each operator is one element carrying its sign twice, once
level with the titles and once level with the maps, and the two share an x centre to within
a tenth of a pixel because they cannot do otherwise.

**A legend's rounded number must be drawn at the rounded number's size.** Round the value so
it reads — a key of 256 and 64 says "a quarter" where 257 and 64 says nothing — then size the
symbol from the value you printed, not from the value you rounded. Otherwise the key is
wrong by exactly the rounding, which is the one error a legend must not have.

**Contrast is measured, not eyeballed.** The 3:1 minimum for a graphical object applies to
the line that shows where a pale area ends, which is easy to miss because the fill looks
fine on its own. In the MAUP widget the palest fill sat within 1.1:1 of the page and the
boundary carrying it was at 2.6:1.

---

## Base and figure

When symbols carry the data, the polygons become a base: a light fill, one set of lines, and
nothing competing.

**Draw one set of boundaries, not two, and draw them in grey.** This file used to say the
finest units should stay drawn under every coarser grouping, so that what an aggregation
throws away is never quite off the screen. That is a good idea and it lost to a better one.
Two sets of lines under the symbols — hairlines for the fine units and heavier lines for the
units being analysed — is twice the visual noise at the exact scale the symbols work at, and
when the heavier set was near-black it buried the small circles outright. A map whose
smallest values cannot be seen has stopped being a map of those values.

So: only the units being analysed are outlined, and the line is a grey with measured
contrast rather than a black. In the MAUP widget that took the boundary from about 16:1
against the land to 4.16:1 — still comfortably past the 3:1 a graphical object needs, and
past it by enough to survive a projector, which is the case that decides it. The small blue
circles on the income map are legible now and were not before.

**A legend belongs to whatever it explains.** That widget's colour key sat inside the last
panel of a row of six, because that panel had room when it was written. It explains all six.
Moved under the row it is readable at every width, stops overflowing its panel on a narrow
window, and no longer competes for space with the size key that genuinely is about that
panel.

Open question, standing: the base says nothing about *where* this is. A reader gets shapes
without learning that the dark cluster is downtown. Naming two or three places would fix it
and would also start steering interpretation.

---

## After you change what is displayed

**Audit every control for whether it still controls something.** The MAUP widget carried a
"left map shows" control for a while after every map became a fixed term of an equation. Dead
UI is worse than missing UI, because a reader assumes it does something.

**Grep the captions, the footer, and the licence line.** Changing what is modelled leaves
stale claims in the places nobody looks. That widget credited a crime category it had
deliberately stopped using, and the line was live on the public site.

**List what a reader sees with everything closed**, at every size and in presentation mode.
See `principles.md` section 13.
