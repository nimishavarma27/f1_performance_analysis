"""
Delta Time Analysis
===================

Calculates lap delta between two drivers using
their fastest lap telemetry.
"""

import numpy as np
import pandas as pd


def calculate(
    telemetry_dictionary,
    reference_driver,
    comparison_driver,
    samples=1200
):
    """
    Calculate delta time between two drivers.

    Parameters
    ----------
    telemetry_dictionary : dict

    reference_driver : str

    comparison_driver : str

    samples : int

    Returns
    -------
    pandas.DataFrame
    """

    if reference_driver not in telemetry_dictionary:
        return None

    if comparison_driver not in telemetry_dictionary:
        return None

    ref_data = telemetry_dictionary[reference_driver]
    comp_data = telemetry_dictionary[comparison_driver]

    reference = ref_data.get("merged", ref_data.get("car")) if isinstance(ref_data, dict) else ref_data
    comparison = comp_data.get("merged", comp_data.get("car")) if isinstance(comp_data, dict) else comp_data

    if reference is None or comparison is None:
        return None

    required = [
        "Distance",
        "Time"
    ]

    for column in required:

        if column not in reference.columns:
            return None

        if column not in comparison.columns:
            return None

    reference = reference.sort_values(
        "Distance"
    )

    comparison = comparison.sort_values(
        "Distance"
    )

    maximum_distance = min(

        reference["Distance"].max(),

        comparison["Distance"].max()

    )

    distance = np.linspace(
        0,
        maximum_distance,
        samples
    )

    reference_time = np.interp(

        distance,

        reference["Distance"],

        reference["Time"].dt.total_seconds()

    )

    comparison_time = np.interp(

        distance,

        comparison["Distance"],

        comparison["Time"].dt.total_seconds()

    )

    delta = comparison_time - reference_time

    dataframe = pd.DataFrame({

        "Distance": distance,

        "ReferenceTime": reference_time,

        "ComparisonTime": comparison_time,

        "Delta": delta

    })

    return dataframe


def statistics(delta_dataframe):
    """
    Delta statistics.
    """

    if delta_dataframe is None:

        return None

    delta = delta_dataframe["Delta"]

    return {

        "Maximum Gain": round(
            abs(delta.min()),
            3
        ),

        "Maximum Loss": round(
            delta.max(),
            3
        ),

        "Final Delta": round(
            delta.iloc[-1],
            3
        )

    }