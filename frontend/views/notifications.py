import streamlit as st
from components.sidebar import show_sidebar


def notifications_page():

    show_sidebar()

    st.title("🔔 Notifications Center")
    st.caption("Milestone 3 - Day 2")

    notifications = [

        {
            "type": "⚠ Low Stock",
            "title": "Laptop Stock Running Low",
            "message": "Only 4 laptops remaining in inventory.",
            "time": "10 mins ago",
            "priority": "High"
        },

        {
            "type": "🧾 Overdue Invoice",
            "title": "Invoice INV-1008",
            "message": "Payment overdue by 5 days.",
            "time": "30 mins ago",
            "priority": "Medium"
        },

        {
            "type": "⚠ Low Stock",
            "title": "Mouse Stock Running Low",
            "message": "Only 8 units remaining.",
            "time": "1 hour ago",
            "priority": "Low"
        }

    ]

    st.subheader(f"Total Alerts : {len(notifications)}")

    st.markdown("---")

    for i, alert in enumerate(notifications):

        with st.expander(f"{alert['type']}  |  {alert['title']}"):

            st.write(f"**Priority :** {alert['priority']}")
            st.write(f"**Message :** {alert['message']}")
            st.write(f"**Time :** {alert['time']}")

            if st.button("View Details", key=i):

                st.success("Notification Details")

                st.write(alert)