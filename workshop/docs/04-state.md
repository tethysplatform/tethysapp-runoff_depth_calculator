---
sidebar_position: 4
title: "Step 4: State"
---

# Step 4: State

**Concept:** Component apps are reactive. `lib.hooks.use_state` gives a page a value and a
setter; calling the setter re-runs the page function and re-renders the UI.

Add state at the top of `home` to track the feature the user selects on the map:

```python
@App.page
def home(lib):
    selected_feature, set_selected_feature = lib.hooks.use_state({})
    area_sqkm = selected_feature.get("area_sqkm", 0)
    area_acres = area_sqkm * 247.105

    # ... return lib.tethys.Display(...) as before
```

## Key ideas

- **`use_state(initial)`** returns `(value, setter)`. `selected_feature` starts as `{}`.
- **Re-render on set.** When you later call `set_selected_feature(...)`, the whole `home`
  function runs again with the new value — there is no manual DOM updating.
- **Derived values** like `area_acres` are just computed from state on each render
  (`area_sqkm * 247.105` converts km² to acres).

You'll wire the setter to a map click in the next step. State you'll add as the app grows:

```python
precip, set_precip = lib.hooks.use_state(0)
soil_group, set_soil_group = lib.hooks.use_state(None)
land_use, set_land_use = lib.hooks.use_state(None)
active_step, set_active_step = lib.hooks.use_state(0)
result, set_result = lib.hooks.use_state(None)
show_results, set_show_results = lib.hooks.use_state(False)
```

## What you should see

No visible change yet — but the page now holds state it can react to. Next we make the map
update that state and drive a step-by-step workflow.
