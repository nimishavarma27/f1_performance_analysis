import pandas as pd


def get_driver_comparison_dataframe(driver1_laps, driver2_laps):
    """
    Create processed DataFrames for comparing two drivers.

    Parameters
    ----------
    driver1_laps : fastf1.core.Laps
        Laps of Driver 1.

    driver2_laps : fastf1.core.Laps
        Laps of Driver 2.

    Returns
    -------
    tuple
        (driver1_df, driver2_df)
    """

    # ---------------- Driver 1 ---------------- #

    driver1_df = driver1_laps[
        driver1_laps["LapTime"].notna()
    ].copy()

    driver1_df["LapTimeSeconds"] = (
        driver1_df["LapTime"]
        .dt
        .total_seconds()
    )

    driver1_df = driver1_df[
        [
            "LapNumber",
            "LapTimeSeconds",
            "Compound",
            "Stint",
            "TyreLife"
        ]
    ].copy()

    # ---------------- Driver 2 ---------------- #

    driver2_df = driver2_laps[
        driver2_laps["LapTime"].notna()
    ].copy()

    driver2_df["LapTimeSeconds"] = (
        driver2_df["LapTime"]
        .dt
        .total_seconds()
    )

    driver2_df = driver2_df[
        [
            "LapNumber",
            "LapTimeSeconds",
            "Compound",
            "Stint",
            "TyreLife"
        ]
    ].copy()

    return driver1_df, driver2_df