TEAM_COLORS = {
    "Red Bull": "#3671C6",
    "Ferrari": "#E80020",
    "Mercedes": "#27F4D2",
    "McLaren": "#FF8000",
    "Aston Martin": "#229971",
    "Alpine": "#FF87BC",
    "Williams": "#64C4FF",
    "RB": "#6692FF",
    "Racing Bulls": "#6692FF",
    "Kick Sauber": "#52E252",
    "Sauber": "#52E252",
    "Haas": "#B6BABD"
}


def get_team_color(team_name):
    """
    Return the official team colour.
    """

    return TEAM_COLORS.get(team_name, "#808080")