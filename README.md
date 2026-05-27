# Runoff Depth Calculator

A demonstration [Tethys Platform](https://docs.tethysplatform.org) application built for a
workshop on creating **Tethys Component Apps** — apps whose entire UI is defined in Python
using Tethys's [ReactPy](https://reactpy.dev/)-based component framework instead of Django
templates.

## Workshop tutorial

A step-by-step workshop that walks through building this app from scratch is published at
**<https://tethysplatform.github.io/tethysapp-runoff_depth_calculator/>**. The tutorial
source lives in [`workshop/`](workshop/).

## What it does

The app estimates stormwater runoff for an urban area using the NRCS Curve Number method:

1. **Select an area** — pick an urban-area polygon on an interactive map.
2. **Assign precipitation** — choose a design storm depth (inches) with a slider.
3. **Assign a soil group** — select a hydrologic soil group (A–D).
4. **Assign land use** — select a land use (Residential, Commercial, Forest).

It then computes the runoff depth and volume for the selected storm and plots runoff volumes
across a range of design storms. The whole experience is a single `Stepper`-driven page.

The code is intentionally small so it can be read top to bottom in a workshop:

- `tethysapp/runoff_depth_calculator/app.py` — the component UI (a single `@App.page`).
- `tethysapp/runoff_depth_calculator/compute.py` — the pure-Python NRCS Curve Number
  calculation, with no UI or framework dependencies.

## Installation

`tethys-platform` is pip-installable, so a standard virtual environment works (no conda
required):

```bash
# Create and activate a virtual environment (Python 3.10–3.12 recommended)
python3.12 -m venv .venv
source .venv/bin/activate

# Install Tethys Platform
pip install --upgrade pip setuptools wheel
pip install tethys-platform

# Initialize the Tethys portal: generates the portal config, configures the
# database, runs migrations, creates a superuser, and starts the dev server.
# (Press Ctrl+C to stop the dev server it launches before continuing.)
tethys quickstart

# Install this app in development mode. Run from the app directory (where
# install.yml lives). The portal/database above must be initialized first,
# because this also syncs the app into the database.
tethys install -d

# Start the development server
tethys start
```

The app is available at <http://127.0.0.1:8000/apps/runoff-depth-calculator/>.

## Development

```bash
# Start the development server (http://127.0.0.1:8000)
tethys start

# Re-register the app with the portal database after changing app metadata
tethys db sync

# List installed apps
tethys list

# Run the test suite
tethys manage test tethysapp/runoff_depth_calculator/tests
```

After editing `app.py` or `compute.py`, refresh the browser — the editable install picks up
code changes without reinstalling. Changes to app metadata in `app.py` (name, URL, settings)
require `tethys db sync`.
