import streamlit as st
import pandas as pd


def display_dashboard_overview(event, session):
    """
    Display an overview of the selected Formula 1 event and session.
    """
    
    st.header("🏁 Dashboard Overview")


    # Event Information
    event_name = event["EventName"]
    location = event["Location"]
    country = event["Country"]

    # Session Information
    session_name = session.name

    try:
        session_date = pd.to_datetime(session.date).strftime("%d %b %Y")
    except Exception:
        session_date = "Unavailable"

    try:
        driver_count = len(session.drivers)
    except Exception:
        driver_count = "N/A"

    try:
        total_laps = int(session.laps["LapNumber"].max())
    except Exception:
        total_laps = "N/A"

    # Display Title
    st.subheader(event_name)

    st.caption(f"{location}, {country}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📅 Date", session_date)
    col2.metric("🏎️ Session", session_name)
    col3.metric("👥 Drivers", driver_count)
    col4.metric("🏁 Laps", total_laps)

    st.divider()