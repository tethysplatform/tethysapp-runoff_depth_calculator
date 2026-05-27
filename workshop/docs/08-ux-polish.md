---
sidebar_position: 8
title: "Step 8: UX polish"
---

# Step 8: UX polish

**Concept:** Small touches make the workflow feel finished — highlight the selected feature,
restrict interaction to the right step, and let users reset.

## Highlight the selected feature

Use a `Styler` with `unique_values` so the chosen polygon is styled differently from the
rest. Replace the layer's `style` with:

```python
style=lib.ol.style.Styler(
    method="unique_values",
    fields=["area_sqkm"],
    values=[
        (
            selected_feature["area_sqkm"] if selected_feature else -9999,
            lib.ol.style.Style(
                stroke=lib.ol.style.Stroke(color="purple", width=1),
                fill=lib.ol.style.Fill(color="white"),
            ),
        ),
    ],
    default=lib.ol.style.Style(
        stroke=lib.ol.style.Stroke(color="#000000", width=1),
        fill=lib.ol.style.Fill(color="#ff0000"),
    ),
)
```

## Restrict and reset

Two UX behaviors you already wired in earlier steps are worth calling out:

- **Click only on step 0** — the `onClick` is attached conditionally
  (`... if active_step == 0 else {}`) so the selection can't change once the workflow
  starts.
- **Start Over** — the second button in `StepperCompleted` resets every piece of state back
  to its initial value, returning the user to step 0.

## Key ideas

- **`method="unique_values"`** styles features by matching a field (`area_sqkm`) against
  given values; the selected feature's value gets the purple/white style, everything else
  falls to `default`. The `-9999` sentinel means "match nothing" when no feature is selected.
- **State-driven UX.** Highlighting, interactivity, and reset are all just functions of
  state — no special framework machinery.

## What you should see

The clicked polygon turns purple/white; other polygons stay red. You can't re-select while
stepping; **Start Over** returns everything to the beginning.
