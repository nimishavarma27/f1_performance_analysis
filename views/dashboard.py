"""
Dashboard View
==============

Renders the dashboard overview section.

Contains:
- Weekend Information
- Dashboard Overview
- Fastest Lap Ranking
"""

import streamlit as st

from processing.weekend_summary import get_weekend_summary

from visualization.weekend_information import (
    render_weekend_information
)

from visualization.dashboard_overview import (
    display_dashboard_overview
)

from visualization.fastest_lap_table import (
    display_fastest_lap_table
)

from visualization.weather_dashboard import (
    render_weather_dashboard,
)

from processing.fastest_lap import (
    get_fastest_lap_ranking
)


def render_dashboard(
    year,
    grand_prix,
    event,
    session
):
    """
    Render dashboard overview.
    """

    st.divider()

    st.header("🏁 Weekend Overview")

    show_weekend = st.toggle(

        "Load Weekend Information",

        value=False,

        key="weekend_toggle"

    )

    if show_weekend:

        with st.spinner(
            "Loading weekend information..."
        ):

            summary = get_weekend_summary(

                year,

                grand_prix

            )

        render_weekend_information(

            summary

        )

    display_dashboard_overview(

        event,

        session

    )

    render_weather_dashboard(session)

    ranking = get_fastest_lap_ranking(

        session

    )

    display_fastest_lap_table(

        ranking

    )
