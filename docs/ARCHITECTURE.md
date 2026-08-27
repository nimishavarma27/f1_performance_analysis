# Architecture

This document explains the internal layout of the F1 Performance Analytics Dashboard for anyone who wants to modify it or add features. For a user-facing overview see the top-level [README](../README.md).

## Layering

The dashboard is organised in four layers, each depending only on the layer below it:

```
app.py                              entry point / tab wiring
   |
   v
views/                              one module per tab
   |
   v
processing/  +  visualization/      calculation and rendering leaf modules
   |
   v
loaders/  +  utils/                 shared infrastructure
```

- `app.py` never imports from `processing/` or `visualization/` directly. It orchestrates: session picker, driver picker, and the four `views/` tabs.
- Each `views/` module imports only what its tab needs.
- `processing/` transforms raw FastF1 data into analysis-ready DataFrames. It never touches Streamlit.
- `visualization/` renders Plotly figures or Streamlit tables/cards. It never talks to FastF1.
- `loaders/` and `utils/` are pure helpers.

## Caching model

The dashboard's snappiness comes from three cache layers stacked on top of FastF1:

| Layer | Where | Keyed on | Lifetime |
| --- | --- | --- | --- |
| FastF1 on-disk cache | `data/cache/` | request URL | across sessions, forever |
| Session cache | `loaders.session_loader.load_session` (`@st.cache_resource`) | `(year, gp, session_type, telemetry)` | Streamlit process |
| Driver data cache | `processing.driver_data.build_driver_data` (`@st.cache_resource`) | `(session_key, drivers)` | Streamlit process |
| Telemetry cache | `processing.telemetry_engine.build_for_driver` (`@st.cache_data`) | `(session_key, driver)` | Streamlit process |

Consequence: switching tabs, changing the theme, or moving the track-map / corner selectors never re-parses the session or rebuilds telemetry for a driver that was already computed.

## Root files

| File | Responsibility |
| --- | --- |
| `app.py` | Streamlit entry point. Configures the page and theme; loads the event schedule; picks the session, drivers, and telemetry mode; builds cached driver data; and mounts the four dashboard tabs (Overview, Driver, Comparison, Telemetry). |
| `requirements.txt` | Pinned runtime dependencies: Streamlit, FastF1, Pandas, Plotly, Matplotlib, and NumPy. |

## `assets/`

| File | Responsibility |
| --- | --- |
| `assets/styles.css` | Global CSS injected into Streamlit by `utils/ui.py`. Flat visual system: 1px borders, small radii, system font stack (Helvetica Neue / Helvetica / Arial), no gradients, no drop shadows, no hover transforms. |

## `data/`

| Path | Responsibility |
| --- | --- |
| `data/cache/` | Automatically created FastF1 cache containing downloaded schedules, timing, car telemetry, position data, weather, and session metadata. It is runtime data, not source code, and should be excluded from Git. |

## `loaders/`

| File | Responsibility |
| --- | --- |
| `loaders/session_loader.py` | Defines the project-relative FastF1 cache directory and three cached loaders: `load_session()` (a `@st.cache_resource`-cached FastF1 `Session`), `get_event_schedule()`, and `get_available_sessions()` (reads the FP/Q/S/R codes off the schedule columns instead of probing FastF1 seven times per rerun). |

## `models/`

| File | Responsibility |
| --- | --- |
| `models/weekend.py` | Reserved for future typed models representing an event weekend, sessions, results, and summary data. Currently contains no production implementation. |

## `processing/`

Data preparation and calculation. These modules do not render Streamlit UI directly.

| File | Responsibility |
| --- | --- |
| `processing/corner_analysis.py` | Reads one driver's merged telemetry and returns braking samples, full-throttle samples, and the distance/speed of the max/min speed points. Handles both bool and numeric `Brake` columns safely. |
| `processing/delta_analysis.py` | Calculates distance-aligned cumulative lap-time delta between two fastest-lap telemetry traces. Ready for a future delta-time panel. |
| `processing/driver_comparison.py` | Normalises two drivers' valid lap tables into comparable DataFrames. Reserved for a future two-driver head-to-head panel; not currently wired in. |
| `processing/driver_data.py` | `build_driver_data()`: the cached (`@st.cache_resource`) builder that turns a session + selected drivers into the `driver_data` mapping (laps, fastest lap, sector/lap/tyre dataframes, team colour) consumed everywhere else. |
| `processing/driver_lap_comparison.py` | Builds a two-driver fastest-lap summary. Reserved (see above). |
| `processing/driver_statistics.py` | Calculates per-driver fastest, average, and median lap time, consistency, completed laps, and tyre/stint information. |
| `processing/fastest_lap.py` | Produces the fastest valid lap for every driver in the loaded session and sorts the result into a ranking table. |
| `processing/lap_analysis.py` | Converts valid driver laps into a compact lap-time DataFrame for plotting. |
| `processing/mini_sector_analysis.py` | Divides the common lap distance into configurable mini sectors (25 by default) and identifies the driver with the highest average speed in each segment. Vectorised: one `pd.cut` + `groupby` per driver. |
| `processing/pace_analysis.py` | Fastest, average, median, and standard-deviation lap pace plus completed-lap count for each selected driver. |
| `processing/pit_stop_analysis.py` | Vectorised stint-change detection that reports each pit-stop lap, the new compound, and the new stint. |
| `processing/sector_analysis.py` | Extracts the three sector times from a driver's fastest lap and converts them to seconds. |
| `processing/session_analyzer.py` | Reserved for a future high-level session-analysis service. Currently contains no production implementation. |
| `processing/speed_trap_analysis.py` | Finds each driver's maximum telemetry speed and the distance at which it occurs, then ranks the drivers by top speed. |
| `processing/telemetry_analysis.py` | Reusable telemetry preparation, available-channel discovery, and per-channel statistics for Speed, Throttle, Brake, RPM, Gear, and DRS. |
| `processing/telemetry_engine.py` | Retrieves car and position data for each driver's fastest lap, adds travelled distance, aligns the two time series with `merge_asof`, and stores merged telemetry with driver/team/colour metadata. Exposes `build_for_driver()` which is cached per `(session_key, driver)`. |
| `processing/track_map.py` | Validates and cleans merged position telemetry for plotting a driver's racing line. |
| `processing/tyre_analysis.py` | Converts valid laps into a tyre-performance DataFrame. |
| `processing/tyre_stint_analysis.py` | Groups a driver's laps by stint and returns compound, start/end lap, and stint length. |
| `processing/weather_analysis.py` | Cleans FastF1 weather samples and calculates temperature, humidity, wind, rainfall, and range summaries. |
| `processing/weekend_summary.py` | Optionally loads the sessions in a race weekend in parallel and derives circuit information, session leaders, and top-three tables. Cached. |

## `services/`

| File | Responsibility |
| --- | --- |
| `services/dashboard_service.py` | Reserved for future orchestration/business logic that sits between views and processing modules. Currently contains no production implementation. |

## `utils/`

| File | Responsibility |
| --- | --- |
| `utils/constants_codes.py` | FastF1 session codes and their preferred display order. |
| `utils/logger.py` | Shared application logger. |
| `utils/session_names.py` | Maps FastF1 session codes to human-readable names and result labels. |
| `utils/session_utils.py` | Safely loads an individual FastF1 session for weekend summaries. |
| `utils/team_colors.py` | Maps Formula 1 team names to chart colours with a neutral fallback. |
| `utils/theme.py` | Defines the Dark, Light, Ferrari, Mercedes, Aston Martin, and Pink palettes and returns Plotly layout values matching the active theme. |
| `utils/ui.py` | Loads the global CSS (file read is cached and keyed on mtime), injects theme CSS variables, creates the sidebar theme selector, exposes the active Plotly layout. |
| `utils/validators.py` | Reserved for shared input and data validation rules. Currently contains no production implementation. |

## `views/`

| File | Responsibility |
| --- | --- |
| `views/dashboard.py` | **Weekend Overview** tab: optional multi-session weekend information, event/session metadata, session weather, and the session fastest-lap table. |
| `views/driver.py` | **Driver Analysis** tab: summary statistic cards, fastest-lap sector charts, lap-time charts, and tyre-performance charts for every selected driver. |
| `views/comparison.py` | **Comparison and Strategy** tab: multi-driver comparison chart, pace analysis, tyre stints, strategy timeline, and pit stops. |
| `views/telemetry.py` | **Telemetry and Track** tab: telemetry dashboard, track map, corner analysis, mini sectors, and speed traps. Builds telemetry lazily via the cached per-driver builder. |

## `visualization/`

Converts processed data into Plotly figures or Streamlit tables, cards, and messages.

| File | Responsibility |
| --- | --- |
| `visualization/comparison_charts.py` | Plotly multi-driver lap-time comparison chart (works for N drivers). |
| `visualization/corner_analysis_cards.py` | Max/min speed, braking, and full-throttle samples from corner analysis. |
| `visualization/dashboard_overview.py` | Event and loaded-session metadata. |
| `visualization/delta_chart.py` | Reserved for the forthcoming interactive delta-time chart. |
| `visualization/driver_lap_comparison_chart.py` | Reserved side-by-side two-driver fastest-lap comparison card. |
| `visualization/driver_statistics_cards.py` | Per-driver summary metrics. |
| `visualization/fastest_lap_table.py` | Session-wide fastest-lap ranking as a formatted table. |
| `visualization/lap_charts.py` | Plotly lap-time trace for one driver. |
| `visualization/mini_sector_table.py` | Mini-sector fastest-driver analysis table. |
| `visualization/pace_table.py` | Pace and consistency DataFrame. |
| `visualization/pit_stop_table.py` | Detected stint changes / pit-stop events. |
| `visualization/sector_charts.py` | Three-bar sector-time chart for a driver's fastest lap. |
| `visualization/speed_trap_table.py` | Ranked speed-trap table. |
| `visualization/strategy_timeline.py` | Horizontal tyre-stint timeline coloured by tyre compound. |
| `visualization/telemetry_charts.py` | Reusable multi-driver telemetry chart. |
| `visualization/telemetry_dashboard.py` | Driver/channel selection, distance-based chart, summary metrics, CSV download. |
| `visualization/telemetry_statistics.py` | Per-driver average/max/min for a telemetry metric. |
| `visualization/track_map_chart.py` | Plotly racing-line map from X/Y position coordinates. |
| `visualization/tyre_charts.py` | Tyre-performance Plotly chart. |
| `visualization/tyre_stint_table.py` | Tyre-stint DataFrame with missing/empty-data handling. |
| `visualization/weather_dashboard.py` | Session weather metric cards and a theme-aware air/track temperature trend chart. |
| `visualization/weekend_information.py` | Optional weekend circuit, leader, and top-three summary. |

## Reserved / awaiting integration

Modules that exist as scaffolding for planned features. Nothing in the current dashboard imports them.

- `processing/delta_analysis.py` and `visualization/delta_chart.py` — distance-based delta-time chart.
- `processing/driver_comparison.py`, `processing/driver_lap_comparison.py`, `visualization/driver_lap_comparison_chart.py` — dedicated two-driver head-to-head panel.
- `processing/telemetry_analysis.py` and `visualization/telemetry_charts.py` — reusable prepared-telemetry pipeline.
- `models/weekend.py`, `services/dashboard_service.py`, `utils/validators.py`, `processing/session_analyzer.py` — future model/service/validation layers.

## Adding a new tab

1. Create `views/<tab>.py` exposing `render_<tab>(driver_data, ...)`.
2. Import any `processing/` modules for calculation and any `visualization/` modules for rendering. Don't put calculation in the view.
3. In `app.py`, add the tab to the `st.tabs([...])` list and call your `render_<tab>` inside its `with` block.

## Adding a new theme

Add a new entry to the `THEMES` dict in `utils/theme.py` with the ten required colour keys (`background`, `secondary_background`, `card_background`, `plot_background`, `paper_background`, `text`, `muted_text`, `accent`, `accent_secondary`, `accent_contrast`, `grid`, `border`, plus optional `success`/`warning`/`error`). It automatically appears in the sidebar theme selector.
