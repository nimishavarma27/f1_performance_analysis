"""
Theme configuration for the F1 Performance Analytics Dashboard.

Each theme provides a consistent color palette that can be used
throughout the application for Streamlit components, Plotly charts,
and custom visualizations.
"""

from copy import deepcopy


THEMES = {
    "Dark": {
        "background": "#0B0F14",
        "secondary_background": "#121923",
        "card_background": "#18212D",
        "plot_background": "#121923",
        "paper_background": "#0B0F14",
        "text": "#F7F9FC",
        "muted_text": "#AAB7C4",
        "accent": "#E10600",
        "accent_secondary": "#FF5A52",
        "accent_contrast": "#FFFFFF",
        "grid": "#2B3747",
        "border": "#263342",
        "success": "#2ECC71",
        "warning": "#F39C12",
        "error": "#E74C3C"
    },

    "Light": {
        "background": "#F5F7FA",
        "secondary_background": "#FFFFFF",
        "card_background": "#FFFFFF",
        "plot_background": "#FFFFFF",
        "paper_background": "#F5F7FA",
        "text": "#14171F",
        "muted_text": "#5E6A79",
        "accent": "#E10600",
        "accent_secondary": "#FF5A52",
        "accent_contrast": "#FFFFFF",
        "grid": "#DDE3EA",
        "border": "#D6DEE8",
        "success": "#2ECC71",
        "warning": "#F39C12",
        "error": "#E74C3C"
    },

    "Ferrari": {
        "background": "#110A0B",
        "secondary_background": "#1D1012",
        "card_background": "#281619",
        "plot_background": "#1D1012",
        "paper_background": "#110A0B",
        "text": "#FFF8F8",
        "muted_text": "#D8B9BD",
        "accent": "#E8002D",
        "accent_secondary": "#FFBE00",
        "accent_contrast": "#FFFFFF",
        "grid": "#48272C",
        "border": "#5C3038",
        "success": "#2ECC71",
        "warning": "#F39C12",
        "error": "#E74C3C"
    },

    "Mercedes": {
        "background": "#071413",
        "secondary_background": "#0E2422",
        "card_background": "#12312E",
        "plot_background": "#0E2422",
        "paper_background": "#071413",
        "text": "#F4FFFD",
        "muted_text": "#B8D2CE",
        "accent": "#27F4D2",
        "accent_secondary": "#C8D0D2",
        "accent_contrast": "#06211D",
        "grid": "#274944",
        "border": "#315A54",
        "success": "#2ECC71",
        "warning": "#F39C12",
        "error": "#E74C3C"
    },

    "Aston Martin": {
        "background": "#061714",
        "secondary_background": "#0B2822",
        "card_background": "#10372F",
        "plot_background": "#0B2822",
        "paper_background": "#061714",
        "text": "#F2FFFB",
        "muted_text": "#B9D9D0",
        "accent": "#229971",
        "accent_secondary": "#C7FF00",
        "accent_contrast": "#FFFFFF",
        "grid": "#255249",
        "border": "#2F6257",
        "success": "#2ECC71",
        "warning": "#F39C12",
        "error": "#E74C3C"
    }
}


DEFAULT_THEME = "Dark"


def get_available_themes():
    """
    Return all available theme names.
    """
    return list(THEMES.keys())


def get_theme(theme_name: str = DEFAULT_THEME):
    """
    Return a copy of the requested theme.

    If the theme does not exist, the default theme is returned.
    """

    if theme_name not in THEMES:
        theme_name = DEFAULT_THEME

    return deepcopy(THEMES[theme_name])


def plotly_layout(theme: dict):
    """
    Generate a standard Plotly layout dictionary based on the
    selected dashboard theme.
    """

    return {
        "paper_bgcolor": theme["paper_background"],
        "plot_bgcolor": theme["plot_background"],

        "font": {
            "color": theme["text"],
            "family": "Arial"
        },

        "xaxis": {
            "gridcolor": theme["grid"],
            "zerolinecolor": theme["grid"]
        },

        "yaxis": {
            "gridcolor": theme["grid"],
            "zerolinecolor": theme["grid"]
        },

        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "orientation": "h",
            "x": 0,
            "y": 1.05
        },

        "hoverlabel": {
            "bgcolor": theme["secondary_background"],
            "font": {
                "color": theme["text"]
            }
        },

        "hovermode": "x unified",

        "margin": {
            "l": 20,
            "r": 20,
            "t": 60,
            "b": 20
        }
    }
