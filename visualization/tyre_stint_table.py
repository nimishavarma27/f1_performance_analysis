"""
Tyre Stint Table
"""

import streamlit as st


def display(dataframe):

    if dataframe is None or dataframe.empty:

        st.warning(
            "No stint data available."
        )

        return

    st.dataframe(

        dataframe,

        use_container_width=True,

        hide_index=True

    )
