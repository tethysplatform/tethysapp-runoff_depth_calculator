---
sidebar_position: 2
title: "Step 2: The App class & page functions"
---

# Step 2: The App class & page functions

**Concept:** Every Tethys app defines an `App` class. For component apps it subclasses
`ComponentBase`, and pages are plain Python functions decorated with `@App.page`.

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
  elements, Tethys components, UI frameworks, maps, and charts all hang off of it. Here
  `lib.tethys.Display` wraps the page and `lib.m.Title` is a Mantine title.

## What you should see

Everything from here is adding components inside this `home` function.
