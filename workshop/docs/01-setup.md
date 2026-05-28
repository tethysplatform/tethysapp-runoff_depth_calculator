---
sidebar_position: 1
title: "Step 1: Set up & scaffold"
---

# Step 1: Set up & scaffold

**Concept:** A Component App is a normal Tethys app project. We start by scaffolding one and
installing it into a Tethys portal.

## Active your Tethys Python Virtual Environment

If you have not already installed Tethys Platform, follow the [Quick Start](https://docs.tethysplatform.org/en/stable/index.html#quick-start) documentation and then return here.

Now, [Activate your Virtual Environment](https://docs.tethysplatform.org/en/stable/supplementary/virtual_environment.html#activate-environment).

## Scaffold the app

From the command line, navigate to a directory where you'd like to keep your code, then scaffold a new app using the **component** template:

```bash
cd /path/to/target/directory
tethys scaffold runoff_depth_calculator -t component
```

The `-t component` flag selects the ReactPy-based component template (as opposed to
`default` Django-template apps or the `react` template). Accept the prompts (or pass
`-d` to accept defaults).

## Install the app

Install the app into your Tethys portal in **development mode**.

```bash
cd tethysapp-runoff_depth_calculator
tethys install -d
```

`tethys install -d` does an editable install of the app, which ensures that your changes to the underlying code will be auto-detected and trigger a restart of the server.

## Run database migrations

If this is your first time installing a Tethys Component app, the Tethys database will also need to be updated.

```bash
tethys db migrate
```

## Run the app

Start the development server:

```bash
tethys start
```

## Key ideas

- **`tethys scaffold ... -t component`** creates a component-app project from a template.
- **`tethys quickstart`** is a one-shot first-time setup: portal config, database, migrations,
  superuser, and dev server.
- **`tethys install -d`** installs the app in development mode — an editable install plus
  dependency installation and a database sync into the portal (so it must run after the
  portal is initialized).

## What you should see

Open [http://127.0.0.1:8000/apps/](http://127.0.0.1:8000/apps/) and log in with `admin:pass`. 
Your scaffolded app should appear as a card item in the app library. Click on it and your app
should load, showing a header banner with a full screen map below. You will explore and modify
the code behind the app in the remaining steps.
