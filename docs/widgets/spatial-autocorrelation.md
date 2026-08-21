# Spatial autocorrelation on a grid

`web/spatial-autocorrelation/index.html` — one self-contained file, no dependencies.
Live: https://foldingspace.github.io/interactive/spatial-autocorrelation/

Written so the widget could be rebuilt from this description alone.

---

## The one thing

**Spatial autocorrelation measures whether nearby places resemble each other — "nearby"
is a weighting you design, and the single global number is just the average of what every
square contributes.**

The second half is the part students usually miss, so the weights are an editable picture
rather than a fixed choice between two options.

## What it is

A 15 by 15 grid of squares, each either black (1) or white (0). Pressing a square flips it,
and with a mouse you can drag to keep painting. Beside it is a second, smaller grid: the
**weights kernel**, 5 by 5, showing what counts as a neighbour of the square at its centre
and by how much. Both are editable and everything recalculates on every change. Ten
patterns and six kernels load from buttons.

The face of the widget carries very little text: the number, its scale, a one or two word
verdict, one short line, and the controls. Everything else sits behind the "?" button.

## Naming and colour

The headline reads **Global Moran's I**, so that it names itself against the Local
Moran's I beside it rather than leaving a student to infer the contrast.

**Filled squares are black, and the rules between them are grey.** They began as grey
squares with black rules, which left the pattern lighter on the page than the cluster map
beside it — wrong, since the pattern is the thing being explained. Black cells on white
carry more ink and the pair now balances. Measured: black against white 17.8:1, the grey
rule 3.45:1 against white and 5.14:1 against black, all clear of the 3:1 needed for a
graphical distinction.

The cluster map's internal rules are **white**, not grey. A grey rule measured 1.16:1
against saturated red, so regions blurred into solid blocks and cells could not be matched
one-to-one against the pattern beside them. White is also how cluster maps are normally
drawn. The kernel keeps dark rules, because its cells are shaded greys and a grey rule
would vanish among them.

### Clustered, random, dispersed

The scale reads **−1 dispersed · 0 random · +1 clustered**, which is the standard
vocabulary — it is what ArcGIS reports and what the textbooks use. Two traps come with it,
and both are addressed in the "?" panel rather than left to catch students out:

**Dispersed does not mean random.** A random scatter scores near zero, not below it. Below
zero means the squares take turns, which is a strong pattern of its own.

**Zero does not prove random.** It means the measure cannot tell this pattern from a random
one, which is not the same claim. The Stripes preset scores exactly zero and is obviously
not random. This is the one place where the widget's own label and its own evidence pull
against each other, so the panel names the tension and points at the preset that shows it.

## The statistic

Moran's I, with the kernel supplying the weights as a moving window clipped at the grid
edges:

```
        n      Σi Σj w_ij (x_i − x̄)(x_j − x̄)
  I = ————— · ———————————————————————————————
       S0            Σi (x_i − x̄)²
```

`n` = 225, `w_ij` is the kernel entry for the offset from i to j, and
`S0 = Σi Σj w_ij` is the total weight actually applied after edge clipping.

**Weights are used raw, never row standardised.** This matters: row standardisation gives
edge cells' neighbours larger shares than interior ones, which breaks the cancellation
that makes stripes score exactly zero (it becomes −0.0028) and shifts every other value.
The shading in the kernel shows each cell's *share* of the total, but that share is a
display, not the arithmetic.

**Only ratios matter.** Multiplying the whole kernel by a constant leaves I unchanged,
because S0 scales with the numerator. Verified: the rook kernel at weight 7 gives values
identical to weight 1 at every decimal place.

### When it is undefined

Two cases, both real results rather than failures, and both reachable from the preset
buttons on purpose:

- **Every square the same colour.** The denominator is zero; there is no variation to
  correlate.
- **No square counts as a neighbour.** S0 is zero. A kernel of all zeros is a legal thing
  to draw and the honest answer is that nothing has been asked.

### Neighbours

The kernel is a 5 by 5 block of whole numbers 0–9, indexed `(dr+2)*5 + (dc+2)`, read as
offsets from the square being measured. The centre, index 12, is permanently zero and not
editable: a place is not its own neighbour. A non-zero self-weight would add a term
proportional to the total variance and inflate I for reasons that have nothing to do with
space.

Edges are **clipped** — weights falling outside the grid are dropped, so edge cells simply
have less kernel. With a 5 by 5 kernel this affects 104 of 225 cells, 46 per cent of the
grid, against 25 per cent for a 3 by 3. Wrapping instead would make every cell's kernel
complete but would make the left edge neighbour to the right edge, which is false of any
real map, and it destroys the exact values: checkerboard becomes −0.8667 rather than −1.

### Verified values

Every kernel against every pattern, computed independently in numpy with a full
weight-matrix formulation and matched against the widget to two decimal places:

| Pattern | Rook | Queen | Half queen | Even | 1/d | 1/d² |
|---|---|---|---|---|---|---|
| Checkerboard | **−1.0000** | −0.0345 | −0.0345 | −0.0123 | −0.1146 | −0.2839 |
| Stripes | **0.0000** | −0.4828 | −0.4828 | +0.1476 | +0.0506 | −0.0603 |
| Stripes every 3 | +0.2679 | −0.0856 | −0.0856 | −0.2321 | −0.1362 | −0.0746 |
| Half and half | +0.9279 | +0.8931 | +0.8931 | +0.8158 | +0.8425 | +0.8634 |
| Patches | +0.5907 | +0.5348 | +0.5348 | +0.3859 | +0.4328 | +0.4730 |
| Random 1 | +0.0382 | +0.0177 | +0.0177 | −0.0129 | −0.0068 | +0.0011 |
| All grey / All white | undefined | undefined | undefined | undefined | undefined | undefined |

If a rebuild does not reproduce these, the implementation is wrong.

### Checks a rook-and-queen test cannot make

Reproducing rook and queen is a good first check but a weak one: both are symmetric,
binary and 3 by 3. A boolean coercion anywhere in the accumulation — treating any non-zero
weight as 1 — reproduces both *exactly* while computing every decay kernel as though it
were uniform. Four further checks catch what it misses:

1. **Scale invariance.** Kernel × 3 gives an identical result.
2. **A weight of 2 equals two contributions of 1.** Catches the boolean bug directly.
3. **Even, 1/d and 1/d² give three distinct values** on the same pattern. If any two
   coincide, weights are being ignored.
4. **Half queen equals queen exactly.** See below — this also confirms `S0` is summing
   weights rather than counting cells.

Stripes-every-3 was also derived by hand. With 75 grey cells the mean is 1/3, so grey
deviations are 2/3 and white −1/3. All 210 vertical pairs match (70 grey-grey, 140
white-white); of the 210 horizontal pairs 135 differ and 75 are white-white. Numerator
70(4/9) + 140(1/9) + 135(−2/9) + 75(1/9) = 25, denominator 75(4/9) + 150(1/9) = 50, so
I = (225/840)(50/50) = **225/840 = 0.267857**. Not near zero; the near-zero figure for that
pattern is the queen one at −0.086.

## Presets

Row `r` and column `c` both count from 0.

| Label | Rule |
|---|---|
| All grey | always 1 |
| All white | always 0 |
| Checkerboard | `(r + c) % 2 === 0` |
| Stripes | `c % 2 === 0` |
| Stripes every 3 | `c % 3 === 0` |
| Half and half | `c < 7.5` |
| Patches | smoothed field, seed 3141, radius 2, 1 pass, 113 grey |
| Big patches | smoothed field, seed 8080, radius 3, 2 passes, 113 grey |
| Random 1 | mulberry32, seed 20260819, threshold 0.5 |
| Random 2 | mulberry32, seed 77123, threshold 0.5 |

### Kernel presets

Digit strings are the URL encoding: 24 digits, row by row, centre omitted.

| Label | Kernel | Digits |
|---|---|---|
| Rook | 1 at N, S, E, W | `000000010001100010000000` |
| Queen | 1 at all eight surrounding | `000000111001100111000000` |
| Half queen | 1 at N, NE, E, SE | `000000011000100001000000` |
| Even | 1 at all 24 | `111111111111111111111111` |
| 1/d | rings 9, 6, 5, 4, 3 | `345434696459954696434543` |
| 1/d² | rings 8, 4, 2, 2, 1 | `122212484228822484212221` |

Ring order is by distance from the centre: 1, √2, 2, √5, 2√2.

**The decay ramps are rounded, and the rounding was chosen by measurement.** Scaling each
curve to K levels and comparing the resulting I against exact fractional weights:

| Levels | 1/d | worst error | 1/d² | worst error |
|---|---|---|---|---|
| 0–3 | 3,2,2,1,1 | 0.093 | 3,1,1,1,**0** | 0.180 |
| 0–4 | 4,3,2,2,1 | 0.040 | 4,2,1,1,**0** | 0.090 |
| 0–8 | 8,6,4,4,3 | 0.016 | **8,4,2,2,1** | **0.029** |
| 0–9 | **9,6,5,4,3** | **0.023** | 9,4,2,2,1 | 0.067 |

Three levels cannot represent 1/d² at all: the corners round to zero and three of the five
rings flatten to the same value. The cells accept 0–9, but **1/d² peaks at 8 rather than
9** — it need not use the top of the range, and halving cleanly (8, 4, 2, 2, 1) is both
more accurate and easier to read as an idea.

### Half queen, and why it matters

Half queen keeps north, north-east, east and south-east: four ones and four zeros, one
cell from each opposite pair. Because it is exactly half the queen ring, it returns
**exactly the same Moran's I as the full queen on every pattern**, to twelve decimal
places.

That is the point of it. The kernel plainly points one way, and the number does not move.
Since `z'Wz = z'((W+W')/2)z`, only the symmetric part of the weight matrix reaches the
numerator: **Moran's I cannot see direction.** A student who builds an eastward kernel to
detect an eastward process gets an answer that looks meaningful and says nothing about
direction.

Note that a non-antipodal choice of four — say N, NE, E, SW — coincides with queen on the
symmetric patterns but *not* on Patches (+0.5668 against +0.5348), so the exact identity
depends on picking one from each opposite pair.

This is stated in the "?" panel and nowhere on the face of the widget.

### The patchy patterns

Fill the grid with `mulberry32` values, then smooth: replace each cell with the mean of
the square window of the given radius around it, clipped at the edges, repeated for the
given number of passes. Rank all 225 cells by smoothed value, descending, ties broken by
ascending index, and make the top 113 grey.

Ranking rather than thresholding fixes the number of grey squares at 113, the same as the
checkerboard and near enough the random patterns. **This is the point**, and it is now `principles.md`
section 5: moving between Random 1 and Patches changes the arrangement while holding the
amount of grey almost constant, so a student can see that autocorrelation is about
arrangement, not about how much of each colour there is.

Both the sort and the smoothing must match exactly or the pattern differs. The comparator
is `f[b] - f[a] || a - b`, and the mean is a plain running sum divided by the count — not
a pairwise or compensated sum, which would differ in the last bits and could reorder cells
near the cut.

**The random patterns use fixed seeds on purpose.** A student's phone and the projector at
the front must show the same grid, or the discussion falls apart. Never replace these
with `Math.random()`.

The opening state is "Patches" with **queen** neighbours. Queen rather than rook because
rook cannot reach significance at all — the strongest result four neighbours can give
happens by luck about six times in a hundred — so a student who turns the test on under
the default would meet a dead end before meeting the idea. Rook is one click away and
`?w=rook` still names it. It shows clear positive
autocorrelation in the first second, and unlike the geometric patterns it looks like
something a student might actually map. "Start over" returns to it.

## Teaching notes

These are why the presets are the presets.

**Stripes scores exactly 0.00 under rook weights.** The pattern is unmistakable, and the
statistic reports nothing. Each cell's left and right neighbours differ from it while its
top and bottom neighbours match, and the two cancel. Moran's I is blind to structure that
runs in one direction only. This is the most valuable thing in the widget, and it is why
the near-zero message says "a clear pattern can still score zero" rather than claiming
the arrangement is random.

**Checkerboard goes from −1.00 to −0.03 when corners are added.** The same picture, a
different definition of neighbour, a completely different answer. Under queen weights the
four diagonal neighbours match while the four side neighbours differ, and they cancel.

**Stripes flips sign**, from 0.00 under rook to −0.48 under queen.

**All one colour is undefined**, which is worth dwelling on: a perfectly uniform map has
no spatial pattern to measure, because it has no pattern at all.

**Patches against Random 1** holds the amount of grey almost fixed (113 against 110) and
changes only the arrangement: +0.59 against +0.04. Spatial autocorrelation is about where
things are, not how many there are.

**The same pattern under six kernels** gives six different answers. Checkerboard runs from
−1.00 under rook to −0.01 under even weights. The pattern did not change; the question did.

**Half queen against Queen** does not move the number at all. See above.

## Local Moran's I

A second, read-only grid beside the data shows each square's own Moran's I, so you can
paint on the left and watch the right respond.

```
        n     z_i * sum_j w_ij z_j
  I*_i = —— * ————————————————————,     m2 = sum_i z_i^2 / n
        S0            m2
```

The `n/S0` factor is not in Anselin's definition. It is here for two reasons, and both
matter.

**The mean of the local values is then exactly the global I.** Verified for every kernel
and every pattern. Without the factor the identity is `global = sum(local) / S0`, which is
true but says nothing to a student; with it, the headline number is simply the average of
the map beside it. That is the whole framing of the feature, and it is checkable on screen.

**One colour scale then serves every kernel.** Raw local values scale with total kernel
weight: under 1/d² they run past ±40 while rook stays near ±3, and no fixed ramp could
show both. Rescaled, every kernel lands in about −1.1 to +1.4.

Undefined in the same two cases as the global number — one colour everywhere, or an empty
kernel — and the grid blanks.

### Two views

**Clusters is the default.** Every square is sorted into one of the four usual LISA
quadrants, with the conventional palette:

| Quadrant | Meaning here | Colour |
|---|---|---|
| High–high | black square among black | red `#ff0000` |
| Low–low | white among white | blue `#0000ff` |
| High–low | black among white | pale red `#f4ada8` |
| Low–high | white among black | pale blue `#a7adf9` |
| not significant | — | light grey `#eeeeee` |

Binary data makes the quadrants unusually concrete: `z` is above the mean exactly when the
square is black, so **high means black and low means white**, and the four categories read
as plain descriptions rather than jargon. A square whose lag is exactly zero is neither, and
is drawn neutral; this is possible but rare.

Verified counts, matched against numpy:

| Pattern / kernel | black in black | white in white | black in white | white in black |
|---|---|---|---|---|
| Patches / rook | 87 | 103 | 26 | 9 |
| Patches / queen | 89 | 101 | 24 | 11 |
| Checkerboard / rook | **0** | **0** | 113 | 112 |
| Checkerboard / queen | 0 | 84 | 113 | 28 |

Checkerboard under rook is the case worth showing: **every square is an outlier and none
is a cluster**, so the map is entirely pale. Nothing sits with its own kind.

**Local I** is the other view, kept because it is what makes the global number an average
you can see. ColorBrewer PuOr, symmetric and **centred at zero**, clamped at ±1.5.

**Neither view carries a second cue beyond colour.** This is a deliberate exception to
`principles.md` section 9. In the cluster view, red against blue survives the common forms
of colour vision deficiency reasonably well, but strong against pale — cluster against
outlier — does not survive greyscale or a compressed recording. Every cell's `aria-label`
names its quadrant and its value, which is the non-visual route. If it proves a problem in
a real room, marking the two outlier categories with a dot is the fix.

## Significance

A switch turns on a conditional permutation test, with Benjamini-Hochberg correction at
q = 0.05 applied by default. Squares that do not pass fade out on the same ramp rather
than switching to a different encoding, so turning it on drains the noise and leaves the
structure.

### Exact where possible, simulated only where necessary

**When every non-zero weight is the same — rook, queen, half queen, even — the p-value has
a closed form and is computed rather than simulated.** The neighbours are k squares drawn
without replacement from the other n−1, so the count of black ones is hypergeometric.
Exact, and it costs 3–10 ms.

This was prompted by the claim that Monte Carlo is used for p-values "because closed-form
solutions for that kind of thing are hard". True for the decay kernels, where the null is a
weighted sum over a random subset and has no tidy form; those still go to the worker. Not
true for the equal-weight case, where the closed form is elementary.

**And simulating it was doing active harm.** Compared against the exact answer on the same
grid, 999 permutations correlated at 0.998 (rook) and 0.982 (queen) — but reported a
smallest p of 0.040 under rook when the true smallest attainable is 0.0587. Nothing can be
that extreme. The handful of squares that "reached significance" under rook uncorrected
were the simulation inventing extremes that cannot occur. **With exact p-values, rook now
returns exactly zero**, and the widget's claim about it is exactly rather than
approximately true.

Two things worth separating, because they are constantly conflated:

- **Monte Carlo error** — noise from a finite number of shuffles. Shrinks as you run more,
  bounded below by 1/(R+1).
- **Discreteness of the null** — with k binary neighbours there are only k+1 possible
  outcomes, so the null has k+1 rungs. Under rook that is 15 distinct p-values, and it is
  15 whether you run 999 shuffles or ten million.

More simulation fixes the first and does nothing for the second. Simulation cannot
manufacture resolution that is not in the data, and if pushed it will manufacture the
appearance of it instead.

### Verified against the exact answer

Computed independently in Python from the hypergeometric, on the widget's own default grid:

| Kernel | uncorrected | FDR | smallest attainable p |
|---|---|---|---|
| Rook | **0** | **0** | 0.05865 |
| Queen | 148 | 148 | 0.00319 |
| Even | 166 | 166 | ~0 |

All three match the widget exactly, the uncorrected-equals-FDR coincidence included —
exact p-values on a strongly clustered pattern come out sharply bimodal, so the step-up
procedure rejects the same set as the flat threshold.

### What the test does

Each square keeps its own value while its neighbours are replaced by a random draw from
the rest of the grid, 999 times. The pseudo p-value is **one-sided, in the direction the
square actually leans**, which is the LISA convention and what GeoDa reports. A two-sided
test roughly doubles p; after correction it made no difference at all under queen and cost
about twenty squares under 1/d². **The seed is fixed**, for the reason in
`principles.md` section 5: a phone at the back and the projector at the front must agree
about which squares are significant, or the discussion falls apart.

The permutation shuffles the whole grid once per iteration rather than drawing
independently for each square. Both randomise a square's neighbours while it keeps its own
value; the difference is that a square's own value can land in its own neighbourhood, with
probability of roughly its neighbour count over 224 — under 2 per cent for rook, about 11
for the widest kernel. This was a performance decision: per-square drawing needs about
4,800 random numbers per permutation against 225, and the generator was the entire cost.

### The threshold is a control, and is named for what it is

Three values, 0.10, 0.05 and 0.01, shown only when a test is running. Because the masks
are derived on the main thread from the stored p-values, changing it is instant.

**Its name changes with the mode, because it is not the same quantity.** Uncorrected it is
the **significance level α** — the chance of calling one square remarkable when it is not,
a promise about each test taken alone. Corrected it is **q, the false discovery rate** —
the share of the squares actually marked that should be expected to be mistakes, a promise
about the map as a whole. Labelling both "how strict" would have blurred a distinction
worth teaching, and neither name is ours: both are the standard terms.

The p-values are **pseudo p-values**, since they come from shuffling rather than a
distributional formula, and 999 shuffles cannot produce anything smaller than 0.001.

The threshold also exposes the discreteness again: under queen, 0.10 and 0.05 select the
same squares, because eight binary neighbours admit only about nine distinct p-values and
none falls in that interval.

### Two thresholds, and why both are offered

The control has three states: off, **uncorrected**, and **corrected** by Benjamini-Hochberg
at q = 0.05. Uncorrected exists because that is where the lesson is: it is what a student
meets in software with the defaults left alone, and the gap between the two columns is the
cost of testing 225 things at once.

Squares passing, one-sided, 999 permutations, checked against an independent numpy
implementation:

| Pattern | Rook raw / FDR | Queen raw / FDR | 1/d² raw / FDR |
|---|---|---|---|
| Patches | 9 / **0** | 116 / **50** | 141 / 127 |
| Big patches | 13 / **0** | 138 / **83** | 158 / 150 |
| Random 1 | 1 / **0** | 13 / **0** | 7 / **0** |
| Random 2 | 9 / **0** | 7 / **0** | 22 / **0** |

**Random 2 under 1/d² is the demonstration**: 22 squares reach p ≤ 0.05 in a pattern with
no structure whatsoever, and correction removes every one. Switching between the two
buttons on that pattern is the whole multiple-comparison lesson in one click.

Masks are derived on the main thread from the p-values the worker returns, so switching
between uncorrected and corrected is instant rather than another 999 permutations.

### Grid extent is a control

A **Zoom / extent** toggle offers 15 × 15 (default) and 30 × 30. The grid containers keep
the same physical size and the squares halve, so the layout, the controls and the sense of
holding the same thing all survive the change. Rules drop from 2 px to 1 px at the larger
extent so the picture does not drown in lines; they are the grid's own background showing
through a `gap`, which keeps them exactly one rule wide however many cells there are.

### One lattice, clipped

Every pattern is generated once on the 30 × 30 lattice, and the smaller extent is a
**centred 15 × 15 window cut out of it**. A square therefore means the same thing at either
size, and the small grid shows less of the same world rather than the same world redrawn.
Verified: all eight patterns match their window exactly, cell for cell.

**Clipping is the only derivation that works for all of them.** Averaging 2 × 2 blocks gives
a 2–2 tie in every block of a checkerboard; sampling every other square turns a
checkerboard into a solid colour. Cutting a window leaves each pattern exactly what it was,
so the exact results survive: **checkerboard −1.00 and stripes 0.00 under rook at both
extents**.

**The patch seeds were chosen by search, and that is not a detail.** Clipping a window out
of a patchy surface lands somewhere black-heavy or white-heavy: the first seeds tried gave
67 per cent black in the window for Patches and 22 per cent for Big patches. At those
densities the small extent confounds how much black there is with how it is arranged,
which is precisely what `principles.md` section 5 exists to prevent. Seeds 209 and 1100
were found by searching for a centred window holding 113 black squares of 225 — the same
share as the full lattice — while staying visibly multi-blob at both sizes. Density now
holds at 50 per cent for both patterns at both extents.

The search ran in Node against a copy of the widget's own generator rather than a
reimplementation, because an earlier reimplementation of the same random number generator
silently diverged and cost a round of confusion.

**What the control shows, and what it turned out not to show.** Clipping holds the square
size fixed and changes only how much is on screen, so this is a change of *study area*,
not of scale.

It was built expecting to demonstrate statistical power — more squares, more tests to
correct for, but more real signal too, with the second winning. Measured, **it does the
opposite**, and the reason is worth more than the expectation was:

| Extent | Survive correction (Patches, 1/d²) | Global I (queen) |
|---|---|---|
| 15 × 15 window | 164 / 225 = **73%** | **+0.69** |
| 30 × 30 full | 606 / 900 = **67%** | **+0.62** |

The window sits over the middle of a large patch, so it is genuinely more clustered than
the whole surface. **Where the boundary is drawn changes the answer**, and here that effect
beats the power effect outright. That is a real and awkward problem in spatial analysis
rather than a defect, so the panel teaches it directly.

Under the earlier aggregation construction the power comparison *was* clean — 58 per cent
against 71 per cent — because the area was held fixed and only resolution changed. Clipping
buys uniform treatment of every pattern, including the checkerboard that aggregation
destroys, and pays for it by confounding the power comparison with the choice of window.
That trade is worth knowing if the control is ever revisited.

**The extent panel carries no citation, and that is the right answer.** It once invoked the
modifiable areal unit problem, which was apt while the control changed resolution. Under
clipping it is not: MAUP concerns the size and drawing of the units, and clipping changes
neither. Both sources were verified and are perfectly good; they were simply about
something else, so they were removed rather than stretched to fit. Raising a related idea
because you happen to have a citation for it is its own kind of dishonesty, and no citation
beats a nearby one.

The kernel is deliberately *not* scaled. It is measured in squares, so the same kernel is
a finer neighbourhood on the larger grid — which is the honest thing for it to be, and a
point worth making out loud.

Changing extent reloads the opening pattern. Carrying a drawing across would mean
inventing what the extra squares contain, so it starts clean and the legend says so.

**15 × 15 stays the default because of the phone.** At 30 × 30 squares fall to about 12 px,
half the 24 px minimum target size. The larger extent is for exploring on a desktop, not
for following along in a lecture theatre on a handset.

Cost at 900 cells: a paint frame goes from 14 ms to about 35 ms, and the permutation test
roughly quadruples. Both stay usable; neither blocks the interface.

### Would a bigger grid help?

Asked and tested, because more cells means more tests but also more true signal. Keeping
patch size proportional to the grid:

| Grid | cells | Rook | Queen | 1/d² |
|---|---|---|---|---|
| 15×15 | 225 | 0% | 71% | 78% |
| 21×21 | 441 | 0% | 75% | 83% |
| 27×27 | 729 | 0% | 81% | 84% |
| 33×33 | 1089 | 0% | 78% | 83% |

Power after correction rises modestly and then plateaus, because BH's threshold scales
with rank and so gains as the number of true signals grows. Rook stays at exactly zero at
every size, for the reason above.

**15×15 stays the default, and the reason is the phone**: at 21×21 cells fall to 17.2 px on
a 375 px viewport, below the 24 px minimum target size. 15×15 gives 24.1 px, which is the
floor. The default grid size is set by the hand holding it, not by the statistics.

**Note that the figures in the table above no longer describe the shipped control.** They
come from an experiment that held the area fixed and varied resolution. The extent toggle
as built clips a window instead, so it varies the study area at fixed resolution, and the
comparison it actually produces runs the other way — 73 per cent surviving on the window
against 67 on the whole. See "One lattice, clipped" above. The table is kept because the
question it answers, whether more cells buys power, is a real one and the answer is yes;
it simply is not what this control demonstrates.

### Corrections that were tried and rejected

**Bonferroni.** Returns zero on Big patches under queen, a pattern with a global I of
+0.67. Genuinely over-conservative, and why Anselin and GeoDa recommend FDR instead.

**Westfall-Young minP**, a permutation method controlling family-wise error that uses the
data's own dependence structure rather than assuming independence — which is the right
objection to raise, since neighbouring local Morans share data and 225 tests are nowhere
near 225 independent ones. Tested, and it returns **zero on every pattern**, including
Big patches with 160 squares passing uncorrected. The reason is resolution: with 999
permutations the smallest per-cell p is 1/1000, and the minimum across 225 cells is
essentially always 1/1000, so no observed value can beat it. minP needs permutations far
in excess of the number of tests, of the order of 10⁶ here, which is seconds of compute
rather than the 60–150 ms available. It also controls family-wise error, which is stricter
than false discovery rate and the wrong target for exploratory mapping.

**Bootstrap resampling.** Does not fit the null. Drawing neighbours with replacement makes
extreme neighbourhoods *more* likely by chance, inflating p rather than sharpening it, and
it does nothing about the discreteness that caps rook at 0.0608. Block bootstrap preserves
dependence for estimating a global statistic's variance, which is not the question being
asked here.

### Rook cannot detect anything, and the reason is exact

The strongest evidence four neighbours can offer is that all four match. Under the null
those four are drawn from the other 224 squares, so with the colours near balanced:

| Neighbours | P(all match) on 15×15 | on 33×33 |
|---|---|---|
| Rook, 4 | **0.0608** | 0.0622 |
| Queen, 8 | 0.0034 | 0.0038 |
| 5×5, 24 | ~0 | ~0 |

**0.0608 is above 0.05.** So under rook no square can reach significance even uncorrected,
whatever the pattern and however large the grid — Patches has a global I of +0.59 and
zero significant squares. The handful that do slip through an uncorrected test are noise
in the permutation, which is itself the point.

This is not the correction being harsh. Four binary neighbours cannot carry enough
information to be surprising. How many neighbours you count decides what is detectable at
all, which ties the significance test straight back to the kernel editor.

Rather than show a silent blank, the widget reports the smallest p-value any square
reached and says a kernel with more neighbours gives finer p-values. This ties the
significance test back to the kernel editor: the weights decide not only the answer but
whether anything is detectable at all.

## Explaining the choices

Every control that embodies a choice carries an **(i)** button opening a short panel: the
headline number, the second grid, the significance test, the kernel, and the extent. Each
says what the choice does, what it costs, and what it cannot do, in plain words but
without dropping the reasoning — a student who understands the trade is better served than
one given a simplified answer they will later have to unlearn.

Each panel ends with **For more, see:** and one or two sources. Per `principles.md`
section 11, none of those appear until an adversarial check has confirmed the work exists,
that its details are exact, and that it supports the claim attached to it.

The **(i)** and **?** buttons are 24 px — the minimum a target may be rather than the 44 px
the primary controls get. They sit inside a legend, where a 44 px hit area would overlap
the control row beneath.

## Performance

Significance runs on a **worker thread**, built from a `<script type="javascript/worker">`
tag via a Blob URL, so the page stays one self-contained file and there is only one copy
of the code — when Workers are unavailable the same source is compiled on the main thread.

Three optimisations, in the order they mattered:

1. **Shuffle once per permutation** rather than drawing per square: 225 random numbers
   instead of about 4,800. Took the worst case from 963 ms to 203 ms.
2. **Integer arithmetic in the hot loop.** The data is binary, so `z` takes only two
   values and the weighted lag is `S − mean·T`, where `T` is the square's total neighbour
   weight and `S` the total weight of its grey neighbours. The inner loop adds integer
   weights and does no floating-point at all. Worst case to about 150 ms.
3. **Incremental DOM writes.** Only cells whose colour or label actually changed are
   touched. A paint frame went from 42 ms to 14 ms, which is what makes dragging smooth.

Measured after warm-up: 57 ms (rook) to 150 ms (even weights), with the UI blocked for
none of it. A matrix library would not help — this is a sparse product, about 4,800
non-zeros in a 225 × 225 matrix, and a dense routine would do ten times the arithmetic.
The remaining avenue, if it is ever needed, is that for equal-weight kernels the null
distribution of the neighbour count is hypergeometric and could be computed exactly with
no simulation at all.

## The kernel editor

Click a cell to step its weight up, wrapping from 9 back to 0; shift-click or right-click
steps down. On a keyboard, arrow keys move around the kernel and alt-up, alt-down, `+` or
`−` change the weight under the cursor.

Each cell shows **its number, shaded by its share of the total**. The numeral carries the
meaning and the shading reinforces it, because nine levels of grey will not survive a
projector, a compressed recording, or a colour-blind reader. Shading runs from white at
zero to 52 per cent lightness at the largest weight — the floor is set by contrast, since
the numeral must keep 4.5:1 against its own cell. Measured worst case is 4.81:1, a 9 on
`rgb(133,133,133)`. Zero cells are left blank rather than showing `0`, so the shape of the
kernel reads at a glance.

A preset button lights up when the kernel matches it exactly, and goes dark the moment a
cell is edited.

## Painting

Pressing a square sets it to the opposite of what it was, and that colour becomes the
brush: dragging then paints every square crossed with the same colour rather than toggling
each one. Press on grey to erase a swathe, on white to draw one.

Pointer positions arrive in jumps, so a quick drag reports a position several squares on
from the last. The path between consecutive positions is filled by stepping along the
straight line between them, `max(|Δrow|, |Δcol|)` steps with rounding. Without it a fast
stroke comes out as a dotted trail — which is exactly what the first test showed.

**Dragging is for mouse and pen only.** On a touch screen the grid fills the display, and
capturing drags there would take away the ability to scroll the page. Touch keeps
tap-to-toggle. `pointerdown` checks `e.pointerType !== "touch"` before arming the brush.

Keyboard activation still works because a click generated by space or enter has
`e.detail === 0`, and the click handler acts only on those; pointer input is handled
entirely by the pointer events.

Two layouts, split at 56rem, following `docs/principles.md` section 3.

- **Narrow**: single column — heading, data grid, local grid, readout, kernel, patterns.
- **Wide**: the two grids side by side on the left; readout, kernel and patterns stacked
  in a right column.
- **Wide and presenting**: four columns — data grid, local grid, readout, kernel — with
  the pattern buttons as one wide row beneath. Stacking the grids made the left column
  taller than any projector; going sideways uses the shape a projector actually has.

Two layout traps, both found by measuring rather than looking. The significance sentence
is one long line, and inside an `auto`-sized grid column it stretched that column and
pushed the controls off screen — the wrappers are now pinned to the grid width. And a
stale `body[data-present="1"] #grid` rule from the previous layout outranked the media
query on specificity, forcing the grid to 435 px inside a 282 px wrapper.

### Presentation mode

The reusable mechanism, settled here for the first time and intended for reuse.

A single custom property `--ui` multiplies every size through `calc()`. Normal is `1`;
`body[data-present="1"]` sets `1.28`. Text stays in `rem` so a reader's own font-size
preference still applies on top. Entered by `?present=1`, by the "Big screen" button, or
by pressing `p`.

Presentation mode also hides the intro paragraph, the keyboard instructions, and the
footer, and on wide screens pins `.wrap` to `100vh` with tightened spacing so the pattern
buttons stay on screen. A presenter cannot scroll mid-lecture. The readout column carries
`overflow-y: auto` as a safety net so a control can never be clipped entirely.

The scale factor is deliberately modest. 1.28 was reached by testing at 1280×800 until
everything fit; larger values pushed the preset buttons off screen.

## URL state

The whole configuration lives in the query string, so a particular case can be put on a
slide or handed out.

- `g` — the 225 cells packed into 29 bytes, little-endian bit order within each byte,
  then base64url with padding stripped. Roughly 39 characters.
- `k` — the kernel as 24 digits, row by row, centre omitted. Absent means queen.
- `w` — `rook` or `queen`, honoured as shorthand when `k` is absent, so links already
  written on slides before the kernel editor existed still work. `k` wins if both appear.
- `sig` — `1` turns the significance test on; absent means off.
- `view` — `values` shows local I as a continuous ramp; absent means the cluster map.
- `present` — `1`; absent means normal size.

The URL is rewritten with `history.replaceState` on every change, so the back button is
not filled with every click.

## Accessibility

Measured, not assumed.

- Kernel cells are 36 px on a 375 px viewport, and the numeral holds at least 4.81:1
  against its own shading.
- Grid cells are 23.98 px on a 375 px viewport. **This is the one place we cannot reach
  the 44 px target size**: fifteen columns across a phone leaves 24 px, and the spatial
  arrangement is the content. It meets the 24 px WCAG 2.2 AA minimum and no more. Keyboard
  operation is the alternative route.
- The pattern buttons, kernel presets, view, significance and threshold controls are at
  least 44 px. The inline **(i)** and **?** buttons are 24 px, which is the minimum a
  target may be rather than the 44 px target size — they sit inside a legend, where a
  44 px hit area would overlap the control row beneath. An earlier draft of this file
  claimed every control was 44 px; that was never true of the ? button.
- Contrast: body text 17.8:1; secondary text 6.3:1; grey against white cells 4.1:1; cell
  borders 3.4:1 against grey and 14.2:1 against white; control borders 3.4:1 light and
  4.0:1 dark; focus ring 6.4:1. The control border started at 1.9:1 and was darkened after
  measurement.
- Colour is never the only cue for a control: pressed buttons invert, not just tint.
- The grid is a `role="grid"` of buttons with roving tabindex. Arrow keys move, Home and
  End jump along a row, space toggles. Each cell announces "Row 3, column 5, grey".
- A visually hidden `aria-live="polite"` region announces the new value after each change.
- The explanation panel is a button with `aria-expanded` and `aria-controls`, not a
  tooltip, so it is reachable by touch and by keyboard. `title` tooltips carry nothing a
  reader needs.
- `prefers-reduced-motion` removes the marker transition.
- Light and dark themes both defined; the grey and white cells never invert, because
  "grey means 1" must not flip.

## Review record

Reviewed 2026-08-19 against `docs/review.md`.

**Pedagogical critique — changes requested and applied.** Two findings. First, the
near-zero message read "About what you would get by shuffling the squares at random",
which is false for the Stripes preset: it scores exactly zero while being obviously
patterned, and the wording would have taught students to read 0 as "no pattern". Replaced
with wording that reports what the statistic says and points back at the grid. Second, the
neighbour buttons used only plain language, leaving no bridge to the literature; the
technical terms now appear in smaller type beside them.

**Text — pass.** Short sentences, no idiom, technical terms defined where they appear.

**Accessibility — pass with one documented exception**, the 24 px cell size above.

**Device and room — pass.** Checked at 375×812 and 1280×800, in normal and presentation
mode, with no horizontal overflow at either size. Presentation mode initially clipped the
pattern buttons at 1280×800; fixed before release.

**Revised 2026-08-19, second pass.** Three changes on instruction. On-screen text was cut
hard — the intro paragraph, the sentence-long verdicts, and the footer all moved behind a
"?" disclosure, leaving the number, the scale, a one or two word verdict, and one short
line. The rule behind this is now in `principles.md` section 8. Drag-to-paint was added.
Two patchy presets were added, which give the widget its first patterns that look like
real data rather than geometry, and which isolate arrangement from density.

Testing the drag found a real defect: pointer events arrive too sparsely for a fast
stroke, and the first implementation painted a dotted trail. Fixed by interpolating along
the line between positions.

**Revised 2026-08-19, third pass: the weights kernel.** The rook and queen buttons are
replaced by an editable 5 by 5 kernel with six presets, so "what counts as a neighbour"
becomes a picture a student designs rather than a word they are told. Decided in a
grilling session; the reasoning is recorded above where it bears on the numbers.

Design questions that turned on evidence rather than taste: row standardisation was
rejected because it destroys stripes = exactly 0; the range is 0–9 but 1/d² peaks at 8
because it rounds better; the kernel is 5 by 5 because 3 by 3 has nothing to add beyond
queen and cannot express decay; edges stay clipped because wrapping loses every exact
value; presentation mode went to three columns because the kernel does not fit vertically
(it has since gone to four, as more was added).

Verification found no errors this pass. The one mismatch during testing was in the
checking script, not the widget — a hand-typed kernel string.

**Known and accepted:** the direction-blindness demonstrated by Half queen is documented
in the "?" panel only, with no on-screen warning when a kernel is asymmetric. A student
who builds a directional kernel without opening the panel has no signal that the statistic
is ignoring what they drew. This was a deliberate call against putting a warning on the
face of the widget.

**Revised 2026-08-19, fourth pass: local Moran's I.** A second grid shows each square's
own local I, with an optional permutation test corrected for false discovery rate. Decided
in a grilling session.

What the evidence settled: the `n/S0` rescaling, because it makes the global number the
plain average of the local map and lets one colour ramp serve every kernel; FDR by default,
because both random patterns then correctly give zero where uncorrected they show 3 to 15;
and naming the cause when rook can detect nothing, because a silent blank map reads as a
statement about the pattern when it is a statement about the weights.

Two bugs found by testing rather than reading. Significance results lagged one edit
behind: an "in flight" flag stopped a new request being issued mid-computation, so the
previous state's answer was applied to the current state. Replaced with a key on the state
actually requested. And the presentation layout was broken by a stale rule from the
previous pass that outranked its replacement on specificity.

**Known and accepted:** no second cue for the sign of a local value, so cluster and
outlier are indistinguishable in greyscale, on a projector, and to a colour-blind reader.
Recorded above as a deliberate exception.

**Scope watch.** The widget now teaches four things: what autocorrelation measures, that
the weights are a design choice, that the global number decomposes into local ones, and
that testing 225 things at once has a cost. `principles.md` says to split when the one
thing takes more than a sentence. Not split yet, but this is the point to watch.

**Revised 2026-08-19, fifth pass: the cluster map.** The second grid now defaults to the
four LISA quadrants in the conventional red and blue, with the continuous local I ramp
kept as the alternative view. Binary data makes the quadrants concrete — high is grey, low
is white — so red means a grey square among grey and the pale colours mean the odd one
out. Checkerboard under rook becomes an entirely pale map: 225 outliers, no clusters.

The legend's technical terms are hidden in presentation mode, because the wrapped labels
made it 90 px tall and pushed the pattern buttons off screen, and nobody reads
"high-high" in small type from the back of a room.

**Revised 2026-08-20, sixth pass: weight and wording.** Filled squares went from grey to
black with grey rules, so the pattern stops sitting lower in the page's visual hierarchy
than the map explaining it. The headline became Global Moran's I. The scale gained the
standard clustered / random / dispersed vocabulary, with both of its traps written into
the "?" panel. The cluster map's rules went white, after measuring a grey rule at 1.16:1
against red.

Presentation mode needed rebalancing again: the significance control moved to the kernel
column and the scale multiplier came down to 1.15. It now fits 1280 × 800 exactly, with
nothing clipped. **That is the binding case, not a projector** — a 1920 × 1080 display has
half again as much vertical room, and the sizes are in `vh`. If this widget gains anything
more, the laptop-mirroring-a-projector case is what will break first.

The readout card is aligned to the **tops of the grids**, not to their captions, by an
`aria-hidden` spacer carrying the caption's own class — so it tracks any change to caption
size automatically — with a negative margin cancelling the difference between the readout's
column gap and the gap beneath a caption. Presentation mode uses a tighter gap and needs
its own compensation.

Two more CSS traps, of the same family as the last: `.key { display: grid }` is an author
style and outranks the browser's `[hidden] { display: none }`, so the quadrant legend
stayed visible in the other view until an explicit `.key[hidden]` rule was added. And a
rule inside a media query still loses to an identical-specificity rule written later in
the file: media queries add no specificity, so `.spacer { display: none }` further down
beat `.spacer { display: block }` in the wide-screen block until the latter was written
`.readout .spacer`.

**Not yet done:** a real projector in a lit room, and a compressed recording. Those need
the lecture machine.

## Known limits and open threads

Two are stale entries removed: there **is** a significance test, and the grid size **is** a
control. What remains:

**The cutoff is arbitrary, and the widget cannot show that it is.** Every kernel here draws
a hard line — everything within two squares counts, everything beyond counts nothing — and
that step function is a convenience, not a claim anyone defends. Tobler's line is that near
things are *more* related, not that distant things are unrelated. A student can already see
that where the line falls changes the answer (checkerboard reads −1.00 under rook and −0.03
under queen), but not what happens as the line recedes.

**The obvious experiment, not yet run:** let the neighbourhood grow — a larger kernel, or an
"everything, weighted by 1/d²" option with no cutoff at all — and watch the number as it
does. The expectation is that it drifts toward zero as distant unrelated pairs swamp the
near ones, which would itself be the argument for having a cutoff. That is a guess and
should be computed before it is written down anywhere a student can read it. Note that
a complete weights matrix is a modelling choice, not a null: the null here is spatial
randomness, and the weights never enter it.

**Weights are not row standardised, and there is no control to switch.** Standardising
changes every number — stripes stops being exactly zero — and that trade is itself
teachable. A toggle would make it visible.

**The kernel is fixed at 5 by 5**, so no decay beyond two squares can be expressed. This is
the same limitation as the cutoff point above, seen from the implementation side.

**Dragging to paint is mouse and pen only.** On touch the grid fills the display and
capturing drags would take away scrolling. A press-and-hold to arm the brush would be one
way round it if it turns out to matter.

**Not yet checked against a real projector in a lit room**, or in a compressed recording.
Those need the lecture machine.

## Picking this up again

Everything is deployed at
https://foldingspace.github.io/interactive/spatial-autocorrelation/ and the repository is
`FoldingSpace/interactive`, pushed over the deploy key described in `deployment.md`.

The verified numbers in this file are the regression suite. Reproduce them before trusting
any change: the exact values (checkerboard −1.0000, stripes 0.0000 under rook at both
extents), the kernel × pattern table, the quadrant counts, and the exact p-values (rook 0,
queen 148, even 166 on the default grid).

Local preview: `python3 -m http.server 8791 --directory web`, then
`http://localhost:8791/spatial-autocorrelation/`. Verify statistics in Python with numpy by
a different route from the widget's own; verify anything involving the random generator by
running the widget's actual source in Node, never a reimplementation.
