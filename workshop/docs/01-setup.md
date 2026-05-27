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

## Install the app

Install the app into your active Tethys environment in editable mode so code changes are
picked up without reinstalling:

```bash
cd tethysapp-runoff_depth_calculator
pip install -e .
```

## Initialize and run the portal

If this is a fresh Tethys install, initialize the portal and start the dev server:

```bash
tethys quickstart
```

`tethys quickstart` generates the portal config, configures the database, runs migrations,
creates a superuser, and starts the development server.

For subsequent runs, just start the server:

```bash
tethys manage start
```

## What you should see

Open [http://127.0.0.1:8000/apps/](http://127.0.0.1:8000/apps/) and log in. Your scaffolded app appears in the app
library with a default home page. In the next step we'll look at what makes it a component
app.
