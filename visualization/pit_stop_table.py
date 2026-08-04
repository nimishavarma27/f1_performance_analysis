"""
Pit Stop Table
"""

import streamlit as st


def display(dataframe):
    """
    Display pit stop analysis.
    """

    if dataframe is None or dataframe.empty:

        st.info(
            "No pit stops detected."
        )

        return

    st.dataframe(

        dataframe,

        use_container_width=True,

        hide_index=True

    )