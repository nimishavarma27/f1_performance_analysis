"""
Telemetry Statistics Cards
"""

import streamlit as st


def display_statistics(
    statistics,
    metric
):
    """
    Display telemetry statistics.
    """

    if statistics is None or (hasattr(statistics, "empty") and statistics.empty) or len(statistics) == 0:

        st.info(
            "Statistics unavailable."
        )

        return

    st.subheader(
        f"{metric} Statistics"
    )

    columns = st.columns(
        len(statistics)
    )

    for column, (_, row) in zip(
        columns,
        statistics.iterrows()
    ):

        with column:

            st.metric(

                row["Driver"],

                f"{row['Average']}"

            )

            st.caption(
                f"Max : {row['Maximum']}"
            )

            st.caption(
                f"Min : {row['Minimum']}"
            )