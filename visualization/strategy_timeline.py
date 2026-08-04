"""
Race Strategy Timeline
======================
"""

import plotly.graph_objects as go

from utils.ui import get_plotly_layout


COMPOUND_COLORS = {

    "SOFT": "#FF3333",

    "MEDIUM": "#FFD23F",

    "HARD": "#FFFFFF",

    "INTERMEDIATE": "#00C853",

    "WET": "#2979FF",

    "UNKNOWN": "#9E9E9E"

}


def create_chart(stints):

    """
    Create tyre strategy timeline.
    """

    fig = go.Figure()

    if stints is None or stints.empty:
        fig.update_layout(
            title="Race Strategy Timeline (No Data)",
            **get_plotly_layout()
        )
        return fig

    drivers = list(
        stints["Driver"].unique()
    )

    for idx, row in stints.iterrows():

        compound = str(
            row["Compound"]
        ).upper()

        color = COMPOUND_COLORS.get(

            compound,

            COMPOUND_COLORS["UNKNOWN"]

        )

        start_lap = row["Start Lap"]
        end_lap = row["End Lap"]

        fig.add_trace(

            go.Bar(

                x=[
                    row["Laps"]
                ],

                y=[
                    row["Driver"]
                ],

                base=start_lap,

                orientation="h",

                marker_color=color,

                text=compound,

                textposition="inside",

                hovertemplate=(

                    "<b>%{y}</b><br>"

                    f"Compound: {compound}<br>"

                    f"Lap {start_lap} → {end_lap}"

                    "<extra></extra>"

                ),

                showlegend=False

            )

        )

    fig.update_layout(

        title="Race Strategy Timeline",

        barmode="stack",

        xaxis_title="Lap",

        yaxis_title="Driver",

        **get_plotly_layout(),

        height=max(

            350,

            70 * len(drivers)

        )

    )

    return fig
