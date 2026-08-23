# Widget files

One file per widget, named for its folder under `web/`. This is the record that lets a
widget be rebuilt, corrected, or argued with a year later, when the reasoning behind a
choice is gone and only the choice is left.

| Widget | File | State |
|---|---|---|
| [Spatial autocorrelation on a grid](https://foldingspace.github.io/interactive/spatial-autocorrelation/) | [spatial-autocorrelation.md](spatial-autocorrelation.md) | Live |
| [Drawing the lines: MAUP in Vancouver](https://foldingspace.github.io/interactive/maup/) | [maup.md](maup.md) | Live |
| [Least cost, whose cost?](https://foldingspace.github.io/interactive/least-cost/) | [least-cost.md](least-cost.md) | Live |
| [Vancouver, measured in minutes](https://foldingspace.github.io/interactive/relative-distance/) | [relative-distance.md](relative-distance.md) | Live |

Anything that would be true of the next widget too goes in the shared documents, not here:
how to draw a quantity in `../visual-forms.md`, how a widget is put together in
`../widget-pattern.md`, how it gets checked in `../review.md`, and what a widget must be in
`../principles.md`. What stays here is the instance — this widget's numbers, this widget's
choices, and why they went this way rather than another. A lesson written in both places
goes stale in one of them.

## What every one of these has to contain

The order is up to you and the headings can be whatever suits the widget. These six have
to be in there somewhere, because each of them has already been needed.

**The one thing it teaches**, in a sentence, at the top. If that sentence is hard to
write, the widget is doing too much.

**Verified numbers.** Specific values the widget produces for specific inputs, checked by
a route that shares no code with it. These are the regression suite: after any change,
they either still come out or something broke. Record how they were checked, not only
what they were.

**Why the choices are what they are.** Defaults, presets, colours, thresholds, wording.
Include the options that were tried and dropped, and why. Half the value of these files
is stopping the same rejected idea from being reinvented.

**Known limits and open threads.** What the widget cannot do, what is misleading about it,
and the questions raised and not settled. Mark a guess as a guess. Anything not yet
computed must be computed before it appears anywhere a student can read it.

**The five-minute task.** What the **For the classroom** panel asks, what it is testing,
the wrong answers expected and what makes each one reasonable, what the share-back does with
them, and the candidates tried and dropped. `../principles.md` section 16. Pair tasks are
easy to reinvent, which is why the rejected ones matter as much as the one that shipped.

**Picking it up again.** The live URL, where the code is, how to preview it locally, and
which numbers to check first. Written for a reader with no memory of building it, because
that reader will be you.

The review record from `docs/review.md` also lives here: which passes were run, what they
found, and what was changed as a result.
