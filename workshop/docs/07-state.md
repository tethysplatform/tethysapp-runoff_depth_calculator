---
sidebar_position: 7
title: "Step 7: State & computing the result"
---

# Step 7: State & computing the result

**Concept:** Now we make the app reactive. `lib.hooks.use_state` gives the page values that persist across renders, plus setters that trigger a re-render. We'll store the four inputs, track the active step, hold the result, then call `calculate_runoff` once the user has provided everything.

## 1. Declare state

Add these at the very top of `home`, before the `return`:

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

    return lib.tethys.Display(
        # ...source unchanged...
    )
```

Each `use_state(initial)` returns `(value, setter)`. Note that `area_acres` is **derived** from the selected feature's `area_sqkm` attribute and thus does not need to be a state variable itself.

## 2. Make the map update state

Add an `onClick` to the map's vector layer that stores the clicked feature and advances to the next step:

```python
lib.ol.layer.Vector(
    onClick=lambda e: (
        set_selected_feature(e.get("features", [{}])[0]),
        set_active_step(1)
    )
)(
    # ...source unchanged...
)
```

## 3. Drive the Stepper from state

Bind the Stepper's `active` to `active_step` and let clicks on the step headers navigate:

```python
lib.m.Stepper(
    active=active_step,
    onStepClick=set_active_step
)(
    # ...steps...
)
```

## 4. Wire each input

Give each input a `value` (so it reflects state) and an `onChange` that updates its own state and advances the stepper. On the **land use** select — the last input — we also run the calculation:

For Step 2 — precipitation

```python
lib.m.Slider(
    min=0, 
    max=10, 
    step=0.1, 
    value=precip,
    marks=[lib.Props(value=i, label=f'{i}in.') for i in range(0, 11)],
    onChange=lambda val: (set_precip(val), set_active_step(2)),
),
```

For Step 3 - soil group

```python
lib.m.Select(
    key="soil_group",
    data=["Group A", "Group B", "Group C", "Group D"],
    value=soil_group, placeholder="Select soil group",
    onChange=lambda val, _: (set_soil_group(val), set_active_step(3)),
),
```

For Step 4 — land use (also computes the result)

```python
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
```

## Key ideas

- **`use_state` drives re-renders.** A setter doesn't mutate the local variable — it schedules `home` to run again with the new value, and the UI re-renders from the result.
- **One integer runs the workflow.** `active_step` lives in state; every input advances it, and the `Stepper` reads it.
- **Pass the event value, not the state you just set.** In the land-use handler we call `calculate_runoff(..., val)`, **not** `calculate_runoff(..., land_use)`. This highlights an essential principle of the state lifecycle, and a common pitfall. Calling a setter does not *immediately* update the associated state variable. The update only takes effect on the *next* render, which gets scheduled when the setter is called. So `land_use` will still hold its default value (`None`) inside this handler. Using `val` ensures the calculation uses the land use the user just chose.

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
        )
    )
```

## What you should see

Click a polygon → the stepper advances and the slider/dropdowns now remember their values.
After choosing a land use, `result` holds the computed dict — but we aren't displaying it
yet. That's next.
