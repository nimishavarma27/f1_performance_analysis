"""FastF1 session loading and on-disk cache configuration."""

from pathlib import Path

import fastf1


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIRECTORY = PROJECT_ROOT / "data" / "cache"
CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIRECTORY))


def load_session(
    year: int,
    grand_prix: str,
    session_type: str,
    *,
    telemetry: bool = False,
):
    """Load a FastF1 session and verify that its lap data is available.

    FastF1 sessions are mutable objects. They are deliberately not stored in
    Streamlit's resource cache: FastF1's own persistent cache already handles
    downloaded data safely, while each dashboard run receives a fully loaded
    session object.
    """

    try:
        session = fastf1.get_session(year, grand_prix, session_type)
        session.load(
            laps=True,
            telemetry=telemetry,
            weather=True,
            messages=False,
        )

        # Accessing ``laps`` raises DataNotLoadedError when FastF1 did not
        # complete the timing-data load, even if Session.load() returned.
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
