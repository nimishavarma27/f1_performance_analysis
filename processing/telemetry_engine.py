"""
Telemetry Engine
================

Loads and prepares telemetry for selected drivers.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.logger import logger


def _build_single(driver: str, data: dict):
    """Build the car / position / merged telemetry for one driver."""

    try:
        fastest = data["fastest"]

        car = (
            fastest
            .get_car_data()
            .add_distance()
            .copy()
        )

        if "Distance" not in car.columns:
            logger.warning(f"{driver}: Distance missing after add_distance()")

        position = fastest.get_pos_data().copy()

        keep = [c for c in ("Date", "X", "Y", "Z", "Status") if c in position.columns]
        position = position[keep]

        merged = pd.merge_asof(
            car.sort_values("Date"),
            position.sort_values("Date"),
            on="Date",
            direction="nearest",
        )

        merged["Driver"] = driver
        merged["Team"] = data["team"]
        merged["Color"] = data["color"]

        return {"car": car, "position": position, "merged": merged}

    except Exception as e:
        logger.warning(f"[Telemetry] {driver}: {e}")
        return None


@st.cache_data(show_spinner=False)
def build_for_driver(session_key: tuple, driver: str, _data: dict):
    """Cached per-driver telemetry builder.

    ``session_key`` participates in the cache key so a new session invalidates
    old telemetry. ``_data`` is prefixed with an underscore so Streamlit skips
    hashing the (unhashable) FastF1 objects and instead relies on the
    ``session_key`` and ``driver`` tuple to identify the entry.
    """

    return _build_single(driver, _data)


def build(driver_data: dict, session_key: tuple = None) -> dict:
    """Build the telemetry dictionary for all provided drivers.

    When ``session_key`` is supplied each driver's entry is memoised via
    :func:`build_for_driver`, so switching between drivers in the same
    session no longer rebuilds them.
    """

    telemetry_dictionary: dict = {}

    for driver, data in driver_data.items():
        if session_key is not None:
            entry = build_for_driver(session_key, driver, data)
        else:
            entry = _build_single(driver, data)

        if entry is not None:
            telemetry_dictionary[driver] = entry

    return telemetry_dictionary


def available_channels(telemetry_dictionary: dict):
    """Return telemetry channels."""

    if not telemetry_dictionary:
        return []

    dataframe = next(iter(telemetry_dictionary.values()))["merged"]

    excluded = {"Date", "SessionTime", "Time", "Source", "Driver", "Team", "Color"}

    return sorted(c for c in dataframe.columns if c not in excluded)
