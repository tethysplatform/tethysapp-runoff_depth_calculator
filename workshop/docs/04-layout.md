---
sidebar_position: 4
title: "Step 4: Page layout"
---

# Step 4: Page layout

**Concept:** Before adding real content, design the overall page structure. For this application, the vision is to have two sections stacked vertically: a map on top, and a step-by-step input panel below. We'll build that and fill it in over the next steps.

We currently have a map filling the entire space of our app, so we need to configure its height to leave space below for our step-by-step input panel, and then add placeholder for that panel. This can be done as seen below:

```python
@App.page
def home(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            style=lib.Style(height="70vh", marginBottom="1em")
        ),
        lib.m.Text("Steps go here")
    )
```

## Key ideas

- **`style=`** is the most standard way to customize the intrinsic, visual properties of a component. This takes a dictionary of key-value pairs, where the keys are the properties you are setting.
- **`lib.Style(...)`** is a helper function that allows you to continue to write pythonic, kwarg-style syntax for the key-value pairs rather than dictionary syntax (e.g. `style=lib.Style(height="100%")` rather than `style={"height": "100%"}`). You may use whichever you prefer.
- **`height="70vh"`** sets the height to 70% of the browser's available view height (vh)
- **`marginBottom="1em"`** sets a margin of 1 "em" (the height of a capital "M" in the currently set font) to provide some responsive white space between the map and the steps section.

## What you should see

Reload the app and you should now see two sections rendered: the Map and just below it the "Steps go here" placeholder.
