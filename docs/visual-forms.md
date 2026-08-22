# Showing a quantity

The other documents cover why we build these (`principles.md`), how a widget is put
together (`widget-pattern.md`), and how it gets checked (`review.md`). This one covers what
to draw, and it exists because the graphical decisions recur across widgets while the
subjects do not.

Written from two builds. Expect it to be wrong somewhere by the fourth.

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

**Contrast is measured, not eyeballed.** The 3:1 minimum for a graphical object applies to
the line that shows where a pale area ends, which is easy to miss because the fill looks
fine on its own. In the MAUP widget the palest fill sat within 1.1:1 of the page and the
boundary carrying it was at 2.6:1.

---

## Base and figure

When symbols carry the data, the polygons become a base: a light fill, a hairline, and
nothing competing. The finest units stay drawn under every coarser grouping, so what an
aggregation throws away is never quite off the screen.

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
