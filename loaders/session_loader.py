"""FastF1 session loading and on-disk cache configuration."""

from pathlib import Path

import fastf1
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIRECTORY = PROJECT_ROOT / "data" / "cache"
CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIRECTORY))


@st.cache_resource(show_spinner=False)
def load_session(
    year: int,
    grand_prix: str,
    session_type: str,
    *,
    telemetry: bool = False,
):
    """Load a FastF1 session and verify that its lap data is available.

    The loaded session object is cached in Streamlit's resource cache keyed
    on ``(year, grand_prix, session_type, telemetry)`` so repeated Streamlit
    reruns (theme changes, dropdown selections, driver toggles) reuse the
    same fully-parsed session instead of re-parsing it on every interaction.
    """

    try:
        session = fastf1.get_session(year, grand_prix, session_type)
        session.load(
            laps=True,
            telemetry=telemetry,
            weather=True,
            messages=False,
        )
        laps = session.laps
    except Exception as error:
        raise RuntimeError(
            f"FastF1 could not load {grand_prix} {year} ({session_type}). "
            "Please try again or select another completed session."
        ) from error

    if laps is None:
        raise RuntimeError(
            f"No lap timing data is available for {grand_prix} {year} "
            f"({session_type})."
        )

    return session


@st.cache_data(show_spinner=False, ttl=3600)
def get_event_schedule(year: int):
    """Cached wrapper around ``fastf1.get_event_schedule``."""

    return fastf1.get_event_schedule(year)


@st.cache_data(show_spinner=False, ttl=3600)
def get_available_sessions(year: int, grand_prix: str) -> list:
    """Return the list of session codes actually held for an event.

    Reads the ``Session1..Session5`` columns from the event row instead of
    calling ``event.get_session`` seven times per rerun.
    """

    event = fastf1.get_event(year, grand_prix)

    name_to_code = {
        "Practice 1": "FP1",
        "Practice 2": "FP2",
        "Practice 3": "FP3",
        "Qualifying": "Q",
        "Sprint Qualifying": "SQ",
        "Sprint Shootout": "SQ",
        "Sprint": "S",
        "Race": "R",
    }

    ordered = ["FP1", "FP2", "FP3", "SQ", "S", "Q", "R"]
    found = set()

    for i in range(1, 6):
        key = f"Session{i}"
        if key not in event:
            continue
        name = event.get(key)
        if not isinstance(name, str):
            continue
        code = name_to_code.get(name)
        if code:
            found.add(code)

    return [c for c in ordered if c in found]
