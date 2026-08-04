"""
Track Map Processing
====================

Prepares circuit position data from telemetry.
"""

import pandas as pd


def prepare(telemetry_dictionary, driver):
    """
    Prepare track map data.

    Parameters
    ----------
    telemetry_dictionary : dict

    driver : str

    Returns
    -------
    pandas.DataFrame
    """

    if driver not in telemetry_dictionary:
        return None

    telemetry = telemetry_dictionary[driver]["merged"]

    required = [
        "X",
        "Y",
        "Speed",
        "Throttle",
        "Brake",
        "nGear",
        "Distance"
    ]

    if "X" not in telemetry.columns or "Y" not in telemetry.columns:
        return None

    available = [
        column
        for column in required
        if column in telemetry.columns
    ]

    if len(available) < 2:
        return None

    dataframe = telemetry[available].copy()

    dataframe.dropna(inplace=True)

    dataframe.reset_index(
        drop=True,
        inplace=True
    )

    return dataframe