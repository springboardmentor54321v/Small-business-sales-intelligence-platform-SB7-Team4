import streamlit as st
import pandas as pd

from components.sidebar import show_sidebar
from components.cards import show_cards
from components.charts import sales_trend_chart, top_products_chart


def dashboard_page():

    show_sidebar()

    st.title("📊 MarketMind AI Dashboard")

    st.caption("Small Business Sales Intelligence Platform")

    st.markdown("---")

    # KPI Cards
    show_cards()

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        sales_trend_chart()

    with col2:
        top_products_chart()

    st.markdown("---")

    # Recent Sales
    st.subheader("🧾 Recent Sales")

    recent_sales = pd.DataFrame({
        "Invoice": [
            "INV001",
            "INV002",
            "INV003",
            "INV004",
            "INV005"
        ],
        "Customer": [
            "Ravi",
            "Priya",
            "Rahul",
            "Anita",
            "Kiran"
        ],
        "Amount": [
            "₹5,000",
            "₹12,000",
            "₹8,500",
            "₹3,200",
            "₹6,700"
        ],
        "Status": [
            "Paid",
            "Paid",
            "Pending",
            "Paid",
            "Pending"
        ]
    })

    st.dataframe(recent_sales, use_container_width=True)

    st.markdown("---")

    # Low Stock Alert
    st.subheader("⚠ Low Stock Alert")

    low_stock = pd.DataFrame({
        "Product": [
            "Keyboard",
            "Mouse",
            "Printer"
        ],
        "Remaining Stock": [
            5,
            2,
            1
        ]
    })

    st.dataframe(low_stock, use_container_width=True)