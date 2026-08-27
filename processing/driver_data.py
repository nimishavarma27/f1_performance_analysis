"""
Driver Data Builder
===================

Builds the per-driver ``driver_data`` mapping (laps, fastest lap,
sector/lap/tyre dataframes) that the rest of the dashboard consumes.

Cached with ``@st.cache_resource`` because the values contain live
FastF1 objects (``Laps`` / ``Lap``) that are not safely picklable.
"""

from __future__ import annotations

import streamlit as st

from processing.lap_analysis import get_lap_time_dataframe
from processing.sector_analysis import get_sector_dataframe
from processing.tyre_analysis import get_tyre_dataframe
from utils.team_colors import get_team_color


@st.cache_resource(show_spinner=False)
def build_driver_data(
    session_key: tuple,
    drivers: tuple,
    _session,
) -> dict:
    """Build the ``driver_data`` mapping used across the dashboard.

    ``session_key`` and ``drivers`` are cache-key inputs; ``_session`` is
    prefixed to opt out of Streamlit's hashing.
    """

    driver_data: dict = {}

    for driver in drivers:
        try:
            laps = _session.laps.pick_drivers(driver)
            if laps.empty:
                continue

            laps = laps[laps["LapTime"].notna()].copy()
            if laps.empty:
                continue

            fastest = laps.pick_fastest()
            team = laps.iloc[0]["Team"]

            driver_data[driver] = {
                "team": team,
                "color": get_team_color(team),
                "laps": laps,
                "fastest": fastest,
                "sector_df": get_sector_dataframe(fastest),
                "lap_df": get_lap_time_dataframe(laps),
                "tyre_df": get_tyre_dataframe(laps),
            }
        except Exception as error:
            st.warning(f"Skipping {driver}: {error}")

    return driver_data
