import plotly.graph_objects as go

from utils.ui import get_plotly_layout


def create_driver_comparison_chart(driver_data):
    """
    Create a comparison chart for one or more drivers.

    Parameters
    ----------
    driver_data : dict
        Dictionary containing processed data for each driver.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = go.Figure()

    for driver, data in driver_data.items():

        lap_df = data["lap_df"]

        fig.add_trace(
            go.Scatter(
                x=lap_df["LapNumber"],
                y=lap_df["LapTimeSeconds"],
                mode="lines+markers",
                name=driver,

                line=dict(
                    color=data["color"],
                    width=3
                ),

                marker=dict(
                    color=data["color"],
                    size=6
                ),

                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Lap: %{x}<br>"
                    "Time: %{y:.3f} s"
                    "<extra></extra>"
                )
            )
        )

    fig.update_layout(
        title="Driver Lap Time Comparison",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        **get_plotly_layout(),
        legend_title="Drivers",
        height=600
    )

    return fig
