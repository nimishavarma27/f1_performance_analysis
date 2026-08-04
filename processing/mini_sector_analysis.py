"""
Mini Sector Analysis
====================

Divides the lap into equal mini sectors and determines
which driver is fastest in each mini sector based on
average speed.
"""

import numpy as np
import pandas as pd


def analyse(
    telemetry_dictionary: dict,
    sectors: int = 25
):
    """
    Analyse mini sectors for all available drivers.

    Parameters
    ----------
    telemetry_dictionary : dict
        Telemetry dictionary produced by telemetry_engine.build()

    sectors : int
        Number of mini sectors.

    Returns
    -------
    pandas.DataFrame | None
    """

    if not telemetry_dictionary:
        return None

    valid_drivers = {}

    # ----------------------------------------------------
    # Validate telemetry
    # ----------------------------------------------------

    for driver, driver_data in telemetry_dictionary.items():

        telemetry = driver_data.get("merged")


        if telemetry is None:
            continue

        required = {"Distance", "Speed"}

        if not required.issubset(telemetry.columns):
            print(
                f"[MiniSector] {driver} missing columns:"
                f" {required - set(telemetry.columns)}"
            )
            continue

        valid_drivers[driver] = telemetry

    if not valid_drivers:
        return None

    # ----------------------------------------------------
    # Common lap distance
    # ----------------------------------------------------

    maximum_distance = min(

        telemetry["Distance"].max()

        for telemetry in valid_drivers.values()

    )

    boundaries = np.linspace(
        0,
        maximum_distance,
        sectors + 1
    )

    results = []

    # ----------------------------------------------------
    # Analyse sectors
    # ----------------------------------------------------

    for sector in range(sectors):

        start = boundaries[sector]
        end = boundaries[sector + 1]

        fastest_driver = None
        fastest_speed = -1

        for driver, telemetry in valid_drivers.items():

            section = telemetry[
                (telemetry["Distance"] >= start)
                &
                (telemetry["Distance"] < end)
            ]

            if section.empty:
                continue

            average_speed = section["Speed"].mean()

            if average_speed > fastest_speed:

                fastest_speed = average_speed
                fastest_driver = driver

        results.append({

            "Mini Sector": sector + 1,
            "Start (m)": round(start, 2),
            "End (m)": round(end, 2),
            "Fastest Driver": fastest_driver,
            "Average Speed (km/h)": (
                round(fastest_speed, 2)
                if fastest_speed >= 0
                else None
            )

        })

    return pd.DataFrame(results)