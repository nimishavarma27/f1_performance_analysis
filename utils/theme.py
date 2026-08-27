"""
Theme configuration for the F1 Performance Analytics Dashboard.

Each theme provides a consistent, restrained colour palette used by
Streamlit components, Plotly charts, and custom visualisations.
"""

from copy import deepcopy


THEMES = {
    "Dark": {
        "background": "#111111",
        "secondary_background": "#161616",
        "card_background": "#1B1B1B",
        "plot_background": "#161616",
        "paper_background": "#111111",
        "text": "#EDEDED",
        "muted_text": "#9A9A9A",
        "accent": "#C81E1E",
        "accent_secondary": "#E64A4A",
        "accent_contrast": "#FFFFFF",
        "grid": "#2A2A2A",
        "border": "#242424",
        "success": "#4CAF50",
        "warning": "#D4A017",
        "error": "#C1443E",
    },

    "Light": {
        "background": "#FAFAFA",
        "secondary_background": "#F2F2F2",
        "card_background": "#F5F5F5",
        "plot_background": "#F5F5F5",
        "paper_background": "#FAFAFA",
        "text": "#1A1A1A",
        "muted_text": "#5C5C5C",
        "accent": "#B01818",
        "accent_secondary": "#C93636",
        "accent_contrast": "#FFFFFF",
        "grid": "#DDDDDD",
        "border": "#D0D0D0",
        "success": "#3E8E41",
        "warning": "#B58A16",
        "error": "#B23A34",
    },

    "Ferrari": {
        "background": "#150808",
        "secondary_background": "#1C0B0C",
        "card_background": "#241012",
        "plot_background": "#1C0B0C",
        "paper_background": "#150808",
        "text": "#F4E9E9",
        "muted_text": "#B99A9E",
        "accent": "#B4001F",
        "accent_secondary": "#D6A21C",
        "accent_contrast": "#FFFFFF",
        "grid": "#3A1F23",
        "border": "#432529",
        "success": "#4CAF50",
        "warning": "#D4A017",
        "error": "#C1443E",
    },

    "Mercedes": {
        "background": "#0C1615",
        "secondary_background": "#122120",
        "card_background": "#172B29",
        "plot_background": "#122120",
        "paper_background": "#0C1615",
        "text": "#E7F2F0",
        "muted_text": "#98B0AC",
        "accent": "#1FB39A",
        "accent_secondary": "#B7C0C2",
        "accent_contrast": "#0C1615",
        "grid": "#213B37",
        "border": "#274641",
        "success": "#4CAF50",
        "warning": "#D4A017",
        "error": "#C1443E",
    },

    "Aston Martin": {
        "background": "#0A1614",
        "secondary_background": "#0F211D",
        "card_background": "#14312A",
        "plot_background": "#0F211D",
        "paper_background": "#0A1614",
        "text": "#E5F0EC",
        "muted_text": "#9CB6AD",
        "accent": "#1F7A5B",
        "accent_secondary": "#9DBF3E",
        "accent_contrast": "#FFFFFF",
        "grid": "#1E4740",
        "border": "#25554C",
        "success": "#4CAF50",
        "warning": "#D4A017",
        "error": "#C1443E",
    },

    "Pink": {
        "background": "#F2D9E3",
        "secondary_background": "#E8C4D1",
        "card_background": "#EACAD5",
        "plot_background": "#E0B8C7",
        "paper_background": "#E0B8C7",
        "text": "#2A0A18",
        "muted_text": "#6E3A52",
        "accent": "#AD1457",
        "accent_secondary": "#6A1338",
        "accent_contrast": "#FFFFFF",
        "grid": "#C99AAF",
        "border": "#C99AAF",
        "success": "#3E8E41",
        "warning": "#B58A16",
        "error": "#B23A34",
    },
}


DEFAULT_THEME = "Dark"


def get_available_themes():
    """Return all available theme names."""

    return list(THEMES.keys())


def get_theme(theme_name: str = DEFAULT_THEME):
    """Return a copy of the requested theme.

    If the theme does not exist, the default theme is returned.
    """

    if theme_name not in THEMES:
        theme_name = DEFAULT_THEME

    return deepcopy(THEMES[theme_name])


def plotly_layout(theme: dict):
    """Return a standard Plotly layout for the selected theme."""

    return {
        "paper_bgcolor": theme["paper_background"],
        "plot_bgcolor": theme["plot_background"],
        "font": {
            "color": theme["text"],
            "family": "Helvetica, Arial, sans-serif",
        },
        "xaxis": {
            "gridcolor": theme["grid"],
            "zerolinecolor": theme["grid"],
        },
        "yaxis": {
            "gridcolor": theme["grid"],
            "zerolinecolor": theme["grid"],
        },
        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "orientation": "h",
            "x": 0,
            "y": 1.05,
        },
        "hoverlabel": {
            "bgcolor": theme["secondary_background"],
            "font": {"color": theme["text"]},
        },
        "hovermode": "x unified",
        "margin": {"l": 20, "r": 20, "t": 60, "b": 20},
    }
