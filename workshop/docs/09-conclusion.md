---
sidebar_position: 9
title: "Step 9: Conclusion"
---

# Step 9: Conclusion

You've built a complete Tethys Component App. Along the way you used:

- **`ComponentBase` + `@App.page`** to define the app and its page.
- **The `lib` namespace** and the props-as-kwargs / children-as-call component syntax.
- **`lib.hooks.use_state`** for reactive state and the re-render model.
- **Event handlers** (`onClick`, `onChange`) and the Mantine **`Stepper`** to drive a
  guided workflow.
- **A pure `compute.py` module** to keep domain logic independent and testable.
- **`lib.m.Modal`** and **`lib.pl.Plot`** to present results conditionally.

## Where to go next

- [Components SDK reference](https://docs.tethysplatform.org/en/latest/tethys_sdk/components.html)
  — the full list of component namespaces (`lib.m`, `lib.ol`, `lib.pl`, `lib.html`, and more).
- [Component App Basics tutorial](https://docs.tethysplatform.org/en/latest/tutorials/component_app_basics.html)
  — the official tutorial this workshop is modeled on.
- Try extending the app: add a second page, persist results, or swap the urban-areas layer
  for your own data.

Thanks for building along!
