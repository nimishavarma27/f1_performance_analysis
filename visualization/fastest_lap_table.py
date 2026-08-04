import pandas as pd
import streamlit as st


def display_fastest_lap_table(df):
    """
    Display the fastest lap ranking table.
    """

    st.header("🏆 Fastest Lap Ranking")

    if df.empty:
        st.info("No lap data available.")
        return

    display_df = df.copy()

    # Format lap times
    display_df["LapTime"] = display_df["LapTime"].apply(
        lambda x: (
            f"{int(x.total_seconds() // 60)}:"
            f"{int(x.total_seconds() % 60):02d}."
            f"{int(x.microseconds / 1000):03d}"
        )
    )

    # Format gaps
    display_df["Gap"] = display_df["Gap"].apply(
        lambda x: (
            "+0.000"
            if x.total_seconds() == 0
            else f"+{x.total_seconds():.3f}"
        )
    )

    st.dataframe(
        display_df.head(10),
        use_container_width=True,
        hide_index=True
    )