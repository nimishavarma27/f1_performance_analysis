"""
Track Map Chart
===============

Plotly visualization of the racing line.
"""

import plotly.graph_objects as go

from utils.ui import get_plotly_layout


def create_chart(
    dataframe,
    color
):
    """
    Create track map.

    Parameters
    ----------
    dataframe : pandas.DataFrame

    color : str

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=dataframe["X"],

            y=dataframe["Y"],

            mode="lines",

            line=dict(

                color=color,

                width=4

            ),

            hoverinfo="skip",

            name="Racing Line"

        )

    )

    layout = get_plotly_layout()
    layout["xaxis"].update(visible=False)
    layout["yaxis"].update(
        visible=False,
        scaleanchor="x",
        scaleratio=1,
    )

    fig.update_layout(
        **layout,
        title="Track Map",
    )

    return fig
