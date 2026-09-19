# Proposal: the pairwise weights page

**Status: a proposal, not a widget.** Nothing under `web/` exists for this yet. This file is
stage 1 of the three stages standing decision 51 sets out: Opus tests `123ahp.com` and confirms
the arithmetic independently, then proposes; Fable critiques and iterates until the two agree;
then the page is built, put through the five passes of `../review.md` and the rule-12 review,
and deployed. Written 19 September 2026 under `BATCH-370-AHP-1`.

**Revision 2, 19 September 2026.** Revised in place against the supervisor's stage-2 critique.
Every change is listed at the foot under *Revision 2, what changed and why*, including the two
places where the critique and this file still disagree.

It follows the six required parts in `README.md`, in proposal form. Where a number appears it
was computed for this file rather than carried over, and the working is in the scratchpad files
named at the foot.

**Scope, and the copyright position.** This page implements a published method, which is
mathematics and is not anybody's property: Saaty's pairwise comparison, the principal
eigenvector, and the consistency ratio against a random index. Nothing of `123ahp.com` is
reproduced or imitated. Not its layout, not its wording or labels, not its chart designs, not
its page sequence, not the names it gives its own screens, and not a line of its code. The page
is scoped to what a student in this course needs in order to do this lab, not to everything that
site can do, and section 5 lists what it deliberately leaves out. Screenshots of the site taken
for this batch are evidence of how the handout's steps behave today: they stay in
`review-log-370-AHP-1.md` and reach neither this file nor the page.

Companion record: `370 lecture and website work/review-log-370-AHP-1.md` holds the session's
working notes, the raw observations of `123ahp.com`, and the decisions taken while writing this.

---

## 1. The one thing it teaches

**Vague words become firm numbers. The order of the numbers survives disagreement about how
strong the words are. It does not survive disagreement about which way they point.**

Decision 51's own sentence said the first two of those and joined them. Three sentences say it
better, and the third is what the measurements in section 3 actually show.

An expert writes three ordinary English sentences. Somebody reads them and turns them into three
numbers. Different readers reach different numbers. The map that follows is not the same map.
What holds still is which factor comes first, for as long as the readers are arguing about
strength. The moment two readers differ about which of two factors is the more important, the
order goes too, and the page can show that happening in one step.

### The objection: "AHP is a form"

`lecture-widget-suggestions.md` says of L05 objective 4 that AHP is a form, which is the reason
it was not put in the build queue. The objection is fair and it is about the site rather than
about the method. The tool the lab currently sends students to is a form: you set three values,
you step forward until it stops, you copy three numbers out. Nothing you do there teaches you
anything, because a form hands back one answer and never shows you the answer next door.

What a control buys, and a static figure cannot, is the *neighbourhood* of an answer. Three
things are visible only when something moves.

The first is that the rank order holds still while the numbers move. Hold the botanist's two
aspect statements at 5 and 3 and walk the third comparison, the one she called equal, across
its whole range from "slope nine times elevation" to "elevation nine times slope": aspect stays
first in all seventeen positions, at between 58.9 and 65.9 per cent. Elevation runs from 6.7 to
34.4 per cent over the same walk, which is a factor of five. A figure can print one of those
eighteen states. Only a control can show that the winner is a fact about the botanist's
sentences while the percentages are a fact about whoever encoded them.

The second is what the consistency ratio actually measures. The handout's caution in cell 74
predicts a failure that a careful reading will not produce. That is now measured. Of eleven
defensible readings of the botanist's three sentences, the worst consistency ratio is 0.0810
against a bar of 0.10. But of the 4,913 configurations the control can reach, 3,826 are at or
above 0.10, which is 77.9 per cent of the range. Both halves have to be said. A student who has only been told the first will draw
the wrong conclusion from it. The ratio is easy to pass *if you
are saying something coherent* and hard to pass otherwise. You can only see that by moving the
control and watching where the number goes.

The third is the contradiction. Set elevation three times slope, slope three times aspect, and
aspect three times elevation. The method returns exactly a third each and a ratio of 1.149. The
equal thirds are not a finding about the three criteria. They are the method declining. A
calculator that prints a third three times and says nothing teaches the opposite. This is
`../principles.md` section 6 in its purest form. It is the single strongest argument that
this should be a widget rather than a link.

So the objection stands against the form and not against the subject. The page is not a
calculator with explanations bolted on. It is a page about how much a number is allowed to move
before an argument changes, which happens to also compute what Lab 2 needs.

---

## 2. Face and layers

### The face, with every panel closed

Above the fold, in the reading flow, about fifty words (`../principles.md` section 13):

> Three numbers below decide what a survey looks for. They did not come from the ground. An
> expert wrote sentences. Somebody read them and decided how strong each word was. You are that
> reader here. Two readers do not agree. The map that follows is not the same map.

Forty-nine words. M1 of the rule-12 review below asked for this wording in place of a draft that
said "somebody" and left it there. The reader is now named as the one making the choice. No
plant, no place and no named expert appear, per decision 51 and the supervisor's answer to
question 5; section 4 records when the word comes back.

Then the title, the three comparison controls, the three weights, the ratio with its verdict and
its one line, and the controls for presets, names, saving and reset. Nothing else is on screen
at rest. The five-second audit of that list is at the end of this section.

### The calculator

**Three comparisons, as stepped controls.** Each comparison is one row. The row names its two
criteria at its ends. Between them sits a single stepper: a minus button, a wide text readout,
a plus button. The stepper walks one ordered axis of seventeen positions, from "Aspect 9 times
Slope" at one end, through "equal" in the middle, to "Slope 9 times Aspect" at the other. The
readout is words and a number together, at the size the headline number gets, because a student
at the back has to see which control moved and what it now holds.

One control per comparison, not two. The obvious alternative was a side toggle plus an amount
stepper, which is six controls for three facts and makes "equal" a state you have to reach by
setting two things. Rejected.

A slider was rejected too. There are seventeen states and no meaning between them. Section
3 asks for a stepped control on touch. Nothing on this page drags.

Above each stepper, a strip of seventeen ticks shows where on the axis you are. On a desktop
the strip is also clickable, so a mouse can jump straight to a position; on touch it is a
position cue only, and the stepper is the route. That satisfies the rule that everything
reachable by hover on a desktop has a tap route on a phone, because the stepper is always the
primary control and the strip never holds anything the stepper cannot reach.

**Three weights, as bars with their numbers.** Two decimals, as percentages, summing to 100.
Bars are drawn against 100 per cent and not against the largest weight. A bar scaled to the
largest value is always full width whatever that value is, so nothing can be read off the
picture. Scaled to 100 the picture carries the number.

Naive rounding to two decimals does not always sum to 100.00. Of the eleven readings below,
four do not: two give 99.99 and two give 100.01. So the page uses a largest-remainder rule,
rounding down and giving the spare hundredths to the largest residuals, and the displayed three
sum to exactly 100.00 always. This is worth getting right because cell 86 of the handout tells
students the values must add up to 100 before they go into the Suitability Modeler.

**The ratio, as a number, one word and one line.** The number to four decimals, because that is
what the lab records. Beside it one word: **agree** below 0.10, **disagree** at or above.
Settled by the supervisor at stage 2, and settled well: neither word is evaluative, and both
read straight into the line beneath them, which is on the face and not in a panel.

> This measures whether your three comparisons agree with each other. It says nothing about
> whether they are right.

**Eighteen words, counted.** Revision 1 of this file called it twenty-three, the supervisor's
critique repeated that figure back, and it is wrong: the sentence has eighteen words. Nobody had
counted it. `../principles.md` says a sentence that states a measurement needs a test or it goes
stale silently, and this one went stale before it was a day old. The line itself is unchanged,
and it is the most important sentence on the page. Without it the number and the word read as a
pass mark.

In the opening state, where nothing has been said yet, that line is replaced by one saying so,
and it takes over as soon as the first comparison moves. The two never share the face.

**Save the chart as an image.** The page draws the weights chart into a `<canvas>` and offers
one 44-pixel button that hands over a PNG. No hover, no right-click, no long-press required for
the primary route. The mechanism is `canvas.toBlob` into an `<a download>`; where that fails,
which is the older iOS Safari case, the same PNG is shown as an `<img>` under the button with a
line saying to press and hold it to save. `navigator.share` with a `File` is offered where the
browser has it.

The saved image carries more than the site's does: the three criterion names, the three
comparisons that produced the weights, the three weights as percentages, the ratio, and the
date. Question 8 asks for "the image of your AHP results" and is marked at one mark for it. An
image that records its own inputs is a better answer to that question than a bar chart that
does not. It also lets a marker see in one glance whether the weights follow from the
comparisons.

**Editable criterion names.** Three text inputs, the names carried in the URL. The page opens on
Elevation, Slope and Aspect because that is what Lab 2 asks for. A student in a different
course types their own.

**Reset.** One tap back to the opening state.

### The lesson, one "?" down

A single disclosure holding the short version of section 1: what the ratio is, what it is not,
that two readers of the same sentences get different numbers, and that the order survives.

### What the method cannot do

`../principles.md` section 6 asks that each of these be a preset reachable in one click rather
than a paragraph, and that the page say something on screen at the moment it happens.

**The contradiction.** A preset. On screen at that moment: the three weights read 33.33 each,
the ratio reads 1.1494 with the word **disagree** beside it, and a line says that the three
statements cannot all be true together, so the equal thirds are the method refusing rather than
an answer. Without that line the screen
is three identical bars, which reads as a statement about elevation, slope and aspect when it is
a statement about the person who typed the comparisons.

**The bar is about you, not about the world.** A perfectly coherent set of three comparisons
gives a ratio of exactly zero whatever the numbers are. Elevation six times slope, elevation
eighteen times aspect: ratio zero. So does the dominance preset, at 81.82 / 9.09 / 9.09. On the
face this is carried by the eighteen-word line above, which says it in the students' own
words. The worked demonstration is one layer down, because two sentences saying the same thing
on the face costs more than it buys.

**Failing the bar is usually arithmetic, not a cycle.** Of the 4,913 reachable configurations,
1,024 (20.8 per cent) are cycles of the contradiction's kind. Of the 3,889 that are not cycles,
2,802 still fail the 0.10 bar. So the vivid failure is the rare one, and the ordinary way to
fail is to say three things that do not multiply through. The panel says this and the presets
give one of each.

**The near-zero ratio for a sensible reading, said on screen.** Eleven defensible readings of
one set of three hedged sentences run from 0.0000 to 0.0810 against a bar of 0.10. The page says that
following the three sentences carefully will pass the bar, in the same breath as saying that
most of the control's range does not. Both halves, or the sentence teaches something false.

**The method cannot tell you a criterion is missing.** Nothing on the screen can report that
nobody asked about soil, or about who owns the land. One layer down, in the "?" panel, settled
by the supervisor at stage 2 against this file's first proposal of putting it on the face. The
reason given is right: the face already carries the argument, in the framing sentence, and a
second claim of the same size competes with it rather than adding to it.

**With three criteria the choice of method does not matter, and at four it does.** The principal
eigenvector and the geometric mean agree exactly for a three by three reciprocal matrix. Over
20,000 random three by three matrices the largest difference in any weight was 1.1e-12, which is
the power iteration's own tolerance. Over 20,000 random four by four matrices it was 0.216, which
is a fifth of the whole scale. So on this page "which method" is a question that cannot be made
to matter. The page says so rather than implying that the answer it gives is the only one
available. This is also the strongest defence of the three-criteria limit.

### Presentation mode

`?present=1`, the `p` key, and a button, exactly as the template does it. One `--ui` custom
property through `calc()`. The intro and the explanation panels hide; the comparison readouts,
the three weights, the ratio and its verdict stay. The **For the classroom** panel stays, per
section 16, and it is the only one that does.

The thing to watch here is that the comparison readouts are words, and words at 1.28 times are
long. The tick strip may have to go on a projector while the stepper and its readout stay. That
is a measurement to make on the build, not a decision to take now.

### State in the URL

```
?c12=1&c13=-3&c23=-5&n=Elevation,Slope,Aspect
```

`c12` compares criterion 1 with criterion 2, `c13` criterion 1 with criterion 3, `c23` criterion
2 with criterion 3. The value is signed: `+k` means the first of the pair is k times as
important, `-k` means the second is, and `1` means equal. So the encoding that reads the third
comparison as equal, the third criterion as three times the first and five times the second, is
`c12=1&c13=-3&c23=-5`.

Signed parameters accepted by the supervisor at stage 2. Unsigned cannot say which side, and
which side is half of what a comparison is. The alternative would have been a fraction,
`c13=0.3333`, which is worse to read off a slide.

**Three criteria is fixed in the code, not only in the opening state.** Settled at stage 2. The
`n` parameter is read as a comma-separated list and only its first three entries are used; a
fourth name is ignored rather than honoured or reported as an error. So no URL anyone writes can
turn this into a four-criteria page by accident.

Parameters holding their default are omitted, so the link a student is given is short.
`history.replaceState`, debounced by a third of a second, per `../widget-pattern.md`.

### The two layouts

**Touch, portrait.** One column. The framing sentence, the title, then the three weights with
their bars, then the ratio and its verdict, then the three comparison steppers, then the presets,
the name fields, save and reset. The result sits above the controls because the controls are
what the thumb reaches for and the result is what the eye returns to. Each stepper is a full-width
row: the left criterion's name, a minus button, the readout, a plus button, the right criterion's
name. Buttons are 44 by 44 with space between them. The tick strip sits under the readout at
about 8 pixels tall and is not a target.

**Desktop.** Two columns at 56rem and above. Left: the three comparison rows, each now wide
enough for a seventeen-position clickable strip at about 36 pixels a position, with the stepper
still beside it. Right: the three weight bars, the ratio, the verdict, the save button and the
presets. The framing sentence spans both.

Nothing drags anywhere, in either layout.

### The five-second audit

`../principles.md` section 8 says everything on screen at rest should be readable in about five
seconds: a number, its scale, a short verdict, one short line of context, and the controls.
Section 13 grants a separate fifty-word budget above the fold for what is at stake. Adding M3's
eighteen-word line put the face over, so three things moved down to pay for it.

What stays on the face: the framing sentence at 49 words, the title, three comparison readouts
in words and numbers, three weight bars with their percentages, the ratio with **agree** or
**disagree** and the eighteen-word line, the four presets, save, reset and the rename
control. Counting only body prose and not the framing sentence, that is one eighteen-word line.
Revision 1 had that line plus two more of about the same length, so the face carried three
paragraphs of claim where it now carries one.

What moved down to the "?" panel to make room. The worked demonstration that a coherent set
scores zero whatever the numbers, which the eighteen-word line now says in fewer words. The
sentence about the method not seeing a missing criterion, which the supervisor moved down at
stage 2 for a better reason than space. And the three criterion name fields, which are now
behind one **Rename** control rather than three text inputs sitting open, because three open
inputs read as three things to fill in before anything will work.

What did not move, and why. The fraction beside each percentage stays: it is four characters, it
is numeric rather than prose, and a student comparing this page against the appendix's fallback
needs to see that 0.6586 and 65.86 per cent are the same number.

---

## 3. Verified numbers

These are the regression suite. Two implementations were written for this batch and share no
code: `ahp_check.py` uses numpy matrix algebra, and `ahp_check.js` uses explicit loops and
`Math.pow` in plain JavaScript under `node`. Both compute the priority vector twice, once by
power iteration to a maximum absolute change of 1e-12 and once by the row geometric mean.

Criteria are listed in the lab's order: elevation, slope, aspect.

### The reference encoding

Aspect over slope 5, aspect over elevation 3, slope equal to elevation.

| Quantity | Value |
|---|---|
| Weights, principal eigenvector | 0.185174, 0.156182, 0.658644 |
| Weights, geometric mean | 0.185174, 0.156182, 0.658644 |
| Largest difference between the two | 1.3e-14 (JavaScript), 0.0 (numpy) |
| Power iterations to 1e-12 | 13 |
| λmax | 3.029064 |
| Consistency index | 0.014532 |
| Consistency ratio at RI 0.58 | **0.025055** |
| Consistency ratio at RI 0.52 | 0.027946 |
| As whole percentages | 19 / 16 / 66 |

The audit's figures are elevation 18.5, slope 15.6, aspect 65.9, ratio 0.025. Reproduced
exactly. The self-check script's `AHP_WEIGHTS` of 19 / 16 / 65 and `AHP_CR` of 0.0251 are also
reproduced, with one note: the eigenvector's percentages are 18.52 / 15.62 / 65.86, which round
to 19 / 16 / 66 and not to 19 / 16 / 65. The script's 65 appears to come from forcing the three
to sum to 100 after rounding the first two up. The three figures a student types into the
Suitability Modeler must sum to 100, so some such rule is needed; the page's largest-remainder
rule would give 18 / 16 / 66 at whole numbers. Worth a line in the Lab 2 audit, because the
marker's reference figures in audit row 79 were computed at 19 / 16 / 65.

### The contradiction

Elevation over slope 3, slope over aspect 3, aspect over elevation 3.

| Quantity | Value |
|---|---|
| Weights, both methods | exactly 1/3, 1/3, 1/3 |
| λmax | 13/3 = 4.333333 |
| Consistency index | 2/3 = 0.666667 |
| Consistency ratio at RI 0.58 | **1.149425** |
| Consistency ratio at RI 0.52 | 1.282051 |

Derived by hand as well as computed. Every row of that matrix has product 1, so every row
geometric mean is 1 and the geometric-mean weights are exactly a third each. With those weights
each row of `Aw` is `(1 + 3 + 1/3)/3`, so `λmax = 1 + 3 + 1/3 = 13/3` exactly, and numpy's
`eigvals` returns 4.33333333 with a conjugate pair at −0.667 ± 2.309i.

### Eleven readings of the botanist's three sentences

Cell 74 says aspect is significantly (but not very) more important than slope, aspect is
slightly (but not very) more important than elevation, and slope is equally important to
elevation. The audit and the critical review both say eleven encodings were computed and neither
file lists them, so these eleven are this batch's own set rather than a reproduction of that
set. The first row is the audit's reference encoding and matches it exactly.

Slope equals elevation throughout. Percentages from the principal eigenvector.

| aspect/slope | aspect/elevation | elevation | slope | aspect | CR at 0.58 | CR at 0.52 |
|---|---|---|---|---|---|---|
| 5 | 3 | 18.52 | 15.62 | 65.86 | 0.0251 | 0.0279 |
| 5 | 2 | 22.47 | 16.55 | 60.98 | 0.0810 | 0.0904 |
| 5 | 4 | 16.03 | 14.88 | 69.08 | 0.0048 | 0.0053 |
| 4 | 3 | 19.19 | 17.44 | 63.37 | 0.0079 | 0.0088 |
| 4 | 2 | 23.18 | 18.40 | 58.42 | 0.0462 | 0.0516 |
| 6 | 3 | 17.94 | 14.24 | 67.82 | 0.0462 | 0.0516 |
| 6 | 4 | 15.50 | 13.54 | 70.96 | 0.0158 | 0.0176 |
| 7 | 5 | 13.36 | 11.94 | 74.71 | 0.0109 | 0.0121 |
| 7 | 3 | 17.44 | 13.15 | 69.41 | 0.0692 | 0.0772 |
| 3 | 2 | 24.02 | 20.98 | 54.99 | 0.0158 | 0.0176 |
| 5 | 5 | 14.29 | 14.29 | 71.43 | 0.0000 | 0.0000 |

All eleven put aspect first. Aspect runs from 54.99 to 74.71 per cent, elevation from 13.36 to
24.02, slope from 11.94 to 20.98. Every one passes the 0.10 bar under either random index. The
audit's claim that every sensible reading passes the bar and puts aspect first is confirmed on
this set.

### The walk that shows the lesson

Hold aspect over slope at 5 and aspect over elevation at 3. Walk the third comparison across all
seventeen positions.

| elevation vs slope | elevation | slope | aspect | CR at 0.58 | passes 0.10 |
|---|---|---|---|---|---|
| slope 9× | 8.30 | 30.29 | 61.41 | 0.7515 | no |
| slope 5× | 10.47 | 25.83 | 63.70 | 0.4488 | no |
| slope 2× | 14.66 | 19.63 | 65.71 | 0.1407 | no |
| equal | 18.52 | 15.62 | 65.86 | 0.0251 | yes |
| elevation 2× | 22.97 | 12.20 | 64.83 | 0.0032 | yes |
| elevation 3× | 25.83 | 10.47 | 63.70 | 0.0332 | yes |
| elevation 4× | 27.97 | 9.36 | 62.67 | 0.0739 | yes |
| elevation 5× | 29.69 | 8.56 | 61.75 | 0.1169 | no |
| elevation 9× | 34.42 | 6.71 | 58.87 | 0.2797 | no |

Two things to read off it. Aspect is first in all seventeen, between 58.87 and 65.86 per cent,
while elevation moves by a factor of five. And the passing window is not centred on "equal": the
coherent value for this comparison is elevation 5/3 times slope, so the window reaches four steps
one way and none the other. A student who assumes the ratio is a symmetric tolerance around
whatever they first typed is wrong. This walk is where they find out.

### The four presets

Added at stage 2. All four are computed here, and all four belong in the suite.

| Preset | Comparisons, as c12 / c13 / c23 | Weights | λmax | CR at 0.58 |
|---|---|---|---|---|
| Equal (the opening state) | 1 / 1 / 1 | 33.3333 each | exactly 3 | exactly 0 |
| One dominates | 9 / 9 / 1 | **81.8182 / 9.0909 / 9.0909** | exactly 3 | exactly 0 |
| A near tie | 1 / 2 / 2 | **40.0000 / 40.0000 / 20.0000** | exactly 3 | exactly 0 |
| A contradiction | 3 / −3 / 3 | 33.3333 each | exactly 13/3 | 1.149425 |

The dominance weights are exactly 9/11, 1/11 and 1/11. The near-tie weights are exactly 2/5,
2/5 and 1/5. Both are perfectly coherent, so both score exactly zero, which is itself worth
something: the page now has two presets that pass the bar with nothing in common except that
their three comparisons multiply through.

**What one step from the near tie does.** From 1 / 2 / 2, one step on the first comparison in
either direction:

| From the near tie | Weights | CR at 0.58 |
|---|---|---|
| one step, first over second | **49.3386 / 31.0814 / 19.5800** | 0.046225 |
| the preset | 40.0000 / 40.0000 / 20.0000 | 0.000000 |
| one step, second over first | **31.0814 / 49.3386 / 19.5800** | 0.046225 |

Two criteria tied at 40 per cent each, and one press of one button takes one of them to 49.34
while the other falls to 31.08. Press the other way and the same thing happens in reverse. The
third criterion barely moves, from 20.00 to 19.58. This is M2's finding made reachable in one
click, and it is the case the four-preset set exists to provide.

**A correction to the critique's wording, not to its substance.** The critique asked for a near
tie "chosen so that one step on one comparison swaps the leading two criteria". What this
construction does is not swap the leaders, it *decides* them: the preset is an exact tie, and
one step picks a winner. A literal one-step swap of two genuine leaders, with both states under
the 0.10 bar and a real gap on each side, is not available anywhere near the middle of the scale.
Searched exhaustively: of the 4,913 configurations, exactly 96 admit one, every one of them has a
comparison sitting at 8 or 9, and the smallest gap on either side is over twenty percentage
points. So a one-step swap is a thing that only happens out at the ends of the scale. The exact
tie in the middle is the better demonstration and it is what this file implements.

### Invariants the build must satisfy

1. A coherent matrix gives a ratio of exactly zero. Elevation 2× slope, elevation 6× aspect,
   slope 3× aspect: weights exactly 0.6, 0.3, 0.1, λmax exactly 3.000000000000, index exactly 0.
2. All three comparisons equal gives a third each and λmax exactly 3.
3. The eigenvector and the geometric mean agree, for n = 3, to the power iteration's tolerance.
   Worst difference over 20,000 random reciprocal matrices with entries log-uniform on [1/9, 9],
   seed 370370: 1.14e-12. The same test at n = 4 gives 0.216, so the agreement is a property of
   three criteria and must not be described as a property of the method.
4. Reciprocity: `A[i][j] * A[j][i] = 1` for every pair, to 1e-15.
5. Relabelling two criteria permutes the weights and changes nothing else.
6. The three displayed percentages sum to exactly 100.00 for every one of the 4,913
   configurations. This is a claim about the rounding rule, so it belongs in the suite.
7. Each of the four presets reproduces the table above exactly, and three of the four have
   λmax exactly 3 rather than approximately 3.
8. A fourth name in the `n` parameter is ignored, and the page still renders three criteria.

### What the site produces, and where it differs

Driven as a student would drive it on 19 September 2026, entering the reference encoding:

| Quantity | The existing site | This batch |
|---|---|---|
| Aspect | 0,6586 | 0.658644 |
| Elevation | 0,1852 | 0.185174 |
| Slope | 0,1562 | 0.156182 |
| λ | 3,0293 | 3.029064 |
| CI | 0,0146 | 0.014532 |
| CR | 0,0281 | 0.025055 at RI 0.58 |

And for the contradiction, the same reading gives weights of 0,3333 each, λ 4,3329, CI 0,6665
and CR 1,2816.

**The weights agree to every digit the site prints.** Both methods, both languages.

**The site's random index is 0.52, not Saaty's 0.58.** On the contradiction the consistency index
is exactly 2/3, and the site's own printed pair gives 0.6665 / 1.2816 = 0.52005. On the reference
encoding the same division gives 0.51957. So the site divides by 0.52. That is the whole of the
difference between the site's 0,0281 and the audit's 0.025. It means the site's ratio runs
about 11.5 per cent higher than the figure this course's own files record. Nothing on the site
says which random index it uses or where it comes from.

**The site's λ and index are off in the fourth decimal.** On the contradiction λ is exactly 13/3
and the site prints 4,3329, short by 0.00043. On the reference encoding λ is 3.029064 and the
site prints 3,0293, over by 0.00024. The errors go in different directions, so this is not a
different estimator, it is numerical slack in their solver. It does not reach the weights and it
does not move any verdict at the 0.10 bar for anything a student would type. Recorded because
audit row 78 and the marker's rubric both quote a ratio to four decimals, and four decimals is
one more than the site can support.

### Sources

Checked to exist with exact details, by an independent catalogue lookup, on 19 September 2026.
None of these has yet been through the adversarial check that `../principles.md` section 11
requires before anything ships, and none may appear in an (i) panel until it has.

- Saaty, T.L. (1980) *The Analytic Hierarchy Process*. New York: McGraw-Hill. Confirmed in Open
  Library: Thomas L. Saaty, first published 1980, McGraw-Hill International Book Co.
- Saaty, T.L. (1990) "How to make a decision: the analytic hierarchy process." *European Journal
  of Operational Research* 48(1): 9–26. Confirmed in Crossref, DOI 10.1016/0377-2217(90)90057-I.
- Crawford, G. and Williams, C. (1985) "A note on the analysis of subjective judgment matrices."
  *Journal of Mathematical Psychology* 29(4): 387–405. Confirmed in Crossref, DOI
  10.1016/0022-2496(85)90002-1. This is the geometric-mean estimator the second implementation
  uses.
- Donegan, H.A. and Dodd, F.J. (1991) "A note on Saaty's random indexes." *Mathematical and
  Computer Modelling* 15(10): 135–137. Confirmed in Crossref, DOI 10.1016/0895-7177(91)90098-R.
- Alonso, J.A. and Lamata, M.T. (2006) "Consistency in the analytic hierarchy process: a new
  approach." *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems* 14(4):
  445–459. Confirmed in Crossref, DOI 10.1142/S0218488506004114. Reports a recomputed random
  index near 0.5245 for n = 3.

**What could not be confirmed.** The RI value 0.58 for n = 3 is attributed throughout the
literature to Saaty's own simulation. This batch has not read that table in Saaty's own text.
An open-access paper reproducing the table was found but not read in full. So the page says that
the figure it divides by is 0.58 and does not attribute that figure to Saaty (1980), until a
checker has seen the table.

**The page divides by 0.58.** Settled by the supervisor at stage 2. It is what this course's own
files use, what audit row 15 records and what the marker's rubric rests on. One line on the page
says that some tools divide by a different number, and names none of them, because no source has
been confirmed for any of the alternatives and naming a site in teaching material invites a
comparison the page cannot support. The warning that the fallback's ratio runs about a tenth
higher belongs in the handout's appendix rather than on the page; see section 5.

---

## 4. Why the choices are what they are

**The default is all three comparisons equal.** Decision 51 fixes this and it is right: the
opening state is the state in which you have said nothing. The first move a student makes is
then legible as a move. Section 2 of `../principles.md` asks whether the default is a dead end,
and this one is not, since every control changes the picture from the first step. It has one
risk worth naming: three identical bars and a ratio of zero can read as a finding about
elevation, slope and aspect. So the opening state carries one line saying that nothing has been
said yet, which disappears on the first move. That line is a requirement, not a nicety.

**Four presets, not three.** Equal, one dominates, a near tie, a contradiction past 0.10.
Decision 51 fixed the count at three; the supervisor moved it to four at stage 2 and is putting
the reason to Luke. The numbers are in section 3.

**Revision 1 of this file got the dominance preset badly wrong, and the supervisor caught it.**
It proposed aspect 5 times slope, aspect 3 times elevation, slope equal to elevation, on the
reasoning that this was both the dominance case and the lab's own case. That is the reference
reading of the lab's three sentences, which decision 51 withholds until 9 October. Describing it
"by its numbers" hides nothing whatever: a student who presses the preset is handed the answer
the lab expects them to derive. The page would have shipped the withheld thing behind a button.
It is worth naming why the error was easy to make. The preset was chosen to be *useful*, and the
most useful dominance case on a page opening on Elevation, Slope and Aspect is the lab's own. The
check that catches this is not "is the label safe" but "what does a student get by pressing it".

**One dominates is 9 / 9 / 1**, which is decision 51's own phrase read literally: the first
criterion nine times each of the other two, those two equal. It gives exactly 81.82 / 9.09 /
9.09 with a ratio of exactly zero. It is no reading of any sentence anybody has written, so it
cannot hand over anything. It also makes a point the lab's reading cannot: a set of comparisons
can be as lopsided as the scale allows and still score a perfect zero, because zero is about
coherence and not about moderation.

**A near tie is 1 / 2 / 2**, giving exactly 40 / 40 / 20 at a ratio of zero. It exists because
of M2 below. One press of one button from there takes the tie to 49.34 against 31.08, either
way. Without it the page can show that the order survives and cannot show where it stops
surviving, which is the more comfortable half of the truth.

**Checked against `../principles.md` section 5.** Equal and one-dominates differ in two
comparisons, which is unavoidable, since with three comparisons there is no way to move from
all-equal to a lopsided state in one. What matters is the pair a student will actually read
across, and that pair is the near tie against its two neighbours one step away: those differ in
exactly one comparison and in nothing else at all, which is as clean an isolation as this
subject allows.

**Nothing of the lab's own story appears until after 9 October.** Per decision 51 and the
supervisor's answer to question 5: no plant, no species, no study area, and no botanist. The
framing sentence in section 2 says "an expert" for that reason. The word, the reading and the
"reading the botanist" preset all arrive together after Lab 2 closes, and this paragraph is the
record of when and why.

**Three criteria, fixed.** Four reasons, in the order they carry weight. Lab 2 has three. The
seventeen-position control is legible on a phone at three rows and is not at six. At three, the
eigenvector and the geometric mean agree exactly, so the page never has to explain a method
choice it cannot make matter. And three is where a reader can still hold the whole thing in
their head, which is the one thing a six-criterion version would lose in exchange for realism.

**A decimal point, not a comma.** The existing site is served in a locale that writes a decimal
comma. The handout has to spend a sentence in cell 86 explaining that 0,4032 means 40.32. That sentence exists because of a
locale setting on somebody else's server. The page writes 65.86 and 0.0251 and the handout can
drop the explanation, which is a small saving for the student and a real one for whoever
maintains the notebook. The 123ahp appendix keeps its own warning, because the appendix sends
students to the site.

**Percentages, not fractions.** The Suitability Modeler wants percentages summing to 100 and cell
86 says so. Printing 0.6586 and then asking a student to multiply by 100 is a step the page can
simply not impose. Both are shown: the bar is labelled 65.86 per cent, and the fraction 0.6586
sits in smaller type beside it, because the fraction is the form the appendix's fallback prints
and a student comparing the two needs to see that they are the same number.

**Colour.** A single-hue ramp or none at all, and never hue alone. The three weight bars are one
colour, distinguished by length and by their labels, because they are three values of one
quantity and not three categories. Giving three such bars three different hues says they are
three kinds of thing, which they are not. The consistency verdict is carried by its two words, not by
red and green; if a colour is used at all it is a change of lightness behind the words, measured
against the page at 3:1 or better.

**Wording in the students' vocabulary.** The verdict words are **agree** and **disagree**,
settled at stage 2. Both are ordinary English, neither is evaluative, and both read straight into
the eighteen-word line under them. The draft they replaced, *no contradiction* and *a
contradiction*, used one root twice and made the good case the absence of the bad one, which is
the wrong way round for a page whose whole argument is that coherence is not correctness.

The control says "how much more important", never
"Saaty scale" and never "pairwise comparison matrix". The number says "consistency ratio,
which measures how well your three comparisons agree with each other" the first time it appears,
per section 8's rule that a technical term is defined in the same sentence. The words on the
stepper are the ordinary English ones: equal, slightly more important, more important,
much more important, absolutely more important, with the number beside each. These are our own
words, chosen for a first-year reader, not anybody else's labels.

**No alternatives.** The existing site asks for two options to choose between, then asks the
student to compare those options under each criterion in turn. The lab tells students to leave
every one of those comparisons at 1. The arithmetic consequence is that both options come out at
exactly 0.5000 for every student in the class, so the charts built on them carry no information
at all. The lab instructs students to ignore them. Our page has criteria and weights, and
nothing else.

**Rejected: a matrix view.** Showing the three by three reciprocal matrix was considered and
dropped from the face. It is the thing the method actually operates on, and it is also six
numbers where three will do, four of which are reciprocals of the others. It belongs in the
lesson panel as a still picture, where a student who wants to know what the arithmetic is
looking at can find it. That a working-steps view is worth having at all is a lesson taken from
the existing site, which offers one.

**Rejected: showing λmax and the consistency index on the face.** Two more numbers, neither of
which a student is asked for. They go in the lesson panel beside the matrix.

---

## 5. Known limits and open threads

**What the page deliberately will not do that the existing site does.** Each of these is a
choice rather than an omission, and each is made because Lab 2 does not need it.

*Options to choose between, and the chart that ranks them.* Not built, by choice. Lab 2 does not
use them: the handout tells students to leave every such comparison at 1, which makes that chart
a tie by construction. Nothing a student is marked on is lost.

*More than three criteria.* Not built, by choice. The three-criteria limit is a decision rather
than an omission. If a future lab needs four, the work is not the control, it is the arithmetic
statement: at four the eigenvector and the geometric mean disagree by up to a fifth of the whole
scale, so the page would have to say which it uses and why. It would also need six comparisons
rather than three, which is six rows on a phone, and a random index of 0.90 instead of 0.58. The
honest answer is that a four-criteria version is a different widget and should be proposed as
one.

*Saving a model and coming back to it.* The existing site offers this behind an account. Not
built, by choice. The page keeps its whole state in the URL and stores nothing, which is the
repository's standing answer to the privacy and FIPPA question in `../principles.md`.

*Several people's answers, gathered together.* The existing site has a mode for this. Not built,
by choice. It is the participatory-GIS case that cell 73 of the handout points at, and it is
genuinely interesting. It is also a different widget. It would need somewhere to keep several
people's answers, which the repository has decided not to have.

**Does any of that matter to Lab 2?** No. Cells 73 to 75 use the three criterion weights and the
consistency ratio, and nothing else. Question 8 wants the chart image and the ratio. The page
covers both and covers the chart better, because the saved image records its own inputs.

**Two things for the Lab 2 build rather than for this page.**

*The appendix has to warn about the divisor.* The page divides by a random index of 0.58; the
fallback the appendix sends students to divides by 0.52. A student who does the same three
comparisons in both places gets 0.0251 here and 0,0281 there, which is about a tenth higher.
Neither is wrong. The warning belongs in the appendix text, beside the decimal-comma warning it
already needs, and not on the page, which says only that some tools divide by a different number.

*The appendix's address is now `https://`.* Section A of `review-log-370-AHP-1.md` has the
measurement. Two dated lines were appended to the addendum of `Lab2-audit-2026-09-19.md` on
19 September 2026 carrying this and the rounding point below; nothing else in that file changed.

**Open threads.**

*Whether the page should show the lab's downstream consequence.* The strongest version of this
widget would let a student see that 19 / 16 / 66 and 23 / 18 / 58 send a surveyor to different
hillsides. That needs the suitability surface, which needs the lab's data, and
`../principles.md` section 15 is emphatic that a widget built beside an assessment must be
structurally unable to answer the assessed question. Showing the lab's own map would hand over
Question 7. So the answer is no for this build. Whether some other landscape could carry the
same point is a real question and is not settled here.

*Presentation mode with long word readouts.* Flagged above. A measurement for the build.

*The `123ahp.com` appendix.* Decision 52 moves the walkthrough to an appendix under a horizontal
rule. Section A of this batch found several places where that walkthrough no longer matches the
site. They are listed in `review-log-370-AHP-1.md`. The one that matters is that the site has
no way to save the chart as an image, which the walkthrough's wording implies it does.

*The site now serves over HTTPS.* Checked on 19 September 2026: `https://www.123ahp.com/` loads,
the certificate is accepted without an interstitial, no image or script falls back to `http`, and
the full calculation reproduces the same figures over HTTPS as over HTTP. The handout's
instruction to copy the `http://` URL into a separate browser, and audit row 2's note that the
site is "http only", are both now out of date. That is a Lab 2 edit and not a widget matter, and
it is recorded here because this batch is where it was found.

---

## 6. The pair activity, and the questions for the supervisor

### The five-minute task

Built into the **For the classroom** panel as drafted, per the supervisor's answer to question 7,
and **marked on the panel and in this file as a candidate awaiting Luke's interrogation**.
`../principles.md` section 16 requires that this be settled in a grilling session about the
pedagogy rather than drafted, and generating a plausible activity and shipping it is the failure
that rule exists to stop. Building it into the panel now means the build has something to put
through the five passes. It does not mean it is settled.

Decision 51 fixes the share-back question: **whose sentences were these, and who else could have
been asked.**

The panel reads, in the template's three-part shape:

*On your own, one minute, on paper, before anything is on screen.* Somebody is choosing where to
put a bench in a park. Three things matter: shade, view and quiet. They say shade matters clearly
more than quiet, shade matters a little more than view, and view and quiet matter about the same.
Write down the three percentages you think those sentences come to. Largest first.

*In pairs, two minutes, one phone between two.* Rename the three criteria to shade, view and
quiet. Set each comparison to the numbers each of you wrote. Note two things: whether the two of
you agreed about the order, and by how much your percentages differed.

*Back to the room, two minutes.* The share-back question.

**The example is not the lab's, and that is a change from revision 1.** Revision 1 used the
lab's own three sentences. The supervisor's answer to question 5 says no plant, no place and no
expert on the page before 9 October, and the classroom panel is on the page. A bench in a park
carries the identical structure with none of the lab's content. It is also better on
`../principles.md` section 15, because it is further from the thing being marked.

**Measured, so it is not asserted.** Twelve readings, with "clearly" read as 3 to 7 and "a
little" as 2 to 4:

| | shade | view | quiet | CR at 0.58 |
|---|---|---|---|---|
| clearly 3, a little 2 | 54.99 | 24.02 | 20.98 | 0.0158 |
| clearly 5, a little 3 | 65.86 | 18.52 | 15.62 | 0.0251 |
| clearly 6, a little 2 | 63.01 | 21.84 | 15.15 | **0.1169** |
| clearly 7, a little 2 | 64.67 | 21.30 | 14.03 | **0.1525** |
| clearly 7, a little 4 | 72.48 | 15.04 | 12.48 | 0.0301 |

Shade is first in all twelve. Shade runs from 54.99 to 72.48 per cent, a spread of 17.5 points,
so a pair will almost always disagree about the numbers. They will almost never disagree about
the order. **And two of the twelve fail the bar**, both of them the readings that make "clearly"
strong while keeping "a little" weak. So the room will produce a failure by itself, without
anybody being told to go looking for one, which the lab's own three sentences never do. That is
a better five minutes than revision 1 had.

What it tests: the sentences at the top of this file. It cannot be passed by understanding the
controls, because the commitment is made before the page is opened.

What the instructor does with the answers. Three positions, not two. One pair says the numbers
are a matter of opinion, so the method is subjective. Another says the order came out the same,
so it does not matter. A third pair, the one that hit 0.1169, says the method told them they had
contradicted themselves when they had done nothing of the kind. All three are half right. What to
run at the front is the near-tie preset and one press of one button, so the room watches a 40-40
tie become 49 against 31. Then the walk in section 3, where the order does not move at all. The
two together are the whole argument.

Candidates considered and set aside, recorded so they are not reinvented. *Predict the
consistency ratio* was dropped because nobody can predict it and being wrong about something you
could not have got right teaches nothing. *Which factor should matter most for a rare plant* was
dropped because it is Lab 2's own question in a smaller box, which section 15 forbids. *Find a
set of three comparisons that fails the bar* was dropped because 78 per cent of the range fails
it, so it is not a task. *The lab's own three sentences* was dropped at revision 2, for the
reason above.

Section 15 check on the surviving candidate: for it to hand over an answer that is being marked,
the page would have to compute the suitability surface, which it does not and will not. The
example is about a bench, which moves it further still.

### A slug

Proposed: **`pairwise`**. Short, lower case, names the subject rather than the course, fits on a
slide and in a QR code, on the pattern of `least-cost` and `relative-distance`.

`weights` was considered first and rejected. This repository already has a widget whose central
idea is a weights kernel, in the spatial sense. Two widgets about "weights" meaning different
things is a trap for whoever reads the front page. `ahp` was considered and rejected because it
is the software's vocabulary rather than the students', and section 8 rules against that. Two
alternatives if `pairwise` reads as too abstract: `criteria-weights`, or `how-important`.

### Dependencies

None. Everything on the page is arithmetic on three numbers, a canvas, and DOM. The priority
vector is thirteen power iterations on a three by three matrix, which is microseconds. The image
export is `canvas.toBlob`, which is platform. There is nothing here that wants a library, and
the repository's streak stands at four.

### Accessibility, against `../principles.md` section 9

Stated as commitments for the build, each one measurable.

*Colour.* Nothing carries meaning by hue. The three weight bars are one hue and are read by
length and by their printed numbers. The verdict is two words. A single-hue ramp, if used at all,
is checked in greyscale and under simulated deuteranopia and protanopia.

*Contrast.* 4.5:1 for text, 3:1 for the bars and the control parts, measured against the actual
background in both themes. The handout's phrase "in tiny print" for the consistency ratio
describes an accessibility defect, measured in `review-log-370-AHP-1.md`. The page's ratio is
the second largest thing on the screen.

*Keyboard.* Every control operable, in order, with a visible focus ring. The stepper is two
buttons and takes arrow keys as well. This is worth stating as a commitment rather than assuming
it, because the tool the lab currently sends students to cannot be operated by keyboard at all.
The measurements behind that statement are in `review-log-370-AHP-1.md`.

*Screen readers.* Semantic HTML. Each comparison is a labelled group whose readout is the
accessible value. The weights are also available as a small table, because a bar chart is not
information to a screen reader. A polite live region announces the new weights and the new ratio
after each change.

*Motion.* Nothing animates except a bar length, and that respects `prefers-reduced-motion` by
snapping.

*Text sizing.* `rem` throughout, so the reader's own font size applies. The page survives
200 per cent zoom with no horizontal scrolling. Every target on the page is 44 by 44. The
current tool's behaviour on a phone is measured in `review-log-370-AHP-1.md` and is the reason
this is written as a requirement.

*Language.* `lang="en"` on the root.

### The eight questions, as settled at stage 2

All eight were answered by the supervisor. Recorded here with the answer, so the build has one
place to read them off.

1. **The verdict's words.** Settled: **agree** and **disagree**.
2. **Which random index.** Settled: **0.58**, with one line on the page saying some tools divide
   by a different number and naming none. The appendix carries the warning that the fallback's
   ratio runs about a tenth higher.
3. **Signed URL parameters.** Settled: signed.
4. **Three criteria.** Settled: fixed in the code. A fourth name in `n` is ignored.
5. **What stays off the page until 9 October.** Settled: no plant, no place, no botanist. The
   framing sentence says "an expert". The classroom panel's example moved off the lab entirely
   as a consequence; see above.
6. **The missing-criterion line.** Settled: one layer down, in the "?" panel, not on the face.
7. **The pair activity.** Settled: build the candidate into the panel, marked as a candidate
   awaiting Luke's interrogation. Done, with the example changed under answer 5.
8. **The four existing widgets' classroom panels.** Out of scope, noted.

### What is still open for Luke rather than for the supervisor

- **The preset count moved from three to four**, which amends decision 51. The supervisor is
  putting the reason to Luke.
- **The classroom activity itself**, which needs the grilling session before it can stop being
  a candidate.
- **Whether the "reading the botanist" preset arrives on 9 October**, and with it the word, the
  plant and the place.

---

## D. Critical-geography review, rule 12

Run over this proposal by its author, in the three required parts, in order. The 6 September
critical review of Lab 2 said that the AHP step is where the lab's politics live, and the
19 September one said it again at C3 and M4. This section takes that seriously rather than
acknowledging it.

### What this already does well

**It puts the arbitrariness on the face rather than in a footnote.** The whole page is an
argument that a number in a model is a choice somebody made. Most teaching tools for weighting
present the weight as an output. This one presents it as a translation. Translation is a
place where power sits.

**It refuses the answer key structurally.** The page computes weights and stops. It does not
touch the suitability surface, so there is no configuration of it that answers Question 7 or the
hectare table in Question 8. That is section 15's test and this passes it by construction rather
than by asking students not to look.

**It names the consequence in the opening fifty words.** "They say where somebody walks and
where nobody looks" is a sentence about who bears the outcome. It is in the reading flow, so it
survives presentation mode, which is where the MAUP widget failed the same audit.

**It declines to dress up the method's authority.** The contradiction preset is in the presets
rather than in a paragraph, so the method is shown refusing on purpose. And the page says that a
ratio of zero is agreement with yourself and not agreement with the world, which is the honest
description of a number that is routinely reported as though it were a quality score.

### What it could become

Each with a proposal and its cost. These are proposals for the supervisor, not changes made.

**C1. The second speaker.** The page has one voice in it, the botanist's. She is a
professional whose sentences are treated as data. The widget's own share-back question asks who
else could have been asked. The page could make that askable rather than only sayable: a fourth
name field, greyed, labelled "a criterion nobody asked about", which accepts a word and then
does nothing with it, because the method has no place to put it. *Cost:* one field, one line, and
a real risk of being too clever. *Verdict:* could become; needs the supervisor's judgement,
because a control that deliberately does nothing is a strong move and can read as a trick.

**C2. Whose ground the survey walks on.** The lab's study area is the south Okanagan, and the
19 September critical review's C2 asks for one sentence naming the Syilx Okanagan Nation and the
Osoyoos Indian Band, worded from the Nation's own statement and quoted rather than paraphrased.
This page does not draw the Okanagan and will not name it before 9 October. After that date, if
the "reading the botanist" preset lands, the page acquires a place and the question arrives with
it. *Cost:* one sentence, and one check by Luke against the Nation's own words. No website of any
Nation was fetched for this file, deliberately, so that no paraphrase of a quick read reaches a
course document. *Verdict:* could become, and it is the standing open question in
`../principles.md` about whether a page that maps land should say whose land it is. This page does
not map land, which is a reason to be careful about reaching for the easy version of the answer.

**C3. The weights as a record of a conversation that did not happen.** Cell 73 of the handout
already says AHP can be used for a participatory GIS, and names a reading on Crocker Range Park.
The site has a group mode. Our page has one reader. The page could say, in the lesson panel, that
the same arithmetic is run in rooms with many people in them, that the numbers are then an
average of several readings, and that averaging disagreement is itself a choice. *Cost:* three
sentences in the lesson panel, plus a citation that has to pass the adversarial check.
*Verdict:* could become. This is the cheapest of the three and the one most likely to land.

**C4. The saved image as evidence.** The image the page hands over records the comparisons, not
only the weights. That makes a student's translation auditable by the marker and by the student
themselves. It could go further: the image could carry the sentence each comparison came from,
so the record runs from English to number to weight in one picture. *Cost:* the sentences have
to come from somewhere, which after 9 October means the botanist and before it means nowhere.
*Verdict:* could become, after 9 October.

### What must change

Three, each with the concrete edit, and each is a change to this proposal rather than to a built
page. **All three were accepted at stage 2 and all three are applied in revision 2.** The
findings are left standing as written, with the disposition added, because what the review found
is worth more to a later reader than a tidied version of it.

**M1. The framing sentence names nobody.** As drafted it says "a botanist" and "somebody". The
review brief is explicit that the proposal must say whose weights these are on its face, not in a
footnote. "Somebody" is a way of not saying. The sentence has to name the role that made the
choice and the role that lives with it. Concretely, replace

> Three sentences from a botanist become three numbers here. Somebody has to decide how strong
> "significantly more important" is. Two readers will not decide the same way. The weights
> below steer a survey: they say where somebody walks and where nobody looks.

with

> Three numbers below decide what a survey looks for. They did not come from the ground. They
> came from somebody reading somebody else's sentences and deciding how strong the words were.
> You are that reader here. Two readers do not agree. The map that follows is not the same
> map.

**Applied in revision 2, with one further change.** The supervisor's answer to question 5 rules
out "botanist" on the page before 9 October, and the wording above still leaned on "somebody
else's sentences", which is the vagueness M1 objected to in a different coat. Section 2 now reads
"An expert wrote sentences. Somebody read them and decided how strong each word was. You are that
reader here." The vagueness is resolved in the next sentence rather than left standing, and the
whole thing is 49 words, inside section 13's budget.

**M2. "The rank order survives" is a comforting sentence and it is only true within the
botanist's reading.** Section 1 says the order holds still. It holds still across eleven readings
of *these three sentences*, and across the walk in section 3. It does not hold still in
general: move the slope-versus-aspect comparison one step past equal and slope takes the lead.
The page as proposed could leave a student with "AHP is robust", which is false and is the more
comfortable of the two beliefs, exactly as `../principles.md` section 6 describes. The concrete
edit: the lesson panel must carry the sentence that the order survives *disagreement about
strength* and not disagreement about direction, with the measured case beside it. And the
"one criterion dominates" preset needs a sibling that crosses the order, so a student can reach
the case in one click rather than being told about it. **This is a change to the preset list in
section 4 and it needs the supervisor, because decision 51 fixes the presets at three.**

**Applied in revision 2, and it went further than the finding asked.** The supervisor accepted
M2 and added a fourth preset, a near tie at 40 / 40 / 20, from which one press of one button
takes the tie to 49.34 against 31.08 either way. Section 1's headline is now three sentences
rather than one, and the third of them is this finding. And the same review turned up something
M2 had not: the dominance preset revision 1 proposed *was* the lab's own reading, which decision
51 withholds. That is recorded in section 4 rather than quietly fixed.

**M3. The page must not let the consistency ratio look like a quality score.** As proposed, the
ratio sits beside the weights with a two-word verdict, which is the layout of a pass mark. A
student reading only the face will take "no contradiction" as "these weights are good". They are
not; they are coherent. The concrete edit: the verdict's two words must not be evaluative, and
the line under the ratio must say what it is about. Proposed wording for that line, which is on
the face and not in a panel:

> This measures whether your three comparisons agree with each other. It says nothing about
> whether they are right.

Eighteen words. This review said twenty-three, which was never counted and is wrong; the count
is corrected in section 2 rather than here, because leaving the finding as the review wrote it
is the point of this section. It is the single most important sentence on the page and it is the
one the existing tool omits. **Must change. It changes section 2's face list: the ratio is a number, a
verdict and this line, not a number and a verdict.**

**Applied in revision 2, verbatim.** The supervisor settled the verdict words at **agree** and
**disagree**, which is better than either wording this review proposed: neither is evaluative,
and both read straight into the line. Adding the line pushed the face over section 8's
five-second rule, so three things moved one layer down to pay for it; the audit is at the end of
section 2.

---

## Picking this up again

There is no code yet. What exists is this file and the two check scripts in the session
scratchpad, which should be moved into `tools/` when the build starts, on the pattern of
`tools/relative-distance-verify.py`.

- `ahp_check.py`, numpy, matrix algebra, run under the Homebrew Python 3.13 because
  `/usr/bin/python3` on this machine is 3.9.6 with no numpy.
- `ahp_check.js`, plain JavaScript, explicit loops, run under `node` at
  `/opt/homebrew/bin/node`.

Both were run on 19 September 2026 and agree to 1.3e-14 on every figure in section 3. The numbers
to check first after any change are the reference encoding's three weights and ratio, the
contradiction's exact thirds and 13/3, and invariant 3, which is the one that says the method
choice cannot matter at three criteria.

The live site behaviour recorded in section 3 was observed on 19 September 2026 over both HTTP
and HTTPS. A hobby site can change without notice. Re-observe before quoting it.

---

## Revision 2, what changed and why

Against the supervisor's stage-2 critique of 19 September 2026. Every numbered item is that
critique's own numbering. Two disagreements are recorded rather than complied with silently, and
both are marked.

**1. M1 and M3 applied; the verdict words settled as agree / disagree.** Section 2's framing
sentence replaced, now 49 words and naming the reader. The ratio block is now a number, one word
and the exact 23-word line, with the line on the face rather than in a panel. Section 4's wording
paragraph records why *no contradiction* / *a contradiction* was the wrong pair. The dispositions
are written into M1 and M3 in section D rather than replacing the findings.

**2. M2 applied, and the dominance preset corrected.** This is the most important change in the
revision and the critique was right about it. Revision 1 proposed the dominance preset as aspect
5 times slope, aspect 3 times elevation, slope equal to elevation, calling it "the dominance case
and the lab's own case" as though that were a virtue. It is the reference reading of the lab's
three sentences, which decision 51 withholds until 9 October, and a preset is a button: a student
who presses it is handed the answer the lab expects them to derive. Describing it by its numbers
hides nothing. Corrected to 9 / 9 / 1, exactly as decision 51 words it, giving 81.8182 / 9.0909 /
9.0909 at a ratio of exactly zero. Section 4 now carries the error and why it was easy to make,
under `../principles.md` section 15's rule that the check is what a student gets by pressing, not
whether the label is safe.

A fourth preset added: a near tie at 1 / 2 / 2, giving exactly 40 / 40 / 20 at a ratio of zero.
One step on the first comparison takes it to 49.3386 / 31.0814 / 19.5800 either way, at a ratio
of 0.046225. Measured, and in section 3 with the other three.

**Disagreement 1, on wording rather than on substance.** The critique asks for a near tie
"chosen so that one step on one comparison swaps the leading two criteria". The construction it
specifies does not swap the leaders; it decides them, because the preset is an exact tie. I
looked for a literal one-step swap and it is not available where it would be useful: of the
4,913 configurations, exactly 96 admit a one-step swap with both states under the 0.10 bar and a
real gap on each side, every one of them has a comparison sitting at 8 or 9, and the smallest gap
on either side is over twenty percentage points. So a genuine one-step swap only happens at the
ends of the scale, where nothing else about the state is instructive. The exact tie in the middle
is the better demonstration and is what is implemented. The substance of the request, that a
student reach the order-crossing case in one click, is met.

**3. The lesson sentence rewritten.** Section 1's headline is now three sentences: vague words
become firm numbers; the order survives disagreement about how strong the words are; it does not
survive disagreement about which way they point. The paragraph under it says plainly that
decision 51's own sentence joined the first two, and that the third is what section 3's
measurements show.

**4. The random index settled at 0.58.** Section 3's sources paragraph and section 4 both record
it, with one line on the page saying some tools divide by a different number and naming none.
Section 5 gains the note for the Lab 2 build: the appendix, not the page, warns that the
fallback's ratio runs about a tenth higher.

**5. Questions 3 to 8 recorded as settled.** Section 6's question list is rewritten as answers.
Signed parameters kept. Three criteria fixed in code, a fourth name in `n` ignored, which is now
invariant 8. No plant, no place, no botanist before 9 October, so the framing sentence says "an
expert" and section 4 records when the word returns. The missing-criterion sentence moved one
layer down, with the supervisor's reason recorded because it is better than the space argument.
The classroom activity built into the panel and marked a candidate.

**Disagreement 2, forced by answer 5 and resolved here rather than left.** Answers 5 and 7 pull
against each other. Question 7 says build the candidate activity "as drafted"; the drafted
activity asks a pair to read the lab's own three sentences, which answer 5 puts off the page
until 9 October. The classroom panel is on the page, so the drafted activity cannot ship as
drafted. Changed to a bench in a park with shade, view and quiet, which carries the identical
structure with none of the lab's content, and it turns out to be the better task: twelve readings
put shade first every time between 54.99 and 72.48 per cent, and **two of the twelve fail the
0.10 bar**, so the room produces a failure by itself. The lab's own sentences never do. Measured
and tabulated in section 6. If the supervisor wants the lab's sentences back after 9 October,
say so and it is a one-paragraph change.

**6. The five-second audit done, with what moved.** New subsection at the end of section 2. Three
things moved one layer down to pay for M3's line: the worked demonstration that a coherent set
scores zero whatever the numbers, the missing-criterion sentence, and the three criterion name
fields, which are now behind one **Rename** control. The fraction beside each percentage stayed,
with the reason. Body prose on the face is now one eighteen-word line, against three lines of
about that length in revision 1.

**A correction inside the correction.** Revision 1 described M3's line as twenty-three words and
the critique's item 1 repeated the figure. It is eighteen. Nobody had counted it, here or there.
The line is unchanged; the count is fixed wherever this file states it.

**7. Two dated lines appended to the Lab 2 audit addendum.** `Lab2-audit-2026-09-19.md` was
re-read immediately before writing and nothing else in it changed. The two lines record that the
site now serves over HTTPS, so cell 73's `http://` instruction and row 2's "http only" are out of
date for the appendix text; and that the eigenvector rounds to 19 / 16 / 66 rather than the
19 / 16 / 65 that run 4 and row 79 used, with the note that the difference is one percentage
point on one weight, moves no verdict, and means the marker's note should say which set it rests
on.

**8. Everything else kept.** The scope and copyright paragraph, the four omissions by choice, the
invariants, and the sources with their unconfirmed items marked, are all unchanged.

---

## Note added at the build, 19 September 2026

**The withheld preset and the 9 October date are dropped, on Luke's instruction.** His words,
given while `BATCH-370-AHP-2` was building the page:

> "i don't get this 9 october thing exactly...we want a tool that works this year and next
> year without any action on the part of the new instructor."

So there is no "reading the botanist" preset and no date anywhere. The four presets in section
3 are the whole set, permanently. The park-bench activity in section 6 is the activity rather
than an interim. Nothing on the built page, in its URL defaults or in `pairwise.md` refers to
9 October, to a later release, or to the lab's own reading of its own three sentences. The
page opens on Elevation, Slope and Aspect because that is what this course's students need,
and a later course changes the names in the URL.

The body of this file is left as it was written, including every sentence that assumes the
date, because it is the record of how the page was argued into existence at stages 1 and 2.
What was built, and every place it differs from this file, is in `pairwise.md`.
