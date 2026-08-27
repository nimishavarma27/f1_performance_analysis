"""UI utilities for the F1 Performance Analytics Dashboard."""

from pathlib import Path

import streamlit as st

from utils.theme import (
    get_available_themes,
    get_theme,
    plotly_layout,
)


ROOT_DIR = Path(__file__).resolve().parent.parent
CSS_FILE = ROOT_DIR / "assets" / "styles.css"


def _theme_css(theme: dict) -> str:
    """Palette-specific CSS variables injected into Streamlit's shell."""

    return f"""
    <style>
    :root {{
        --f1-background: {theme['background']};
        --f1-secondary-background: {theme['secondary_background']};
        --f1-card-background: {theme['card_background']};
        --f1-text: {theme['text']};
        --f1-muted-text: {theme['muted_text']};
        --f1-accent: {theme['accent']};
        --f1-accent-secondary: {theme['accent_secondary']};
        --f1-accent-contrast: {theme['accent_contrast']};
        --f1-grid: {theme['grid']};
        --f1-border: {theme['border']};
    }}

    html, body, .stApp,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"] {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background-color: {theme['secondary_background']} !important;
    }}

    [data-testid="stHeader"],
    [data-testid="stToolbar"] {{
        background-color: {theme['background']} !important;
    }}

    div[data-testid="metric-container"],
    [data-testid="stDataFrame"],
    [data-testid="stPlotlyChart"] {{
        background-color: {theme['card_background']} !important;
        border-color: {theme['border']} !important;
    }}

    [data-testid="stAppViewContainer"] *,
    [data-testid="stSidebar"] * {{
        border-color: {theme['border']};
    }}
    </style>
    """


@st.cache_data(show_spinner=False)
def _read_css_file(path_str: str, mtime: float) -> str:
    """Cached CSS file read, keyed on mtime."""

    with open(path_str, "r", encoding="utf-8") as file:
        return file.read()


def load_css(theme: dict):
    """Load the global stylesheet."""

    if CSS_FILE.exists():
        css = _read_css_file(str(CSS_FILE), CSS_FILE.stat().st_mtime)
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    st.markdown(_theme_css(theme), unsafe_allow_html=True)


def initialize_theme():
    """Initialise the dashboard theme state."""

    if "dashboard_theme" not in st.session_state:
        st.session_state.dashboard_theme = "Dark"

    if st.session_state.dashboard_theme not in get_available_themes():
        st.session_state.dashboard_theme = "Dark"

    if "theme_selector" not in st.session_state:
        st.session_state.theme_selector = st.session_state.dashboard_theme


def theme_selector():
    """Sidebar theme selector."""

    initialize_theme()

    st.sidebar.divider()
    st.sidebar.subheader("Appearance")

    selected_theme = st.sidebar.selectbox(
        "Theme",
        options=get_available_themes(),
        key="theme_selector",
    )

    st.session_state.dashboard_theme = selected_theme
    st.sidebar.caption(f"Active palette: {selected_theme}")

    return get_theme(selected_theme)


def get_current_theme():
    """Return the current active theme."""

    initialize_theme()
    return get_theme(st.session_state.dashboard_theme)


def get_plotly_layout():
    """Plotly layout for the currently selected theme."""

    return plotly_layout(get_current_theme())


def initialize_ui():
    """Initialise the complete dashboard UI. Call once from app.py."""

    theme = theme_selector()
    load_css(theme)
    return theme
