"""
Speed Trap Table
"""

import streamlit as st


def display(dataframe):
    """
    Display speed trap results.
    """

    if dataframe is None or dataframe.empty:

        st.warning(
            "No speed trap data available."
        )

        return

    st.dataframe(

        dataframe,

        use_container_width=True,

        hide_index=True

    )