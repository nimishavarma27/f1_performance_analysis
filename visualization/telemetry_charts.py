"""
Telemetry Charts
================

Plotly charts for telemetry comparison.
"""

import plotly.graph_objects as go

from utils.ui import get_plotly_layout


Y_AXIS_LABELS = {

    "Speed": "Speed (km/h)",

    "Throttle": "Throttle (%)",

    "Brake": "Brake",

    "RPM": "RPM",

    "nGear": "Gear",

    "DRS": "DRS"

}


def create_chart(
    telemetry_dictionary,
    metric,
    driver_data
):
    """
    Create telemetry comparison chart.

    Parameters
    ----------
    telemetry_dictionary : dict

    metric : str

    driver_data : dict

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = go.Figure()

    for driver, driver_telemetry in telemetry_dictionary.items():

        telemetry = driver_telemetry.get("merged", driver_telemetry.get("car")) if isinstance(driver_telemetry, dict) else driver_telemetry

        if telemetry is None or metric not in telemetry.columns:
            continue

        fig.add_trace(

            go.Scatter(

                x=telemetry["Distance"],

                y=telemetry[metric],

                mode="lines",

                name=driver,

                line=dict(

                    color=driver_data[driver]["color"],

                    width=3

                ),

                hovertemplate=(

                    "<b>%{fullData.name}</b><br>"

                    "Distance: %{x:.0f} m<br>"

                    f"{metric}: %{{y}}"

                    "<extra></extra>"

                )

            )

        )

    fig.update_layout(

        title=f"{metric} Comparison",

        xaxis_title="Distance (m)",

        yaxis_title=Y_AXIS_LABELS.get(
            metric,
            metric
        ),


        **get_plotly_layout(),


    )

    return fig
