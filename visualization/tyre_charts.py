import plotly.express as px

from utils.ui import get_plotly_layout


def create_tyre_chart(tyre_df, driver, color):
    """
    Create a scatter plot to analyze tyre performance.

    Parameters
    ----------
    tyre_df : pandas.DataFrame
        DataFrame returned by get_tyre_dataframe().

    driver : str
        Driver abbreviation.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = px.scatter(
        tyre_df,
        x="TyreLife",
        y="LapTimeSeconds",
        color="Compound",
        symbol="Stint",
        hover_data=[
            "LapNumber",
            "FreshTyre"
        ],
        title=f"{driver} - Tyre Performance Analysis",
        labels={
            "TyreLife": "Tyre Life (Laps)",
            "LapTimeSeconds": "Lap Time (seconds)",
            "Compound": "Tyre Compound",
            "Stint": "Stint"
        }
    )

    fig.update_layout(
        **get_plotly_layout(),
        xaxis_title="Tyre Life (Laps)",
        yaxis_title="Lap Time (seconds)",
        legend_title="Compound"
    )

    return fig
