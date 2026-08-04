import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import show_sidebar


def business_overview_page():

    # ---------------- Sidebar ---------------- #

    show_sidebar()

    # ---------------- Title ---------------- #

    st.title("📊 Business Overview")
    st.caption("Milestone 3 - Day 5")

    st.markdown("---")

    # ---------------- Filters ---------------- #

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        start_date = st.date_input("📅 Start Date")

    with f2:
        end_date = st.date_input("📅 End Date")

    with f3:
        category = st.selectbox(
            "📦 Category",
            [
                "All",
                "Electronics",
                "Furniture",
                "Office Supplies"
            ]
        )

    with f4:
        region = st.selectbox(
            "🌍 Region",
            [
                "All",
                "East",
                "West",
                "South",
                "Central"
            ]
        )

    st.markdown("---")

    # ---------------- KPI Cards ---------------- #

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Revenue", "₹2,45,000")
    c2.metric("📦 Products", "120")
    c3.metric("👥 Customers", "78")
    c4.metric("🚨 Alerts", "3")

    st.markdown("---")

    # ---------------- Revenue Data ---------------- #

    revenue = pd.DataFrame({
        "Month": pd.to_datetime([
            "2026-01-01",
            "2026-02-01",
            "2026-03-01",
            "2026-04-01",
            "2026-05-01"
        ]),

        "Revenue": [
            120000,
            150000,
            180000,
            210000,
            245000
        ]
    })

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

    chart1, chart2 = st.columns(2)

    # ---------------- Revenue Chart ---------------- #
    with chart1:
        st.subheader("📈 Revenue Trend")
        fig = px.line(
            revenue,
            x="Month",
            y="Revenue",
            markers=True
    )

        fig.update_xaxes(
            tickformat="%b"
        )

        fig.update_layout(
            template="plotly_dark",

            plot_bgcolor="#0E1117",

            paper_bgcolor="#0E1117",
            height=350
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )
    
    # ---------------- Top Products ---------------- #

    with chart2:

        st.subheader("🏆 Top Products")

        fig = px.bar(

            products,

            x="Product",

            y="Sales",

            color="Sales",

            template="plotly_dark"

        )

        fig.update_layout(

            plot_bgcolor="#0E1117",

            paper_bgcolor="#0E1117",

            height=350

        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    # ---------------- Product Drill Down ---------------- #

    st.subheader("🔍 Product Drill Down")

    selected_product = st.selectbox(
        "Select Product",
        products["Product"]
    )

    if selected_product == "Laptop":

        revenue_value = "₹1,95,000"
        sold = 55
        profit = "₹48,000"
        stock = 18
        trend = [10, 12, 15, 14, 18, 20, 22]

    elif selected_product == "Mouse":

        revenue_value = "₹82,000"
        sold = 120
        profit = "₹18,500"
        stock = 45
        trend = [20, 18, 22, 25, 30, 28, 32]

    elif selected_product == "Keyboard":

        revenue_value = "₹64,000"
        sold = 85
        profit = "₹14,000"
        stock = 30
        trend = [15, 16, 14, 18, 20, 21, 23]

    elif selected_product == "Monitor":

        revenue_value = "₹96,000"
        sold = 40
        profit = "₹22,000"
        stock = 25
        trend = [8, 10, 9, 12, 14, 16, 15]

    else:

        revenue_value = "₹32,000"
        sold = 22
        profit = "₹7,000"
        stock = 60
        trend = [5, 6, 8, 9, 8, 10, 11]

    d1, d2, d3, d4 = st.columns(4)

    d1.metric("💰 Revenue", revenue_value)
    d2.metric("📦 Units Sold", sold)
    d3.metric("📈 Profit", profit)
    d4.metric("📦 Stock Left", stock)

    st.subheader(f"📊 {selected_product} Sales Trend")

    trend_df = pd.DataFrame({
        "Day Number":[1,2,3,4,5,6,7],
        "Day":[
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ],
        "Sales":trend
    })
    fig = px.line(
        trend_df,
        x="Day Number",
        y="Sales",
        markers=True
    )
    fig.update_xaxes(
        tickmode="array",

        tickvals=[1,2,3,4,5,6,7],

        ticktext=[
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]
    )
    

    fig.update_layout(

        template="plotly_dark",

        xaxis=dict(

            categoryorder="array",

            categoryarray=[
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ]

        ),

        plot_bgcolor="#0E1117",

        paper_bgcolor="#0E1117",

        height=350

    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("---")
    # ---------------- Customer Groups ---------------- #

    st.subheader("👥 Customer Groups")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.metric(
            "⭐ Premium",
            "20"
        )

    with g2:
        st.metric(
            "👤 Regular",
            "45"
        )

    with g3:
        st.metric(
            "🆕 New",
            "13"
        )

    customer_df = pd.DataFrame({

        "Group": [

            "Premium",

            "Regular",

            "New"

        ],

        "Customers": [

            20,

            45,

            13

        ]

    })

    st.markdown("---")

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

            st.error(
                f"🔴 {row['Alert']}"
            )

        elif row["Priority"] == "Medium":

            st.warning(
                f"🟡 {row['Alert']}"
            )

        else:

            st.success(
                f"🟢 {row['Alert']}"
            )

    st.markdown("---")

    # ---------------- Dashboard Actions ---------------- #

    a1, a2 = st.columns(2)

    with a1:

        if st.button(
            "🔄 Refresh Dashboard",
            width="stretch"
        ):

            st.rerun()

    with a2:

        csv = customer_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            label="⬇ Download Customer Report",

            data=csv,

            file_name="customer_report.csv",

            mime="text/csv",

            width="stretch"

        )

    st.markdown("---")

    st.success("✅ Business Overview Loaded Successfully")