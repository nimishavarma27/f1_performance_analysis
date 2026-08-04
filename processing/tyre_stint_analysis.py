"""
Tyre Stint Analysis
===================
"""

import pandas as pd


def analyse(driver_data):
    """
    Analyse tyre stints for selected drivers.
    """

    rows = []

    for driver, data in driver_data.items():

        laps = data["laps"]

        if laps.empty:
            continue

        compounds = laps["Compound"].fillna("Unknown")

        stints = laps["Stint"].fillna(0)

        grouped = laps.groupby("Stint")

        for stint, dataframe in grouped:

            try:
                stint_num = int(stint) if pd.notna(stint) else 0
            except Exception:
                stint_num = 0

            rows.append({

                "Driver": driver,

                "Stint": stint_num,

                "Compound": str(dataframe["Compound"].iloc[0]) if not dataframe.empty else "UNKNOWN",

                "Start Lap": int(dataframe["LapNumber"].min()),

                "End Lap": int(dataframe["LapNumber"].max()),

                "Laps": len(dataframe)

            })

    if not rows:
        return pd.DataFrame(columns=[
            "Driver", "Stint", "Compound", "Start Lap", "End Lap", "Laps"
        ])

    dataframe = pd.DataFrame(rows)

    dataframe.sort_values(

        ["Driver", "Stint"],

        inplace=True

    )

    dataframe.reset_index(

        drop=True,

        inplace=True

    )

    return dataframe