import streamlit as st
import pandas as pd

from components.sidebar import show_sidebar


def business_overview_page():

    show_sidebar()

    st.title("📊 Business Overview")
    st.caption("Milestone 3 - Day 3")

    st.markdown("---")

    # ---------------- KPI Cards ---------------- #

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Revenue", "₹2,45,000")
    c2.metric("Products", "120")
    c3.metric("Customers", "78")
    c4.metric("Alerts", "3")

    st.markdown("---")

    # ---------------- Charts ---------------- #

    col1, col2 = st.columns(2)

    revenue = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "Revenue": [120000, 150000, 180000, 210000, 245000]
    })

    with col1:

        st.subheader("📈 Revenue Trend")

        st.line_chart(
            revenue.set_index("Month")
        )

    products = pd.DataFrame({

        "Product": [
            "Laptop",
            "Mouse",
            "Keyboard",
            "Monitor",
            "Printer"
        ],

        "Sales": [
            55,
            120,
            85,
            40,
            22
        ]
    })

    with col2:

        st.subheader("🏆 Top Products")

        st.bar_chart(
            products.set_index("Product")
        )

    st.markdown("---")

    # ---------------- Customer Groups ---------------- #

   # ---------------- Customer Groups ---------------- #
    # ---------------- Customer Groups ---------------- #

    st.subheader("👥 Customer Groups")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            label="⭐ Premium",
            value="20"
        )

    with c2:
        st.metric(
            label="👤 Regular",
            value="45"
        )

    with c3:
        st.metric(
            label="🆕 New",
            value="13"
        )

    st.markdown("---")

    # ---------------- Recent Alerts ---------------- #

    # ---------------- Recent Alerts ---------------- #

    st.subheader("🔔 Recent Alerts")

    alerts = pd.DataFrame({

        "Alert": [
            "Laptop Stock Low",
            "Invoice INV-1008 Overdue",
            "Mouse Stock Low"
        ],

       "Priority": [
            "High",
            "Medium",
            "Low"
        ]

   })

    for _, row in alerts.iterrows():

        if row["Priority"] == "High":
            st.error(f"🔴 {row['Alert']}")

        elif row["Priority"] == "Medium":
            st.warning(f"🟡 {row['Alert']}")

        else:
            st.success(f"🟢 {row['Alert']}")
    