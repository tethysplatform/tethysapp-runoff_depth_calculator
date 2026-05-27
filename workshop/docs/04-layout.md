---
sidebar_position: 4
title: "Step 4: Page layout"
---

# Step 4: Page layout

**Concept:** Before adding real content, lay out the page structure. Our app has two
regions stacked vertically: a map on top, and a step-by-step input panel below. We'll
build that with a grid and fill it in over the next steps.

Replace the body of `home` (the `lib.m.Title(...)` from Step 2) with a grid containing two
full-width columns. We'll use placeholders for now:

```python
@App.page
def home(lib):
    return lib.tethys.Display(
        lib.m.Grid(
            lib.m.GridCol(span=12, style=lib.Style(height="70vh"))(
                lib.m.Text("Map goes here")
            ),
            lib.m.GridCol(span=12)(
                lib.m.Text("Steps go here")
            ),
        )
    )
```

## Reading the component syntax

This is the core pattern you'll use everywhere, so it's worth slowing down:

- **Props are keyword arguments.** `lib.m.GridCol(span=12, style=...)` configures the
  component.
- **Children come from calling the result.** `lib.m.GridCol(span=12)( ...children... )`.
  So `GridCol(span=12)(Text("..."))` is "a column containing a Text".
- **`lib.tethys.Display`** wraps the whole page in the app's standard layout.
- **`lib.m.Grid` / `lib.m.GridCol`** are the Mantine grid. `span=12` means full width (the
  grid is 12 columns wide), so the two columns stack.
- **`lib.Style(height="70vh")`** sets inline CSS — the map column is 70% of the viewport
  height.

## What you should see

Reload the app: two stacked regions, one reading "Map goes here" (tall) and one reading
"Steps go here". Next we replace the first placeholder with a real map.
