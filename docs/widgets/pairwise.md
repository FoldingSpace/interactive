# Three criteria, three weights

`web/pairwise/`. Built 19 September 2026 under `BATCH-370-AHP-2`, stage 3 of standing
decision 51. **Live:** https://foldingspace.github.io/interactive/pairwise/, deployed the
same day under `BATCH-370-AHP-3`.

The specification is `PROPOSAL-ahp.md` at revision 2, which is stages 1 and 2 of the same
decision. That file stays as the record of how the page was argued into existence. This file
does not repeat it. Where the two differ, this file is what was built and the proposal says
what was intended, with the reason for every divergence recorded below.

---

## The one thing it teaches

**Vague words become firm numbers. The order of the numbers survives disagreement about how
strong the words are. It does not survive disagreement about which way they point.**

The page does not say any of that. It shows it, and the student finds it by moving a
control. That is Luke's instruction of 19 September and it is the largest single difference
between the proposal and the build; the wording is in the next section.

---

## What Luke changed while this was being built

Seven instructions arrived during the build and the review. All seven are recorded verbatim,
because each one changed what shipped. The fourth is in *The shape of the tool* below, with the design
argument it settles.

**1. Show, do not tell.**

> "the student needs to be able to think about ambiguities, not be told what to do. you
> often tell them too much."

What it changed. The framing sentence lost its conclusion: no "two readers do not agree", no
"the map that follows is not the same map", no "you are that reader here". It went from 49
words to 24. The lesson panel lost everything that stated a finding: that the order survives,
that it stops surviving, that a careful reading passes the bar. What is left says what a
comparison is, what the weights are and what the ratio measures, and then stops. The
classroom panel's student-facing half is the task and the commit-first instruction; what to
watch for is addressed to whoever is running the room.

The word counts are in the five-second audit below.

**2. No withheld preset, and no date.**

> "i don't get this 9 october thing exactly...we want a tool that works this year and next
> year without any action on the part of the new instructor."

What it changed. The "reading the botanist" preset is dropped for good. The four presets are
the whole set. The park-bench activity is permanent rather than an interim. Nothing on the
page, in the URL defaults or in this file refers to 9 October, to a later release or to the
lab's own reading of its own three sentences. The page opens on Elevation, Slope and Aspect
because that is what this course's students need; a later course changes the names in the
URL and nothing else is course-specific. A dated note at the foot of `PROPOSAL-ahp.md`
records the drop against that file without rewriting it.

**3. Every string through the anti-AI rules.**

> "all text is to be sent through our anti-ai set of text rules. no mannered text. simple and
> clear. etc."

What it changed. Nine findings, listed under the text pass in the review record below. Then
the scan was run again after the classroom panel was cut, at 640 words.

**4. A free hand on the shape of the tool.** Recorded with the design argument under
*The shape of the tool, and why it is one screen*.

**5, 6 and 7. Three changes after Luke looked at the built page.**

> "doesn't the thicker line for 'balanced' confuse with the actually selected relative
> criteria selection? maybe just make the center look the same as others."

> "'big screen' loses the choosers."

> "saving to an image, the text is too terse for the students to know what it means. improve
> clarity."

The first is under the accessibility pass, the second under what goes on a projector, and the
third under why the choices are what they are. All three are applied and measured.

---

## Verified numbers

Checked by three routes that share no code: the page itself, `tools/pairwise-verify.js`
(plain JavaScript, explicit loops, `Math.pow`) and `tools/pairwise-verify.py` (numpy matrix
algebra). The two check scripts began as `ahp_check.js` and `ahp_check.py` in the 370 folder
under batch 370-AHP-1; they were moved into `tools/` for this build, on the pattern of
`relative-distance-verify.py`, and the four presets, the walk, the rounding rule, the cycle
count and the exhaustive sweep were folded in. Both were run on 19 September 2026.

The suite in `tools/test/pairwise.test.js` runs the page's shipped HTML in the stub DOM and
reads these back off what the page **draws**, not off what it computes.

### The state encoding

`c12`, `c13`, `c23`, each a signed integer. `+k` means the first of the pair is k times as
important, `-k` means the second is, `1` means equal. Seventeen positions per comparison, so
4,913 settings in all. Criteria are in the lab's order: elevation, slope, aspect.

### The reference encoding, `?c13=-3&c23=-5`

| Quantity | Value |
|---|---|
| Weights, principal eigenvector | 0.185174, 0.156182, 0.658644 |
| Weights, row geometric mean | the same to 1.1e-12 |
| Power iterations to 1e-12 | 13 |
| λmax | 3.029064 |
| Consistency index | 0.014532 |
| Consistency ratio at RI 0.58 | **0.025055** |
| Displayed shares | 18.52 / 15.62 / 65.86 |
| Bar widths read back off the page | `18.52%`, `15.62%`, `65.86%` |

### The four presets

| Preset, as labelled | c12 / c13 / c23 | Weights | λmax | CR |
|---|---|---|---|---|
| All equal | 1 / 1 / 1 | 1/3 each | exactly 3 | exactly 0 |
| One far ahead | 9 / 9 / 1 | 9/11, 1/11, 1/11 | exactly 3 | exactly 0 |
| Two tied | 1 / 2 / 2 | 2/5, 2/5, 1/5 | exactly 3 | exactly 0 |
| Each beats the next | 3 / −3 / 3 | 1/3 each | exactly 13/3 | 1.149425 |

Displayed: 33.34 / 33.33 / 33.33; 81.82 / 9.09 / 9.09; 40.00 / 40.00 / 20.00; 33.34 / 33.33
/ 33.33.

### One step from the near tie

| From 1 / 2 / 2 | Weights, as percentages | Displayed | CR |
|---|---|---|---|
| one step, first over second | 49.3386 / 31.0814 / 19.5800 | 49.34 / 31.08 / 19.58 | 0.046225 |
| the preset | 40.0000 / 40.0000 / 20.0000 | 40.00 / 40.00 / 20.00 | 0.000000 |
| one step, second over first | 31.0814 / 49.3386 / 19.5800 | 31.08 / 49.34 / 19.58 | 0.046225 |

Both the exact figures and the drawn ones are in the suite, and the drawn ones are reached by
clicking the stepper rather than by setting state.

### The walk, `c13=-3`, `c23=-5`, `c12` across the axis

| c12 | Displayed shares | CR | Verdict |
|---|---|---|---|
| 9 | 34.42 / 6.71 / 58.87 | 0.2797 | disagree |
| 5 | 29.69 / 8.56 / 61.75 | 0.1169 | disagree |
| 4 | 27.97 / 9.36 / 62.67 | 0.0739 | agree |
| 2 | 22.97 / 12.20 / 64.83 | 0.0032 | agree |
| 1 | 18.52 / 15.62 / 65.86 | 0.0251 | agree |
| −2 | 14.66 / 19.63 / 65.71 | 0.1407 | disagree |
| −9 | 8.30 / 30.29 / 61.41 | 0.7515 | disagree |

Aspect is first in all seventeen positions, between 58.87 and 65.86 per cent, while elevation
moves from 8.30 to 34.42. The window that passes 0.10 is not centred on equal: it reaches
four steps one way and none the other. The suite checks the verdict word either side of the
bar at c12 = 4 and c12 = 5.

### The eight invariants of the proposal's section 3

All eight are in the suite, and six of them are checked over every one of the 4,913 settings
rather than on a sample.

1. A coherent set scores exactly zero. `c12=2, c13=6, c23=3` gives weights exactly 0.6, 0.3,
   0.1, λmax exactly 3 and an index of exactly 0, to 1e-12.
2. All three equal gives a third each and λmax exactly 3.
3. The eigenvector and the row geometric mean agree. Worst difference over all 4,913
   settings: **1.111e-12**, which is the power iteration's own tolerance. The proposal
   measured 1.14e-12 over 20,000 random matrices; the exhaustive sweep is the stronger check
   and it is what the suite runs. At four criteria the same two estimators differ by up to
   0.216, so this is a property of three criteria and must never be written down as a
   property of the method.
4. Reciprocity. Worst `|A[i][j] * A[j][i] − 1|` over all 4,913 settings: **0.0**.
5. Relabelling two criteria permutes the weights and moves nothing else. Worst difference
   after the permutation: 0.0.
6. The three displayed shares sum to exactly 100.00, in whole hundredths, for all 4,913
   settings. **1,244 of the 4,913 would miss 100.00 under plain rounding**, which is what the
   largest-remainder rule is for.
7. Each preset reproduces the table above, and three of the four have λmax exactly 3 rather
   than approximately 3.
8. A fourth name in `n` is ignored. `?n=Shade,View,Quiet,Cost` draws three criteria named
   Shade, View and Quiet.

### The shape of the whole range

| Quantity | Count | Share |
|---|---|---|
| Settings the controls can reach | 4,913 | |
| Circles, where each criterion beats the next | 1,024 | 20.8 per cent |
| At or above the 0.10 bar | 3,826 | 77.9 per cent |
| Not a circle and still failing | 2,802 of 3,889 | |

The counts of circles and of failures are in the suite, because the circle line on the page
fires on exactly the first of them.

### What the suite printed

```
pairwise.test.js
  ok   invariant 1: a coherent set of comparisons scores exactly zero
  ok   invariant 2: all three equal gives a third each and an eigenvalue of 3
  ok   invariant 3: eigenvector and geometric mean agree at three criteria
  ok   invariant 4: the matrix is reciprocal
  ok   invariant 5: relabelling two criteria permutes the weights and nothing else
  ok   invariant 6: the three displayed shares sum to 100.00 everywhere
  ok   invariant 7: the reference encoding, to every figure recorded
  ok   invariant 8: a fourth name in the link is ignored
  ok   the bars are scaled to 100 per cent, not to the largest weight
  ok   the four presets reproduce the recorded table
  ok   the readout says the right thing at all seventeen positions
  ok   the stepper stops at the ends and reaches both of them
  ok   the verdict changes on the right side of 0.10
  ok   one step from the near tie decides the tie
  ok   the saved picture says in words what produced it
  ok   the saved picture draws its bars against 100, like the page
  ok   a saved picture does not stay on the page after a control moves
  ok   the opening state says nothing has been said, and stops saying it
  ok   a circle of comparisons is named on screen at the moment it happens
  ok   the classroom panel holds the three student steps and nothing else
  ok   nothing can make the layout wider than the viewport
  ok   nothing on the page is empty
  ok   the argument is in the reading flow, not behind a control
  ok   presentation mode keeps the numbers and drops the rest
  ok   the link carries the setting, and drops what is at its default
  ok   the live region says what changed
  ok   the page ships no unchecked citation and none of the lab's own story

661 passed, 0 failed
```

`661 passed` is the whole repository, on 19 September 2026. The pairwise suite is 283 of
those assertions across 27 tests.

### A figure that was written before it was counted

The sentence above says 1,244 settings would miss 100.00 under plain rounding. It said 1,206
first, in two documents, and nobody had counted it: the suite asserted only that the count was
greater than zero, so the number in the prose was free to be wrong. `CLAUDE.md`'s own working
notes say that a sentence stating a measurement needs a test or it goes stale silently, and
this one was wrong before it was an hour old. The suite now asserts the exact count. The same
correction was made to the review log and to the 370 folder's `CLAUDE.md` row.

The word count in the text pass below went the same way, in the other direction: the first
scan reported 3,076 student-facing words, which was a crude extraction that had swept in
JavaScript source tokens. Counted properly it was 744, and after the classroom panel lost its
two instructor paragraphs it is **640**.

### The bug that would pass a test of the numbers alone

Named before the checks were written, as `review.md` section 2 asks. The weights are right
and the bars are scaled to the largest weight rather than to 100, so the longest bar is full
width whatever it holds and nothing can be read off the picture. Every assertion about a bar
reads the width back off the element for that reason, and one of them asserts that the
largest bar is not full width.

---

## Why the choices are what they are

Most of the reasoning is in `PROPOSAL-ahp.md` sections 2 and 4 and is not repeated. What
follows is what the build decided, or decided differently.

**One stepper per comparison, on one seventeen-position axis.** The proposal's design.
Measured on the build at 375 px: the readout wraps to two lines at the long settings and to
three with a nineteen-character custom name, and the row grows to fit. Nothing scrolls
sideways in any state.

**The minus button moves towards the name on the left.** The names sit at the ends of the
row and the tick strip runs between them, so the direction of a press is the direction of the
movement. Arrow keys do the same, Home and End reach the ends, and a button at an end is
disabled rather than silently doing nothing.

**Largest remainder, ties to the lowest index.** Cell 86 of the lab tells students the three
values must add up to 100. Plain rounding to two decimals misses 100 on 1,244 of the 4,913
settings. So the page rounds down and hands the spare hundredths to the largest residuals.

**This puts the proposal in conflict with itself, and the conflict is reported rather than
hidden.** Section 2 of the proposal says that at the contradiction "the three weights read
33.33 each". Invariant 6 says the three displayed shares sum to exactly 100.00 everywhere.
Both cannot hold: three equal thirds displayed at two decimals are 99.99, and any rule that
reaches 100.00 has to give one of them the spare hundredth. The build follows invariant 6,
because it is the testable requirement and it is the one the lab's own instruction rests on,
so the equal case displays **33.34 / 33.33 / 33.33**. The tie is broken by index, which is
deterministic and is recorded here because no choice of tie-break is neutral: the first
criterion is a hundredth ahead for a reason that is arithmetic and not about the world. The
circle line on the face is what stops that reading at the moment it could happen.

**The verdict words are agree and disagree**, settled at stage 2. Under the rule-12 review
the verdict was cut to 23.55 px against the ratio's 36.86 px in presentation mode, because a
word at the number's own size reads as a mark out of ten.

**The presets are named for what they set, not for what comes out.** The proposal called them
Equal, One dominates, A near tie and A contradiction. A button labelled "A contradiction"
announces the result before the student has seen it, which is the thing Luke's first
instruction is about. They are now **All equal**, **One far ahead**, **Two tied** and **Each
beats the next**. Each name describes the three numbers the button sets. What comes out is
left to the screen.

**The stepper's words are equal, slightly more important, more important, much more
important, far more important.** The proposal's top rung was "absolutely more important",
which is awkward English. "far more important" is the same rung in plainer words.

**One hue, and nothing carried by colour.** The three bars are one blue, read by length and
by the number printed above them. The verdict is two words with no colour behind it. The tick
strip separates its three states by lightness and by height together.

**Three criteria, fixed in the code.** `n` is read as a comma-separated list and only the
first three entries are used. No URL turns this into a four-criteria page.

**The saved picture records its own inputs.** The three names, the three comparisons behind
the weights, the three weights with their fractions, the ratio with its verdict, and the
date. A marker can see in one glance whether the weights follow from what was typed.

**A saved picture is put away as soon as a control moves.** Found in the browser and not in
the suite: press Save on the older-Safari route and then press a stepper, and a picture of the
old setting sits under a page showing the new one, looking exactly as current. `render()` now
hides it, and the suite has an assertion.

**The framing sentence stays in presentation mode.** Section 2 of the proposal says the intro
hides on a projector. Section D of the same file says the opening words survive presentation
mode, which is where the MAUP widget failed the same audit. `principles.md` sections 3 and 13
settle it: presentation mode may drop controls and may not drop the argument. So the framing
sentence has no hiding rule, and the suite asserts that no such rule exists in the
stylesheet. This is the second place the proposal contradicts itself, and the repository's
rules win, as the brief directs.

**What goes on a projector, and the 720 px that decides it.** A lecture projector is 1280 by
720, not 1280 by 900. Luke, looking at the page: *"'big screen' loses the choosers."*

Measured before the fix, at 1280 by 720 with `--ui` at 1.28. The page ran **1,084 px tall**
against a 720 px viewport, so 364 px sat below the fold and a room could not scroll to it. The
three comparison rows were visible (183..299, 299..416, 416..534) and so were all six stepper
buttons, so the steppers were never the thing that went. What went was everything under the
ratio in the right column: the presets fieldset at 740..907 and the action row at 777..891,
both entirely off screen, with the ratio card's bottom edge four pixels past the fold. The
presets are the control that sets all three comparisons at once, which is the thing an
instructor reaches for at the front, so "loses the choosers" is exactly right about what a
room could reach.

The fix is a third column. In presentation mode the grid is
`minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr)` with the areas `"cmps result tools"`, which
came out at 392.8 px each at 1280. The weight rows, the ratio card and the gaps between blocks
were trimmed in presentation mode as well, because the ratio card was still nine pixels past
the fold with three columns alone.

Measured after, at **1280 by 720**: the page is **755 px tall**, so the only thing below the
fold is 35 px of the wrapper's bottom padding. Everything is on screen. The framing sentence
20..80, the title 96..130, the comparisons 147..633 with all three rows (183..327, 327..472,
472..618) and all six steppers, the three shares 147..493, the ratio card 503..715, the
presets 147..313, the classroom (i) 328..359, and Reset and Normal size 397..450. At **1280 by
900** the page is 900 px tall and nothing is below the fold at all.

Kept on a projector: the framing sentence, the title, the three readouts (29.70 px), the three
shares (40.96 px), the ratio (36.86 px), the verdict (23.55 px), the line under the ratio
(20.48 px), the presets, Reset and the classroom panel. **Dropped: the fractions and the tick
strips**, and nothing else that a room uses; How this works, Rename, Save as image, the footer
and every (i) but the classroom one also go, as they always did. The proposal left the tick
strip as a measurement for the build, and this is it: in a 392.8 px column the readouts wrap
to two lines rather than one, the rows grow to 145 px each, and all three still fit, so the
strip goes for height rather than out of necessity.

**No dependency.** Arithmetic on three numbers, a canvas and the DOM. Thirteen power
iterations on a three by three matrix. `docs/libraries.md` needs no new entry.

### The shape of the tool, and why it is one screen

Luke, 19 September 2026, giving this batch a free hand on the question:

> "to the extent that the 123ahp site doesn't make sense design-wise (is it a good idea to
> have all those separate pages or not in sequence?) please have a free hand to critique and
> revise that for better learning and usability."

The tool the lab currently sends students to is a sequence of pages. This one is not, and the
departures are four, each with its reason. Nothing below describes that tool's own screens;
the observations are in `review-log-370-AHP-1.md`.

**One screen instead of a sequence.** Every control and every result is on the page at the
same time. A sequence hides the thing you just set behind the thing you are setting now, so a
student cannot see what their own answer depends on. Here the three comparisons, the three
weights and the ratio are all visible together, which is what makes the neighbourhood of an
answer legible at all. A sequence can show one answer. It cannot show the one next door.

**The result beside the control rather than after it.** Press a stepper and the shares and
the ratio move under your hand. When the result arrives on a later page, the student has to
carry the change in their head across a navigation, which is the step where the connection
between a word and a number gets lost. This is also the usability gain: the number of actions
between changing your mind and seeing the consequence is one.

**The ratio is always on screen rather than at the end.** A number that appears only at the
finish reads as a mark. A number that moves while you work reads as a property of what you are
doing. The eighteen-word line under it is on the face for the same reason.

**Nothing to click through that carries no information for this lab.** The lab tells students
to leave every comparison between the two options at 1, so those screens produce 0.5000 for
every student in the class and the chart built on them says nothing. Steps whose output is
fixed by the instructions are steps that teach a student the tool is something to be got
through. They are not here.

**One further improvement, proposed rather than built.** A single screen shows the current
answer and still cannot show two answers at once, so the neighbourhood is something a student
has to hold in memory while pressing a button. A **Hold this** control would pin the current
three shares as faint marks on the same three bars, so the previous state and the present one
are on screen together and the size of a one-press change is a thing you see rather than a
thing you remember. It is the largest learning gain still available here and it costs one
control and one set of marks. `least-cost` already does the same trick with kept routes, which
is an argument that it works and an argument for waiting until a second widget needs it. Not
built in this batch. It needs the supervisor, because it adds a control to a face that Luke
has just asked to be cut.

---

## Known limits and open threads

**The four omissions by choice** are in `PROPOSAL-ahp.md` section 5 and stand unchanged:
options to choose between and the chart that ranks them; more than three criteria; saving a
model and coming back to it; several people's answers gathered together. None of them is
needed by anything a student is marked on.

**The random index.** The page divides by 0.58 and says so in the ratio's (i), with one line
that some tools divide by a different number and no name attached to any of them. The
attribution of 0.58 to Saaty's own simulation has not been confirmed by reading that table,
so the page states the figure and attributes it to nobody.

**No citation ships.** Non-negotiable 9 wants a separate adversarial check before any source
goes in front of a student, and the proposal's five sources are marked unchecked. No (i)
panel ends in "For more, see:", and the suite asserts that. The five sources sit in an HTML
comment at the top of the widget file so a later check has one place to start. Every claim on
the page stands without them.

**The withheld preset is gone, not deferred.** Luke's instruction 2. There is no "reading the
botanist" preset, no date and no plan to add one. The suite asserts that the words botanist,
Okanagan, species and plant appear nowhere in the page.

**The rename control's (i) tells where it could show.** The names panel carries "Nothing here
can tell you a criterion is missing." That is a sentence doing the work a control could do;
see C1 in the rule-12 review below. It is the clearest surviving case of the thing Luke's
first instruction is against, and it is left standing because the alternative needs his
judgement.

**The tick strip is a mouse shortcut.** It is `aria-hidden` and not focusable, so a keyboard
user reaches every position through the stepper and the arrow keys and never through the
strip. Nothing is unreachable. The scale's (i) now says the strip can be clicked, so the
shortcut is discoverable rather than found by accident.

**Three documents said "four widgets", and somebody else has now fixed them.** This batch
listed them rather than editing them, because the brief limited the edits to
`web/index.html` and `docs/widgets/README.md`: `CLAUDE.md` line 79 and `docs/libraries.md`
lines 7 and 34. As of the end of this batch all three read "five", changed by another session
in the working tree and not by this one. One of them was ahead of the facts while it sat in
the working tree: `CLAUDE.md` says "Five widgets, deployed and live" and gives this page's
live URL. The push of `BATCH-370-AHP-3` made it true.

**Proposed and not built: a Hold this control.** One screen shows the current answer and
still cannot show two at once, so the neighbourhood is something a student holds in memory
while pressing a button. The reasoning and the cost are under *The shape of the tool* above.
It needs the supervisor.

**Not settled: whether the page should show what the weights do downstream.** A student
cannot see here that 19 / 16 / 66 and 23 / 18 / 58 send a surveyor to different hillsides.
That needs a suitability surface, and `principles.md` section 15 forbids the lab's own. Some
other landscape might carry the same point. Open, and not for this build.

---

## The five-minute task

**A candidate, and recorded as one here rather than on the page.** `principles.md` section 16
requires that it be settled in a session with whoever teaches the course rather than drafted.
That session has not happened. The task is built into the panel so the build had something to
put through the five passes, which is not the same as it being settled.

**The panel carries the three student steps and nothing else.** It stays on the projector, so
whatever is in it is read by the room. Two paragraphs were taken out of it after the first
pass of the review, on Luke's rule that a student should be left to think about an ambiguity
rather than told about it: one told the class what the task would produce before the class had
done it, and one was a note about our own process, addressed to nobody in the room. Both are
below, the first of them verbatim.

### For whoever is running the room

This paragraph was on the page and is now here. Verbatim, as it read there:

> **For whoever is running the room.** Across twelve readings of those three sentences, shade
> came first in all twelve. It ran from 54.99 to 72.48 per cent. Two of the twelve came out at
> 0.10 or above. So pairs will differ about the numbers while agreeing about the order. Some
> pairs will be told they disagree with themselves. At the front, press **Two tied** and then
> press one stepper once. Then walk one comparison from end to end.

And the candidate note, which was the second paragraph, also verbatim:

> This activity is a candidate. Section 16 of `principles.md` asks that it be settled in a
> session with whoever teaches the course rather than drafted. That session has not happened.

Whoever runs this reads it here, from this file, before the class. That is the cost of taking
it off the page, and it is the right trade: the panel's reader in the moment it matters is the
person at the front, but its reader at every other moment is a student, and the panel cannot
tell them apart.

**The task.** A bench in a park. Three things matter: shade, view and quiet. Somebody says
shade matters clearly more than quiet, shade matters a little more than view, and view and
quiet matter about the same. Each student writes down, on paper and before opening the page,
the three percentages they think those sentences come to, largest first. Then in pairs, one
phone between two, they rename the criteria and enter each other's numbers in turn. Then the
room is asked whose sentences these were, and who else could have been asked.

**What it tests.** The sentence at the top of this file. It cannot be passed by understanding
the controls, because the commitment is made before the page is open.

**The wrong answers, and what makes each reasonable.** Measured, twelve readings, with
"clearly" read as 3 to 7 and "a little" as 2 to 4. Shade comes first in all twelve. Shade
runs from 54.99 to 72.48 per cent, a spread of 17.5 points. Two of the twelve come out at
0.10 or above, and both are the readings that make "clearly" strong while keeping "a little"
weak. So three positions arrive from the room, and all three are half right. One pair says the
numbers are a matter of opinion, so the method is subjective. Another says the order came out
the same, so it does not matter. The pair that hit 0.1169 says the method told them they had
contradicted themselves when they had done nothing of the kind.

**What the instructor does with them.** Press **Two tied** at the front and then press one
stepper once, so the room watches a 40-40 tie become 49.34 against 31.08. Then walk one
comparison from end to end, where the order does not move at all. The two together are the
whole argument, and neither is stated anywhere on the page.

**Candidates tried and dropped**, so they are not reinvented. *Predict the consistency ratio*:
nobody can, and being wrong about something you could not have got right teaches nothing.
*Which factor should matter most for a rare plant*: the lab's own question in a smaller box,
which section 15 forbids. *Find a set of three comparisons that fails the bar*: 77.9 per cent
of the range fails, so it is not a task. *The lab's own three sentences*: dropped at the
proposal's revision 2, and now dropped permanently under Luke's instruction 2.

**Section 15 check.** For this task to hand over anything that is marked, the page would have
to compute a suitability surface. It does not and will not. The example is about a bench,
which moves it further still.

---

## Review record

All five passes of `docs/review.md`, in order, on 19 September 2026, against the page served
from the repository root and opened in the app's browser pane. Anything that failed was fixed
and measured again before this record said it passed.

**A note on the server.** `docs/widget-pattern.md` and `docs/deployment.md` both say to
preview with the `repo` configuration on port 8792. That configuration is now in the
repository's own `.claude/launch.json`, which is gitignored. In this session the preview tool
reads `.claude/launch.json` from the primary working directory instead, and ports 8791 and
8792 there were already held by another session's servers, so the review ran on port 8796
against the same directory. Nothing else differed.

### Pass 1, the pedagogical critique

Run against the questions in `review.md` in order. The proposal's own measurements are cited
rather than repeated.

**What is the one thing a student should understand?** The sentence at the top of this file.
It is three sentences rather than one, and the proposal argues at its section 1 why joining
the first two loses the third.

**Does the interaction teach it, or only illustrate it?** Three things are visible only when
something moves, and all three are reachable in one or two presses. The walk: seventeen
settings in which aspect stays first between 58.87 and 65.86 per cent while elevation moves
by a factor of four. The near tie: 40-40 becomes 49.34 against 31.08 on one press, either
way. The circle: three identical bars and a ratio of 1.1494. A screenshot can print one of
those states. None of them can print the neighbourhood, and the neighbourhood is the lesson.

**What will a student do first, and what will they conclude?** Traced, three actions.

*First: press a plus or minus button on the top comparison.* The page opens with every
comparison equal and one line saying nothing has been said yet. That line disappears on the
first press and the eighteen-word line takes its place, so the first action changes the prose
as well as the numbers. What it shows: one press moves one share by a few points and leaves
the order alone. A novice concludes, correctly, that the control does something small.

*Second: hold the button down, or press it to the end.* Novices drag the biggest control to
its extremes. The extremes here are 9 times and 9 times the other way, and the button
disables at each end rather than going quiet. At the end the ratio is 0.2797 and the verdict
reads disagree. What it shows: the extremes are not degenerate and they are not the same as
each other. One end still leaves aspect first; the other end, on a different comparison,
does not. A novice concludes that pushing a control hard makes the method complain, which is
half right and is the half the second and third actions correct.

*Third: press a preset.* All four are one press and all four are legible. **Each beats the
next** is the one that pays: three bars of the same length, a ratio of 1.1494, and a line
saying the three comparisons run in a circle so they cannot all be true. A novice who has
just been complained at by the ratio meets the case where the complaint is the whole answer.

**Do the cases a student compares differ in only the thing being taught?** Taken two at a
time. **Two tied** against either of its one-step neighbours differs in exactly one
comparison and in nothing else, which is the cleanest isolation this subject allows and is
the pair the task above sends the room to. **All equal** against **One far ahead** differs in
two comparisons, which is unavoidable: with three comparisons there is no single step from
all-equal to a lopsided state. **One far ahead** against **Two tied** differs in all three
and is not a pair anybody should read across; they exist to show that two settings with
nothing in common can both score exactly zero.

**Where can a student form a wrong idea?** Three named.

The first is that a ratio of zero means the weights are good. The eighteen-word line on the
face is the only thing standing against it, and it is why that line is not in a panel.

The second is that the three shares at the equal state are a finding about elevation, slope
and aspect. The opening line says nothing has been said yet, and it returns whenever all
three comparisons are equal rather than only on load, so the state and the sentence cannot
come apart.

The third is new to the build and comes from the rounding rule. At the equal state the first
share reads 33.34 and the other two read 33.33, which invites the reading that elevation is
very slightly ahead. It is not; the hundredth is an artefact of making three thirds sum to
100.00. No sentence on the page says so, because saying it would cost more attention than the
misreading does. It is recorded here and it is a fair thing for the supervisor to overturn.

**Is the vocabulary the students' or the software's?** Nothing on the page says Saaty, scale,
pairwise comparison matrix, eigenvector or priority vector. The one technical term on the
face is "consistency ratio", and the line directly under it defines it in ordinary words in
the same breath, as `principles.md` section 8 requires. "Largest eigenvalue" and "consistency
index" appear once each, in the working shown inside How this works, beside the numbers they
name.

**Is there a way to be wrong the widget does not reveal?** Yes, and it is the honest limit.
A student can set three perfectly coherent comparisons that are wrong about the world, and
the page will print a ratio of exactly zero and say agree. That is the whole point of the
eighteen-word line, and the page cannot do better, because nothing on the screen knows
anything about the ground.

**Does the control demonstrate what you think it demonstrates? Measured.** Yes, and the
measurement changed one thing. The proposal expected the passing window to sit around the
setting a student first types. Measured on the walk, it does not: from the reference encoding
the window reaches four steps one way and none the other, because the coherent value for that
comparison is elevation 5/3 times slope. A student who assumes the ratio is a symmetric
tolerance is wrong, and the walk is where they find out. This is in the suite as the verdict
either side of the bar.

**Where does the method fail, and does the page say so?** Three failures, each reachable.
The circle is a preset and fires a line on the face. Failing the bar without a circle is
2,802 of the 3,889 non-circle settings and is reachable from the reference encoding in one
press. A coherent but false set scores zero and the face line covers it. Silence at any of
those moments would be the failure `principles.md` section 6 describes, and none of them is
silent.

**What should the instructor say while it is on screen?** The classroom panel's last two
paragraphs, which stay on the projector.

**And what does the room do for five minutes?** The four questions of `review.md`. Each
student commits on paper before the page is open: yes, and the panel says so. Two reasonable
people will differ: measured, twelve readings with a 17.5-point spread on shade. One phone
between two, five minutes including the share-back: yes, one minute, two, two. Does the
instructor know what to do with the answers: yes, three positions named and two things to run
at the front.

**Verdict: pass, with two changes requested and applied.** The preset names announced their
results, which is the same fault as telling a student the conclusion; they are renamed to
describe what each button sets. And the classroom panel carried two paragraphs a student
should not read: one told the class what the task would produce before the class had done it,
and one was a note about our own process. The panel stays on the projector, so whatever is in
it is read by the room. Both are now in this file, the first verbatim, and the panel holds the
three student steps and nothing else. It went from 224 words to 116.

### Pass 2, correctness

The bug that would pass the obvious test is named above. The suite has 283 assertions across
27 tests, six of them exhaustive over all 4,913 settings. Two independent implementations in
two languages agree with the page on every figure recorded. One case is derived by hand: for
the circle at k = 3 every row of the matrix has product 1, so every row geometric mean is 1
and the weights are exactly a third each; with those weights each row of `Aw` is
`(1 + 3 + 1/3)/3`, so λmax is exactly 13/3 and the index is exactly 2/3.

What the suite reads back off the drawing rather than off the model: the three bar widths,
the three printed shares, the ratio, the verdict word, the readout's two parts at each of the
seventeen positions, which tick is marked, whether a stepper button is disabled, the text of
the line under the ratio, whether the circle line is showing, the live region, the URL, and
what the saved picture records.

What was recorded against what was shown: the picture is drawn by different code from the
page, so the suite changes two inputs, reads the record after each, and checks that the saved
shares are the shares on screen and that a rename reaches the picture.

**Verdict: pass, with two defects found and fixed.** A saved picture stayed on screen after a
control moved, so two answers were on the page at once; fixed in `render()` and asserted in
the suite. And the layout ran 14 px wider than a 320 px viewport whenever the lesson panel was
open; measured, isolated, fixed three ways and re-measured under pass 5 below. Neither was
found by the suite, and the second was found only because a capture from outside this session
said something the review had passed.

### Pass 3, text

Every string a student can meet was read: the face, every (i) and the "?" panel, the
classroom panel, the readout words, the verdict words, the preset names, the button labels,
the `title` and `aria-label` attributes, the image alt text, the live-region announcements,
the text drawn into the PNG, the credit line, and `web/index.html`'s entry for this page.

Luke's third instruction asked for a pass against
`~/claude scratch/anti-ai-writing-style.md`. **Nine findings, all fixed.**

| # | What was found | What replaced it |
|---|---|---|
| 1 | "the method refusing, **not an answer**" — the emphasis-tail family; cut the tail and the sentence still says it | "the method refusing to answer" |
| 2 | "the three things being **weighed up**" — a phrasal verb, and the file's own warning about readers of English as an additional language | "the three things being compared" |
| 3 | "it grows as they **pull apart**" — a phrasal verb | "The further they are from fitting, the larger it gets." |
| 4 | "shade matters clearly more than quiet, shade matters a little more than view, **and** view and quiet matter about the same" — three separate statements fused | three sentences |
| 5 | "Whose sentences were these, **and** who else could have been asked?" — two questions in one sentence | two questions, two sentences |
| 6 | "shade came first in all twelve **and** ran from 54.99 to 72.48 per cent, **and** two of the twelve came out at 0.10 or above" — two run-ons in one sentence | three sentences |
| 7 | "pairs will differ about the numbers, agree about the order, **and** some will be told they disagree with themselves" — the rule-of-three reflex, and a run-on | two sentences, no triad |
| 8 | "**Two things to run at the front:** …" — a list where an instruction belongs | "At the front, press Two tied and then press one stepper once. Then walk one comparison from end to end." |
| 9 | Four `title` tooltips written as questions: "What does this number do?", "What is the scale?", "What do these buttons set?" | "About the consistency ratio", "About the scale", "About these buttons" |

Then a machine pass over every student-facing string against the file's banned vocabulary
list, its banned-phrase list, em-dashes and exclamation marks: **640 words scanned, zero
hits.** No banned verb, noun, adjective or phrase; no em-dash or en-dash anywhere in the
student-facing text; no exclamation mark. No `, and` joining two separate ideas anywhere in
the student-facing prose. The scan was run twice: once at 744 words, and again at 640 after
the classroom panel lost its two instructor paragraphs.

**Citations.** None on the page, so nothing to check adversarially. The five unchecked
sources sit in an HTML comment with a line saying not to move one onto the page until it has
been through the check.

**Verdict: pass.**

### Pass 4, accessibility

Measured from computed styles in the browser, in both themes, not eyeballed.

**Contrast, light theme.** Worst text 6.26:1, against a floor of 4.5:1. Framing 17.76, title
17.76, criterion name 6.26, share 15.99, fraction 6.26, ratio label 6.26, ratio number 15.99,
the face line 15.99, readout 17.76 and 6.95, legend 6.95, buttons 17.76, footer 6.95, the (i)
glyph 6.26, help-panel prose and matrix cells 15.99.

**Contrast, dark theme.** Worst text 7.21:1. Framing 15.29, share 13.61, ratio number 13.61,
face line 13.61, readout 15.29 and 8.11, help-panel prose 13.61, matrix head 7.21.

**Graphical parts, against a floor of 3:1.** Light: bar against its track 3.44, bar against
the page 6.29, track against the panel 1.65, marked tick against unmarked 5.17, unmarked tick
against the page 3.44, fieldset and button borders 3.44. Dark: bar against track 3.51, bar
against page 7.94, track against panel 2.01, marked tick against unmarked 3.87, unmarked tick
against page 3.95, focus ring against page 7.94.

Two things were changed by this pass and measured again. The bar track was #d7dade and sat at
1.27:1 against the panel, which is a track a reader cannot see, so a bar drawn against 100
looked like a bar drawn against nothing; it is #bcc0c6 and 1.65:1 now, with the bar still at
3.44:1 against it. The unmarked ticks were drawn in the track colour at 1.40:1 against the
page, which is not a scale anybody can read; they are the edge colour at 3.44:1 now, the
marked tick is the ink colour and full height. Lightness and height both separate it, so the
cue survives greyscale.

A second version of that rule was taken out again after Luke looked at the page. It drew the
middle of the axis heavier as well, in the soft ink colour at 80 per cent height, which on an
8.8 px strip is 7.0 px. Luke: *"doesn't the thicker line for 'balanced' confuse with the
actually selected relative criteria selection? maybe just make the center look the same as
others."* He is right: two emphasised marks on one axis read as two selections. Measured after
the change, on a row set to position 4: the marked tick is `rgb(22, 24, 29)` at 8.8 px, the
centre tick is `rgb(132, 139, 149)` at 4.8 px, and the fifteen other ticks are
`rgb(132, 139, 149)` at 4.8 px. The centre is now drawn exactly like every other tick, the
`mid` class is written nowhere and the rule that styled it is gone. On a row whose comparison
is equal the one dark tick sits in the middle, which is correct: it is the selected position
rather than a marker.

**Colour carries nothing.** The three bars are one hue and are read by length and by the
number above them. The verdict is two words with no colour behind it. In greyscale the page
loses nothing, because every distinction it makes is a distinction in lightness, length or
text.

**Keyboard.** Twenty tab stops, in reading order: the ratio's (i), the comparisons' (i), the
six stepper buttons, the presets' (i), the four presets, the classroom (i), How this works,
Rename, Save as image, Reset, Big screen, and the source link. Every control was operated
from the keyboard. Arrow left and down step one way, arrow right and up the other, Home and
End reach the axis ends, and the handler ignores a keypress carrying a modifier. The focus
ring is a 3 px solid outline at 2 px offset, measured at 7.94:1 against the page in dark and
drawn in the screenshot on the third comparison's plus button.

**Targets.** Every button and input is at least 44 by 44 CSS pixels on every pointer, not
only under `pointer: coarse`. The template's 2.6rem comes out at 41.6 px on a laptop, so the
sizes are now `max(44px, …)` and the coarse-pointer override was removed rather than left
beside them. The (i) glyphs are 25 by 25, which is the documented exception: they sit inline
in a legend where 44 would overlap the row beneath, and 24 is the floor. The footer's source
link is a text link in a sentence rather than a control.

**Screen readers.** Each comparison is a `role="group"` whose accessible name is "Elevation
compared with Slope" and so on. Each stepper button says where it moves and in which
comparison: "More weight to Elevation, in the Elevation against Slope comparison". The bar
tracks are `aria-hidden`, and the same information is beside them as text, which is what
`principles.md` section 9 asks for. The live region is polite and, after one press, reads
"Elevation 2 times Aspect, slightly more important. Elevation 41.26 per cent, Slope 32.75 per
cent, Aspect 25.99 per cent. Consistency ratio 0.0462, agree."

**Motion.** Three animated things on the whole page, all of them a bar's width, and the
`prefers-reduced-motion: reduce` block turns off exactly those. Read out of the stylesheet
rather than assumed: `@media (prefers-reduced-motion: reduce) { .fill { transition: none; } }`.
Nothing flashes and nothing is on a timer.

**Zoom.** At 640 by 450, which is 1280 by 900 at 200 per cent: document scroll width 640
against a viewport of 640, nothing overflowing, one column, and the three readouts on one
line each.

**Language.** `lang="en"` on the root. Text in `rem` throughout.

**Verdict: pass, with two changes requested and applied** (the track and the ticks), both
measured again above.

### Pass 5, device and room

**Touch, 375 by 812.** One column: framing, title, the three shares with their bars, the
ratio with its verdict and its line, the three comparisons, the presets, the classroom panel,
then the buttons. Document scroll width 375 against a viewport of 375, in the opening state,
at the longest readout, and with nineteen-character custom names in two of the three slots.
The readout wraps to two lines at the long settings and to three with the long names, and the
row grows rather than clipping. Smallest control 44 px. Nothing needs hover, nothing needs a
drag, and the tick strip is a cue rather than a target there.

**Laptop, 1280 by 900.** Two columns above 56rem: the three comparisons on the left, the
shares, the ratio, the presets, the classroom panel and the buttons on the right, with the
framing sentence spanning both. Scroll width 1265 against 1280. Nothing is oversized.

**Projected, `?present=1` at 1280.** Read back above under what goes on a projector. The
`p` key and the Big screen button do the same thing, and the button's label and pressed state
follow.

**Embedded, an iframe at 600 by 800.** Loaded with `?c12=5&c13=-3&c23=-5`. It restored the
setting (0.1169, disagree, 29.69 / 8.56 / 61.75), laid out in one column, scroll width 585
against 600, nothing overflowing, and a stepper press inside the frame moved it to 0.0739 and
27.97 / 9.36 / 62.67.

**Narrow phones, measured the hard way after a headless capture reported clipping at
375 × 812.** The report could not be reproduced at 375 and something worse was found below it.
At 375, with every panel open and two nineteen-character custom names,
`document.documentElement.scrollWidth` is 375 against a `clientWidth` of 375, no element has a
right edge past the viewport, and no element's `scrollWidth` exceeds its `clientWidth`. The
framing sentence's box ends at 360.6 and the line under the ratio at 346.8. The viewport meta
tag is `width=device-width, initial-scale=1`. So nothing is clipped at 375.

At **320** it was. The page laid out 334 px wide inside a 320 px viewport, 54 elements had a
right edge past it, and the text at the right margin was cut. The cause, isolated by hiding
one panel at a time: the three by three matrix inside **How this works**. A table will not
shrink below its own min-content width, that panel's min-content was 313 px, and the single
column of `.main` was an `auto` track, which takes its width from the widest min-content
inside it. Add the wrapper's padding and the minimum layout width the page could accept was
about 342 px. Below that it overflowed, and at 375 it did not.

Fixed three ways at once, because one guard is not enough for this class of bug. The track is
`minmax(0, 1fr)` rather than `auto`. The three grid areas and their children declare
`min-width: 0`. The table sits in a `matrix-wrap` box with `overflow-x: auto`, so wide content
scrolls inside its own box and never the page body. Re-measured at 320, 360 and 375, every
panel open, with the long names: **scrollWidth equals clientWidth at all three, zero elements
past the edge, zero clipped**, and the matrix scrolls inside its own box as intended.

**What the headless capture was probably showing.** Two numbers bear on it. At 1280 in this
browser the classic scrollbar takes 15 px, so `clientWidth` is 1265 against an `innerWidth` of
1280; a capture that sizes its image to the window rather than to the layout viewport crops
the rightmost 15 px of the picture without anything being clipped by CSS. And the pre-fix
minimum layout width was about 342 px, so any capture whose layout viewport was narrower than
that, for whatever combination of scrollbar reservation and device scale, met a real overflow.
Both mechanisms produce the reported symptom and the second one was a genuine defect. It is
fixed either way.

**A layout assertion cannot live in this suite**, because the stub lays nothing out and every
`getBoundingClientRect` is whatever the test sets. `tools/test/README.md` says so. What the
suite asserts instead is the three guards above, which is what would regress, plus that no
rule gives any element a fixed width of 100 px or more. The measurement stays here, with its
numbers.

**Links.** The URL writes 330 ms after things settle and omits anything at its default. Three
comparisons and two names came back as `?c12=4&c13=-3&c23=-5&n=Shade%2CView%2CQuiet`. Pressing
All equal writes an empty query. A link carrying a setting restores it, including which way
round each comparison points. `c12=0`, `c13=99` and `c23=abc` all fall back to equal.

**Responsiveness.** The solve is thirteen power iterations on a three by three matrix. There
is nothing to stutter and no worker.

**The picture.** Save was exercised without triggering a download, by removing `toBlob` so the
page took its documented older-Safari route and put the same PNG on the page. The canvas is
780 by 1,262 for the reference encoding, and it reads: the title, *What was compared* with the
three comparisons as sentences, *The weights these give* with the line explaining that each
number appears twice, the three names with their percentages and fractions and a bar each,
*How well the comparisons agree* with the ratio sentence and the line saying what it does not
measure, the address of the page, and the date. On a 375 px phone the picture displays at
346 px, which puts the title at 16 CSS pixels, the sentences at 13.3, the percentages at 19.5
and the address at 10.7.

The three bars were read back off the canvas pixels rather than trusted: 18.50, 15.61 and
65.75 per cent of the track against the 18.52, 15.62 and 65.86 printed beside them, the
difference being one column of antialiasing at each bar's end. The suite now reads the same
three widths out of the recorded `fillRect` calls and checks them to a hundredth of a point,
because a bar scaled to the largest weight would be full width whatever it held, in a file a
marker opens months later, and no assertion about the text would see it.

**Console.** No errors, no warnings, in a fresh tab.

**Verdict: pass.**

### Sign-off

```
Widget: pairwise
Reviewed: 2026-09-19

Pedagogical critique: pass — preset names renamed to describe what they set rather
  than what comes out; the classroom panel cut to the three student steps
Correctness: pass — 283 assertions, six exhaustive over all 4,913 settings; two defects
  found and fixed (a saved picture outliving the setting that produced it, and a layout
  14 px wider than a 320 px phone)
Text: pass — nine anti-AI findings fixed; 640 student-facing words scanned against
  the banned lists with zero remaining hits; no citation ships
Accessibility: pass — worst text contrast 6.26:1 light and 7.21:1 dark; every graphic
  part past 3:1; all targets 44 px; two changes applied and re-measured
Device and room: pass — 320x800, 360x800, 375x812, 1280x900, ?present=1, 200 per cent
  zoom, iframe 600x800

Outstanding: the classroom activity is a candidate and needs the session with Luke.
  Three documents go stale at the deploy and are listed above. The tie-break in the
  rounding rule puts a hundredth on the first criterion at the equal state.
```

---

## Rule 12, the critical review

Three parts, in order, with the proposal's section D as the starting point and a verdict on
each item. Section D was written against a proposal. This is written against a page.

### What it already does well

**The translation is on the face and the conclusion is not.** The framing sentence says the
three numbers decide what a survey looks for and that somebody made them by reading
sentences. It stops there. Under the proposal it went on to say that two readers do not agree
and that the map is not the same map. A student who is told that has been given the finding;
a student who presses a button twice has found it. Luke's instruction made the page better
at the thing rule 12 is for, which is worth saying plainly because the usual direction of
travel is the other way.

**It refuses the answer key by construction.** The page computes three weights and stops.
There is no configuration of it that produces a suitability surface, so nothing here answers
the questions the lab marks. `principles.md` section 15 by construction rather than by asking
students not to look.

**The method is shown refusing.** One press reaches a setting where the arithmetic returns
three equal shares and a ratio of 1.1494, and a line on the face says the three comparisons
run in a circle. A calculator that prints a third three times and says nothing teaches the
opposite of what happened.

**It declines to dress the number up as a grade.** The eighteen-word line is on the face, not
in a panel, and it survives the projector. The verdict was cut to two thirds of the ratio's
size in this review for the same reason.

**It now costs a later instructor nothing.** Luke's second instruction removed the withheld
preset and the date. A page that needs somebody to remember to change it in October is a page
that will be wrong in November.

### What it could become

Proposals for the supervisor, not changes made.

**C1. The second speaker.** The proposal's C1 asked for a fourth name field, greyed, labelled
as a criterion nobody asked about, which accepts a word and then does nothing with it, because
the method has no place to put it. The page currently *says* this instead: the rename panel
carries "Nothing here can tell you a criterion is missing." Under Luke's first instruction the
sentence is the weaker version and the control is the stronger one, so C1 is more attractive
now than when the proposal weighed it. *Cost:* one field, one line, and a real risk of being
read as a bug. *Verdict: could become, and it needs Luke, because a control that deliberately
does nothing is a strong move that can also read as a trick.*

**C2. Whose ground the survey walks on.** The proposal expected this question to arrive with
the "reading the botanist" preset, which would have given the page a place. Instruction 2
removed that preset for good, so the page names no place and never will. The question does not
arrive here. *Verdict: not applicable to this page, and recorded so the next person knows the
route by which it would have arrived was closed deliberately.* It belongs to whatever page
draws the Okanagan.

**C3. The weights as a record of a conversation that did not happen.** The proposal wanted
three sentences in the lesson panel saying that the same arithmetic is run in rooms with many
people in them and that averaging disagreement is itself a choice. Luke's first instruction
takes that panel down to what a comparison is, what the weights are and what the ratio
measures, so the sentences cannot go there. The showing version is a build: a second reader's
column, two sets of three comparisons side by side, and the page drawing what averaging them
does. *Cost:* a real change to the page, and a citation that would have to pass the
adversarial check. *Verdict: could become, as a build rather than as a paragraph.* Of the
three it is the one most likely to land.

**C4. The saved image as evidence.** Already half done: the picture records the three
comparisons that produced the weights, so a student's translation is auditable by the marker
and by the student. The proposal wanted it to carry the sentence each comparison came from.
There are no sentences on the page now. The classroom panel's three bench sentences are the
only ones available, and putting them in a picture of a different setting would be wrong.
*Verdict: closed by instruction 2, unless a later build gives the page sentences of its own.*

### What must change

Three, each with the concrete edit. **All three were applied in this build and measured
again.**

**M1. The verdict was drawn at the size of a result.** In presentation mode at 1280 the ratio
read 36.86 px and the word beside it read 36.86 px, while the eighteen-word line that stops
the pair reading as a pass mark read 20.48 px. A word at a number's own size is a grade. The
concrete edit: the verdict is a word and not a measurement, so it takes its own size.
**Applied:** `.verdict` is now `calc(1.15rem * var(--ui))`, measured at 23.55 px in
presentation mode, and the word and the line now read as one block under the number.

**M2. The tick strip was a shortcut only a mouse user could find.** It is clickable on a
desktop, `aria-hidden`, and not focusable. Nothing is unreachable, because the stepper and
the arrow keys reach every position. But a shortcut that exists only for whoever happens to
try clicking is a shortcut distributed by luck, which is the small local version of the thing
this page is about. The concrete edit: say it exists. **Applied:** the scale's (i) now reads
"On a computer you can also click the row of ticks to jump straight to a position."

**M3. The 0.10 bar was presented as a fact rather than as a convention.** The ratio's (i)
already attributed the divisor ("The ratio divides by 0.58… Some tools divide by a different
number") and already attributed the words to the page ("Below 0.10 this page prints agree").
The threshold itself was unattributed, so a student met one number chosen by somebody and one
number apparently given by nature. The concrete edit: two short factual sentences, no
coaching. **Applied:** "The 0.10 is a convention. Nothing in the arithmetic picks it."

### Considered and left standing

**The framing sentence still names nobody.** The proposal's own M1 said that "somebody" is a
way of not saying. The framing now reads "Somebody made them by reading an expert's
sentences", so the objection survives the cut in a new coat. Luke's first instruction rules
out the repair the proposal made, which was to name the reader as the student. The page's
answer is that the student is the one pressing the buttons, and the classroom panel's
share-back question asks the room whose sentences these were. That panel stays on the
projector. Recorded as a standing tension between a rule-12 finding and an instruction, with
the instruction winning and the demonstration standing in for the sentence.

**The verdict words have no subject.** "0.1169 disagree" does not say who or what disagrees.
Adding a subject costs words on a face Luke has just asked to be cut. The eighteen-word line
supplies it. Left, with the reason.

**The default names are three terrain variables**, so the page opens looking like a page
about terrain rather than about weighing anything up. Instruction 2 fixes the defaults. The
classroom panel renames them to shade, view and quiet, which is the showing version of the
point. Left.

---

## The five-second audit, before and after

`principles.md` section 8 asks that everything on screen at rest be readable in about five
seconds. Section 13 grants a separate fifty-word budget above the fold. Luke's first
instruction asked for the audit to be done again after the cut, with the counts.

| | Proposal, revision 2 | Built |
|---|---|---|
| Framing sentence | 49 words | **24 words** |
| Line under the ratio | 18 words | 18 words |
| Body prose on the face | 67 words | **42 words** |
| Opening-state line, in place of the 18 | not counted | 10 words |
| Circle line, only in a circle | not counted | 23 words |
| The "?" lesson panel | the short version of section 1, what the ratio is and is not, that two readers differ, that the order survives, the worked demonstration, the missing-criterion sentence, the arithmetic-not-a-cycle paragraph, and the near-zero pair | **81 words** and the working shown: the three by three matrix, the largest eigenvalue and the index |

What is on the face at rest, everything closed: the framing sentence, the title, three
criterion names, three percentages, three fractions, three bars, the words "Consistency
ratio", the ratio, one verdict word, one line, three pairs of criterion names, three readouts
in words and numbers, three tick strips, four preset names, two legends, five button labels
and the credit line. 109 words in total, of which 42 are prose.

The other panels: the ratio's 47 words, the scale's 69, the presets' 29, the classroom
panel's **116**, the names panel's 21, the save note's 8. The classroom panel was 224 words
until the two paragraphs addressed to the instructor came out of it; it is now three
paragraphs of 67, 33 and 16 words, one per step, and every one of them is addressed to a
student.

---

## Picking it up again

The page is `web/pairwise/index.html`, one self-contained file with no dependency and no
second request. The suite is `tools/test/pairwise.test.js`, run by `node tools/test/run.js`.
The two independent checks are `tools/pairwise-verify.js` under `node` and
`tools/pairwise-verify.py` under a Python with numpy, which on this machine is
`/opt/homebrew/bin/python3` because `/usr/bin/python3` is 3.9.6 with none.

To look at it: serve the repository root and open `/web/pairwise/`. The `repo` configuration
in `.claude/launch.json` does this on port 8792. Do not use a `file://` URL: `replaceState`
is unreliable there.

The numbers to check first after any change. The reference encoding's three weights and its
ratio of 0.025055. The circle's exact thirds and its λmax of exactly 13/3. Invariant 3, which
is the one that says the choice between the eigenvector and the geometric mean cannot be made
to matter at three criteria. Invariant 6, which is the rounding rule, because it is the claim
a student's mark rests on. And the bar widths, because a bar scaled to the largest weight
looks right and says nothing.

Done: the deploy, on 19 September 2026 under `BATCH-370-AHP-3`. `docs/deployment.md` has the
deploy key, the Pages workflow and the gate. The three "four widgets" sentences read "five" and
none of them is ahead of the facts any longer.

Not yet done: the adversarial check on the five sources, after which an (i) panel may end in
"For more, see:" for the first time on this page.

Not yet done: the session with Luke that turns the classroom activity from a candidate into
the activity.
