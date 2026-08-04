import streamlit as st


def display_driver_statistics(statistics):
    """
    Display driver statistics as metric cards.

    Parameters
    ----------
    statistics : dict
        Output from processing.driver_statistics.get_driver_statistics()
    """

    if not statistics:

        st.warning("No driver statistics available.")

        return

    st.divider()

    st.header("📊 Driver Statistics")

    for driver, stats in statistics.items():

        st.subheader(driver)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🏁 Fastest Lap",
                stats["Fastest Lap"]
            )

            st.metric(
                "🥇 Best Sector 1",
                stats["Best Sector 1"]
            )

            st.metric(
                "🏎️ Top Speed",
                stats["Top Speed"]
            )

        with col2:

            st.metric(
                "📈 Average Lap",
                stats["Average Lap"]
            )

            st.metric(
                "🥈 Best Sector 2",
                stats["Best Sector 2"]
            )

            st.metric(
                "⚡ Average Speed",
                stats["Average Speed"]
            )

        with col3:

            st.metric(
                "🥉 Best Sector 3",
                stats["Best Sector 3"]
            )

            st.metric(
                "🏁 Completed Laps",
                stats["Completed Laps"]
            )

            st.metric(
                "🛞 Tyre Stints",
                stats["Tyre Stints"]
            )

        st.divider()