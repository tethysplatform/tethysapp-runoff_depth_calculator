---
sidebar_position: 3
title: "Step 3: Adding a Map"
---

# Step 3: Adding a Map

**Concept:** Components nest. You pass **props as keyword arguments** and **children by
calling** the component. We'll add a Tethys `Map` with an OpenLayers vector layer of urban
areas.

Replace the body of `home` so it returns a map inside a grid:

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
            )
        )
    )
```

## Key ideas

- **Props vs children.** `lib.m.GridCol(span=12, style=...)` sets props with kwargs. Calling
  the result `(...)` passes children. So `GridCol(...)(Map(...))` means "a GridCol with a Map
  child."
- **`lib.ol`** is the OpenLayers namespace: `layer.Vector`, `source.Vector`, and the
  `style.*` helpers. The source loads a remote GeoJSON of urban areas.
- **`lib.Props`** builds a plain options object (here passed to the vector source).
- **`lib.Style`** sets inline CSS (the column is 70% of viewport height).

## What you should see

Reload the app — a full-width map renders with red urban-area polygons outlined in black.
They're not clickable yet; that's next.
