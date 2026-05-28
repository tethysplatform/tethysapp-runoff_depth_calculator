---
sidebar_position: 3
title: "Step 3: The runoff function"
---

# Step 3: The runoff function

**Recall the premise of this workshop:** you already have a useful Python function and you want to build an app around it. Here that function is a stormwater **runoff calculator**. We'll treat it as a given black box since the goal is the app, not the hydrology.

Create `tethysapp/runoff_depth_calculator/compute.py` with the following content:

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

## All you need to know about it

You don't need to understand the NRCS math to build the app — just the **inputs and outputs**:

**Inputs**

| Argument | Meaning |
| --- | --- |
| `area_acres` | Area of the selected region, in acres |
| `precipitation_inches` | A design storm depth, in inches |
| `soil_group` | One of `"Group A"`–`"Group D"` |
| `land_use` | One of `"Residential"`, `"Commercial"`, `"Forest"` |

**Outputs** — a dict:

| Key | Meaning |
| --- | --- |
| `cn` | The Curve Number used |
| `user_volume` | Runoff volume (cubic feet) for the chosen storm |
| `storms` | A list of design-storm depths (for plotting) |
| `volumes` | Runoff volume at each storm depth (for plotting) |

That's the contract. The rest of the workshop builds an interface that collects those four inputs from the user and displays the result.

## Import your "black-box" compute function to app.py to be called there

Add the following to the top of your `tethysapp/runoff_depth_calculator/app.py` script:

```python
from .compute import calculate_runoff
```

We will tie this function into the UI, wiring it up to user-driven actions/events later.

## Key ideas

- **Separation of concerns.** `compute.py` should contain no component nor application UI logic — it's plain Python that takes numbers and strings and returns a dict, so it's trivial to test on its own.
- **Design the app around the data contract.** Knowing the function's inputs and outputs is enough to design the UI: four inputs to gather, one result dict to display.

## What you should see

No visible change in the app yet — we've just added the function we're going to build
around. Next we'll lay out the page.
