import streamlit as st
import pandas as pd
import fastf1

from concurrent.futures import ThreadPoolExecutor

from utils.session_utils import load_session_safe
from utils.constants_codes import SESSION_CODES
from utils.session_names import SESSION_NAMES


# ==========================================================
# Circuit Information
# ==========================================================

def get_circuit_information(event):
    """
    Returns circuit information.
    """

    return {
        "Grand Prix": event.EventName,
        "Location": event.Location,
        "Country": event.Country,
        "Round": event.RoundNumber,
        "Date": str(event.EventDate.date())
    }


# ==========================================================
# Session Leader
# ==========================================================

def get_session_leader(session, session_code):
    """
    Returns leader information for a session.
    """

    try:

        # --------------------------------------------------
        # Race & Sprint
        # --------------------------------------------------

        if session_code in ["R", "S"]:

            results = (
                session.results
                .sort_values("Position")
                .reset_index(drop=True)
            )

            winner = results.iloc[0]

            try:
                fastest = session.laps.pick_fastest()
            except Exception:
                fastest = None

            result_name = (
                "Race Winner"
                if session_code == "R"
                else "Sprint Winner"
            )

            session_name = (
                "Race"
                if session_code == "R"
                else "Sprint"
            )

            return {
                "Session": session_name,
                "Driver": winner.get("Abbreviation", winner.get("DriverNumber", "-")),
                "Team": winner.get("TeamName", "-"),
                "Result": result_name,
                "Time": str(winner.get("Time", "-")),
                "FastestLapDriver": (
                    fastest["Driver"] if fastest is not None and "Driver" in fastest else None
                ),
                "FastestLapTime": (
                    str(fastest["LapTime"]) if fastest is not None and "LapTime" in fastest else None
                )
            }

        # --------------------------------------------------
        # Practice / Qualifying
        # --------------------------------------------------

        fastest = session.laps.pick_fastest()

        if fastest is None:
            return None

        session_name, result = SESSION_NAMES.get(
            session_code,
            (session_code, "P1")
        )

        return {
            "Session": session_name,
            "Driver": fastest["Driver"],
            "Team": fastest["Team"],
            "Result": result,
            "Time": str(fastest["LapTime"])
        }

    except Exception:

        return None


# ==========================================================
# Top Three
# ==========================================================

def get_top_three(session, session_code):
    """
    Returns the top three drivers for a session.
    """

    try:

        # --------------------------------------------------
        # Race & Sprint
        # --------------------------------------------------

        if session_code in ["R", "S"]:

            results = (
                session.results
                .sort_values("Position")
                .head(3)
            )

            return pd.DataFrame({
                "Position": results["Position"].tolist(),
                "Driver": results["Abbreviation"].tolist(),
                "Team": results["TeamName"].tolist()
            })

        # --------------------------------------------------
        # Practice / Qualifying
        # --------------------------------------------------

        fastest = (
            session.laps
            .dropna(subset=["LapTime"])
            .sort_values("LapTime")
            .drop_duplicates(subset="Driver")
            .head(3)
        )

        return pd.DataFrame({
            "Position": list(range(1, len(fastest) + 1)),
            "Driver": fastest["Driver"].tolist(),
            "Team": fastest["Team"].tolist(),
            "Time": fastest["LapTime"].astype(str).tolist()
        })

    except Exception:

        return None


# ==========================================================
# Weekend Summary
# ==========================================================

@st.cache_data(show_spinner=False)
def get_weekend_summary(year, grand_prix):
    """
    Loads all available sessions for a race weekend
    and returns summary information.
    """

    event = fastf1.get_event(year, grand_prix)

    # --------------------------------------------------
    # Load sessions in parallel
    # --------------------------------------------------

    def load(code):
        return load_session_safe(
            year,
            grand_prix,
            code
        )

    # Timing-only loads are much smaller than telemetry loads. Limiting the
    # workers avoids overwhelming FastF1's data sources on an uncached weekend.
    with ThreadPoolExecutor(max_workers=3) as executor:

        loaded_sessions = dict(
            executor.map(load, SESSION_CODES)
        )

    leaders = []
    top_three = {}

    # --------------------------------------------------
    # Process sessions
    # --------------------------------------------------

    for code, session in loaded_sessions.items():

        if session is None:
            continue

        leader = get_session_leader(
            session,
            code
        )

        if leader is not None:
            leaders.append(leader)

        podium = get_top_three(
            session,
            code
        )

        if podium is not None:
            top_three[code] = podium

    return {
        "circuit": get_circuit_information(event),
        "leaders": pd.DataFrame(leaders),
        "top3": top_three
    }
