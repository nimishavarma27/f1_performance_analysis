"""
Pit Stop Analysis
=================

Analyse pit stops from FastF1 lap data.
"""

import pandas as pd


def analyse(driver_data):
    """
    Analyse pit stops for each driver.

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

        if laps.empty:
            continue

        laps = laps.sort_values("LapNumber")

        previous_stint = None

        for _, lap in laps.iterrows():

            current_stint = lap["Stint"]

            if previous_stint is None:

                previous_stint = current_stint
                continue

            if current_stint != previous_stint:

                rows.append({

                    "Driver": driver,

                    "Pit Lap": int(lap["LapNumber"]),

                    "New Compound": lap["Compound"],

                    "New Stint": int(current_stint)

                })

                previous_stint = current_stint

    dataframe = pd.DataFrame(rows)

    if dataframe.empty:

        return dataframe

    dataframe.sort_values(

        ["Driver", "Pit Lap"],

        inplace=True

    )

    dataframe.reset_index(

        drop=True,

        inplace=True

    )

    return dataframe