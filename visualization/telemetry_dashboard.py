"""
Telemetry Dashboard
===================

Professional telemetry visualization for multiple drivers.

Compatible with the telemetry engine.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.ui import get_plotly_layout


# ==========================================================
# Axis Labels
# ==========================================================

AXIS_LABELS = {

    "Speed": "Speed (km/h)",

    "Throttle": "Throttle (%)",

    "Brake": "Brake",

    "RPM": "RPM",

    "nGear": "Gear",

    "DRS": "DRS"

}


# ==========================================================
# Statistics
# ==========================================================

def statistics(dataframe, metric):

    series = dataframe[metric].dropna()

    if series.empty:
        return None

    return {

        "Maximum": float(series.max()),

        "Average": float(series.mean()),

        "Minimum": float(series.min())

    }


# ==========================================================
# Dashboard
# ==========================================================

def render(
    telemetry_dictionary,
    driver_data
):
    """
    Render telemetry dashboard.
    """

    st.header("Telemetry Analysis")

    available_drivers = [
        driver
        for driver, telemetry in telemetry_dictionary.items()
        if telemetry.get("merged") is not None
        and not telemetry["merged"].empty
    ]

    if not available_drivers:

        st.warning(
            "Telemetry unavailable."
        )

        return

    metrics = [

        "Speed",

        "Throttle",

        "Brake",

        "RPM",

        "nGear",

        "DRS"

    ]

    selected_drivers = st.multiselect(

        "Drivers",

        available_drivers,

        default=available_drivers,

        key="telemetry_drivers"

    )

    if len(selected_drivers) == 0:

        st.info(
            "Select at least one driver."
        )

        return

    metrics = [
        metric
        for metric in metrics
        if any(
            metric in telemetry_dictionary[driver]["merged"].columns
            and telemetry_dictionary[driver]["merged"][metric].notna().any()
            for driver in selected_drivers
        )
    ]

    if not metrics:
        st.warning("No telemetry channels are available for the selected drivers.")
        return

    metric = st.selectbox(

        "Telemetry Metric",

        metrics,

        key="telemetry_metric"

    )

    fig = go.Figure()

    for driver in selected_drivers:

        telemetry = telemetry_dictionary[driver]["merged"]

        if metric not in telemetry.columns:
            continue

        fig.add_trace(

            go.Scatter(

                x=telemetry["Distance"],

                y=telemetry[metric],

                mode="lines",

                name=driver,

                line=dict(

                    color=driver_data[driver]["color"],

                    width=3

                )

            )

        )

    fig.update_layout(

        title=f"{metric} Comparison",

        xaxis_title="Distance (m)",

        yaxis_title=AXIS_LABELS.get(

            metric,

            metric

        ),


        **get_plotly_layout(),

        

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.subheader("Statistics")

    columns = st.columns(

        len(selected_drivers)

    )

    for column, driver in zip(

        columns,

        selected_drivers

    ):

        telemetry = telemetry_dictionary[driver]["merged"]

        stats = statistics(

            telemetry,

            metric

        )

        if stats is None:
            continue

        with column:

            st.metric(

                driver,

                f"{stats['Average']:.2f}"

            )

            st.caption(

                f"Max : {stats['Maximum']:.2f}"

            )

            st.caption(

                f"Min : {stats['Minimum']:.2f}"

            )

    st.download_button(

        label="Download Telemetry CSV",

        data=pd.concat(

            [

                telemetry_dictionary[d]["merged"]

                for d in selected_drivers

            ]

        ).to_csv(index=False),

        file_name="telemetry.csv",

        mime="text/csv"

    )
