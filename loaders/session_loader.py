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
        # Route the session's internal schedule lookup through FastF1's
        # offline backend so it does not touch the rate-limited Ergast /
        # Jolpica endpoints on Streamlit Cloud. Older FastF1 versions do
        # not accept the backend keyword on get_session, so fall back.
        try:
            session = fastf1.get_session(
                year, grand_prix, session_type, backend="fastf1"
            )
        except TypeError:
            session = fastf1.get_session(year, grand_prix, session_type)

        session.load(
            laps=True,
            telemetry=telemetry,
            weather=True,
            messages=False,
        )
        laps = session.laps
    except Exception as error:
        # Distinguish shared-hosting rate-limit failures so visitors see an
        # actionable message ("this is the free-tier limit, run locally for
        # reliable access") instead of a scary generic wrapper.
        error_name = type(error).__name__
        error_text = str(error)
        is_rate_limit = (
            "RateLimit" in error_name
            or "rate limit" in error_text.lower()
            or "500 calls" in error_text
        )

        if is_rate_limit:
            raise RuntimeError(
                "Free-tier rate limit reached on this deployment.\n\n"
                "This live demo runs on Streamlit Community Cloud, which "
                "shares an outbound IP with many other apps that also use "
                "the F1 data API. When the shared 500-calls-per-hour "
                "quota is exhausted, new session loads pause for the rest "
                "of the hour.\n\n"
                "Try again in 30-60 minutes, or clone the repo and run "
                "locally for uninterrupted access - there is no rate "
                "limit on your own machine:\n\n"
                "  git clone https://github.com/nimishavarma27/f1_performance_analysis\n"
                "  cd f1_performance_analysis\n"
                "  pip install -r requirements.txt\n"
                "  streamlit run app.py"
            ) from error

        # A session that exists in the schedule but has no published timing
        # data yet (very recent or future-dated rounds) raises
        # DataNotLoadedError. Tell the user plainly rather than showing the
        # raw "See Session.load" internal reference.
        is_no_data = (
            "DataNotLoaded" in error_name
            or "has not been loaded" in error_text
            or "no data" in error_text.lower()
        )
        if is_no_data:
            raise RuntimeError(
                f"No timing data is available yet for {grand_prix} {year} "
                f"({session_type}).\n\n"
                "This usually means the session hasn't happened yet, or its "
                "data has not been published to the F1 timing service. Pick a "
                "different Grand Prix or an earlier season from the sidebar - "
                "seasons 2018 to 2024 are fully archived."
            ) from error

        # Surface any other underlying FastF1 exception so the visible error
        # is diagnosable (timeout, cache write, etc.).
        raise RuntimeError(
            f"FastF1 could not load {grand_prix} {year} ({session_type}).\n\n"
            f"Underlying error: {error_name}: {error}\n\n"
            "Please try a different session or year."
        ) from error

    if laps is None:
        raise RuntimeError(
            f"No lap timing data is available for {grand_prix} {year} "
            f"({session_type})."
        )

    return session


@st.cache_data(show_spinner=False, ttl=3600)
def get_event_schedule(year: int):
    """Cached wrapper around ``fastf1.get_event_schedule``.

    Prefers FastF1's built-in offline schedule backend to avoid the shared
    Ergast/Jolpica rate limit (500 calls/hour per IP) that hits hard on
    Streamlit Cloud, where many apps share an outbound IP. Falls back to
    the default backend if the offline one is unavailable.
    """

    try:
        return fastf1.get_event_schedule(year, backend="fastf1")
    except Exception:
        return fastf1.get_event_schedule(year)


@st.cache_data(show_spinner=False, ttl=3600)
def get_available_sessions(year: int, grand_prix: str) -> list:
    """Return the list of session codes actually held for an event.

    Reads the ``Session1..Session5`` columns from the event row instead of
    calling ``event.get_session`` seven times per rerun.
    """

    # Read the event row from the schedule (which we already fetched via the
    # offline FastF1 backend) instead of calling fastf1.get_event(), which
    # would re-hit the rate-limited Ergast/Jolpica API on Streamlit Cloud.
    schedule = get_event_schedule(year)
    matches = schedule[schedule["EventName"] == grand_prix]
    if matches.empty:
        return []
    event = matches.iloc[0]

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
