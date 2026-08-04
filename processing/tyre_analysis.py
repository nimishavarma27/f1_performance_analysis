import pandas as pd


def get_tyre_dataframe(laps):
    """
    Create a DataFrame for tyre performance analysis.

    Parameters
    ----------
    laps : fastf1.core.Laps
        All laps of the selected driver.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing tyre information.
    """

    # Keep only laps with valid lap times
    valid_laps = laps[laps["LapTime"].notna()].copy()

    # Convert lap time from Timedelta to seconds
    valid_laps["LapTimeSeconds"] = (
        valid_laps["LapTime"]
        .dt
        .total_seconds()
    )

    # Keep only the columns required for tyre analysis
    tyre_df = valid_laps[
        [
            "LapNumber",
            "LapTimeSeconds",
            "Compound",
            "TyreLife",
            "Stint",
            "FreshTyre"
        ]
    ].copy()

    # Remove rows where tyre compound is missing
    tyre_df = tyre_df[tyre_df["Compound"].notna()]

    return tyre_df