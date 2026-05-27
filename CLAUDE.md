# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A [Tethys Platform](https://docs.tethysplatform.org) web app that estimates stormwater
runoff for an urban area using the NRCS Curve Number method. The user picks an urban-area
polygon on a map, then steps through assigning precipitation, hydrologic soil group, and
land use; the app computes runoff depth/volume and plots runoff volumes across a range of
design storms.

The entire app is two source files: a single-page ReactPy UI (`app.py`) and a pure-Python
hydrology calculation (`compute.py`).

## Package name

The Tethys app **package name** is `runoff_depth_calculator`, matching the package
directory `tethysapp/runoff_depth_calculator/`. This identifier must stay consistent across:

- `pyproject.toml` → `name = "tethysapp-runoff_depth_calculator"`, package-data key `tethysapp.runoff_depth_calculator`
- `install.yml` → `name: runoff_depth_calculator`
- `app.py` → `package = "runoff_depth_calculator"` (marked `WARNING: Do not change this value`), `root_url = "runoff-depth-calculator"`

The `package` attribute in `app.py` must stay in sync with `pyproject.toml`/`install.yml`
or the app will fail to load.

## Commands

This app installs into a Tethys Platform environment (Tethys >= 4.0.0); it is not run
standalone.

### First-time setup

`tethys-platform` is pip-installable (the PyPI build omits the heavy conda-only geospatial
stack), so a plain venv works:

```bash
# 1. Create a venv and install Tethys + this app (editable)
python3.12 -m venv .venv          # Tethys targets 3.10; 3.12 is the safe modern choice
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/pip install tethys-platform
.venv/bin/pip install -e .

# 2. Initialize the portal (generates portal_config.yml, configures the database,
#    runs migrations, and prompts to create a portal superuser). This is the
#    standard, verified way to initialize a fresh install:
tethys quickstart
```

`tethys quickstart` also scaffolds and starts a `hello_world` demo app and launches the dev
server. By default it writes the portal config and SQLite database under `TETHYS_HOME`
(`~/.tethys` unless overridden by the `TETHYS_HOME` env var).

### Day-to-day

```bash
# Start the dev server (http://127.0.0.1:8000; default superuser created during setup)
tethys manage start

# Re-register apps with the portal database after code/metadata changes
tethys db sync

# List installed apps
tethys list

# Run tests (requires the configured DB user to be a superuser, e.g. tethys_super)
tethys manage test tethysapp/runoff_depth_calculator/tests
```

Test prerequisites and the exact test invocation are documented in
`tethysapp/runoff_depth_calculator/tests/tests.py`. Tests inherit from
`tethys_sdk.testing.TethysTestCase`.

## Architecture

**UI layer (`app.py`)** — Built on Tethys's ReactPy component framework, NOT Django
templates. `App` subclasses `ComponentBase`; the `@App.page`-decorated `home(lib)` function
returns the entire UI tree. Key conventions:

- `lib` is the component library namespace passed into each page: `lib.m.*` (Mantine
  components — `Stepper`, `Slider`, `Select`, `Modal`, etc.), `lib.tethys.*` (`Map`,
  `Display`), `lib.ol.*` (OpenLayers map layers/sources/styles), `lib.pl.Plot` (Plotly),
  `lib.hooks.use_state`, `lib.Props`, `lib.Style`.
- State is React-style hooks: `value, set_value = lib.hooks.use_state(initial)`. The whole
  page re-renders on state change. There is no separate controller/model layer.
- The flow is driven by a single `active_step` integer advancing a Mantine `Stepper`.
  Each step's `onChange`/`onClick` both updates its own state and calls `set_active_step`
  to advance. `calculate_runoff` is invoked at the final step (land-use selection), and
  results render in a `Modal` gated on `result` being non-None.
- The map loads urban-area polygons from a remote Natural Earth GeoJSON URL; clicking a
  feature stores `selected_feature` (notably `area_sqkm`) and is only interactive while
  `active_step == 0`.

**Computation layer (`compute.py`)** — `calculate_runoff(area_acres, precipitation_inches,
soil_group, land_use)` is a self-contained, dependency-free NRCS Curve Number
implementation. It looks up a composite Curve Number from a `(soil_group, land_use)` matrix
(default 75 on miss), computes potential maximum retention `S = 1000/CN - 10` and initial
abstraction `Ia = 0.2*S`, then applies the runoff equation `Q = (P-Ia)²/(P-Ia+S)` (0 when
`P <= Ia`). Returns `cn`, the user's `user_volume`, and parallel `storms`/`volumes` lists
for the chart. Unit conversion uses `area_acres` (the UI converts `area_sqkm * 247.105`)
and `1 acre-inch = 3630 cubic feet`.

Keep hydrology logic in `compute.py` as pure functions so it stays testable independently
of the ReactPy UI.

## Dependencies

Beyond Tethys Platform itself, the only declared dependency is `reactpy-django`
(`>=5.2.1, <6.0.0`), specified in both `pyproject.toml` and `install.yml`. Keep those two
files in sync when changing dependencies.
