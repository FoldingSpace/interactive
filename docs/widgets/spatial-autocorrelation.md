# Spatial autocorrelation on a grid

`web/spatial-autocorrelation/index.html` — one self-contained file, no dependencies.
Live: https://foldingspace.github.io/interactive/spatial-autocorrelation/

Written so the widget could be rebuilt from this description alone.

---

## The one thing

**Spatial autocorrelation measures whether nearby places resemble each other — and the
answer depends on what you decide "nearby" means.**

The second half is the part students usually miss, so the neighbour definition is a
control rather than a fixed choice.

## What it is

A 15 by 15 grid of squares, each either grey (1) or white (0). Pressing a square flips it,
and with a mouse you can drag to keep painting. Every change recalculates Moran's I and a
count of matching neighbours. A row of buttons loads ten fixed patterns.

The face of the widget carries very little text: the number, its scale, a one or two word
verdict, one short line, and the controls. Everything else sits behind the "?" button.

## The statistic

Moran's I with binary contiguity weights:

```
        n      Σi Σj w_ij (x_i − x̄)(x_j − x̄)
  I = ————— · ———————————————————————————————
       S0            Σi (x_i − x̄)²
```

where `n` = 225, `w_ij` = 1 if i and j are neighbours and 0 otherwise, and
`S0 = Σi Σj w_ij` is the number of ordered neighbour pairs. Weights are not row
standardised; they are plain binary contiguity.

**When every square is the same colour the denominator is zero and I is undefined.**
There is no variation to correlate. This is a real property of the statistic, not a
failure, and the two presets "All grey" and "All white" exist so that students meet it.
The interface says so in words instead of printing `NaN`.

I is not strictly bounded by ±1 — the achievable range depends on the weights — so the
scale bar clamps the marker to [−1, +1] and the number itself is printed unclamped.

### Neighbours

Two definitions, both binary contiguity on the lattice:

- **Sides only (rook)** — up, down, left, right. Interior cells have 4 neighbours,
  420 unordered pairs in total.
- **Sides and corners (queen)** — the eight surrounding cells. 812 unordered pairs.

### Verified values

Computed independently in Python and matched against the widget:

| Pattern | Rook | Queen |
|---|---|---|
| All grey / All white | undefined | undefined |
| Checkerboard | **−1.0000** | −0.0345 |
| Stripes | **0.0000** | −0.4828 |
| Stripes every 3 | +0.2679 | −0.0856 |
| Half and half | +0.9279 | +0.8931 |
| Patches | +0.5907 | +0.5348 |
| Big patches | +0.7240 | +0.6653 |
| Random 1 | +0.0382 | +0.0177 |
| Random 2 | −0.0471 | +0.0114 |

If a rebuild does not reproduce these numbers, the implementation is wrong.

These were checked three ways: the neighbour-list loop the widget uses, the same
calculation in Python, and a full weight-matrix formulation `(n/S0)·(z'Wz)/(z'z)` in
numpy. Stripes-every-3 was also derived by hand. With 75 grey cells the mean is 1/3, so
grey deviations are 2/3 and white −1/3. All 210 vertical pairs match (70 grey-grey, 140
white-white) and of the 210 horizontal pairs 135 differ and 75 are white-white, giving a
numerator of 70(4/9) + 140(1/9) + 135(−2/9) + 75(1/9) = 25 and a denominator of
75(4/9) + 150(1/9) = 50. So I = (225/840)(50/50) = **225/840 = 0.267857**, which is what
the widget shows. It is *not* near zero; the near-zero value for that pattern is the queen
one, −0.086.

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

### The patchy patterns

Fill the grid with `mulberry32` values, then smooth: replace each cell with the mean of
the square window of the given radius around it, clipped at the edges, repeated for the
given number of passes. Rank all 225 cells by smoothed value, descending, ties broken by
ascending index, and make the top 113 grey.

Ranking rather than thresholding fixes the number of grey squares at 113, the same as the
checkerboard and near enough the random patterns. **This is the point**: moving between
Random 1 and Patches changes the arrangement while holding the amount of grey almost
constant, so a student can see that autocorrelation is about arrangement, not about how
much of each colour there is.

Both the sort and the smoothing must match exactly or the pattern differs. The comparator
is `f[b] - f[a] || a - b`, and the mean is a plain running sum divided by the count — not
a pairwise or compensated sum, which would differ in the last bits and could reorder cells
near the cut.

**The random patterns use fixed seeds on purpose.** A student's phone and the projector at
the front must show the same grid, or the discussion falls apart. Never replace these
with `Math.random()`.

The opening state is "Patches" with rook neighbours. It shows clear positive
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

- **Narrow**: single column — heading, grid, readout, controls, presets.
- **Wide**: grid on the left, readout and controls in a sticky right column.

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
- `w` — `queen`; absent means rook.
- `present` — `1`; absent means normal size.

The URL is rewritten with `history.replaceState` on every change, so the back button is
not filled with every click.

## Accessibility

Measured, not assumed.

- Grid cells are 23.98 px on a 375 px viewport. **This is the one place we cannot reach
  the 44 px target size**: fifteen columns across a phone leaves 24 px, and the spatial
  arrangement is the content. It meets the 24 px WCAG 2.2 AA minimum and no more. Keyboard
  operation is the alternative route.
- All other controls are at least 44 px.
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
line. The rule behind this is now in `principles.md` section 6. Drag-to-paint was added.
Two patchy presets were added, which give the widget its first patterns that look like
real data rather than geometry, and which isolate arrangement from density.

Testing the drag found a real defect: pointer events arrive too sparsely for a fast
stroke, and the first implementation painted a dotted trail. Fixed by interpolating along
the line between positions.

**Not yet done:** a real projector in a lit room, and a compressed recording. Those need
the lecture machine.

## Known limits

- No significance test. A permutation-based reference distribution would let students see
  what "significant" means, and is the obvious next addition.
- No option to change grid size.
- Weights are binary, not row standardised. Row standardisation changes the numbers and is
  worth a future control.
- Dragging to paint works with a mouse or pen but not by touch, for the scrolling reason
  above. A press-and-hold to arm the brush would be one way round it if it turns out to
  matter.
