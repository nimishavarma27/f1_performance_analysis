"""
Pace Analysis
=============

Analyse race pace and lap consistency.
"""

import pandas as pd


def analyse(driver_data):
    """
    Analyse lap pace.

    Parameters
    ----------
    driver_data : dict

    Returns
    -------
    pandas.DataFrame
    """

    rows = []

    for driver, data in driver_data.items():

        laps = data["laps"].copy()

        laps = laps.dropna(subset=["LapTime"])

        if laps.empty:
            continue

        lap_seconds = laps["LapTime"].dt.total_seconds()

        rows.append({

            "Driver": driver,

            "Fastest Lap": round(lap_seconds.min(), 3),

            "Average Lap": round(lap_seconds.mean(), 3),

            "Median Lap": round(lap_seconds.median(), 3),

            "Consistency (Std Dev)": round(lap_seconds.std(), 3),

            "Completed Laps": len(lap_seconds)

        })

    if not rows:
        return pd.DataFrame(columns=[
            "Driver", "Fastest Lap", "Average Lap",
            "Median Lap", "Consistency (Std Dev)", "Completed Laps"
        ])

    dataframe = pd.DataFrame(rows)

    dataframe.sort_values(

        "Average Lap",

        inplace=True

    )

    dataframe.reset_index(

        drop=True,

        inplace=True

    )

    return dataframe