---
sidebar_position: 6
title: "Step 6: Add the Stepper"
---

# Step 6: Add the Stepper

**Concept:** The input panel is a Mantine `Stepper` — a guided, multi-step form. Recall the
four inputs `calculate_runoff` needs: area (from the map), precipitation, soil group, and
land use. We'll lay those out as steps now, as **static UI** — no interactivity yet. That
comes in the next step.

Replace the second column's `lib.m.Text("Steps go here")` placeholder with a Stepper:

```python
lib.m.GridCol(span=12)(
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

## Key ideas

- **`lib.m.Stepper`** shows numbered steps; `active=0` hardcodes it on the first step for
  now. Each child is a **`lib.m.StepperStep`** with a `label` and `description`, and content
  passed as children.
- **The inputs map to the function's arguments.** `lib.m.Slider` collects precipitation;
  two `lib.m.Select`s collect the soil group and land use; the area comes from the map click
  (Step 1). Their `data`/`min`/`max` mirror what `calculate_runoff` expects.
- **Static for now.** Nothing updates yet — there's no state and no handlers. The slider and
  selects don't remember their values, and the active step never changes.

## Full `home()` so far

```python
@App.page
def home(lib):
    return lib.tethys.Display(
        lib.m.Grid(
            lib.m.GridCol(span=12, style=lib.Style(height="70vh"))(
                lib.tethys.Map(
                    lib.ol.layer.Vector(
                        style=lib.ol.style.Styler(
                            default=lib.ol.style.Style(
                                stroke=lib.ol.style.Stroke(color="#000000", width=1),
                                fill=lib.ol.style.Fill(color="#ff0000"),
                            ),
                        )
                    )(
                        lib.ol.source.Vector(
                            options=lib.Props(
                                url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                                format="GeoJSON",
                            )
                        )
                    )
                )
            ),
            lib.m.GridCol(span=12)(
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
            ),
        )
    )
```

## What you should see

Reload the app — below the map, a four-step stepper with a slider and two dropdowns. You can
move the slider and open the dropdowns, but nothing is remembered and the stepper stays on
Step 1. Next we bring it to life with state.
