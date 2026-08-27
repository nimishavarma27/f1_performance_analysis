"""
Pit Stop Analysis
=================

Analyse pit stops from FastF1 lap data.
"""

import pandas as pd


def analyse(driver_data):
    """Analyse pit stops for each driver.

    A pit stop is inferred whenever the ``Stint`` value changes between
    consecutive laps. Detection is vectorised per driver, no ``iterrows``.
    """

    frames = []

    for driver, data in driver_data.items():
        laps = data["laps"]
        if laps.empty or "Stint" not in laps.columns:
            continue

        laps = laps.sort_values("LapNumber")

        stint_changed = laps["Stint"].ne(laps["Stint"].shift())
        stint_changed.iloc[0] = False

        if not stint_changed.any():
            continue

        pit_laps = laps.loc[stint_changed, ["LapNumber", "Compound", "Stint"]].copy()
        pit_laps.insert(0, "Driver", driver)
        pit_laps = pit_laps.rename(
            columns={
                "LapNumber": "Pit Lap",
                "Compound": "New Compound",
                "Stint": "New Stint",
            }
        )
        pit_laps["Pit Lap"] = pit_laps["Pit Lap"].astype(int)
        pit_laps["New Stint"] = pit_laps["New Stint"].astype(int)

        frames.append(pit_laps)

    if not frames:
        return pd.DataFrame(columns=["Driver", "Pit Lap", "New Compound", "New Stint"])

    dataframe = pd.concat(frames, ignore_index=True)
    return dataframe.sort_values(["Driver", "Pit Lap"]).reset_index(drop=True)
