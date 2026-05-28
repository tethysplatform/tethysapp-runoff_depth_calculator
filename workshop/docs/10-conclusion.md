---
sidebar_position: 10
title: "Step 10: Conclusion"
---

# Step 10: Conclusion

Starting from a plain Python function, you built a complete Tethys Component App around it. Along the way you used:

- **A given `compute.py` function** as the premise — designing the UI around its inputs and outputs, with the domain logic kept separate and testable.
- **The `lib` namespace** and the props-as-kwargs / children-as-call component syntax.
- **`lib.tethys.Map`** and **`lib.m.Stepper`** components for collecting inputs for the compute function.
- **`lib.hooks.use_state`** for reactive state and the re-render model
- **Event handlers** (`onClick`, `onChange`) to drive a guided workflow and call the
  computation.
- **`lib.m.Modal`** and **`lib.pl.Plot`** to present results of the compute function.

## Where to go next

- [Components SDK reference](https://docs.tethysplatform.org/en/latest/tethys_sdk/components.html)
  — the full list of component namespaces (`lib.m`, `lib.ol`, `lib.pl`, `lib.html`, and more).
- [Component App Basics tutorial](https://docs.tethysplatform.org/en/latest/tutorials/component_app_basics.html)
  — the official tutorial this workshop is modeled on.
- Try wrapping a function of your own: define its input/output contract, then build the UI
  around it the same way.

Thanks for building along!
