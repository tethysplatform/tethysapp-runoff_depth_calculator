---
sidebar_position: 6
title: "Step 6: Add the Stepper"
---

# Step 6: Add the Stepper

**Concept:** For the input panel, we will use a [Mantine `Stepper`](https://mantine.dev/core/stepper/), which facilitates guiding users through a multi-step process. Recall the four inputs `calculate_runoff` needs: area (from the map), precipitation, soil group, and land use. We'll lay those out as steps now, as **static UI** — no interactivity yet. That comes in the next step.

Replace the second column's `lib.m.Text("Steps go here")` placeholder with a Stepper:

```python
lib.m.Stepper(active=0)(
    lib.m.StepperStep(
        label="Step 1",
        description="Select an urban area on the map"
    )("Click on a map feature"),
    lib.m.StepperStep(
        label="Step 2",
        description="Assign precipitation"
    )(
        lib.m.Slider(
            min=0,
            max=10,
            step=0.1,
            marks=[lib.Props(value=i, label=f'{i}in.') for i in range(0, 11)],
        )
    ),
    lib.m.StepperStep(
        label="Step 3",
        description="Assign soil group"
    )(
        lib.m.Select(
            data=["Group A", "Group B", "Group C", "Group D"],
            placeholder="Select soil group",
        )
    ),
    lib.m.StepperStep(
        label="Step 4",
        description="Assign land use"
    )(
        lib.m.Select(
            data=["Residential", "Commercial", "Forest"],
            placeholder="Select land use",
        )
    ),
)
```

## Key ideas

- **`lib.m.Stepper`** shows numbered steps; `active=0` hardcodes it on the first step for now. Each child is a **`lib.m.StepperStep`** with a `label` and `description`, and content passed as children.
- **The inputs map to the function's arguments**:
  - the area will come from the user's feature selection on the map via click
  - a `lib.m.Slider` ([Mantine Slider](https://mantine.dev/core/slider/)) collects precipitation;
  - two `lib.m.Select`s ([Mantine Select](https://mantine.dev/core/select/)) collect the soil group and land use. Their `data`/`min`/`max` mirror what `calculate_runoff` expects.
- **Static for now.** Nothing updates yet — there's no state and no handlers. The slider and selects don't remember their values, and the active step never changes.

## Full `home()` so far

```python
@App.page
def home(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            style=lib.Style(height="70vh", marginBottom="1em")
        )(
            lib.ol.layer.Vector(
                lib.ol.source.Vector(
                    options=lib.Props(
                        url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                        format="GeoJSON",
                    )
                )
            )
        ),
        lib.m.Stepper(active=0)(
            lib.m.StepperStep(
                label="Step 1",
                description="Select an urban area on the map"
            )("Click on a map feature"),
            lib.m.StepperStep(
                label="Step 2",
                description="Assign precipitation"
            )(
                lib.m.Slider(
                    min=0,
                    max=10,
                    step=0.1,
                    marks=[lib.Props(value=i, label=f'{i}in.') for i in range(0, 11)],
                )
            ),
            lib.m.StepperStep(
                label="Step 3",
                description="Assign soil group"
            )(
                lib.m.Select(
                    data=["Group A", "Group B", "Group C", "Group D"],
                    placeholder="Select soil group",
                )
            ),
            lib.m.StepperStep(
                label="Step 4",
                description="Assign land use"
            )(
                lib.m.Select(
                    data=["Residential", "Commercial", "Forest"],
                    placeholder="Select land use",
                )
            ),
        )
    )
```

## What you should see

Reload the app and you should now see a four-step stepper below the map. Nothing is interactive, so you are stuck seeing "Step 1", meaning that content for steps 2-4 remain hidden. Next, we will bring it to life by applying principles of ***state***.
