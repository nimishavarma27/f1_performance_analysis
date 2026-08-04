import streamlit as st
import fastf1
from datetime import datetime
import pandas as pd

from loaders.session_loader import load_session

from processing.sector_analysis import get_sector_dataframe
from processing.lap_analysis import get_lap_time_dataframe
from processing.tyre_analysis import get_tyre_dataframe
from processing.telemetry_engine import (build)
from processing.track_map import prepare
from processing.corner_analysis import analyse
from processing.mini_sector_analysis import analyse as analyse_mini_sector
from processing.speed_trap_analysis import analyse as analyse_speed_trap
from processing.tyre_stint_analysis import analyse as analyse_stints
from processing.pace_analysis import analyse as analyse_pace
from processing.pit_stop_analysis import (analyse as analyse_pit_stops)


from visualization.comparison_charts import create_driver_comparison_chart
from visualization.track_map_chart import (create_chart as create_track_map)
from visualization.corner_analysis_cards import (display as display_corner_analysis)
from visualization.mini_sector_table import (display as display_mini_sector)
from visualization.speed_trap_table import (display as display_speed_trap)
from visualization.tyre_stint_table import (display as display_stints)
from visualization.strategy_timeline import (create_chart as create_strategy_chart)
from visualization.pace_table import (display as display_pace)
from visualization.pit_stop_table import (display as display_pit_stops)
from visualization.telemetry_dashboard import render

from utils.team_colors import get_team_color
from utils.ui import initialize_ui


from views.dashboard import render_dashboard
from views.driver import render_driver


# --------------------------------------------------------
# Streamlit Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="F1 Performance Analytics Dashboard",
    page_icon="🏎️",
    layout="wide"
)

theme = initialize_ui()

# --------------------------------------------------------
# Dashboard Header
# --------------------------------------------------------

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

# --------------------------------------------------------
# Sidebar - Session Selection
# --------------------------------------------------------

st.sidebar.header("🏁 Session")

current_year = datetime.now().year

years = list(range(current_year, 1949, -1))

year = st.sidebar.selectbox(
    "Season",
    years
)

# --------------------------------------------------------
# Load Event Schedule
# --------------------------------------------------------

try:

    schedule = fastf1.get_event_schedule(year)

except Exception as e:

    st.error(f"Unable to load schedule.\n\n{e}")
    st.stop()

today = pd.Timestamp.now().tz_localize(None)

schedule["EventDate"] = (
    pd.to_datetime(schedule["EventDate"])
    .dt.tz_localize(None)
)

completed_events = schedule[
    schedule["EventDate"] <= today
]

if completed_events.empty:

    st.warning(
        "No completed events are available for this season."
    )

    st.stop()

grand_prix = st.sidebar.selectbox(
    "Grand Prix",
    completed_events["EventName"].tolist()
)

# --------------------------------------------------------
# Available Sessions
# --------------------------------------------------------

event = fastf1.get_event(year, grand_prix)

available_sessions = []

session_mapping = {
    "Practice 1": "FP1",
    "Practice 2": "FP2",
    "Practice 3": "FP3",
    "Qualifying": "Q",
    "Sprint Qualifying": "SQ",
    "Sprint": "S",
    "Race": "R"
}

for session_name, session_code in session_mapping.items():

    try:

        event.get_session(session_name)

        available_sessions.append(session_code)

    except Exception:

        pass

if not available_sessions:

    st.error("No sessions available.")

    st.stop()

session_type = st.sidebar.selectbox(
    "Session",
    available_sessions
)

load_detailed_telemetry = st.sidebar.toggle(
    "Load detailed telemetry",
    value=False,
    help=(
        "Enables track map, speed traces, mini-sector, corner, and speed-trap "
        "analysis. It downloads substantially more data and is slower on first load."
    ),
)

# --------------------------------------------------------
# Load Session
# --------------------------------------------------------

with st.spinner("Loading session..."):

    try:

        session = load_session(
            year,
            grand_prix,
            session_type,
            telemetry=load_detailed_telemetry,
        )
        

        


    except Exception as e:

        st.error(
            f"Unable to load this session.\n\n{e}"
        )

        st.stop()

# --------------------------------------------------------
# Driver Selection
# --------------------------------------------------------

st.sidebar.divider()
st.sidebar.header("👤 Drivers")

try:
    drivers = sorted(
        session.laps["Driver"]
        .dropna()
        .unique()
    )
except Exception as error:
    st.error(
        "The session loaded without accessible lap data. "
        "Please reload the page or select another session.\n\n"
        f"Technical detail: {error}"
    )
    st.stop()

if len(drivers) == 0:

    st.error("No driver data available.")

    st.stop()

selected_drivers = st.sidebar.multiselect(
    "Select Driver(s)",
    options=drivers,
    default=[drivers[0]]
)

if len(selected_drivers) == 0:

    st.warning(
        "Please select at least one driver."
    )

    st.stop()

# --------------------------------------------------------
# Driver Data Processing
# --------------------------------------------------------

driver_data = {}

progress_bar = st.progress(0)
status = st.empty()

total_drivers = len(selected_drivers)

for i, driver in enumerate(selected_drivers):

    status.text(f"Processing {driver}...")

    try:

        laps = session.laps.pick_drivers(driver)

        if laps.empty:
            continue

        laps = laps[laps["LapTime"].notna()].copy()

        if laps.empty:
            continue

        fastest = laps.pick_fastest()

        team = laps.iloc[0]["Team"]

        driver_data[driver] = {

            "team": team,

            "color": get_team_color(team),

            "laps": laps,

            "fastest": fastest,

            "sector_df": get_sector_dataframe(
                fastest
            ),

            "lap_df": get_lap_time_dataframe(
                laps
            ),

            "tyre_df": get_tyre_dataframe(
                laps
            )

        }

    except Exception as e:

        st.warning(
            f"Skipping {driver}: {e}"
        )

    progress_bar.progress(
        (i + 1) / total_drivers
    )

progress_bar.empty()
status.empty()

if len(driver_data) == 0:

    st.error(
        "No usable data available for the selected drivers."
    )

    st.stop()

# ========================================================
# WEEKEND OVERVIEW
# ========================================================

render_dashboard(
    year=year,
    grand_prix=grand_prix,
    event=event,
    session=session
)

# ========================================================
# DRIVER ANALYSIS
# ========================================================

render_driver(
    driver_data
)

# ========================================================
# COMPARATIVE ANALYSIS
# ========================================================

st.divider()

st.header("📈 Comparative Analysis")

# --------------------------------------------------------
# Driver Comparison
# --------------------------------------------------------

if len(driver_data) > 1:

    comparison_chart = create_driver_comparison_chart(
        driver_data
    )

    st.plotly_chart(
        comparison_chart,
        use_container_width=True
    )

else:

    st.info(
        "Select two or more drivers to enable the comparison chart."
    )

# --------------------------------------------------------
# Telemetry Dashboard
# --------------------------------------------------------
st.subheader("Telemetry")

telemetry_dictionary = (
    build(driver_data)
    if load_detailed_telemetry
    else {}
)

if not load_detailed_telemetry:
    st.info(
        "Detailed telemetry is off for a faster load. Enable **Load detailed "
        "telemetry** in the sidebar to use the telemetry, track map, corner, "
        "mini-sector, and speed-trap views."
    )


render(
    telemetry_dictionary,
    driver_data
)


# --------------------------------------------------------
# Track Map
# --------------------------------------------------------

st.subheader("Track Map")

selected_driver = st.selectbox(

    "Driver",

    list(driver_data.keys()),

    key="track_map_driver"

)

track = prepare(

    telemetry_dictionary,

    selected_driver

)

if track is not None:

    figure = create_track_map(

        track,

        driver_data[selected_driver]["color"]

    )

    st.plotly_chart(

        figure,

        use_container_width=True

    )

else:

    st.warning(

        "Track position data unavailable."

    )


# --------------------------------------------------------
# Corner Analysis
# --------------------------------------------------------

st.subheader("Corner Analysis")

corner_driver = st.selectbox(

    "Driver for Corner Analysis",

    list(driver_data.keys()),

    key="corner_driver"

)

corner_results = analyse(

    telemetry_dictionary,

    corner_driver

)

display_corner_analysis(

    corner_results

)

# --------------------------------------------------------
# Mini Sector Analysis
# --------------------------------------------------------

st.subheader("Mini Sector Analysis")

mini_sector = analyse_mini_sector(
    telemetry_dictionary,
    sectors=25
)

display_mini_sector(
    mini_sector
)


# --------------------------------------------------------
# Speed Trap Analysis
# --------------------------------------------------------

st.subheader("Speed Trap Analysis")

speed_trap = analyse_speed_trap(
    telemetry_dictionary
)

display_speed_trap(
    speed_trap
)

# --------------------------------------------------------
# Tyre Stint Analysis
# --------------------------------------------------------

st.subheader("Tyre Stint Analysis")

stints = analyse_stints(
    driver_data
)

display_stints(
    stints
)

# --------------------------------------------------------
# Strategy Timeline
# --------------------------------------------------------

st.subheader(
    "Race Strategy Timeline"
)

strategy_chart = create_strategy_chart(
    stints
)

st.plotly_chart(

    strategy_chart,

    use_container_width=True

)

# --------------------------------------------------------
# Pace Analysis
# --------------------------------------------------------

st.subheader(
    "Pace Analysis"
)

pace = analyse_pace(
    driver_data
)

display_pace(
    pace
)


# --------------------------------------------------------
# Pit Stop Analysis
# --------------------------------------------------------

st.subheader(
    "Pit Stop Analysis"
)

pit_stops = analyse_pit_stops(
    driver_data
)

display_pit_stops(
    pit_stops
)


# ========================================================
# FOOTER
# ========================================================

st.divider()

st.caption(
    "🏎️ F1 Performance Analytics Dashboard | Powered by FastF1 • Streamlit • Pandas • Plotly"
)
