---
sidebar_position: 0
slug: /
title: Introduction
---

# Runoff Depth Calculator Workshop

Welcome! In this workshop you will build a **Tethys Component App** from scratch — a web
app whose entire interface is written in Python using Tethys's component framework (no
Django templates, no JavaScript).

## What you'll build

The **Runoff Depth Calculator** estimates stormwater runoff for an urban area using the
NRCS Curve Number method. The finished app lets a user:

1. Click an urban-area polygon on an interactive map.
2. Choose a design storm depth with a slider.
3. Pick a hydrologic soil group and a land use.
4. View the estimated runoff volume and a chart of runoff across design storms.

You'll add each piece one concept at a time, so by the end you understand *why* the app is
structured the way it is — not just *what* to type.

## What you'll learn

- The Component App `App` class and `@App.page` functions
- The `lib` namespace and component syntax (props-as-kwargs, children-as-call)
- Reactive state with `lib.hooks.use_state`
- Event handlers and the Mantine `Stepper`
- Separating pure Python logic from the UI
- Showing results with a modal and a Plotly chart

## Prerequisites

- A working Tethys Platform install. If you don't have one, complete the
  [Tethys Quick Start](https://docs.tethysplatform.org/en/latest/getting_started.html)
  first.
- Basic Python familiarity. No React or JavaScript experience required.

When you're ready, start with **[Step 1: Set up & scaffold](./01-setup.md)**.
