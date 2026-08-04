"""
Corner Analysis Cards
"""

import streamlit as st


def display(results):
    """
    Display corner analysis metrics.
    """

    if results is None:

        st.warning(
            "Corner analysis unavailable."
        )

        return

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Maximum Speed",

            f"{results['MaximumSpeed']['Speed']:.1f} km/h"

        )

        st.caption(

            f"At {results['MaximumSpeed']['Distance']:.0f} m"

        )

    with col2:

        st.metric(

            "Minimum Speed",

            f"{results['MinimumSpeed']['Speed']:.1f} km/h"

        )

        st.caption(

            f"At {results['MinimumSpeed']['Distance']:.0f} m"

        )

    st.divider()

    st.write(
        f"Brake Samples: **{len(results['Braking'])}**"
    )

    st.write(
        f"Full Throttle Samples: **{len(results['FullThrottle'])}**"
    )