"""
Telemetry View
==============

Renders the Telemetry tab: telemetry dashboard, track map, corner
analysis, mini-sector, speed-trap.

Telemetry is built lazily and cached per driver, so switching drivers
in the selectbox does not rebuild ones already computed.
"""

import streamlit as st

from processing.corner_analysis import analyse as analyse_corner
from processing.mini_sector_analysis import analyse as analyse_mini_sector
from processing.speed_trap_analysis import analyse as analyse_speed_trap
from processing.telemetry_engine import build as build_telemetry
from processing.track_map import prepare as prepare_track
from visualization.corner_analysis_cards import display as display_corner_analysis
from visualization.mini_sector_table import display as display_mini_sector
from visualization.speed_trap_table import display as display_speed_trap
from visualization.telemetry_dashboard import render as render_telemetry_dashboard
from visualization.track_map_chart import create_chart as create_track_map


def render_telemetry(
    driver_data: dict,
    session_key: tuple,
    telemetry_enabled: bool,
) -> None:
    """Render the Telemetry tab."""

    st.header("Telemetry and Track Analysis")

    if not telemetry_enabled:
        st.info(
            "Detailed telemetry is disabled. Enable 'Load detailed telemetry' "
            "in the sidebar to use the telemetry, track map, corner, "
            "mini-sector, and speed-trap views."
        )
        return

    with st.spinner("Building telemetry..."):
        telemetry_dictionary = build_telemetry(driver_data, session_key=session_key)

    if not telemetry_dictionary:
        st.warning("Telemetry could not be built for any of the selected drivers.")
        return

    driver_options = list(telemetry_dictionary.keys())

    st.subheader("Telemetry Traces")
    render_telemetry_dashboard(telemetry_dictionary, driver_data)

    st.divider()

    st.subheader("Track Map")
    map_driver = st.selectbox("Driver", driver_options, key="track_map_driver")
    track = prepare_track(telemetry_dictionary, map_driver)

    if track is not None:
        figure = create_track_map(track, driver_data[map_driver]["color"])
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.warning("Track position data unavailable.")

    st.divider()

    st.subheader("Corner Analysis")
    corner_driver = st.selectbox(
        "Driver for corner analysis", driver_options, key="corner_driver"
    )
    corner_results = analyse_corner(telemetry_dictionary, corner_driver)
    display_corner_analysis(corner_results)

    st.divider()

    st.subheader("Mini Sector Analysis")
    mini_sector = analyse_mini_sector(telemetry_dictionary, sectors=25)
    display_mini_sector(mini_sector)

    st.divider()

    st.subheader("Speed Trap Analysis")
    speed_trap = analyse_speed_trap(telemetry_dictionary)
    display_speed_trap(speed_trap)
