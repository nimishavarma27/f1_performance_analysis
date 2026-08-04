import pandas as pd


def get_sector_dataframe(fastest_lap):
    """
    Create a DataFrame containing the sector times
    of the driver's fastest lap.

    Parameters
    ----------
    fastest_lap : pandas.Series
        Fastest lap returned by FastF1.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing Sector and Time columns.
    """

    def safe_seconds(val):
        if pd.notna(val) and hasattr(val, "total_seconds"):
            return val.total_seconds()
        return None

    sector_df = pd.DataFrame({
        "Sector": [
            "Sector 1",
            "Sector 2",
            "Sector 3"
        ],
        "Time": [
            safe_seconds(fastest_lap.get("Sector1Time")),
            safe_seconds(fastest_lap.get("Sector2Time")),
            safe_seconds(fastest_lap.get("Sector3Time"))
        ]
    })

    return sector_df