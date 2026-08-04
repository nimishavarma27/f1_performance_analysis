import pandas as pd


def get_lap_time_dataframe(laps):
    """
    Create a DataFrame containing valid lap times.

    Parameters
    ----------
    laps : fastf1.core.Laps
        All laps of the selected driver.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing lap information.
    """

    # Remove laps with missing lap time
    valid_laps = laps[laps["LapTime"].notna()].copy()

    # Convert Timedelta to seconds
    valid_laps["LapTimeSeconds"] = (
        valid_laps["LapTime"]
        .dt
        .total_seconds()
    )

    # Keep only required columns
    lap_df = valid_laps[
        [
            "LapNumber",
            "LapTimeSeconds",
            "Compound",
            "TyreLife",
            "Stint"
        ]
    ].copy()

    return lap_df