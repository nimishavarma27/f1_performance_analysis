"""
Driver Lap Comparison
=====================
"""

import streamlit as st


def display(result):

    if result is None:

        st.warning(
            "Comparison unavailable."
        )

        return

    st.subheader(
        f"{result['Driver 1']} vs {result['Driver 2']}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Lap Time",
            str(result["Lap Time 1"])
        )

        st.metric(
            "Sector 1",
            str(result["Sector 1 1"])
        )

        st.metric(
            "Sector 2",
            str(result["Sector 2 1"])
        )

        st.metric(
            "Sector 3",
            str(result["Sector 3 1"])
        )

        st.metric(
            "Top Speed",
            f"{result['Top Speed 1']} km/h"
        )

        st.write(
            f"Tyre: **{result['Compound 1']}**"
        )

    with col2:

        st.metric(
            "Lap Time",
            str(result["Lap Time 2"])
        )

        st.metric(
            "Sector 1",
            str(result["Sector 1 2"])
        )

        st.metric(
            "Sector 2",
            str(result["Sector 2 2"])
        )

        st.metric(
            "Sector 3",
            str(result["Sector 3 2"])
        )

        st.metric(
            "Top Speed",
            f"{result['Top Speed 2']} km/h"
        )

        st.write(
            f"Tyre: **{result['Compound 2']}**")