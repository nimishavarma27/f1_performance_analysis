"""F1 Performance Analytics Dashboard entry point."""

from datetime import datetime

import pandas as pd
import streamlit as st

from loaders.session_loader import (
    get_available_sessions,
    get_event_schedule,
    load_session,
)
from processing.driver_data import build_driver_data
from utils.ui import initialize_ui
from views.comparison import render_comparison
from views.dashboard import render_dashboard
from views.driver import render_driver
from views.telemetry import render_telemetry


st.set_page_config(
    page_title="F1 Performance Analytics",
    page_icon=":checkered_flag:",
    layout="wide",
)

theme = initialize_ui()

EARLIEST_YEAR = 2018

# The app lands on this season by default. It is a fully-archived year with
# complete FastF1 data, so first-time visitors never hit a session whose data
# is missing. Every other year (including the current one) stays selectable.
DEFAULT_YEAR = 2024

SESSION_LABELS = {
    "FP1": "Practice 1",
    "FP2": "Practice 2",
    "FP3": "Practice 3",
    "SQ": "Sprint Qualifying",
    "S": "Sprint",
    "Q": "Qualifying",
    "R": "Race",
}


st.markdown(
    """
    <section class="f1-hero">
        <p class="f1-kicker">Formula 1 data intelligence</p>
        <h1>Performance Analytics</h1>
        <p>Compare drivers, unpack tyre strategy, and trace every decisive metre of a lap with FastF1 timing and telemetry data.</p>
    </section>
    """,
    unsafe_allow_html=True,
)


st.sidebar.header("Session")

current_year = datetime.now().year
years = list(range(current_year, EARLIEST_YEAR - 1, -1))

default_year_index = years.index(DEFAULT_YEAR) if DEFAULT_YEAR in years else 0
year = st.sidebar.selectbox("Season", years, index=default_year_index)

try:
    schedule = get_event_schedule(year)
except Exception as error:
    st.error(f"Unable to load schedule.\n\n{error}")
    st.stop()

today = pd.Timestamp.now().tz_localize(None)
schedule = schedule.copy()
schedule["EventDate"] = pd.to_datetime(
    schedule["EventDate"], utc=True, errors="coerce"
).dt.tz_localize(None)

completed_events = schedule[schedule["EventDate"] <= today]

if completed_events.empty:
    st.warning("No completed events are available for this season.")
    st.stop()

grand_prix = st.sidebar.selectbox(
    "Grand Prix",
    completed_events["EventName"].tolist(),
)

available_sessions = get_available_sessions(year, grand_prix)

if not available_sessions:
    st.error("No sessions available for this event.")
    st.stop()

session_type = st.sidebar.selectbox(
    "Session",
    available_sessions,
    format_func=lambda code: f"{code}  {SESSION_LABELS.get(code, code)}",
)

load_detailed_telemetry = st.sidebar.toggle(
    "Load detailed telemetry",
    value=False,
    help=(
        "Enables track map, speed traces, mini-sector, corner, and speed-trap "
        "analysis. Downloads substantially more data and is slower on first load."
    ),
)

session_key = (year, grand_prix, session_type, bool(load_detailed_telemetry))


with st.spinner("Loading session..."):
    try:
        session = load_session(
            year,
            grand_prix,
            session_type,
            telemetry=load_detailed_telemetry,
        )
    except Exception as error:
        st.error(f"Unable to load this session.\n\n{error}")
        st.stop()


st.sidebar.divider()
st.sidebar.header("Drivers")

try:
    drivers = sorted(session.laps["Driver"].dropna().unique())
except Exception as error:
    st.error(
        "The session loaded without accessible lap data. Please reload the "
        "page or select another session.\n\n"
        f"Technical detail: {error}"
    )
    st.stop()

if not drivers:
    st.error("No driver data available.")
    st.stop()

selected_drivers = st.sidebar.multiselect(
    "Select driver(s)",
    options=drivers,
    default=[drivers[0]],
)

if not selected_drivers:
    st.warning("Please select at least one driver.")
    st.stop()


with st.spinner("Preparing driver data..."):
    driver_data = build_driver_data(
        session_key,
        tuple(selected_drivers),
        session,
    )

if not driver_data:
    st.error("No usable data available for the selected drivers.")
    st.stop()


overview_tab, driver_tab, comparison_tab, telemetry_tab = st.tabs(
    [
        "Weekend Overview",
        "Driver Analysis",
        "Comparison and Strategy",
        "Telemetry and Track",
    ]
)

with overview_tab:
    render_dashboard(
        year=year,
        grand_prix=grand_prix,
        event=session.event,
        session=session,
    )

with driver_tab:
    render_driver(driver_data)

with comparison_tab:
    render_comparison(driver_data)

with telemetry_tab:
    render_telemetry(
        driver_data=driver_data,
        session_key=session_key,
        telemetry_enabled=load_detailed_telemetry,
    )


st.divider()
st.caption(
    "F1 Performance Analytics  |  Powered by FastF1, Streamlit, Pandas, Plotly"
)
