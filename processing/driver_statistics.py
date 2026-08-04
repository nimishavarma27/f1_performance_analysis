import pandas as pd


def format_timedelta(value):
    """
    Safely format a pandas Timedelta.
    """

    if pd.isna(value):
        return "-"

    total_seconds = value.total_seconds()

    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:06.3f}"


def get_driver_statistics(driver_data):
    """
    Returns summary statistics for each selected driver.

    Parameters
    ----------
    driver_data : dict

    Returns
    -------
    dict
    """

    statistics = {}

    for driver, data in driver_data.items():

        laps = data["laps"]

        if laps.empty:
            continue

        valid_laps = laps.dropna(subset=["LapTime"]).copy()

        if valid_laps.empty:
            continue

        # -------------------------------------------------
        # Fastest Lap
        # -------------------------------------------------

        fastest_lap = valid_laps["LapTime"].min()

        # -------------------------------------------------
        # Average Lap
        # -------------------------------------------------

        average_lap = valid_laps["LapTime"].mean()

        # -------------------------------------------------
        # Best Sectors
        # -------------------------------------------------

        best_sector1 = valid_laps["Sector1Time"].min()

        best_sector2 = valid_laps["Sector2Time"].min()

        best_sector3 = valid_laps["Sector3Time"].min()

        # -------------------------------------------------
        # Completed Laps
        # -------------------------------------------------

        completed_laps = len(valid_laps)

        # -------------------------------------------------
        # Tyre Stints
        # -------------------------------------------------

        if "Stint" in valid_laps.columns:

            tyre_stints = valid_laps["Stint"].nunique()

        else:

            tyre_stints = 0

        # -------------------------------------------------
        # Top Speed
        # -------------------------------------------------

        if "SpeedST" in valid_laps.columns:

            top_speed = valid_laps["SpeedST"].max()

            average_speed = valid_laps["SpeedST"].mean()

        else:

            top_speed = None
            average_speed = None

        # -------------------------------------------------
        # Store
        # -------------------------------------------------

        statistics[driver] = {

            "Fastest Lap": format_timedelta(fastest_lap),

            "Average Lap": format_timedelta(average_lap),

            "Best Sector 1": format_timedelta(best_sector1),

            "Best Sector 2": format_timedelta(best_sector2),

            "Best Sector 3": format_timedelta(best_sector3),

            "Completed Laps": completed_laps,

            "Tyre Stints": tyre_stints,

            "Top Speed": (
                f"{top_speed:.1f} km/h"
                if pd.notna(top_speed)
                else "-"
            ),

            "Average Speed": (
                f"{average_speed:.1f} km/h"
                if pd.notna(average_speed)
                else "-"
            )

        }

    return statistics