# Principles

Standing rules for the interactive widgets in this repository. They are made to
explain ideas in cartography and GIS: mostly in teaching, also in talks and
alongside writing. Where these rules say "student", read "whoever is looking at
it" — the lecture case is the demanding one, so it sets the standard.
This file is edited as we learn. Date and initial substantive changes.

Started 2026-08-19.

---

## 1. Delivery

How this is actually wired up — the deploy key, the Pages workflow, the folder layout —
is recorded in `deployment.md`.

**Static hosting, no exceptions.** Everything must run from GitHub Pages: plain HTML,
CSS, JavaScript, and WebAssembly served as files. No server-side code, no database, no
API key that would have to be kept secret. If a widget needs data, the data ships with
it or is fetched from a documented open source over plain HTTPS.

**No install, no account.** A student opens a link in whatever browser they already have
and it works. Nothing to download, nothing to sign into, no extension.

**One URL per widget.** Each interactive is its own page at its own stable address, so
it can be linked from a PowerPoint slide, a Canvas page, an email, or a QR code on a
slide. Once an address is used in a lecture, it does not move.

**Embeddable.** Each widget must also work inside an `<iframe>` on someone else's page.
In practice: no code that assumes it owns the whole window, no navigation away from
itself, no reliance on the URL bar being visible, and a sensible minimum size. State that
matters goes in the URL query string so an embed can be pre-set to a particular
configuration.

**Offline-tolerant where cheap.** Lecture rooms lose their network. Prefer bundled data
over live requests. If a widget must fetch, it should say plainly what went wrong rather
than sit blank.

## 2. It starts by itself

A widget loads with defaults already chosen and something already drawn. The student sees
the finished case first and then takes it apart. No empty state, no wizard, no "select a
variable to begin". If a computation is slow, show the default result computed ahead of
time and let interaction replace it.

**And the default must not be a dead end.** It is not enough for the opening state to show
something; it has to be a state in which the widget's own lesson is reachable. The
autocorrelation grid opened on rook weights, under which no square can ever be significant
— so a student who found the significance control and switched it on met "nothing here"
before they met the idea. Queen is the default now and rook is one click away, which is
where a limit belongs: something you arrive at, not something you start inside. Check every
default by asking what happens when a student turns on each control in turn.

## 3. Three viewing contexts, two layouts

Every widget has to work in three situations, and they are not variations of one problem.

**A. Phone, portrait, touch, held at arm's length.** Students following along in class or
afterwards. Touch only: no hover, no right-click, no precise pointer, no fine drag.
Little screen, and the important controls belong low where the thumb reaches. The
control set itself is different here, not just its size — a stepped segmented control
often beats a slider, a bottom sheet often beats a side panel, and anything needing two
hands is out. Everything revealed by hover on desktop must have a tap route here.
Portrait first; landscape should not break, but is not where the work goes.

**B. Desktop or laptop browser, mouse and keyboard, reading distance.** Students
reviewing later, doing an assignment, poking at it properly. Wide screen, so panels can
sit side by side. Hover is available, so tooltips and readouts on hover are worth having.
Keyboard shortcuts are worth having. Fine pointer control means sliders, drag handles,
and small hit targets are all reasonable.

**C. Desktop browser projected, seen from the back of a lit room, and later in a
compressed recording.** This is the lecture case. It is the same browser and the same
CSS as B — the machine cannot tell the difference, and no media query will separate them.
Projector gamma crushes dark tones and washes out light ones; video compression destroys
thin lines, small text, and low-contrast edges.

So: two layouts, not three. A touch layout and a desktop layout, and the split is not one
query. Width decides the column count, because whether two panels fit side by side is a
question about width. Pointer type decides control shape and target size, because whether
a slider is usable is a question about the pointer, and a narrow desktop window is not a
phone. Ask `pointer: coarse` and `hover: none` for the second of those, never for the
first.

The first widget sizes its targets for touch in both layouts rather than only under
`pointer: coarse`. That is simpler, it costs a mouse user nothing, and it means the touch
query is left for the cases that genuinely need a different control rather than a bigger
one.

**The hard part is that B and C share their CSS.** Sizing that reads from fifteen metres
looks absurd on a laptop at sixty centimetres, and sizing that is right on a laptop
disappears on a projector. This cannot be solved automatically, so it is solved by an
explicit choice:

Every widget has a presentation mode, entered by a URL parameter (`?present=1`) and
toggled by a key. Presentation mode scales up type, line weights, markers, control parts,
and legend, and it may drop secondary controls and explanatory text that nobody at the
back will read anyway. The URL in the PowerPoint slide points at presentation mode; the
URL given to students points at the ordinary one. This fits the way the materials are
already handed out, and it means neither audience gets a compromise.

Build it so one variable drives the scaling rather than a second stylesheet. Keep text in
`rem` so a reader's own font-size preference still works, and put the presentation
multiplier in a custom property applied through `calc()`. Settle the exact mechanism on
the first widget and write it down here.

**Presentation mode may drop controls. It may not drop the argument.** Building the MAUP
widget, the (i) buttons were hidden on a projector to buy height, which put every critical
claim behind a control that no longer existed. A lecture would have shown the statistics
and none of the reasoning. Whatever a widget is *for* — the thing you would say if you had
one sentence — belongs in the reading flow at every size, not in a panel and not in a
footer. Cut secondary controls and explanatory detail instead.

**Rules that hold in every context.** Never encode anything that matters in a one-pixel
line, a small marker, or a subtle tint. Controls must be as legible as results: a student
at the back needs to see which control moved and what value it now holds, so show current
values as text beside the control. Contrast high enough to survive a projector. No
horizontal scrolling anywhere. Touch targets at least 44x44 CSS pixels in the touch
layout.

## 4. Interaction

Few controls, each doing one clear thing. Prefer three good controls to eight that
cover every case. Name each control in words a first-year student would use, not in the
vocabulary of the underlying library.

Changes are immediate and visible. Something on screen must move when a control moves.

Every widget has a reset. A student who has made a mess gets back to the opening state
in one tap.

**It must stay responsive while being used.** A control that stutters while it is being
dragged teaches that the thing is fragile. Two rules serve this. Anything expensive goes
off the main thread, into a worker, so the interface never waits for it; and the cheap
result is drawn immediately while the expensive one arrives when it is ready. And redraw
only what changed — rewriting every cell of a grid on every frame is usually the cost, not
the arithmetic.

Measure this rather than assume it. In the first widget, moving the heavy computation to a
worker made it *slower* until the algorithm was fixed, and the single largest win came from
not touching DOM nodes whose value had not changed.

Deep-linking: the current configuration should be expressible in the URL, so a
particular case can be handed out or put on a slide.

## 5. Examples that isolate one thing

A widget teaches by comparison: this case against that one. **Whatever is not being taught
must be held constant between them**, or students will attribute the difference to the
wrong cause, and the widget will have taught something false with more conviction than any
sentence could.

The case that produced this rule: the spatial autocorrelation grid compares a scattered
pattern with a clustered one. Generated naively, the two also differ in how much grey they
contain, and a student cannot tell which difference is doing the work. Fixing the number
of grey squares at 113 in both makes arrangement the only thing that changed, so +0.04
against +0.59 can mean one thing and one thing only. Same amount of grey, different
arrangement, different answer.

So when building the presets, defaults, and ranges for a widget, ask what varies between
the cases a student will actually compare, and pin everything that is not the lesson.
This usually means generating examples under a constraint rather than taking whatever a
sampling procedure hands you.

Two habits follow:

**Fixed seeds, always.** Anything random uses a seed written into the code, never
`Math.random()`. A student's phone in the third row and the projector at the front must
show the same example, or the discussion falls apart. It also means a value quoted in a
lecture is still true next year.

**Defaults and ranges are claims.** The opening state says "this is what this normally
looks like", and the ends of a slider say "this is how far this goes". Both are read as
assertions about the world whether or not they were meant that way. Choose them as
carefully as you would choose a sentence, and check what the extremes actually show: if a
range ends somewhere degenerate or misleading, change the range.

## 6. Show what the method cannot do

Every method has a blind spot, and a widget is the best place a student will ever meet it,
because they can watch it happen instead of being told. **When a method fails, silence is
the wrong answer.** A blank result reads as a statement about the data when it is a
statement about the method, and a student who draws that conclusion has learned something
false with the widget's authority behind it.

Three of these turned up in the first widget, and each one became a preset rather than a
paragraph:

**A structure the measure cannot see.** Stripes score exactly zero on Moran's I under
sides-only weights. The pattern is unmistakable; the number says nothing. So the wording
for a near-zero result says what the number reports and sends the reader back to the grid,
rather than claiming the arrangement is random.

**A distinction the measure discards.** Half of the queen's ring, pointing one way, gives
exactly the same answer as the whole ring, because only the symmetric part of the weights
reaches the arithmetic. A kernel that visibly points east, and a number that does not move.

**A question the data cannot answer.** With four binary neighbours the smallest possible
p-value is about 0.042, so under those weights nothing can ever pass a corrected
significance test, whatever the pattern. Instead of an empty map, the widget reports the
smallest p-value reached and says a wider kernel gives finer ones.

**An answer that is one of several the method cannot choose between.** `least-cost` draws a
route; at its tightest setting one of the alternatives it offers shares barely a third of its
length and costs the same to within a thousandth of a per cent. And changing the queue inside
the solver — a detail with nothing geographic in it — moved half the route at a cost identical
to every digit that can be printed. Where an optimisation has ties, which answer you are shown
is a property of the software. Software normally shows one and says nothing, which is the
strongest version of this section's problem: not a blank result but a confident one.

**A choice that changes nothing.** The least-cost widget carries a preset called "keep
away from homes" that moves the route by 0.2 km, because the cheapest route was already
avoiding houses. Whether a value you assert has any consequence is a fact about the ground,
not about how strongly you hold it. A widget whose every control visibly works teaches that
every value you hold has an effect, which is false and is the more comfortable of the two
beliefs.

The rule that falls out: **when a result is empty, undefined, or unmoved, say why on
screen.** Not in the notes, not in the lecture — on screen, at the moment it happens. It
costs a line and it converts the widget's worst moment into its best one.

The related habit is to build the failing case into the presets deliberately, so it can be
reached in one click and demonstrated on purpose rather than stumbled into.

### Some limits are a reason to build something else

Not every blind spot should be demonstrated. The least-cost widget was designed to route to
Roberts Bank, and any route there reaches the causeway through Tsawwassen First Nation
treaty land. A cost surface can only deal with that by giving it a number, and consent does
not have a price; making it an impassable barrier is the same category error with the sign
flipped. The two ways of handling it inside the widget were to draw the land and refuse to
price it, or to price it and let students find the error themselves.

The corridor was moved instead, and that was the right call. A widget has one screen and a
few sentences. A subject that needs more than that is not made safe by being handled
carefully in a corner of something about power lines, and a page that raises it and then
moves on has used it. Move the example, and put in the widget's own file why it moved — so
the next person does not rediscover the problem and solve it worse.

Note what this does not license, and note what is still unresolved. Choosing a corridor
that avoids land under separate Indigenous jurisdiction says nothing whatever about the land
it does cross. At present that is written in the widget's own file and not on the page, so
a reader of the page meets a silence. Whether a page that maps land and prices it should say
something, and what, is in the open questions below — it is a decision about how the course
speaks, not a technical one, and the failure mode described two paragraphs up applies to the
easy answer.

## 7. Content and tools

The subject is cartography and GIS, which means the browser has to do real spatial work:
projections, tiling, raster handling, spatial statistics, symbolisation. That is a
constraint on the JavaScript and WebAssembly we can lean on, and it is the reason
`docs/libraries.md` exists. Keep it current.

**Prefer the exact answer to the simulated one.** Where a quantity has a closed form,
compute it; simulate only where it does not. A simulation is an approximation carrying its
own error, and that error can exceed what it is estimating: in the first widget, 999
permutations reported a smallest p-value of 0.040 where the smallest genuinely attainable
was 0.0587, so the simulation was inventing extremes that cannot occur and the widget was
reporting them as findings.

Two things worth keeping apart, because they are routinely conflated. **Simulation error**
is noise from a finite number of trials and shrinks as you run more. **Discreteness** is
structural — with four binary neighbours there are five possible outcomes and therefore
fifteen possible p-values, whether you run 999 trials or ten million. More simulation fixes
the first and does nothing for the second, and pushed at a problem of the second kind it
manufactures the appearance of resolution instead of the thing itself.

**Try it with no dependency first.** The first widget here needed none: the statistics,
the seeded random numbers, the colour interpolation, the drag painting and the worker are
all a few dozen lines each, and a library for any of them would have been more code to
integrate than to write. A widget with no dependencies is also a widget that still runs in
2031, which matters when a URL is printed on a slide.

Preference order when a dependency is genuinely needed: something we have already used here
and that worked; then a small, well-maintained open library with a clear licence; then
WebAssembly ports of the desktop tools; then writing it ourselves. Every dependency is
pinned to a version and vendored or loaded from a stable source, so a widget used in a
lecture in 2029 still runs.

## 8. Text

### How much

**The commonest fault is too much of it.** Words on screen compete with the thing the
widget exists to show, and a paragraph beside a graphic is a paragraph nobody reads while
the graphic is moving. Prose belongs in the lecture, in the reading, and in the
instructor's mouth. What stays on screen is the minimum that makes the display legible on
its own.

The working rule: everything on screen at rest should be readable in about five seconds.
A number, its scale, a two-word verdict, one short line of context, and the controls. If
a sentence is explaining rather than labelling, it does not belong on the face of the
widget.

Everything else goes one layer down, reachable and never in the way:

- A **disclosure** — a "?" button opening a short panel — for the explanation a student
  might want on their own time. This is the main mechanism, because it works by touch, by
  mouse, and by keyboard, and screen readers announce it properly.
- **`title` tooltips** as a small extra for mouse users. Never put anything there that a
  reader must have: tooltips do not appear on touch and are unreliable for screen readers.

Presentation mode strips further. At the back of a room nobody reads a sentence, so
explanatory text hides and only the number, the verdict, and the controls remain.

### How it reads

Student-facing text is short and plain.

- Concrete words over abstract ones. Short sentences. One idea per sentence.
- Assume little technical background, and assume many readers are reading English as an
  additional language. Avoid idiom, avoid metaphor that needs cultural knowledge, avoid
  academic register.
- Define a technical term the first time it appears, in the same sentence, in ordinary
  words.
- No AI-register vocabulary or structure. Follow
  `~/claude scratch/anti-ai-writing-style.md`. In particular: no hype adjectives, no
  "dive in", no fake questions, no three-part lists used as decoration.
- Labels and instructions say what will happen, not what the interface is called.
- Prose, not bullet fragments, in explanatory passages. Lists are for actual lists.

Note: the `luke-david-style` voice skill is for scholarly prose written as Luke and
David. Student-facing interface text is a different register and should not go through
it. Repository documentation and lecture prose written in Luke's own voice may.

## 9. Accessibility

Treat WCAG 2.1 AA as the floor, and go past it where a classroom makes it easy.

**Colour.** Never carry meaning in hue alone. Pair colour with shape, pattern, position,
direction, or a label. Default to colour schemes that hold up under the common forms of
colour vision deficiency and in greyscale: for sequential data, viridis or cividis or a
single-hue ColorBrewer ramp; for diverging data, a ColorBrewer diverging scheme checked
for deuteranopia; for categories, keep the count low and choose a set checked for
distinguishability. Red and green never oppose each other as the only cue. Every widget
that uses a colour ramp shows its legend on screen, sized like the rest of the interface.

**Contrast.** 4.5:1 for normal text, 3:1 for large text and for the graphical parts of
controls. Check against the actual background, including over map tiles.

**Keyboard.** Everything operable by mouse or touch is operable by keyboard, in a
sensible order, with a visible focus outline. Sliders respond to arrow keys.

**Screen readers.** Semantic HTML first. Label every control. Give each graphic a text
alternative that says what it shows, and where a map or chart carries data a student
needs, provide the same information in a table or in text.

**Motion and timing.** Respect `prefers-reduced-motion`. Nothing flashes. Nothing is on a
timer that a student has to keep up with. Nothing depends on a precise gesture, a drag
that cannot be done another way, or fine motor control.

**Text sizing.** The page must survive being zoomed to 200% and must respect the reader's
default font size. Do not disable pinch zoom.

**Dark and light.** Respect the reader's theme where it does not fight the cartography.
Note that a projector in a lit room usually favours dark marks on a light ground, which
is the opposite of what many students set on their phones. If a widget offers both, it
opens in the version that projects well.

## 10. Openness and attribution

Everything we ship is open, and everything borrowed is credited.

- Only use data, basemaps, imagery, fonts, icons, and code whose licence permits
  reuse and redistribution, including in teaching. Record the licence, not just the
  name.
- Attribution is visible in the widget itself, not only in the source, and it stays
  legible at classroom distance. Basemap and data credits go in a persistent line or a
  clearly marked info control.
- Every external thing gets an entry in `docs/attributions.md` when it is added.

**Settle the licence before the subject, not after the build.** The least-cost widget was
designed around a dataset it could never have shipped — DMTI, licensed to institutions, the
basis of the whole lab it came from — and moving to Metro Vancouver's open land use changed
the city, the corridor, the classes, and what the widget could argue. That was not damage
control. The open data has an agricultural class where the licensed data has none, which is
exactly the class the lab's own question needs and cannot express, so the constraint handed
over the widget's best idea.

Expect that to be usual rather than lucky. Openly licensed data is generally published by
somebody with a public reason to maintain it, and the categories follow the reason. A
licence check is not paperwork to do at the end; it is one of the first things that decides
what the widget can be about.
- Our own code is MIT and our own text and figures are CC BY 4.0, so anyone can pick a
  widget up and adapt it. Anything we add must be compatible with that.

## 11. Explanations and what they cite

Every control that embodies a choice carries an **(i)** button: a short explanation, in
plain words, of what the choice does and why it matters. Explaining to a beginner is not
the same as leaving out the reasoning. Say what the thing does, say what it costs, and
say what it cannot do — a student who understands the trade is better served than one who
has been given a simplified answer they will later have to unlearn.

Each explanation ends with **For more, see:** and one or two real sources, so a student who
wants the proper treatment knows where to go and can see that the widget is reporting
established work rather than inventing it.

### Citations are checked adversarially, always

**No source appears in this repository until a separate adversarial check has confirmed it
exists and says what we claim it says.** The check is run by a subagent whose brief is to
falsify, not confirm: assume every entry is wrong until independent evidence says
otherwise, and report CANNOT CONFIRM rather than guessing.

Three failure modes, in increasing order of harm:

1. **The work does not exist.** A fabricated citation.
2. **The work exists but the details are wrong** — year, journal, volume, pages. Makes a
   real source hard to find and signals carelessness about the rest.
3. **The work exists and is cited accurately, but does not support the claim attached to
   it.** This is the worst, because it survives a casual look. A plausible paper next to a
   claim it never made is harder to catch and more damaging than an obvious invention.

The check must test all three, and the third explicitly. Anything reported as wrong is
corrected or removed before the material ships — never softened, never left in with a
hedge. Anything reported as CANNOT CONFIRM is removed, because an unverifiable citation in
teaching material is worse than no citation.

This applies to every explanation, caption, and document in the repository, not only to
things labelled as a bibliography.

### One sentence, one claim

`maup.md` said the aspatial model draws "exactly zero circles — not small ones, none". The
drawing part is exactly right: zero circle elements against 992. The values are not
identically zero, though — they are floating-point noise below 7.11e-15, because the term is a
subtraction of two quantities the code reaches by different routes. One sentence was standing
for a claim about the picture and a claim about the arithmetic, and a reader could reasonably
have taken either. Where a statement could be read two ways and only one of them is true,
split it and assert both separately.

The same discipline applies to recorded numbers. Reordering the terms of a sum changed a
tolerance from 7.1e-15 to 1.42e-14, because floating-point addition is not associative.
Neither figure is more correct; the new one is what a rebuild will now see, so it is the one
recorded, with the reason beside it.

### The citation most likely to fail is the one attached to a framing

Cite a paper for a method or a number and it either has it or it does not; the check is
quick and it usually passes. Cite one for a *stance* — that a practice opens something up,
that a technique is participatory, that a tool democratises anything — and you are almost
always reaching for a review, and a review reports the argument rather than settling it.

Four citations went out with the least-cost widget. The two attached to methods passed
outright. Both of the two attached to framings came back needing the claim rewritten, and
one of them was carrying the opposite of what its author had argued: Sieber's review treats
"GIS broadens participation" as the field's contested question and gives serious space to
the objection that such software lends the illusion of control while control stays where it
was.

The repair is not to soften the claim. It is to cite the argument rather than the side of it
you like, objection included. That is more accurate, and it is better teaching — a student
who is told a thing is contested and shown by whom has been given something to do.

### The claim drives the citation, never the reverse

When what a widget does changes, the sources attached to it have to be re-examined, and the
temptation is to keep a verified citation by adjusting the claim until it fits. Don't.

The extent control was built to change resolution, and cited the modifiable areal unit
problem, correctly. When it became a clipped window it stopped changing the units at all,
and MAUP no longer applied. Both sources were real, verified, and about something else, so
they were removed and that panel now carries no citation. **Raising a neighbouring idea
because you happen to have a source for it is its own kind of dishonesty**, and no citation
is better than a nearby one.

Keep such entries in `attributions.md` under "verified, then dropped". That they were
checked and found irrelevant is worth more to a future reader than a silent deletion.

## 12. Review before shipping

No widget goes in front of students without the passes described in `docs/review.md`.
The pedagogical critique is the one that can send the work back for redesign, not just
for polish.

## 12b. How a thing gets drawn is its own body of practice

Graphical decisions recur across widgets while their subjects do not, so they live in
`docs/visual-forms.md`: quantities on areas, small multiples, showing that something
decomposes, colour, and the audit to run after changing what is displayed. Two rules from it
are load-bearing enough to repeat here. A count is never a choropleth. And a row of small
multiples needs one shared scale, or it is a row of unrelated pictures.

## 13. What is at stake belongs on the face of the page

A widget that teaches a method will be read as a widget about the method. If the point is
partly about what the data is, who made it, and what it is used for, that has to be visible
before anyone opens anything.

Audit it by listing what a reader sees with every explanation closed, at every screen size.
The MAUP widget failed that audit: the visible text was a title, a methods question, four
control labels and two grey lines in the footer, and the city it was about was not named
anywhere. The fix was about fifty words above the fold, in the reading flow.

Fifty words is the budget. Section 8's rule still applies, and a paragraph of framing that
nobody reads is worth less than three sentences that land.

## 14. One repository, many widgets

The widgets are meant to feel like one family and to be maintainable one at a time. Those
two goals pull against each other, and the resolution is that the family resemblance comes
from shared *conventions*, copied, rather than shared *code*, imported.

Each widget stays a single self-contained file. That is what keeps it embeddable, linkable,
and independent of anything else in the repository, and it is what makes it safe to leave
a widget untouched for a year. `template/` holds a working skeleton with the machinery
every widget needs, and starting a widget means copying it. `docs/widget-pattern.md` says
what to keep and what to replace.

**A shared file waits for the second widget that needs it, and usually for the third.**
Duplication between two files is visible and cheap. A shared file is a thing that can break
a page nobody is currently looking at, and its cost lands later, on whoever is not
expecting it. When something is finally shared, every widget depending on it has to
re-pass the verified numbers in its own file before the change goes out.

**Expect the rules to bend on the next widget, and write down the bending.** The first
widget was pure computation, so it needed no libraries, made no network calls after load,
and could be checked exactly. A widget with a basemap breaks at least two of those, and the
honest response is to change the claim, not to work around it to keep the claim true. What
generalises from one build is a way of working — measure, check by an independent route,
say what the method cannot do. What does not generalise is any particular answer.

**A widget that is not on the front page does not exist.** `web/index.html` is the only
route in for anyone who was not handed a URL, and it is part of shipping, not a follow-up.

## 15. A widget built beside an assessment

Two of these came out of a course lab, and both had to answer the same question before
anything else: what stops this being the answer key? A public page that hands over a marked
exercise is worse than no page, because it arrives looking like teaching.

**The refusal has to be structural, not a warning label.** Anything that depends on a
student choosing not to look has already failed. The MAUP widget refuses the crime category
its lab asks students to model. The least-cost widget runs on a different city, a different
destination and a different classification, so there is no configuration of it that
reproduces the lab's surface.

**And the refusal should be the lesson.** This is the part worth aiming for rather than
settling for. The category the MAUP widget declines to model is declined for a reason it
states on screen, and that reason is the substantive point about police data. The
classification the least-cost widget uses has an agricultural class where the lab's has
none — which is the finding the widget exists to make, arrived at by working the lab and
noticing that the value its own question asks students to defend cannot be expressed in its
own categories.

The working order that produced both:

Work the lab through in full first, computing every answer rather than reasoning about them.
That is where the widget's subject comes from, and it is where the lab's own errors turn up:
between them these two produced a friction table with no class for the thing it asks about,
a topography claim that is false twice over, a distance comparison a quarter of which is a
grid artefact, and two questions that are the same question and are never joined.

Keep that worked version in the local folder, outside the public repository, and say in
`CLAUDE.md` that it is to stay there.

Then design so the widget cannot answer the questions, and check it by trying: take each
question in turn and say what the widget would have to become for it to hand the answer
over. If the answer is "nothing, a student would just have to read it carefully", start
again.

A last note on tone. Neither widget is coy about where it came from. Being unable to serve
as an answer key is not the same as pretending to be unrelated, and a student who works out
that the widget is about the same methods as their lab has understood something rather than
cheated.

---

## Open questions

- **How the widgets should be grouped once there are more than a handful.** The front page
  is a flat list, which stops working somewhere around eight. By topic, by course, by what
  kind of thing they do — all defensible, none obviously right, and it does not have to be
  settled until the list is long enough to be annoying.
- Whether the template earns being more than a copy. See section 14: the answer stays no
  until a second widget wants the same code, and the decision belongs to whoever builds it.
- Whether widgets should record anything (a student's answers, a saved configuration).
  Anything stored raises privacy questions and a FIPPA question at UBC. Default for now:
  store nothing, keep state in the URL only.
- **How to show that a cutoff is a choice.** Every spatial weighting in use draws a hard
  line and treats everything beyond it as unrelated, which nobody really defends — Tobler's
  line is that near things are *more* related, not that far things are unrelated. The
  autocorrelation widget shows that *where* the line falls changes the answer, but not what
  happens as it recedes. Letting a neighbourhood grow without limit, and watching the
  number as it does, is the experiment. Not yet run; see that widget's file.
- **Whether a page that maps land should say whose land it is, and how.** Two of these draw
  real places in British Columbia, price them, and cut them up. Neither says anything on
  screen about territory, and the least-cost widget's corridor was chosen partly to avoid a
  jurisdiction the method cannot represent, which makes the silence louder rather than
  quieter. The obvious fix — a line of acknowledgement in the footer — is close to the
  failure section 6 warns about, where a subject too big for one screen gets handled in a
  corner and moved past. Doing nothing is also a position. This is Luke's call and it has
  not been made; until it is, the reasoning stays in each widget's file where the next
  person will find it.
