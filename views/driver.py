"""
Driver View
===========

Renders all driver-specific analysis.

Contains:
- Driver Statistics
- Session Summary
- Sector Analysis
- Lap Time Analysis
- Tyre Performance Analysis
"""

import streamlit as st

from processing.driver_statistics import get_driver_statistics

from visualization.driver_statistics_cards import (
    display_driver_statistics
)

from visualization.sector_charts import (
    create_sector_chart
)

from visualization.lap_charts import (
    create_lap_time_chart
)

from visualization.tyre_charts import (
    create_tyre_chart
)


def render_driver(
    driver_data
):
    """
    Render all driver analysis.
    """

    st.divider()

    st.header("👤 Driver Analysis")

    # --------------------------------------------------------
    # Driver Statistics
    # --------------------------------------------------------

    statistics = get_driver_statistics(
        driver_data
    )

    display_driver_statistics(
        statistics
    )

    # --------------------------------------------------------
    # Session Summary
    # --------------------------------------------------------

    st.subheader("Session Summary")

    metric_columns = st.columns(
        len(driver_data)
    )

    for col, (driver, data) in zip(
        metric_columns,
        driver_data.items()
    ):

        fastest = data["fastest"]

        with col:

            st.metric(

                label=driver,

                value=f"{fastest['LapTime'].total_seconds():.3f} s"

            )

    # --------------------------------------------------------
    # Sector Analysis
    # --------------------------------------------------------

    st.subheader("Sector Analysis")

    for driver, data in driver_data.items():

        st.markdown(f"### {driver}")

        figure = create_sector_chart(

            data["sector_df"],

            driver,

            data["color"]

        )

        st.plotly_chart(

            figure,

            use_container_width=True

        )

    # --------------------------------------------------------
    # Lap Time Analysis
    # --------------------------------------------------------

    st.subheader("Lap Time Analysis")

    for driver, data in driver_data.items():

        st.markdown(f"### {driver}")

        figure = create_lap_time_chart(

            data["lap_df"],

            driver,

            data["color"]

        )

        st.plotly_chart(

            figure,

            use_container_width=True

        )

    # --------------------------------------------------------
    # Tyre Performance Analysis
    # --------------------------------------------------------

    st.subheader("Tyre Performance Analysis")

    for driver, data in driver_data.items():

        st.markdown(f"### {driver}")

        figure = create_tyre_chart(

            data["tyre_df"],

            driver,

            data["color"]

        )

        st.plotly_chart(

            figure,

            use_container_width=True

        )