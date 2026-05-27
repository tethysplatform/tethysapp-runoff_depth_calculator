---
sidebar_position: 6
title: "Step 6: The computation layer"
---

# Step 6: The computation layer

**Concept:** Keep domain logic out of the UI. The runoff math is pure Python in its own
module, so it's easy to read and test independently of the components.

Create `tethysapp/runoff_depth_calculator/compute.py`:

```python
def calculate_runoff(area_acres, precipitation_inches, soil_group, land_use):
    """
    Calculates runoff depth and volume using the NRCS Curve Number method.
    """
    # Simple composite CN lookup matrix
    cn_matrix = {
        'Group A': {'Residential': 46, 'Commercial': 89, 'Forest': 36},
        'Group B': {'Residential': 65, 'Commercial': 92, 'Forest': 60},
        'Group C': {'Residential': 77, 'Commercial': 94, 'Forest': 73},
        'Group D': {'Residential': 82, 'Commercial': 95, 'Forest': 79},
    }

    # Get Curve Number based on user inputs
    cn = cn_matrix.get(soil_group, {}).get(land_use, 75)

    # Calculate Potential Maximum Retention (S)
    S = (1000 / cn) - 10
    # Initial Abstraction (Ia) typically assumed as 0.2 * S
    Ia = 0.2 * S

    # Design storm depths to simulate for the Plotly chart (in inches)
    storms = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    runoff_volumes_cf = []

    for p in storms:
        if p > Ia:
            # NRCS Runoff Equation
            q_depth = ((p - Ia) ** 2) / (p - Ia + S)
        else:
            q_depth = 0.0

        # Convert depth (inches) + Area (acres) to Volume (Cubic Feet)
        # 1 acre-inch = 3630 cubic feet
        volume_cf = q_depth * area_acres * 3630
        runoff_volumes_cf.append(round(volume_cf, 1))

    # Calculate specific user selected storm runoff volume
    if precipitation_inches > Ia:
        user_q_depth = ((precipitation_inches - Ia) ** 2) / (precipitation_inches - Ia + S)
    else:
        user_q_depth = 0.0
    user_volume_cf = user_q_depth * area_acres * 3630

    return {
        'cn': cn,
        'user_volume': round(user_volume_cf, 1),
        'storms': storms,
        'volumes': runoff_volumes_cf
    }
```

## Call it from the UI

Import it at the top of `app.py`:

```python
from .compute import calculate_runoff
```

Then compute the result when the user picks a land use — extend the Step 4 `Select`
handler from the previous step:

```python
onChange=lambda val, _: (
    set_land_use(val),
    set_active_step(4),
    set_result(calculate_runoff(area_acres, precip, soil_group, land_use))
)
```

## Key ideas

- **Separation of concerns.** `compute.py` has no Tethys/ReactPy imports. It takes numbers
  and strings, returns a dict — trivially unit-testable.
- **The CN method.** Look up a Curve Number, derive retention `S` and abstraction `Ia`,
  then apply `Q = (P - Ia)² / (P - Ia + S)`. Returns the user's volume plus parallel
  `storms`/`volumes` lists for charting.

## What you should see

When you select a land use, `result` is populated in state. We render it next.
