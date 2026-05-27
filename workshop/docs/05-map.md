---
sidebar_position: 5
title: "Step 5: Add the map"
---

# Step 5: Add the map

**Concept:** Tethys provides a map component, and OpenLayers components for layers and data
sources. We'll show urban-area polygons loaded from a remote GeoJSON file.

Replace the first column's `lib.m.Text("Map goes here")` placeholder with a map:

```python
lib.m.GridCol(span=12, style=lib.Style(height="70vh"))(
    lib.tethys.Map(
        lib.ol.layer.Vector(
            style=lib.ol.style.Styler(
                default=lib.ol.style.Style(
                    stroke=lib.ol.style.Stroke(color="#000000", width=1),
                    fill=lib.ol.style.Fill(color="#ff0000"),
                ),
            )
        )(
            lib.ol.source.Vector(
                options=lib.Props(
                    url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                    format="GeoJSON",
                )
            )
        )
    )
)
```

## Key ideas

- **`lib.tethys.Map`** renders an interactive map and takes layers as children.
- **`lib.ol`** is the OpenLayers namespace. A `layer.Vector` (styled by a `style.Styler`)
  wraps a `source.Vector` that loads the GeoJSON from a URL.
- **`lib.ol.style.Styler`** with a `default` style draws every polygon the same way here —
  red fill, black outline. (In Step 9 we'll make it highlight the selected polygon.)
- **`lib.Props`** builds the options object passed to the source.

## Full `home()` so far

```python
@App.page
def home(lib):
    return lib.tethys.Display(
        lib.m.Grid(
            lib.m.GridCol(span=12, style=lib.Style(height="70vh"))(
                lib.tethys.Map(
                    lib.ol.layer.Vector(
                        style=lib.ol.style.Styler(
                            default=lib.ol.style.Style(
                                stroke=lib.ol.style.Stroke(color="#000000", width=1),
                                fill=lib.ol.style.Fill(color="#ff0000"),
                            ),
                        )
                    )(
                        lib.ol.source.Vector(
                            options=lib.Props(
                                url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                                format="GeoJSON",
                            )
                        )
                    )
                )
            ),
            lib.m.GridCol(span=12)(
                lib.m.Text("Steps go here")
            ),
        )
    )
```

## What you should see

Reload the app — a full-width map with red urban-area polygons. They aren't clickable yet;
we'll wire interaction once state is in place.
