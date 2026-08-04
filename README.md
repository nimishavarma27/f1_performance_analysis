# F1 Performance Analytics Dashboard

An interactive Formula 1 analysis dashboard built with Python, Streamlit, FastF1, Pandas, and Plotly. Select a completed Formula 1 session, choose one or more drivers, and explore lap times, sector performance, tyres, strategy, weather, telemetry, track position, and pace from official timing data exposed by FastF1.

> This is an educational and portfolio project. It is not affiliated with Formula 1, FIA, or any Formula 1 team.

## Contents

- [What the dashboard does](#what-the-dashboard-does)
- [How it works](#how-it-works)
- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Folder and file reference](#folder-and-file-reference)
- [Current implementation status](#current-implementation-status)
- [Development roadmap](#development-roadmap)
- [Data, caching, and limitations](#data-caching-and-limitations)
- [Technology stack](#technology-stack)
- [Contributing](#contributing)

## What the dashboard does

The current application lets a user:

- Select a season, a completed Grand Prix, and an available session: FP1, FP2, FP3, Sprint Qualifying, Sprint, Qualifying, or Race.
- Select one or more drivers from that session.
- See weekend and session context, including circuit information and the session fastest-lap ranking.
- Review session air and track temperatures, humidity, rainfall detection, wind speed, and a temperature trend chart.
- Compare selected drivers' fastest laps, sectors, lap-time traces, tyres, race pace, stints, pit-stop changes, speed traps, and telemetry.
- View a track map derived from FastF1 position telemetry.
- Keep ordinary session loads fast by enabling detailed telemetry only when track-map and telemetry analysis is needed.
- Switch between Dark, Light, Ferrari, Mercedes, and Aston Martin dashboard themes.
- Download the displayed telemetry for the selected drivers as a CSV file.

The dashboard uses FastF1's timing, car, and position telemetry data. Availability varies by season and session; when a channel is unavailable, the app displays a clear unavailable-data message rather than failing.

## How it works

```text
Choose season / Grand Prix / session
                |
                v
FastF1 downloads or reads its local cache
                |
                v
Build per-driver lap, sector, tyre, and weather datasets
                |
                +--> Overview, weather, and fastest-lap ranking
                +--> Driver statistics and charts
                +--> Comparison, pace, strategy, and pit analysis
                +--> Optional fastest-lap telemetry and position data
                              |
                              v
                    Telemetry, track map, mini sectors,
                    corner metrics, and speed traps
```

`app.py` is the Streamlit entry point. It coordinates the workflow, while `loaders/` fetches sessions, `processing/` turns raw FastF1 data into analysis-ready tables, `visualization/` renders Plotly charts and Streamlit components, and `views/` groups sections of the page.

## Getting started

### Prerequisites

- Python 3.10 or later
- Internet access the first time a session is loaded
- Git (optional, for cloning the project)

### Installation

```bash
git clone <your-repository-url>
cd f1_performance_analysis
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in a browser, choose a session in the sidebar, and select one or more drivers.

### First-load behaviour

The first load of a session can take time because FastF1 must retrieve timing and weather data. The default load intentionally skips large car and position telemetry downloads, so lap, tyre, pace, strategy, and weather analysis are available sooner. Enable **Load detailed telemetry** in the sidebar when you need telemetry traces, track maps, corner analysis, mini sectors, or speed traps. The project stores downloaded data in `data/cache/`; subsequent loads of the same session are usually much faster.

## Project structure

```text
f1_performance_analysis/
├── app.py                         # Streamlit application entry point
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── assets/
│   └── styles.css                 # Global Streamlit CSS overrides
├── data/
│   └── cache/                     # Generated FastF1 cache; do not commit
├── loaders/
│   └── session_loader.py          # Cached FastF1 session loading
├── models/
│   └── weekend.py                 # Reserved weekend-domain model module
├── processing/                    # Raw FastF1 data -> analysis datasets
├── services/
│   └── dashboard_service.py       # Reserved application-service layer
├── utils/                         # Shared configuration and helpers
├── views/                         # Page-level Streamlit sections
└── visualization/                 # Plotly charts and Streamlit display helpers
```

## Folder and file reference

This section documents every tracked source file. Empty/reserved modules are identified explicitly so contributors know they are planned extension points, not missing files.

### Root files

| File | Responsibility |
| --- | --- |
| `app.py` | Main Streamlit script. Configures the page and theme; loads the event schedule and selected session; builds the selected drivers' data; then renders dashboard, driver, comparison, telemetry, track-map, tyre, pace, and pit-stop sections. |
| `requirements.txt` | Declares the runtime packages: Streamlit, FastF1, Pandas, Plotly, Matplotlib, and NumPy. |
| `README.md` | This GitHub-facing project guide. |

### `assets/`

| File | Responsibility |
| --- | --- |
| `assets/styles.css` | Global CSS injected into Streamlit by `utils/ui.py`. It adjusts page spacing, headings, sidebar, metric cards, charts, tables, controls, scrollbars, and the Streamlit header/footer. |

### `data/`

| Path | Responsibility |
| --- | --- |
| `data/cache/` | Automatically created FastF1 cache containing downloaded schedules, timing, car telemetry, position data, weather, and session metadata. It is runtime data, not source code, and should normally be excluded from Git. |

### `loaders/`

| File | Responsibility |
| --- | --- |
| `loaders/session_loader.py` | Defines the project-relative FastF1 cache directory and `load_session()`. It loads and verifies a fresh mutable session, requesting lightweight lap/weather data by default and detailed telemetry only when requested. |

### `models/`

| File | Responsibility |
| --- | --- |
| `models/weekend.py` | Reserved for future typed models representing an event weekend, sessions, results, and summary data. It currently contains no production implementation. |

### `processing/`

These modules are responsible for data preparation and calculation. They should not render Streamlit UI directly.

| File | Responsibility |
| --- | --- |
| `processing/corner_analysis.py` | Reads one driver's merged telemetry and returns braking samples, full-throttle samples, and the distance/speed of the maximum and minimum speed points. |
| `processing/delta_analysis.py` | Calculates distance-aligned cumulative lap-time delta between two fastest-lap telemetry traces, with summary statistics. It is ready for a future delta-time dashboard panel. |
| `processing/driver_comparison.py` | Normalises two drivers' valid lap tables into comparable DataFrames containing lap number, lap time in seconds, compound, stint, and tyre life. |
| `processing/driver_lap_comparison.py` | Builds a two-driver fastest-lap summary: lap time, sector times, tyre compound, and speed-trap value. |
| `processing/driver_statistics.py` | Calculates per-driver fastest, average, and median lap time, consistency, completed laps, and tyre/stint information. It also formats timedeltas for display. |
| `processing/fastest_lap.py` | Produces the fastest valid lap for every driver in the loaded session and sorts the result into a ranking table. |
| `processing/lap_analysis.py` | Converts valid driver laps into a compact lap-time DataFrame for plotting, preserving lap number, compound, tyre life, and stint. |
| `processing/mini_sector_analysis.py` | Divides the common lap distance into configurable mini sectors (25 by default) and identifies the driver with the highest average speed in each segment. |
| `processing/pace_analysis.py` | Calculates fastest, average, median, and standard-deviation lap pace plus completed-lap count for each selected driver. |
| `processing/pit_stop_analysis.py` | Detects changes in FastF1 stint number and reports the lap, new compound, and new stint as pit-stop/strategy events. |
| `processing/sector_analysis.py` | Extracts the three sector times from a driver's fastest lap and converts them to seconds for charting. |
| `processing/session_analyzer.py` | Reserved for a future high-level session-analysis service. It currently contains no production implementation. |
| `processing/speed_trap_analysis.py` | Finds each driver's maximum telemetry speed and the distance at which it occurs, then ranks the drivers by top speed. |
| `processing/telemetry_analysis.py` | Provides reusable telemetry preparation, available-channel discovery, and per-channel statistics for Speed, Throttle, Brake, RPM, Gear, and DRS. It is available for more specialised telemetry views. |
| `processing/telemetry_engine.py` | Retrieves car and position data from each driver's fastest lap, adds travelled distance, aligns the time series, and stores merged telemetry with driver/team/colour metadata. |
| `processing/track_map.py` | Validates and cleans merged position telemetry for plotting a driver's racing line, retaining X/Y coordinates and available driving channels. |
| `processing/tyre_analysis.py` | Converts valid laps into a tyre-performance DataFrame containing lap time, compound, tyre life, stint, and fresh-tyre status. |
| `processing/tyre_stint_analysis.py` | Groups a driver's laps by stint and returns compound, start/end lap, and stint length for strategy tables and timelines. |
| `processing/weather_analysis.py` | Cleans FastF1 weather samples, normalises numeric weather channels, and calculates temperature, humidity, wind, rainfall, and range summaries. |
| `processing/weekend_summary.py` | Optionally loads the sessions in a race weekend in parallel, derives circuit information, session leaders, and top-three tables, and caches the resulting weekend summary. |

### `services/`

| File | Responsibility |
| --- | --- |
| `services/dashboard_service.py` | Reserved for future orchestration/business logic that sits between views and processing modules. It currently contains no production implementation. |

### `utils/`

| File | Responsibility |
| --- | --- |
| `utils/constants_codes.py` | Defines the FastF1 session codes and their preferred display order. |
| `utils/logger.py` | Configures the shared application logger and exposes `logger` for safe-load warnings and diagnostics. |
| `utils/session_names.py` | Maps FastF1 session codes to human-readable names and the result label used in weekend summaries. |
| `utils/session_utils.py` | Safely loads an individual FastF1 session for weekend summaries; it logs a warning and returns `None` rather than stopping the whole summary when a session is unavailable. |
| `utils/team_colors.py` | Maps Formula 1 team names to chart colours and provides a neutral fallback when a team is not recognised. |
| `utils/theme.py` | Defines the Dark, Light, Ferrari, Mercedes, and Aston Martin palettes and returns Plotly layout values that match the active dashboard theme. |
| `utils/ui.py` | Loads the global CSS, creates the sidebar theme selector, stores the chosen theme in Streamlit session state, and exposes the active Plotly layout. |
| `utils/validators.py` | Reserved for shared input and data validation rules. It currently contains no production implementation. |

### `views/`

| File | Responsibility |
| --- | --- |
| `views/dashboard.py` | Renders the Weekend Overview section: optional multi-session weekend information, event/session metadata, and the session fastest-lap table. |
| `views/driver.py` | Renders the Driver Analysis section: summary statistic cards, fastest-lap sector charts, lap-time charts, and tyre-performance charts for every selected driver. |

### `visualization/`

These modules convert processed data into Plotly figures or Streamlit tables, cards, and messages.

| File | Responsibility |
| --- | --- |
| `visualization/comparison_charts.py` | Creates a Plotly multi-driver lap-time comparison chart. |
| `visualization/corner_analysis_cards.py` | Displays maximum/minimum speed, braking samples, and full-throttle samples from corner analysis. |
| `visualization/dashboard_overview.py` | Displays event and loaded-session metadata in the dashboard overview. |
| `visualization/delta_chart.py` | Reserved for the forthcoming interactive delta-time chart. It currently contains no production implementation. |
| `visualization/driver_lap_comparison_chart.py` | Displays a side-by-side two-driver fastest-lap comparison card. |
| `visualization/driver_statistics_cards.py` | Displays the per-driver summary metrics calculated by `driver_statistics.py`. |
| `visualization/fastest_lap_table.py` | Displays the session-wide fastest-lap ranking as a formatted Streamlit table. |
| `visualization/lap_charts.py` | Creates a Plotly lap-time trace for one driver, including tyre-related hover information. |
| `visualization/mini_sector_table.py` | Displays the mini-sector fastest-driver analysis table and handles unavailable data. |
| `visualization/pace_table.py` | Displays the pace and consistency DataFrame. |
| `visualization/pit_stop_table.py` | Displays detected stint changes/pit-stop events and handles sessions without pit stops. |
| `visualization/sector_charts.py` | Creates a three-bar Plotly sector-time chart for a driver's fastest lap. |
| `visualization/speed_trap_table.py` | Displays the ranked speed-trap table. |
| `visualization/strategy_timeline.py` | Creates a horizontal tyre-stint timeline coloured by tyre compound. |
| `visualization/telemetry_charts.py` | Creates a reusable multi-driver telemetry chart for a selected metric. |
| `visualization/telemetry_dashboard.py` | Renders the interactive telemetry section: driver/channel selection, distance-based chart, summary metrics, and CSV download. It tolerates partial or unavailable telemetry. |
| `visualization/telemetry_statistics.py` | Displays per-driver average, maximum, and minimum values for a telemetry metric. |
| `visualization/track_map_chart.py` | Creates the Plotly racing-line map from X/Y position coordinates. |
| `visualization/tyre_charts.py` | Creates a tyre-performance Plotly chart using lap time, compound, tyre life, and stint information. |
| `visualization/tyre_stint_table.py` | Displays the tyre-stint DataFrame and handles missing/empty stint data. |
| `visualization/weather_dashboard.py` | Displays session weather metric cards and a theme-aware air/track temperature trend chart. |
| `visualization/weekend_information.py` | Renders the optional weekend circuit, leader, and top-three summary returned by `weekend_summary.py`. |

### Generated folders

| Path | Responsibility |
| --- | --- |
| `**/__pycache__/` | Python bytecode generated automatically when modules are imported. It should not be committed. |

## Current implementation status

### Implemented and connected to the dashboard

- Session selection and FastF1 loading
- Local FastF1 cache, validated session loading, and an optional detailed-telemetry mode for faster default loads
- Multi-driver selection
- Weekend overview, weather conditions, and fastest-lap ranking
- Driver statistics
- Sector, lap-time, tyre, and multi-driver comparison charts
- Telemetry charting, telemetry CSV export, track map, corner metrics, mini sectors, and speed traps when detailed telemetry is enabled
- Tyre stints, strategy timeline, pace, and stint-change/pit-stop analysis
- Dark, Light, Ferrari, Mercedes, and Aston Martin theme selector with matching global styling and Plotly charts
- Graceful empty-data handling in telemetry and analysis tables

### Implemented modules awaiting interface integration

- Distance-based fastest-lap delta analysis (`processing/delta_analysis.py`)
- Dedicated two-driver fastest-lap comparison panel (`processing/driver_lap_comparison.py` and `visualization/driver_lap_comparison_chart.py`)
- Reusable prepared-telemetry/chart pipeline (`processing/telemetry_analysis.py` and `visualization/telemetry_charts.py`)

### Planned module work

- Domain models in `models/weekend.py`
- Shared dashboard service in `services/dashboard_service.py`
- Reusable validation helpers in `utils/validators.py`
- Session-analysis orchestration in `processing/session_analyzer.py`
- Delta-time chart rendering in `visualization/delta_chart.py`

## Development roadmap

The roadmap is organised in phases so users and contributors can see what is already available and what comes next.

### Phase 1 — Foundation and core analysis (complete)

- Streamlit application shell and sidebar-driven session selection
- FastF1 data loading and persistent local cache
- Lightweight default loading for laps and weather, with detailed telemetry loaded on demand
- Driver lap, sector, tyre, and fastest-lap analysis
- Basic multi-driver comparison and Plotly visualisation
- Team colours and theme support

### Phase 2 — Advanced session insights (complete)

- Weekend overview and session rankings
- Driver statistics and pace consistency
- Tyre stints, strategy timeline, and stint-change detection
- Session weather conditions and temperature trends
- Fastest-lap telemetry, speed trap, mini-sector, corner, and track-map analysis on demand
- Telemetry download and resilience when telemetry channels are unavailable

### Phase 3 — Comparison experience and dashboard polish

- Add a visible two-driver fastest-lap comparison control and panel.
- Add the distance-based delta-time chart, including who gains/loses time through each part of the lap.
- Group related dashboard outputs into tabs or expanders to make large multi-driver pages easier to scan.
- Extend the theme system with additional team and accessibility palettes as the dashboard grows.
- Add formatted time values, units, explanatory tooltips, and better mobile responsiveness.
- Improve event/session availability checks and error messages for incomplete or recently published sessions.
- Add weather-aware lap filtering and correlate pace changes with temperature, rainfall, and wind.

### Phase 4 — Data quality, architecture, and testing

- Introduce typed weekend/session models and a dashboard service layer.
- Move repeated validation and transformation logic into shared utilities.
- Add automated unit tests for every processor using cached or fixture FastF1 data.
- Add integration tests for the Streamlit user flow.
- Add linting, formatting, type checking, and a GitHub Actions workflow.
- Add a `.gitignore` policy for virtual environments, FastF1 cache files, and Python bytecode.

### Phase 5 — Deeper performance analysis

- Compare braking points, throttle application, gears, RPM, and DRS usage between drivers.
- Add track-map colour modes for speed, throttle, brake, gear, and delta time.
- Detect corner entry, apex, and exit markers from circuit/telemetry data.
- Filter lap data by tyre compound, stint, safety-car period, track status, and weather conditions.
- Add qualifying segment analysis and race-lap filtering to exclude pit in/out laps and disrupted laps.

### Phase 6 — Product and sharing features

- Save and share analysis configurations through URL parameters or saved reports.
- Export tables and figures as CSV, PNG, and PDF reports.
- Add a season-comparison workspace for drivers, teams, circuits, and race-to-race trends.
- Publish a hosted version with setup documentation, issue templates, and contributor guidelines.

## Data, caching, and limitations

- FastF1 is the data-access library used by this project. Session coverage and telemetry completeness depend on the underlying data sources.
- Recent or historical sessions can load slowly on first use. The cache makes later loads faster.
- The cache can become large. Do not commit `data/cache/` to GitHub.
- Weather samples are periodic observations, not a continuous measurement at every point on track. The dashboard reports the samples supplied by FastF1 for the selected session.
- A session may contain laps without valid lap times, tyre information, car data, or position data. The processing modules intentionally skip invalid samples where possible.
- The pit-stop table detects stint changes; it is a strategy-event approximation and is not a direct official pit-lane-duration measurement.
- The mini-sector view currently uses average speed within equal-distance segments as a practical fastest-driver indicator. It is not yet a time-delta mini-sector calculation.

## Technology stack

| Technology | Use in this project |
| --- | --- |
| [Python](https://www.python.org/) | Application and analysis language. |
| [Streamlit](https://streamlit.io/) | Interactive web dashboard framework. |
| [FastF1](https://docs.fastf1.dev/) | Formula 1 timing, event, car, position, and telemetry data access. |
| [Pandas](https://pandas.pydata.org/) | Data cleaning, grouping, and tabular analysis. |
| [NumPy](https://numpy.org/) | Numeric calculations and mini-sector boundaries. |
| [Plotly](https://plotly.com/python/) | Interactive charts, telemetry traces, and track maps. |
| [Matplotlib](https://matplotlib.org/) | Available for future static analysis/exports. |

## Contributing

Contributions are welcome. A good workflow is:

1. Create a branch for one focused change.
2. Keep calculation logic in `processing/` and presentation logic in `visualization/` or `views/`.
3. Test the change with a cached session and with missing-data paths where relevant.
4. Update this README when you add a feature, module, dependency, or roadmap item.
5. Open a pull request that describes the user-facing change and includes screenshots for UI work.

## Acknowledgements

- [FastF1](https://github.com/theOehrly/Fast-F1) for the Formula 1 data-access library.
- Formula 1 and FIA for the sport and timing ecosystem that make this analysis possible.
- Streamlit, Pandas, NumPy, Plotly, and Matplotlib for the open-source tools used by the project.

## License

