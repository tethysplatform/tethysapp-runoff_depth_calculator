---
sidebar_position: 10
title: "Step 10: Conclusion"
---

# Step 10: Conclusion

Starting from a plain Python function, you built a complete Tethys Component App around it.
Along the way you used:

- **`ComponentBase` + `@App.page`** to define the app and its page.
- **A given `compute.py` function** as the premise — designing the UI around its inputs and
  outputs, with the domain logic kept separate and testable.
- **The `lib` namespace** and the props-as-kwargs / children-as-call component syntax.
- **`lib.m.Grid` / `lib.tethys.Map` / `lib.m.Stepper`** to lay out the page incrementally.
- **`lib.hooks.use_state`** for reactive state and the re-render model — and the reminder to
  read fresh values from the event (`val`), not the state you just set.
- **Event handlers** (`onClick`, `onChange`) to drive a guided workflow and call the
  computation.
- **`lib.m.Modal`** and **`lib.pl.Plot`** to present results conditionally.

## Where to go next

- [Components SDK reference](https://docs.tethysplatform.org/en/latest/tethys_sdk/components.html)
  — the full list of component namespaces (`lib.m`, `lib.ol`, `lib.pl`, `lib.html`, and more).
- [Component App Basics tutorial](https://docs.tethysplatform.org/en/latest/tutorials/component_app_basics.html)
  — the official tutorial this workshop is modeled on.
- Try wrapping a function of your own: define its input/output contract, then build the UI
  around it the same way.

Thanks for building along!
