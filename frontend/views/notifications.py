import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar

# ---------------- API Configuration ---------------- #

BASE_URL = "https://undefined-arrest-crescent.ngrok-free.dev"

NOTIFICATION_API = f"{BASE_URL}/notifications"


# ---------------- Notifications ---------------- #

def notifications_page():

    show_sidebar()

    st.title("Notifications Center")
    st.caption("Real-Time Business Notifications")

    st.markdown("---")

    try:

        with st.spinner("Loading Notifications..."):

            response = requests.get(
                NOTIFICATION_API,
                timeout=10
            )

        response.raise_for_status()

        data = response.json()

        notifications = data.get(
            "notifications",
            []
        )

        if len(notifications) == 0:

            st.warning("No Notifications Available")
            return

        df = pd.DataFrame(notifications)

    except requests.exceptions.Timeout:

        st.error("❌ Backend request timed out.")
        return

    except requests.exceptions.ConnectionError:

        st.error("❌ Unable to connect to backend.")
        return

    except requests.exceptions.HTTPError as e:

        st.error(f"❌ API Error: {e}")
        return

    except Exception as e:

        st.error(f"❌ Unexpected Error: {e}")
        return

    # ---------------- KPI Cards ---------------- #

    total = len(df)

    high = len(
        df[df["severity"] == "HIGH"]
    )

    medium = len(
        df[df["severity"] == "MEDIUM"]
    )

    low = len(
        df[df["severity"] == "LOW"]
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("🔔 Total", total)
    k2.metric("🔴 High", high)
    k3.metric("🟡 Medium", medium)
    k4.metric("🟢 Low", low)

    st.markdown("---")

    # ---------------- Filters ---------------- #

    c1, c2 = st.columns(2)

    with c1:

        priority = st.selectbox(
            "Severity",
            [
                "All",
                "HIGH",
                "MEDIUM",
                "LOW"
            ]
        )

    with c2:

        search = st.text_input(
            "Search Notification"
        )

    filtered = df.copy()

    if priority != "All":

        filtered = filtered[
            filtered["severity"] == priority
        ]

    if search:

        filtered = filtered[
            filtered["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.markdown("---")
    # ---------------- Notification Cards ---------------- #

    for i, row in filtered.iterrows():

        with st.expander(
            f"{row['type']} | {row['title']}"
        ):

            st.write(f"**Severity:** {row['severity']}")

            st.write(f"**Message:** {row['message']}")

            if "reference_id" in row:
                st.write(
                    f"**Reference ID:** {row['reference_id']}"
                )

            b1 = st.columns(1)[0]

            with b1:

                if st.button(
                    "View Details",
                    key=f"view{i}"
                ):

                    st.markdown("###  Notification Details")

                    st.write(f"**Type:** {row['type']}")

                    st.write(f"**Title:** {row['title']}")

                    st.write(f"**Severity:** {row['severity']}")

                    st.write(f"**Message:** {row['message']}")

                    if "reference_id" in row:
                        st.write(
                            f"**Reference ID:** {row['reference_id']}"
                        )

                    

           

    st.markdown("---")

    # ---------------- Notification Log ---------------- #

    st.subheader(" Notification Log")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ---------------- Actions ---------------- #

    a1, a2 = st.columns(2)

    with a1:

        csv = filtered.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            " Download Notification Log",
            data=csv,
            file_name="notifications.csv",
            mime="text/csv",
            use_container_width=True
        )

    with a2:

        if st.button(
            " Refresh Notifications",
            use_container_width=True
        ):

            st.rerun()

    