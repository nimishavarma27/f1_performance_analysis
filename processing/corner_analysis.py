"""
Corner Analysis
===============

Extract braking and acceleration events from telemetry.
"""

import pandas as pd


def analyse(telemetry_dictionary, driver):
    """Analyse a driver's telemetry."""

    if driver not in telemetry_dictionary:
        return None

    telemetry = telemetry_dictionary[driver]["merged"].copy()

    required = ["Distance", "Speed", "Throttle", "Brake", "nGear"]
    for column in required:
        if column not in telemetry.columns:
            return None

    telemetry = telemetry.dropna(subset=required)
    if telemetry.empty:
        return None

    # FastF1 exposes Brake as either bool or 0/1 numeric depending on the
    # season. Coerce and mask defensively so operator precedence can't bite
    # us (``a > 0 | a == True`` parses as ``a > (0 | a) == True``).
    brake = telemetry["Brake"]
    if brake.dtype == bool:
        brake_mask = brake
    else:
        brake_mask = brake.astype(float) > 0

    braking = telemetry[brake_mask]
    full_throttle = telemetry[telemetry["Throttle"] >= 99]

    maximum_speed = telemetry.loc[telemetry["Speed"].idxmax()]
    minimum_speed = telemetry.loc[telemetry["Speed"].idxmin()]

    return {
        "Telemetry": telemetry,
        "Braking": braking,
        "FullThrottle": full_throttle,
        "MaximumSpeed": {
            "Distance": float(maximum_speed["Distance"]),
            "Speed": float(maximum_speed["Speed"]),
        },
        "MinimumSpeed": {
            "Distance": float(minimum_speed["Distance"]),
            "Speed": float(minimum_speed["Speed"]),
        },
    }
