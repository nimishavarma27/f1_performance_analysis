"""
Telemetry Engine
================

Loads and prepares telemetry for all selected drivers.

Compatible with FastF1 3.8.3
"""

from __future__ import annotations

import pandas as pd


def build(driver_data: dict) -> dict:
    """
    Build telemetry dictionary.
    """

    telemetry_dictionary = {}

    for driver, data in driver_data.items():

        try:

            fastest = data["fastest"]

            # ------------------------------------------
            # Car telemetry
            # ------------------------------------------

            car = (
                fastest
                .get_car_data()
                .add_distance()
                .copy()
            )

            if "Distance" not in car.columns:
              print(f"{driver}: Distance missing after add_distance()")

            # ------------------------------------------
            # Position telemetry
            # ------------------------------------------

            position = (
                fastest
                .get_pos_data()
                .copy()
            )

            # Keep only columns we actually need
            keep = []

            for column in ["Date", "X", "Y", "Z", "Status"]:

                if column in position.columns:

                    keep.append(column)

            position = position[keep]

            # ------------------------------------------
            # Merge
            # ------------------------------------------

            merged = pd.merge_asof(

                car.sort_values("Date"),

                position.sort_values("Date"),

                on="Date",

                direction="nearest"

            )

            # ------------------------------------------
            # Metadata
            # ------------------------------------------

            merged["Driver"] = driver
            merged["Team"] = data["team"]
            merged["Color"] = data["color"]

            telemetry_dictionary[driver] = {

                "car": car,

                "position": position,

                "merged": merged

            }

        except Exception as e:

            print(f"[Telemetry] {driver}: {e}")

    return telemetry_dictionary


def available_channels(
    telemetry_dictionary: dict
):
    """
    Return telemetry channels.
    """

    if not telemetry_dictionary:

        return []

    dataframe = next(

        iter(

            telemetry_dictionary.values()

        )

    )["merged"]

    excluded = {

        "Date",
        "SessionTime",
        "Time",
        "Source",
        "Driver",
        "Team",
        "Color"

    }

    return sorted(

        [

            column

            for column in dataframe.columns

            if column not in excluded

        ]

    )