"""
Telemetry Analysis
==================

This module prepares telemetry data returned by
telemetry_engine.py for visualization.

It performs:

- Channel validation
- Data cleaning
- Statistics calculation
"""

import pandas as pd


# ==========================================================
# Available Metrics
# ==========================================================

SUPPORTED_METRICS = [
    "Speed",
    "Throttle",
    "Brake",
    "RPM",
    "nGear",
    "DRS"
]


# ==========================================================
# Prepare Telemetry
# ==========================================================

def prepare(
    telemetry_dictionary,
    metric
):
    """
    Prepare telemetry for plotting.

    Parameters
    ----------
    telemetry_dictionary : dict

    metric : str

    Returns
    -------
    dict
    """

    if metric not in SUPPORTED_METRICS:

        raise ValueError(
            f"{metric} is not supported."
        )

    prepared = {}

    for driver, telemetry in telemetry_dictionary.items():

        if metric not in telemetry.columns:

            continue

        dataframe = telemetry[
            [
                "Distance",
                metric
            ]
        ].copy()

        dataframe.dropna(
            inplace=True
        )

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        prepared[driver] = dataframe

    return prepared


# ==========================================================
# Driver Statistics
# ==========================================================

def calculate_statistics(
    telemetry_dictionary,
    metric
):
    """
    Compute telemetry statistics.

    Returns
    -------
    pandas.DataFrame
    """

    rows = []

    for driver, telemetry in telemetry_dictionary.items():

        if metric not in telemetry.columns:

            continue

        series = telemetry[
            metric
        ].dropna()

        if series.empty:

            continue

        rows.append({

            "Driver": driver,

            "Maximum": round(
                float(series.max()),
                2
            ),

            "Average": round(
                float(series.mean()),
                2
            ),

            "Minimum": round(
                float(series.min()),
                2
            )

        })

    return pd.DataFrame(rows)


# ==========================================================
# Available Metrics
# ==========================================================

def available_metrics(
    telemetry_dictionary
):
    """
    Return metrics that exist
    for every selected driver.
    """

    if len(
        telemetry_dictionary
    ) == 0:

        return []

    metrics = []

    first_driver = next(
        iter(
            telemetry_dictionary.values()
        )
    )

    for metric in SUPPORTED_METRICS:

        if metric in first_driver.columns:

            metrics.append(metric)

    return metrics