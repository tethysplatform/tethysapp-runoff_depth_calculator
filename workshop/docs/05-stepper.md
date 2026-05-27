---
sidebar_position: 5
title: "Step 5: Event handlers & the Stepper"
---

# Step 5: Event handlers & the Stepper

**Concept:** Components accept event handlers (`onClick`, `onChange`) as props. We'll make
the map clickable and add a Mantine `Stepper` that walks the user through inputs, advancing
`active_step` as each is provided.

## Make the map clickable

Give the vector layer an `onClick` that stores the clicked feature and advances to step 1.
We only attach it while on step 0 so the selection can't change mid-workflow:

```python
lib.ol.layer.Vector(
    **{
        "onClick": lambda e: (
            set_selected_feature(e.get("features", [{}])[0]),
            set_active_step(1)
        )
    } if active_step == 0 else {},
    style=lib.ol.style.Styler(
        # ...styler from Step 3...
    )
)(
    # ...source from Step 3...
)
```

## Add the Stepper

Below the map's `GridCol`, add a second `GridCol` containing a `Stepper`. Each step's input
updates its own state **and** advances `active_step`:

```python
lib.m.GridCol(span=12)(
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
                min=0, max=10, step=0.1, value=precip,
                marks=[lib.Props(value=i, label=f'{i}in.') for i in range(0, 11)],
                onChange=lambda val: (set_precip(val), set_active_step(2))
            )
        ),
        lib.m.StepperStep(
            label="Step 3",
            description="Assign soil group"
        )(
            lib.m.Select(
                key="soil_group",
                data=["Group A", "Group B", "Group C", "Group D"],
                value=soil_group, placeholder="Select soil group",
                onChange=lambda val, _: (set_soil_group(val), set_active_step(3))
            )
        ),
        lib.m.StepperStep(
            label="Step 4",
            description="Assign land use"
        )(
            lib.m.Select(
                key="land_use",
                data=["Residential", "Commercial", "Forest"],
                value=land_use, placeholder="Select land use",
                onChange=lambda val, _: (set_land_use(val), set_active_step(4))
            )
        ),
    )
)
```

## Key ideas

- **Handlers are props.** `onClick` / `onChange` take callables. The `lambda ...: (a, b)`
  tuple trick lets one handler call multiple setters.
- **Driving a workflow with state.** A single integer `active_step` (held in state) controls
  which Stepper step is active; every input advances it.
- **Conditional props.** Spreading `**({...} if active_step == 0 else {})` attaches `onClick`
  only on the first step.

## What you should see

Click a polygon → the Stepper advances to Step 2. Move the slider → Step 3. Choose a soil
group and land use → the stepper reaches the end. Next we compute a result.
