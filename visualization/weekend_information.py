import streamlit as st


def render_weekend_information(summary):
    """
    Display the Weekend Information section.

    Parameters
    ----------
    summary : dict
        Output from processing.weekend_summary.get_weekend_summary()
    """

    with st.expander("🏁 Weekend Information", expanded=False):

        leaders = summary["leaders"]

        # ======================================================
        # Metric Cards
        # ======================================================

        pole = None
        winner = None
        fastest_driver = None
        fastest_time = None

        if not leaders.empty:

            # ----------------------------------------------
            # Pole Position
            # ----------------------------------------------

            pole_data = leaders[
                leaders["Result"] == "Pole Position"
            ]

            if not pole_data.empty:
                pole = pole_data.iloc[0]

            # ----------------------------------------------
            # Race Winner
            # ----------------------------------------------

            race_data = leaders[
                leaders["Result"] == "Race Winner"
            ]

            if not race_data.empty:

                winner = race_data.iloc[0]

                fastest_driver = winner.get(
                    "FastestLapDriver",
                    None
                )

                fastest_time = winner.get(
                    "FastestLapTime",
                    None
                )

        col1, col2, col3 = st.columns(3)

        # --------------------------------------------------
        # Pole Position
        # --------------------------------------------------

        with col1:

            if pole is not None:

                st.metric(
                    label="🏁 Pole Position",
                    value=pole["Driver"],
                    delta=pole["Time"]
                )

            else:

                st.metric(
                    label="🏁 Pole Position",
                    value="-"
                )

        # --------------------------------------------------
        # Race Winner
        # --------------------------------------------------

        with col2:

            if winner is not None:

                st.metric(
                    label="🥇 Race Winner",
                    value=winner["Driver"],
                    delta=winner["Team"]
                )

            else:

                st.metric(
                    label="🥇 Race Winner",
                    value="-"
                )

        # --------------------------------------------------
        # Fastest Lap
        # --------------------------------------------------

        with col3:

            if fastest_driver:

                st.metric(
                    label="⚡ Fastest Lap",
                    value=fastest_driver,
                    delta=fastest_time
                )

            else:

                st.metric(
                    label="⚡ Fastest Lap",
                    value="-"
                )

        st.divider()

        # ======================================================
        # Tabs
        # ======================================================

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Session Leaders",
                "🥇 Top 3",
                "📍 Circuit Information"
            ]
        )

        # ======================================================
        # Session Leaders
        # ======================================================

        with tab1:

            if leaders.empty:

                st.info("No session data available.")

            else:

                display = leaders.copy()

                st.dataframe(
                    display[
                        [
                            "Session",
                            "Result",
                            "Driver",
                            "Team",
                            "Time"
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

        # ======================================================
        # Top Three
        # ======================================================

        with tab2:

            if not summary["top3"]:

                st.info("No podium information available.")

            else:

                session_names = {
                    "FP1": "Practice 1",
                    "FP2": "Practice 2",
                    "FP3": "Practice 3",
                    "SQ": "Sprint Qualifying",
                    "S": "Sprint",
                    "Q": "Qualifying",
                    "R": "Race"
                }

                for code, podium in summary["top3"].items():

                    st.subheader(
                        session_names.get(code, code)
                    )

                    st.dataframe(
                        podium,
                        use_container_width=True,
                        hide_index=True
                    )

        # ======================================================
        # Circuit Information
        # ======================================================

        with tab3:

            circuit = summary["circuit"]

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Grand Prix:** {circuit['Grand Prix']}"
                )

                st.write(
                    f"**Location:** {circuit['Location']}"
                )

                st.write(
                    f"**Country:** {circuit['Country']}"
                )

            with col2:

                st.write(
                    f"**Round:** {circuit['Round']}"
                )

                st.write(
                    f"**Date:** {circuit['Date']}"
                )