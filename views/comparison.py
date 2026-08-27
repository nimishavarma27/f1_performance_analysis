"""
Comparison View
===============

Renders the "Comparative Analysis" tab: driver comparison chart, pace,
tyre stints, strategy timeline, and pit stops.
"""

import streamlit as st

from processing.pace_analysis import analyse as analyse_pace
from processing.pit_stop_analysis import analyse as analyse_pit_stops
from processing.tyre_stint_analysis import analyse as analyse_stints
from visualization.comparison_charts import create_driver_comparison_chart
from visualization.pace_table import display as display_pace
from visualization.pit_stop_table import display as display_pit_stops
from visualization.strategy_timeline import create_chart as create_strategy_chart
from visualization.tyre_stint_table import display as display_stints


def render_comparison(driver_data: dict) -> None:
    """Render the Comparison tab."""

    st.header("Comparative Analysis")

    if len(driver_data) > 1:
        st.subheader("Driver Comparison")
        comparison_chart = create_driver_comparison_chart(driver_data)
        st.plotly_chart(comparison_chart, use_container_width=True)
    else:
        st.info("Select two or more drivers in the sidebar to enable the comparison chart.")

    st.divider()

    st.subheader("Pace Analysis")
    pace = analyse_pace(driver_data)
    display_pace(pace)

    st.divider()

    stints = analyse_stints(driver_data)

    st.subheader("Tyre Stint Analysis")
    display_stints(stints)

    st.subheader("Race Strategy Timeline")
    strategy_chart = create_strategy_chart(stints)
    st.plotly_chart(strategy_chart, use_container_width=True)

    st.divider()

    st.subheader("Pit Stop Analysis")
    pit_stops = analyse_pit_stops(driver_data)
    display_pit_stops(pit_stops)
