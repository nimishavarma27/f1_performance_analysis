"""
Corner Analysis
===============

Extract braking and acceleration events from telemetry.
"""

import pandas as pd


def analyse(telemetry_dictionary, driver):
    """
    Analyse driver's telemetry.

    Parameters
    ----------
    telemetry_dictionary : dict

    driver : str

    Returns
    -------
    dict
    """

    if driver not in telemetry_dictionary:
        return None

    telemetry = telemetry_dictionary[driver]["merged"].copy()

    required = [
        "Distance",
        "Speed",
        "Throttle",
        "Brake",
        "nGear"
    ]

    for column in required:

        if column not in telemetry.columns:
            return None

    telemetry = telemetry.dropna(
        subset=required
    )

    if telemetry.empty:
        return None

    braking = telemetry[
        (telemetry["Brake"] > 0) | (telemetry["Brake"] == True)
    ]

    full_throttle = telemetry[
        telemetry["Throttle"] >= 99
    ]

    maximum_speed = telemetry.loc[
        telemetry["Speed"].idxmax()
    ]

    minimum_speed = telemetry.loc[
        telemetry["Speed"].idxmin()
    ]

    return {

        "Telemetry": telemetry,

        "Braking": braking,

        "FullThrottle": full_throttle,

        "MaximumSpeed": {

            "Distance": float(maximum_speed["Distance"]),

            "Speed": float(maximum_speed["Speed"])

        },

        "MinimumSpeed": {

            "Distance": float(minimum_speed["Distance"]),

            "Speed": float(minimum_speed["Speed"])

        }

    }