---
sidebar_position: 5
title: "Step 5: Add data to the map"
---

# Step 5: Add data to the map

**Concept:** Tethys provides a map component, and OpenLayers components for layers and data sources. We'll show urban-area polygons loaded from a remote GeoJSON file.

```python
lib.tethys.Map(
    style=lib.Style(height="70vh", marginBottom="1em")
)(
    lib.ol.layer.Vector(
        lib.ol.source.Vector(
            options=lib.Props(
                url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                format="GeoJSON",
            )
        )
    )
)
```

## Reading the component syntax

This is the core pattern you'll use everywhere, so it's worth slowing down:

- **Props are keyword arguments.** `lib.tethys.Map(style=...)` configures the component with specific styles
- **Children are standard positional arguments to the Component if there are no kwargs, or they are positional arguments to a subsequent, chained call of the Component if there the Component requires both Props and Children**
- **Children are from a chained call on the result.** Because `ol.tethys.Map` has a `style` configured, the child `lib.ol.layer.Vector` must be passed to a chained call. However, `lib.ol.layer.Vector` has children and no props, and so the `lib.ol.source.Vector` component can be passed directly to `lib.ol.layer.Vector` rather than as a nested call.

## Key ideas

- **`lib.tethys.Map`** renders an interactive map and takes layers as children.
- **`lib.ol`** is the namespace for the OpenLayers package. A `layer.Vector` contains a `source.Vector` that defines the underlying features/data that in this case comes from a GeoJSON URL.
- **`lib.Props`**, like `lib.Style` is a helper function that allows you to continue to write pythonic, kwarg-style syntax for the key-value pairs rather than dictionary syntax (e.g. `options=lib.Props(url="...", format="GeoJSON")` rather than `options={"url": "...", "format": "GeoJSON"}`). You may use whichever you prefer.

## Full `home()` so far

```python
@App.page
def home(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            style=lib.Style(height="70vh", marginBottom="1em")
        )(
            lib.ol.layer.Vector(
                lib.ol.source.Vector(
                    options=lib.Props(
                        url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                        format="GeoJSON",
                    )
                )
            )
        ),
        lib.m.Text("Steps go here")
    )
```

## What you should see

Reload the app and you should now see urban-area polygons rendering on the map.