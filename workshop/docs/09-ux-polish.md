---
sidebar_position: 9
title: "Step 9: UX polish"
---

# Step 9: UX polish

**Concept:** Though the app is now functional, users appreciate feedback confirming their actions have been aknowledged and accepted by the application. Guard rails also help to prevent users from doing something they shouldn't. Two small, state-driven touches will address these concepts and make the workflow feel finished: highlight the selected polygon, and prevent the user from changing the selection during a subsequent step.

## 1. Highlight the selected feature

To allow the selected feature to be highlighted, we need to apply a custom styler to the `ol.layer.Vector` component that defines both a default style and that of the selected feature. This is done by adding the following `style` property to the `ol.layer.Vector` component, alongside the existing `onClick` property:

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

## 2. Restrict map clicks to the first step

To ensure the `onClick` is only present/active during Step 1, we can use the following in-line trick to get a conditional kwarg property:

```python
lib.ol.layer.Vector(
    **{
        "onClick": lambda e: (
            set_selected_feature(e.get("features", [{}])[0]),
            set_active_step(1)
        )
    } if active_step == 0 else {},
    style=lib.ol.style.Styler(
        # ...the unique_values styler from above...
    )
)(
    # ...source unchanged...
)
```

## Key ideas

- **`method="unique_values"`** styles features by matching a field (`area_sqkm`) against listed values; the selected feature's value gets the purple/white style, everything else falls to `default`. The `-9999` sentinel matches nothing when no feature is selected.
- **Conditional props.** Spreading `**({...} if active_step == 0 else {})` adds `onClick` only on the first step — interactivity itself becomes a function of state.

## The complete `home()`

```python
@App.page
def home(lib):
    selected_feature, set_selected_feature = lib.hooks.use_state({})
    area_acres = selected_feature.get("area_sqkm", 0) * 247.105
    precip, set_precip = lib.hooks.use_state(0)
    soil_group, set_soil_group = lib.hooks.use_state(None)
    land_use, set_land_use = lib.hooks.use_state(None)
    active_step, set_active_step = lib.hooks.use_state(0)
    result, set_result = lib.hooks.use_state(None)
    show_results, set_show_results = lib.hooks.use_state(False)

    return lib.tethys.Display(
        lib.tethys.Map(
            style=lib.Style(height="70vh", marginBottom="1em")
        )(
            lib.ol.layer.Vector(
                **{
                    "onClick": lambda e: (
                        set_selected_feature(e.get("features", [{}])[0]),
                        set_active_step(1)
                    )
                } if active_step == 0 else {},
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
            )(
                lib.ol.source.Vector(
                    options=lib.Props(
                        url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                        format="GeoJSON",
                    )
                )
            )
        ),
        lib.m.Stepper(
            active=active_step,
            onStepClick=set_active_step
        )(
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
                    value=precip,
                    marks=[lib.Props(value=i, label=f'{i}in.') for i in range(0, 11)],
                    onChange=lambda val: (set_precip(val), set_active_step(2)),
                ),
            ),
            lib.m.StepperStep(
                label="Step 3",
                description="Assign soil group"
            )(
                lib.m.Select(
                    key="soil_group",
                    data=["Group A", "Group B", "Group C", "Group D"],
                    value=soil_group, placeholder="Select soil group",
                    onChange=lambda val, _: (set_soil_group(val), set_active_step(3)),
                ),
            ),
            lib.m.StepperStep(
                label="Step 4",
                description="Assign land use"
            )(
                lib.m.Select(
                    key="land_use",
                    data=["Residential", "Commercial", "Forest"],
                    value=land_use, placeholder="Select land use",
                    onChange=lambda val, _: (
                        set_land_use(val),
                        set_active_step(4),
                        set_result(calculate_runoff(area_acres, precip, soil_group, val)),
                    ),
                ),
            ),
            lib.m.StepperCompleted(
                lib.m.Center(
                    lib.m.Button(onClick=lambda _: set_show_results(True))("View Results"),
                    lib.m.Button(
                        onClick=lambda _: (
                            set_selected_feature({}),
                            set_precip(0),
                            set_soil_group(None),
                            set_land_use(None),
                            set_active_step(0),
                        )
                    )("Start Over")
                )
            ),
        ),
        lib.m.Modal(
            opened=show_results,
            onClose=lambda *args: set_show_results(False),
            title="Runoff Calculation Results",
        )(
            lib.m.Text(f"Estimated runoff volume for selected storm: {result['user_volume']} cubic feet"),
            lib.m.Text(f"Curve Number used in calculation: {result['cn']}"),
            lib.pl.Plot(
                style=lib.Style(width="100%", height="100%"),
                data=[
                    lib.Props(
                        x=result["storms"],
                        y=result["volumes"],
                        type="scatter",
                        mode="lines+markers",
                        marker=lib.Props(color="red"),
                    ),
                ],
                layout=lib.Props(
                    autosize=True,
                    title=lib.Props(text="Design Storm Runoff Volumes"),
                    xaxis=lib.Props(title=lib.Props(text="Design storm depth (in)")),
                    yaxis=lib.Props(title=lib.Props(text="Runoff Volume (cubic feet)")),
                ),
            )
        ) if result else None
    )
```

## What you should see

The clicked polygon turns purple/white while the others stay red, and you can no longer re-select once you've started unless you return to Step 1.
