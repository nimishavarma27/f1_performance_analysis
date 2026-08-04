import plotly.express as px

from utils.ui import get_plotly_layout


def create_sector_chart(sector_df, driver, color):
    """
    Create a bar chart showing sector times
    for the fastest lap of a driver.
    """

    fig = px.bar(
        sector_df,
        x="Sector",
        y="Time",
        text="Time",
        title=f"{driver} - Fastest Lap Sector Times",
        labels={
            "Sector": "Sector",
            "Time": "Time (seconds)"
        },
        color_discrete_sequence=[color]
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Time (seconds)",
        **get_plotly_layout()
    )

    return fig
