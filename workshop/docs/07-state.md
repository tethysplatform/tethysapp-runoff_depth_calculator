---
sidebar_position: 7
title: "Step 7: State & computing the result"
---

# Step 7: State & computing the result

**Concept:** Now we make the app reactive. `lib.hooks.use_state` gives the page values that
persist across renders, plus setters that trigger a re-render. We'll store the four inputs,
track the active step, hold the result, then call `calculate_runoff` once the user has
provided everything.

## 1. Declare state

Add these at the very top of `home`, before the `return`:

```python
@App.page
def home(lib):
    selected_feature, set_selected_feature = lib.hooks.use_state({})
    area_sqkm = selected_feature.get("area_sqkm", 0)
    area_acres = area_sqkm * 247.105
    precip, set_precip = lib.hooks.use_state(0)
    soil_group, set_soil_group = lib.hooks.use_state(None)
    land_use, set_land_use = lib.hooks.use_state(None)
    active_step, set_active_step = lib.hooks.use_state(0)
    result, set_result = lib.hooks.use_state(None)

    return lib.tethys.Display(
        # ...grid from before...
    )
```

Each `use_state(initial)` returns `(value, setter)`. `area_acres` is **derived** from the
selected feature on every render (`area_sqkm * 247.105` converts km² to acres) — it's not
its own state.

## 2. Make the map update state

Add an `onClick` to the map's vector layer that stores the clicked feature and advances to
the next step:

```python
lib.ol.layer.Vector(
    onClick=lambda e: (
        set_selected_feature(e.get("features", [{}])[0]),
        set_active_step(1)
    ),
    style=lib.ol.style.Styler(
        # ...unchanged...
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

Give each input a `value` (so it reflects state) and an `onChange` that updates its own
state and advances the stepper. On the **land use** select — the last input — we also run
the calculation:

```python
# Step 2 — precipitation
lib.m.Slider(
    min=0, max=10, step=0.1, value=precip,
    marks=[lib.Props(value=i, label=f'{i}in.') for i in range(0, 11)],
    onChange=lambda val: (set_precip(val), set_active_step(2)),
),

# Step 3 — soil group
lib.m.Select(
    key="soil_group",
    data=["Group A", "Group B", "Group C", "Group D"],
    value=soil_group, placeholder="Select soil group",
    onChange=lambda val, _: (set_soil_group(val), set_active_step(3)),
),

# Step 4 — land use (also computes the result)
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

- **`use_state` drives re-renders.** A setter doesn't mutate the local variable — it
  schedules `home` to run again with the new value, and the UI re-renders from the result.
  There's no manual DOM updating.
- **One integer runs the workflow.** `active_step` lives in state; every input advances it,
  and the `Stepper` reads it.
- **Pass the event value, not the state you just set.** In the land-use handler we call
  `calculate_runoff(..., val)`, **not** `..., land_use`. `set_land_use(val)` only takes
  effect on the *next* render, so `land_use` still holds its previous value (`None` the first
  time) inside this handler. Using `val` ensures the calculation uses the land use the user
  just chose.

## What you should see

Click a polygon → the stepper advances and the slider/dropdowns now remember their values.
After choosing a land use, `result` holds the computed dict — but we aren't displaying it
yet. That's next.
