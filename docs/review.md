# Review before shipping

Four passes. A widget is not finished until it has been through all of them. Record the
result in the widget's own folder as `REVIEW.md` so we can see what was checked and when.

The passes are ordered so that the expensive one comes first. There is no point polishing
the contrast on a widget that teaches the wrong thing.

---

## 1. Pedagogical critique

This pass can send the work back for redesign. It is not a polish pass.

The critic is given the widget and the teaching context, and is asked, in this order:

**What is the one thing a student should understand after using this?** State it in a
sentence. If it takes more than a sentence, the widget is doing too much and should be
split.

**Does the interaction teach that thing, or does it only illustrate it?** A student
should learn something by moving a control that they could not learn by looking at a
static figure. If a screenshot would do the same work, the interactivity is decoration.

**What will a student do first, and what will they conclude from it?** Trace the likely
first three actions. Novices poke at the biggest control and drag it to the extremes.
What do the extremes show? If the extreme cases are degenerate or misleading, fix the
ranges.

**Where can a student form a wrong idea?** Name the specific misconception the widget
might create or reinforce. Defaults, ranges, and colour choices all carry implications
that students read as claims.

**Is the vocabulary the students' or the software's?** Every label should be a word the
course has already taught or a word in ordinary use.

**Is there a way to be wrong that the widget does not reveal?** If students can reach a
nonsensical configuration, does the widget show them that it is nonsense, or does it
draw it as though it were fine?

**What should the instructor say while this is on screen?** If that is not obvious, the
widget probably needs a caption or a clearer default.

The critique produces requested changes, in priority order. Changes that affect what
students learn come before changes that affect how it looks.

## 2. Text

Read every string in the widget: titles, labels, tooltips, instructions, error messages,
legend text, captions.

- Would a first-year student with no technical background understand this sentence on
  first reading?
- Would someone reading English as an additional language understand it? Idiom, phrasal
  verbs, and metaphor are the usual failures.
- Is any technical term used before it is defined?
- Does anything read as machine-written? Check against
  `~/claude scratch/anti-ai-writing-style.md`.
- Can any sentence be shorter without losing its meaning?
- Read it aloud. Anything that trips the tongue gets rewritten.

## 3. Accessibility

- Keyboard only: reach every control, operate every control, see where focus is.
- Zoom the page to 200%. Nothing overlaps, nothing is cut off, nothing scrolls sideways.
- Screen reader: does every control announce what it is and what its value is? Does the
  graphic have a text alternative that conveys the same information?
- Colour: view in greyscale, and simulate deuteranopia and protanopia. Is any distinction
  now lost? If so, add a second cue.
- Contrast: check text and control graphics against their actual backgrounds, including
  over map tiles. 4.5:1 for body text, 3:1 for large text and control parts.
- Motion: check `prefers-reduced-motion`. Nothing flashes, nothing is on a timer.
- Touch targets at least 44x44 CSS pixels, with space between.

## 4. Device and room check

Three contexts, checked separately. See `docs/principles.md` section 3.

**Phone.** Open it in portrait on a real phone, over a slow connection, and use it for a
minute. Every control reachable by thumb. Nothing that needs hover. Nothing that needs a
precise drag. No horizontal scrolling. Reload with the network off after the first load
and see what it says.

**Laptop at reading distance.** Mouse and keyboard. Hover readouts work. Keyboard
shortcuts work. Nothing is comically oversized — this is the ordinary student URL and it
should look like a normal web page.

**Projected.** Open the presentation URL (`?present=1`) on the machine used in the
lecture room, put it on the projector in a lit room, and walk to the back. Read the
controls, the current values, and the legend from there, not just the graphic. Then look
at it in a compressed recording at medium resolution and check that thin lines and small
type have survived.

**Embedding and links.** Open it in an `<iframe>` at the sizes we actually embed at.
Click the URL from a PowerPoint slide on the lecture machine. Confirm that a URL carrying
a particular configuration restores that configuration.

---

## Sign-off

```
Widget:
Course:
Reviewed: YYYY-MM-DD

Pedagogical critique: pass / changes requested — summary
Text: pass / changes requested — summary
Accessibility: pass / changes requested — summary
Room and device: pass / changes requested — summary

Outstanding:
```
