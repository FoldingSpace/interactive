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

So: two layouts, not three. A touch layout and a desktop layout, split on pointer type
and width, not on width alone. Use `pointer: coarse` and `hover: none` to detect the
touch case rather than guessing from the viewport, since a narrow desktop window is not a
phone and a tablet is not a laptop.

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

Deep-linking: the current configuration should be expressible in the URL, so a
particular case can be handed out or put on a slide.

## 5. Content and tools

The subject is cartography and GIS, which means the browser has to do real spatial work:
projections, tiling, raster handling, spatial statistics, symbolisation. That is a
constraint on the JavaScript and WebAssembly we can lean on, and it is the reason
`docs/libraries.md` exists. Keep it current.

Preference order when choosing a dependency: something we have already used here and
that worked; then a small, well-maintained open library with a clear licence; then
WebAssembly ports of the desktop tools; then writing it ourselves. Every dependency is
pinned to a version and vendored or loaded from a stable source, so a widget used in a
lecture in 2029 still runs.

## 6. Text

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

## 7. Accessibility

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

## 8. Openness and attribution

Everything we ship is open, and everything borrowed is credited.

- Only use data, basemaps, imagery, fonts, icons, and code whose licence permits
  reuse and redistribution, including in teaching. Record the licence, not just the
  name.
- Attribution is visible in the widget itself, not only in the source, and it stays
  legible at classroom distance. Basemap and data credits go in a persistent line or a
  clearly marked info control.
- Every external thing gets an entry in `docs/attributions.md` when it is added.
- Our own code is MIT and our own text and figures are CC BY 4.0, so anyone can pick a
  widget up and adapt it. Anything we add must be compatible with that.

## 9. Review before shipping

No widget goes in front of students without the passes described in `docs/review.md`.
The pedagogical critique is the one that can send the work back for redesign, not just
for polish.

---

## Open questions

- How much lives in `web/shared/`. A common stylesheet and a common set of controls
  is cheaper to maintain and makes the widgets feel like one family, but it couples
  them, so a change to shared code means rechecking everything. Decide after the
  second widget, not before the first.
- Whether widgets should record anything (a student's answers, a saved configuration).
  Anything stored raises privacy questions and a FIPPA question at UBC. Default for now:
  store nothing, keep state in the URL only.
