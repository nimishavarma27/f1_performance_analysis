"""
Pace Analysis Table
"""

import streamlit as st


def display(dataframe):
    """
    Display pace statistics.
    """

    if dataframe is None or dataframe.empty:

        st.warning(
            "No pace data available."
        )

        return

    st.dataframe(

        dataframe,

        use_container_width=True,

        hide_index=True

    )