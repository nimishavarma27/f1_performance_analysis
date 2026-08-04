"""Prepare FastF1 weather samples for dashboard summaries and charts."""

from __future__ import annotations

import pandas as pd


WEATHER_COLUMNS = (
    "Time",
    "AirTemp",
    "TrackTemp",
    "Humidity",
    "Pressure",
    "Rainfall",
    "WindSpeed",
    "WindDirection",
)


def get_weather_dataframe(session) -> pd.DataFrame:
    """Return cleaned session weather samples, or an empty DataFrame.

    Weather is loaded with the lightweight session path, so this function does
    not require the substantially larger car and position telemetry downloads.
    """

    try:
        weather = session.weather_data.copy()
    except Exception:
        return pd.DataFrame(columns=WEATHER_COLUMNS)

    available_columns = [column for column in WEATHER_COLUMNS if column in weather]
    if not available_columns:
        return pd.DataFrame(columns=WEATHER_COLUMNS)

    weather = weather[available_columns].copy()
    if "Time" in weather:
        weather = weather.sort_values("Time").reset_index(drop=True)

    for column in ("AirTemp", "TrackTemp", "Humidity", "Pressure", "WindSpeed"):
        if column in weather:
            weather[column] = pd.to_numeric(weather[column], errors="coerce")

    if "Rainfall" in weather:
        weather["Rainfall"] = weather["Rainfall"].fillna(False).astype(bool)

    return weather


def get_weather_summary(weather: pd.DataFrame) -> dict | None:
    """Calculate concise weather metrics from cleaned weather samples."""

    if weather is None or weather.empty:
        return None

    def average(column: str) -> float | None:
        if column not in weather or weather[column].dropna().empty:
            return None
        return round(float(weather[column].mean()), 1)

    def minimum_maximum(column: str) -> tuple[float | None, float | None]:
        if column not in weather or weather[column].dropna().empty:
            return None, None
        values = weather[column]
        return round(float(values.min()), 1), round(float(values.max()), 1)

    air_min, air_max = minimum_maximum("AirTemp")
    track_min, track_max = minimum_maximum("TrackTemp")

    return {
        "samples": len(weather),
        "air_temperature": average("AirTemp"),
        "track_temperature": average("TrackTemp"),
        "humidity": average("Humidity"),
        "wind_speed": average("WindSpeed"),
        "rain_detected": bool(weather["Rainfall"].any()) if "Rainfall" in weather else False,
        "air_range": (air_min, air_max),
        "track_range": (track_min, track_max),
    }
