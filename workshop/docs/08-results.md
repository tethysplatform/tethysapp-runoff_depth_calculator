---
sidebar_position: 8
title: "Step 8: Displaying the results"
---

# Step 8: Displaying the results

**Concept:** With `result` in state, we add a completion panel and a modal that shows the
numbers and a chart. We render the modal **conditionally** — only when a result exists.

## 1. Add modal-visibility state

The modal is opened/closed by its own boolean. Add it with the other `use_state` calls at
the top of `home`:

```python
show_results, set_show_results = lib.hooks.use_state(False)
```

## 2. Add a completed panel to the Stepper

After the four `StepperStep`s, add a `StepperCompleted` with two buttons — one to open the
results, one to reset:

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

After the `Stepper` (still inside the second `GridCol`), add a modal that renders only once
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

- **Conditional rendering.** `... if result else None` returns nothing until a calculation
  has run — so referencing `result['user_volume']` is safe.
- **`lib.m.Modal`** is controlled by the `show_results` boolean via `opened`/`onClose`.
- **`lib.pl.Plot`** is Plotly. `data` is a list of trace `Props`; `layout` sets titles and
  axes. The `storms`/`volumes` lists returned by `calculate_runoff` feed the chart directly —
  this is exactly why the function returns them.

## What you should see

Complete all four inputs, then **View Results** → a modal opens with the runoff volume, the
Curve Number, and a line+marker chart of runoff volume across design storms. **Start Over**
resets every input and returns to Step 1.
