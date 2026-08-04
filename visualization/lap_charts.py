import plotly.express as px

from utils.ui import get_plotly_layout


def create_lap_time_chart(lap_df, driver, color):
    """
    Create a line chart showing lap times
    throughout the session.

    Parameters
    ----------
    lap_df : pandas.DataFrame
        DataFrame returned by get_lap_time_dataframe().

    driver : str
        Driver abbreviation.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    # Official F1 tyre colours
    tyre_colors = {
        "SOFT": "#E10600",
        "MEDIUM": "#FFD12E",
        "HARD": "#FFFFFF",
        "INTERMEDIATE": "#43B02A",
        "WET": "#0067AD"
    }

    fig = px.line(
        lap_df,
        x="LapNumber",
        y="LapTimeSeconds",
        color="Compound",
        markers=True,
        color_discrete_map=tyre_colors,
        title=f"{driver} - Lap Time Analysis",
        labels={
            "LapNumber": "Lap Number",
            "LapTimeSeconds": "Lap Time (seconds)",
            "Compound": "Tyre Compound"
        },
        hover_data={
            "TyreLife": True,
            "Stint": True,
            "Compound": True,
            "LapNumber": False,
            "LapTimeSeconds": ":.3f"
        }
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    fig.update_layout(
        **get_plotly_layout(),
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        legend_title="Tyre Compound",
    )

    return fig
