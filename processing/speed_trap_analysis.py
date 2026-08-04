"""
Speed Trap Analysis
===================

Find the maximum speed reached by each driver.
"""

import pandas as pd


def analyse(telemetry_dictionary):

    rows = []

    for driver, driver_data in telemetry_dictionary.items():

        telemetry = driver_data["merged"]

        if not {"Speed", "Distance"}.issubset(telemetry.columns):
            continue

        telemetry = telemetry.dropna(
            subset=["Speed", "Distance"]
        )

        if telemetry.empty:
            continue

        fastest = telemetry.loc[
            telemetry["Speed"].idxmax()
        ]

        rows.append({

            "Driver": driver,

            "Top Speed (km/h)": round(
                float(fastest["Speed"]), 1
            ),

            "Distance (m)": round(
                float(fastest["Distance"]), 1
            )

        })

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values(
            "Top Speed (km/h)",
            ascending=False
        ).reset_index(drop=True)

    return df