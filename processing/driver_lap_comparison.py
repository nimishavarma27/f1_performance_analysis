"""
Driver Lap Comparison
=====================

Compare the fastest laps of two selected drivers.
"""

import pandas as pd


def compare(driver_data, driver1, driver2):
    """
    Compare the fastest laps of two drivers.

    Parameters
    ----------
    driver_data : dict
    driver1 : str
    driver2 : str

    Returns
    -------
    dict
    """

    if driver1 not in driver_data:
        return None

    if driver2 not in driver_data:
        return None

    lap1 = driver_data[driver1]["fastest"]
    lap2 = driver_data[driver2]["fastest"]

    comparison = {

        "Driver 1": driver1,
        "Driver 2": driver2,

        "Lap Time 1": lap1["LapTime"],
        "Lap Time 2": lap2["LapTime"],

        "Sector 1 1": lap1["Sector1Time"],
        "Sector 1 2": lap2["Sector1Time"],

        "Sector 2 1": lap1["Sector2Time"],
        "Sector 2 2": lap2["Sector2Time"],

        "Sector 3 1": lap1["Sector3Time"],
        "Sector 3 2": lap2["Sector3Time"],

        "Compound 1": lap1["Compound"],
        "Compound 2": lap2["Compound"],

        "Top Speed 1": lap1["SpeedST"],
        "Top Speed 2": lap2["SpeedST"]

    }

    return comparison