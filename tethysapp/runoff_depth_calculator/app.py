from tethys_sdk.components import ComponentBase
from .compute import calculate_runoff


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
    selected_feature, set_selected_feature = lib.hooks.use_state({})
    area_sqkm = selected_feature.get("area_sqkm", 0)
    area_acres = area_sqkm * 247.105
    precip, set_precip = lib.hooks.use_state(0)
    soil_group, set_soil_group = lib.hooks.use_state(None)
    land_use, set_land_use = lib.hooks.use_state(None)
    active_step, set_active_step = lib.hooks.use_state(0)
    result, set_result = lib.hooks.use_state(None)
    show_results, set_show_results = lib.hooks.use_state(False)

    return lib.tethys.Display(
        lib.m.Grid(
            lib.m.GridCol(span=12, style=lib.Style(height="70vh"))(
                lib.tethys.Map(
                    lib.ol.layer.Vector(
                        **{
                            "onClick": lambda e: (
                                set_selected_feature(e.get("features", [{}])[0]),
                                set_active_step(1)
                            )
                        } if active_step == 0 else {},
                        style=lib.ol.style.Styler(
                            method="unique_values",
                            fields=["area_sqkm"],
                            values=[
                                (
                                    selected_feature["area_sqkm"] if selected_feature else -9999,
                                    lib.ol.style.Style(
                                        stroke=lib.ol.style.Stroke(color="purple", width=1),
                                        fill=lib.ol.style.Fill(color="white"),
                                    ),
                                ),
                            ],
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
                lib.m.Stepper(
                    active=active_step,
                    onStepClick=set_active_step
                )(
                    lib.m.StepperStep(
                        label="Step 1", 
                        description="Select an urban area on the map"
                    )("Click on a map feature"),
                    lib.m.StepperStep(
                        label="Step 2", 
                        description=f"Assign precipitation"
                    )(
                        lib.m.Slider(
                            min=0,
                            max=10,
                            step=0.1,
                            value=precip,
                            marks=[lib.Props(value=i, label=f'{i}in.') for i in range(0, 11)],
                            onChange=lambda val: (
                                set_precip(val),
                                set_active_step(2)
                            )
                        )
                    ),
                    lib.m.StepperStep(
                        label="Step 3", 
                        description="Assign soil group"
                    )(
                        lib.m.Select(
                            key="soil_group",
                            data=[
                                "Group A",
                                "Group B",
                                "Group C",
                                "Group D"
                            ],
                            value=soil_group,
                            placeholder="Select soil group",
                            onChange=lambda val, _: (
                                set_soil_group(val),
                                set_active_step(3)
                            )
                        )
                    ),
                    lib.m.StepperStep(
                        label="Step 4", 
                        description="Assign land use"
                    )(
                        lib.m.Select(
                            key="land_use",
                            value=land_use,
                            data=[
                                "Residential",
                                "Commercial",
                                "Forest"
                            ],
                            placeholder="Select land use",
                            onChange=lambda val, _: (
                                set_land_use(val),
                                set_active_step(4),
                                set_result(calculate_runoff(area_acres, precip, soil_group, val))
                            )
                        )
                    ),
                    lib.m.StepperCompleted(
                        lib.m.Center(
                            lib.m.Button(onClick=lambda _: set_show_results(True))("View Results"),
                            lib.m.Button(
                                onClick=lambda _: (
                                    set_selected_feature({}), 
                                    set_precip(0),
                                    set_soil_group(None),
                                    set_land_use(None),
                                    set_active_step(0),
                                )
                            )("Start Over")
                        )
                    ),
                ),
                lib.m.Modal(
                    opened=show_results,
                    onClose=lambda *args: set_show_results(False),
                    title="Runoff Calculation Results",
                )(
                    lib.m.Text(f"Estimated runoff volume for selected storm: {result['user_volume']} cubic feet"),
                    lib.m.Text(f"Curve Number used in calculation: {result['cn']}"),
                    lib.pl.Plot(
                        style=lib.Style(width="100%", height="100%"),
                        data=[
                            lib.Props(
                                x=result["storms"],
                                y=result["volumes"],
                                type="scatter",
                                mode="lines+markers",
                                marker=lib.Props(color="red"),
                            ),
                        ],
                        layout=lib.Props(
                            autosize=True,
                            title=lib.Props(text="Design Storm Runoff Volumes"),
                            xaxis=lib.Props(
                                title=lib.Props(text="Design storm depth (in)"),
                            ),
                            yaxis=lib.Props(
                                title=lib.Props(text="Runoff Volume (cubic feet)"),
                            ),
                        ),
                    )
                ) if result else None
            )
        )
    )
