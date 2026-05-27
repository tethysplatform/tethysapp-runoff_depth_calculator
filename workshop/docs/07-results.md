---
sidebar_position: 7
title: "Step 7: Displaying results"
---

# Step 7: Displaying results

**Concept:** Conditionally render components from state. We add a `StepperCompleted` section
with a button that opens a `Modal` containing the result text and a Plotly chart.

## Add the completed step

As the last child of the `Stepper`, add a completed panel:

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

## Add the results modal

After the `Stepper` (still inside the second `GridCol`), add a modal that only renders once
`result` exists:

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

- **Conditional rendering.** `... if result else None` returns `None` when there's no result,
  so nothing renders until the calculation runs.
- **`lib.m.Modal`** is controlled by the `show_results` boolean state via `opened`/`onClose`.
- **`lib.pl.Plot`** is Plotly: `data` is a list of trace `Props`, `layout` configures titles
  and axes — driven by the `storms`/`volumes` returned by `calculate_runoff`.

## What you should see

Complete all four inputs, click **View Results** → a modal opens showing the runoff volume,
the Curve Number, and a line+marker chart of runoff volume vs. design storm depth.
