"""
Mini Sector Table
"""

import streamlit as st


def display(dataframe):
    """
    Display mini sector results.
    """

    if dataframe is None or dataframe.empty:

        st.warning(
            "Mini sector analysis unavailable."
        )

        return

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True
    )