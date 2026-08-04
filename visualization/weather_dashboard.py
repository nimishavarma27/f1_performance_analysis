"""Streamlit and Plotly weather presentation for a loaded session."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from processing.weather_analysis import get_weather_dataframe, get_weather_summary
from utils.ui import get_current_theme, get_plotly_layout


def _value(value: float | None, suffix: str) -> str:
    """Format an optional weather value for a metric card."""

    return f"{value:.1f}{suffix}" if value is not None else "—"


def render_weather_dashboard(session) -> None:
    """Render weather summary cards and a temperature trend chart."""

    st.subheader("Weather Conditions")

    weather = get_weather_dataframe(session)
    summary = get_weather_summary(weather)
    if summary is None:
        st.info("Weather data is unavailable for this session.")
        return

    air_min, air_max = summary["air_range"]
    track_min, track_max = summary["track_range"]
    columns = st.columns(4)
    columns[0].metric(
        "Air temperature",
        _value(summary["air_temperature"], " °C"),
        None if air_min is None else f"Range {air_min:.1f}–{air_max:.1f} °C",
    )
    columns[1].metric(
        "Track temperature",
        _value(summary["track_temperature"], " °C"),
        None if track_min is None else f"Range {track_min:.1f}–{track_max:.1f} °C",
    )
    columns[2].metric("Humidity", _value(summary["humidity"], "%"))
    columns[3].metric(
        "Conditions",
        "Rain detected" if summary["rain_detected"] else "Dry samples",
        _value(summary["wind_speed"], " km/h") + " average wind",
    )

    temperature_columns = [
        column for column in ("AirTemp", "TrackTemp") if column in weather
    ]
    if "Time" not in weather or not temperature_columns:
        return

    theme = get_current_theme()
    figure = go.Figure()
    colours = {"AirTemp": theme["accent_secondary"], "TrackTemp": theme["accent"]}
    labels = {"AirTemp": "Air temperature", "TrackTemp": "Track temperature"}

    for column in temperature_columns:
        figure.add_trace(
            go.Scatter(
                x=weather["Time"],
                y=weather[column],
                mode="lines+markers",
                name=labels[column],
                line=dict(color=colours[column], width=3),
                marker=dict(size=5),
                hovertemplate=f"{labels[column]}: %{{y:.1f}} °C<extra></extra>",
            )
        )

    figure.update_layout(
        title="Temperature Trend",
        xaxis_title="Session time",
        yaxis_title="Temperature (°C)",
        height=360,
    )

    st.plotly_chart(figure, use_container_width=True)
    return
