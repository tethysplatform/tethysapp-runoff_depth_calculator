---
sidebar_position: 2
title: "Step 2: The App class & page functions"
---

# Step 2: The App class & page functions

**Concept:** Every Tethys Component App defines 1) an `App` class that inherits from the `ComponentBase` subclass and contains the high-level configuration of your app, and 2) one or more functions decorated with `@App.page` that accept a `lib` argument and return a component tree representing the content of the page.

Open `tethysapp/runoff_depth_calculator/app.py`. You should see the following:

```python
from tethys_sdk.components import ComponentBase


class App(ComponentBase):
    """
    Tethys app class for Runoff Depth Calculator.
    """

    name = "Runoff Depth Calculator"
    description = ""
    package = "runoff_depth_calculator"  # WARNING: Do not change this value
    index = "home"
    icon = f"{package}/images/icon.png"
    root_url = "runoff-depth-calculator"
    color = "#718093"
    tags = ""
    enable_feedback = False
    feedback_emails = []
    exit_url = "/apps/"
    default_layout = "NavHeader"
    nav_links = "auto"


@App.page
def home(lib):
    return lib.tethys.Display(
        lib.tethys.Map()
    )
```

## Key ideas

- **`ComponentBase`** — the base class for component apps. The class attributes are
  metadata: `name`, `package` (must match the directory and `pyproject.toml`), `index`
  (the default page), `root_url`, theme `color`, and layout/navigation settings.
- **`@App.page`** — turns a function into a page/route. The function name (`home`) matches
  `index`, so it's the landing page.
- **`lib`** — the single argument every page receives. It's the component library: HTML
  elements, Tethys components, UI frameworks, maps, and charts are all accessed from it. Here
  `lib.tethys.Display` is the root component and container for the page that right now holds 
  a `lib.tethys.Map` component.

## What you should see

We haven't changed any code yet, so you should still see the single home page of your app, with a title banner and a map filling the remaining space underneath.