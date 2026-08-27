"""
Mini Sector Analysis
====================

Divides the lap into equal mini sectors and determines which driver is
fastest in each mini sector based on average speed.
"""

import numpy as np
import pandas as pd

from utils.logger import logger


def analyse(telemetry_dictionary: dict, sectors: int = 25):
    """Analyse mini sectors for all available drivers.

    Vectorised implementation: a single ``pd.cut`` + ``groupby`` per driver
    replaces the 25 x N boolean scans of the original version.
    """

    if not telemetry_dictionary:
        return None

    valid_drivers = {}

    for driver, driver_data in telemetry_dictionary.items():
        telemetry = driver_data.get("merged")
        if telemetry is None:
            continue

        required = {"Distance", "Speed"}
        if not required.issubset(telemetry.columns):
            logger.warning(
                f"[MiniSector] {driver} missing columns: "
                f"{required - set(telemetry.columns)}"
            )
            continue

        valid_drivers[driver] = telemetry

    if not valid_drivers:
        return None

    maximum_distance = min(t["Distance"].max() for t in valid_drivers.values())
    boundaries = np.linspace(0, maximum_distance, sectors + 1)
    labels = list(range(sectors))

    per_driver_means = {}
    for driver, telemetry in valid_drivers.items():
        bins = pd.cut(
            telemetry["Distance"],
            bins=boundaries,
            labels=labels,
            include_lowest=True,
            right=False,
        )
        per_driver_means[driver] = (
            telemetry["Speed"].groupby(bins, observed=False).mean()
        )

    speeds = pd.DataFrame(per_driver_means)

    results = []
    for sector in range(sectors):
        row = speeds.loc[sector] if sector in speeds.index else pd.Series(dtype=float)
        row = row.dropna()

        if row.empty:
            fastest_driver = None
            fastest_speed = None
        else:
            fastest_driver = row.idxmax()
            fastest_speed = round(float(row.max()), 2)

        results.append(
            {
                "Mini Sector": sector + 1,
                "Start (m)": round(float(boundaries[sector]), 2),
                "End (m)": round(float(boundaries[sector + 1]), 2),
                "Fastest Driver": fastest_driver,
                "Average Speed (km/h)": fastest_speed,
            }
        )

    return pd.DataFrame(results)
