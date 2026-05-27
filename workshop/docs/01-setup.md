---
sidebar_position: 1
title: "Step 1: Set up & scaffold"
---

# Step 1: Set up & scaffold

**Concept:** A Component App is a normal Tethys app project. We start by scaffolding one and
installing it into a Tethys portal.

## Scaffold the app

From a directory where you keep your code, scaffold a new app using the **component**
template:

```bash
tethys scaffold runoff_depth_calculator -t component
```

The `-t component` flag selects the ReactPy-based component template (as opposed to
`default` Django-template apps or the `react` template). Accept the prompts (or pass
`-d` to accept defaults).

## Initialize the Tethys portal

If this is a fresh Tethys install, initialize the portal first:

```bash
tethys quickstart
```

`tethys quickstart` generates the portal config, configures the database, runs migrations,
creates a superuser, and starts the development server. Press `Ctrl+C` to stop that server
before continuing.

## Install the app

Install the app into your Tethys portal in **development mode**. Run this from inside the
app directory (where `install.yml` lives):

```bash
cd tethysapp-runoff_depth_calculator
tethys install -d
```

`tethys install -d` does an editable install of the app, installs its dependencies, and
syncs it into the portal database — which is why the portal must be initialized first.

## Run the app

Start the development server:

```bash
tethys manage start
```

## Key ideas

- **`tethys scaffold ... -t component`** creates a component-app project from a template.
- **`tethys quickstart`** is a one-shot first-time setup: portal config, database, migrations,
  superuser, and dev server.
- **`tethys install -d`** installs the app in development mode — an editable install plus
  dependency installation and a database sync into the portal (so it must run after the
  portal is initialized).

## What you should see

Open [http://127.0.0.1:8000/apps/](http://127.0.0.1:8000/apps/) and log in. Your scaffolded app appears in the app
library with a default home page. In the next step we'll look at what makes it a component
app.
