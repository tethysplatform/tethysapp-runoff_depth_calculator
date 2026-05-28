---
sidebar_position: 8
title: "Step 8: Displaying the results"
---

# Step 8: Displaying the results

**Concept:** With `result` now able to be stored in state, we wire up a completion step that contains a button to view the results in a modal.

## 1. Add modal-visibility state

The modal is opened/closed by its own boolean. Add it with the other `use_state` calls at the top of `home`:

```python
show_results, set_show_results = lib.hooks.use_state(False)
```

## 2. Add a completed panel to the Stepper

After the four `StepperStep`s, add a `StepperCompleted` with two buttons — one to open the results, and one to reset:

```python
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
```

## 3. Add the results modal

After the `Stepper`, add a modal that renders only once `result` exists:

```python
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
```

## Key ideas

- **Conditional rendering.** `... if result else None` returns nothing until a calculation has run. This is done so that referencing `result['user_volume']` is safe.
- **`lib.m.Modal`** is controlled by the `show_results` boolean via `opened`/`onClose`.
- **`lib.pl`** is the namespace for the Plotly component library. 
- **`lib.pl.Plot`** is configured with one dataset where the x/y data comes from the `storms`/`volumes` lists returned by `calculate_runoff` and is rendered as a scatter plot with lines and red markers.

## Full `home()` so far

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
                onClick=lambda e: (
                    set_selected_feature(e.get("features", [{}])[0]),
                    set_active_step(1)
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

Complete all four inputs, then click the **View Results** button. This should open a modal containing the results: a the runoff volume, the
Curve Number, and a chart of runoff volume across design storms. 

Close the modal and then click the **Start Over** button. This should reset every input and return to Step 1.
