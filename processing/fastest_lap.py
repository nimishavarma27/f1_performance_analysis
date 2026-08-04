import pandas as pd


def get_fastest_lap_ranking(session):
    """
    Returns a DataFrame containing the fastest lap for every driver
    in the selected session.

    Parameters
    ----------
    session : fastf1.core.Session

    Returns
    -------
    pandas.DataFrame
    """

    rankings = []

    for driver in session.drivers:

        try:
            driver_laps = session.laps.pick_drivers(driver)

            if driver_laps.empty:
                continue

            fastest_lap = driver_laps.pick_fastest()

            if fastest_lap is None or pd.isna(fastest_lap.get("LapTime")):
                continue

            driver_code = (
                fastest_lap["Driver"]
                if "Driver" in fastest_lap and pd.notna(fastest_lap["Driver"])
                else str(driver)
            )

            rankings.append(
                {
                    "Driver": driver_code,
                    "Team": fastest_lap.get("Team", "N/A"),
                    "LapTime": fastest_lap["LapTime"],
                }
            )

        except Exception:
            continue

    if not rankings:
        return pd.DataFrame(
            columns=[
                "Position",
                "Driver",
                "Team",
                "LapTime",
                "Gap",
            ]
        )

    df = pd.DataFrame(rankings)

    # Remove invalid lap times
    df = df.dropna(subset=["LapTime"])

    # Sort by fastest lap
    df = df.sort_values(
        by="LapTime"
    ).reset_index(drop=True)

    # Add position
    df.insert(
        0,
        "Position",
        range(1, len(df) + 1)
    )

    # Calculate gap to fastest lap
    fastest_time = df.loc[0, "LapTime"]

    df["Gap"] = df["LapTime"] - fastest_time

    return df