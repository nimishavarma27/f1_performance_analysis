import fastf1
from utils.logger import logger


def load_session_safe(year, grand_prix, session_code):
    """Load timing and result data without expensive telemetry downloads."""

    try:

        session = fastf1.get_session(
            year,
            grand_prix,
            session_code
        )

        session.load(
            laps=True,
            telemetry=False,
            weather=False,
            messages=False,
        )

        return session_code, session

    except Exception as e:

        logger.warning(
            f"{session_code} could not be loaded: {e}"
        )

        return session_code, None
