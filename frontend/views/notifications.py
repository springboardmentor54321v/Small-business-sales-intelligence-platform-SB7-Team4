import streamlit as st
import pandas as pd

from components.sidebar import show_sidebar


def notifications_page():

    show_sidebar()

    st.title(" Notifications Center")
    st.caption("Milestone 3 - Day 6")

    st.markdown("---")

    # ---------------- Sample Notifications ---------------- #

    notifications = [

        {
            "Type": " Low Stock",
            "Title": "Laptop Stock Running Low",
            "Message": "Only 4 laptops remaining in inventory.",
            "Priority": "High",
            "Time": "10 mins ago"
        },

        {
            "Type": " Invoice",
            "Title": "Invoice INV-1008 Overdue",
            "Message": "Payment overdue by 5 days.",
            "Priority": "Medium",
            "Time": "30 mins ago"
        },

        {
            "Type": " Inventory",
            "Title": "Mouse Stock Running Low",
            "Message": "Only 8 units remaining.",
            "Priority": "Low",
            "Time": "1 hour ago"
        },

        {
            "Type": " Forecast",
            "Title": "Forecast Accuracy Improved",
            "Message": "Forecast accuracy reached 94%.",
            "Priority": "Low",
            "Time": "2 hours ago"
        },

        {
            "Type": " Sales",
            "Title": "Daily Sales Target Achieved",
            "Message": "Sales exceeded today's target by 8%.",
            "Priority": "High",
            "Time": "Today"
        }

    ]

    df = pd.DataFrame(notifications)

    # ---------------- KPI Cards ---------------- #

    total = len(df)
    high = len(df[df["Priority"] == "High"])
    medium = len(df[df["Priority"] == "Medium"])
    low = len(df[df["Priority"] == "Low"])

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
            "Priority",
            ["All", "High", "Medium", "Low"]
        )

    with c2:

        search = st.text_input(
            " Search Notification"
        )

    filtered = df.copy()

    if priority != "All":
        filtered = filtered[
            filtered["Priority"] == priority
        ]

    if search:
        filtered = filtered[
            filtered["Title"].str.contains(
                search,
                case=False
            )
        ]

    st.markdown("---")

    # ---------------- Notification Cards ---------------- #

    for i, row in filtered.iterrows():

        with st.expander(
            f"{row['Type']} | {row['Title']}"
        ):

            st.write(f"**Priority:** {row['Priority']}")
            st.write(f"**Message:** {row['Message']}")
            st.write(f"**Time:** {row['Time']}")

            b1, b2 = st.columns(2)

            with b1:

                if st.button(
                    " View Details",
                    key=f"view{i}"
                ):
                    st.json(row.to_dict())

            with b2:

                if st.button(
                    " Mark as Read",
                    key=f"read{i}"
                ):
                    st.success("Notification marked as read.")

    st.markdown("---")

    # ---------------- Notification Log ---------------- #

    st.subheader(" Notification Log")

    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # ---------------- Actions ---------------- #

    a1, a2 = st.columns(2)

    with a1:

        csv = filtered.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Notification Log",
            data=csv,
            file_name="notifications.csv",
            mime="text/csv",
            width="stretch"
        )

    with a2:

        if st.button(
            "🔄 Refresh Notifications",
            width="stretch"
        ):
            st.rerun()

    st.markdown("---")

    st.success(" Notifications Dashboard Loaded Successfully")