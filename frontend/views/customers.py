import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import show_sidebar


def customers_page():

    show_sidebar()

    st.title(" Customer Insights")
    st.caption("Customer Segmentation & Business Insights")

    st.markdown("---")

    # ---------------- Sample Customer Data ---------------- #

    df = pd.DataFrame({

        "Customer": [
            "Ravi",
            "Priya",
            "Rahul",
            "Anita",
            "Kiran",
            "Suresh",
            "Meena",
            "Ajay",
            "Neha",
            "Arjun"
        ],

        "Segment": [
            "Loyal",
            "High Value",
            "Occasional",
            "Loyal",
            "Occasional",
            "High Value",
            "Loyal",
            "Occasional",
            "High Value",
            "Loyal"
        ],

        "Orders": [
            28,
            17,
            5,
            22,
            8,
            16,
            30,
            4,
            18,
            26
        ],

        "Total Spend": [
            185000,
            145000,
            24000,
            132000,
            41000,
            160000,
            210000,
            18000,
            152000,
            198000
        ]

    })

    # ---------------- Dashboard Cards ---------------- #

    loyal = len(df[df["Segment"] == "Loyal"])

    high = len(df[df["Segment"] == "High Value"])

    occasional = len(df[df["Segment"] == "Occasional"])

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "⭐ Loyal Customers",
        loyal
    )

    c2.metric(
        "💎 High Value",
        high
    )

    c3.metric(
        "🛍 Occasional",
        occasional
    )

    st.markdown("---")

    search = st.text_input(
        "🔍 Search Customer"
    )

    if search:

        df = df[
            df["Customer"].str.contains(
                search,
                case=False
            )
        ]

    st.subheader("📊 Customer Distribution")
        # ---------------- Pie Chart ---------------- #

    segment_count = (
        df.groupby("Segment")
        .size()
        .reset_index(name="Customers")
    )

    pie = px.pie(
        segment_count,
        names="Segment",
        values="Customers",
        title="Customer Segmentation"
    )

    st.plotly_chart(
        pie,
        width="stretch"
    )

    st.markdown("---")

    # ---------------- Revenue Chart ---------------- #

    revenue = (
        df.groupby("Segment")["Total Spend"]
        .sum()
        .reset_index()
    )

    bar = px.bar(
        revenue,
        x="Segment",
        y="Total Spend",
        text="Total Spend",
        title="Revenue by Customer Segment"
    )

    bar.update_traces(
        texttemplate="₹%{text:,}",
        textposition="outside"
    )

    st.plotly_chart(
        bar,
        width="stretch"
    )

    st.markdown("---")

    # ---------------- Customer Table ---------------- #

    st.subheader("📋 Customer Insights")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # ---------------- Summary ---------------- #

    st.subheader("📈 Business Summary")

    total_customers = len(df)

    total_orders = df["Orders"].sum()

    total_revenue = df["Total Spend"].sum()

    avg_spend = int(df["Total Spend"].mean())

    c1, c2 = st.columns(2)

    c3, c4 = st.columns(2)

    c1.metric(
        "👥 Total Customers",
        total_customers
    )

    c2.metric(
        "🛒 Total Orders",
        total_orders
    )

    c3.metric(
        "💰 Revenue",
        f"₹ {total_revenue:,}"
    )

    c4.metric(
        "📊 Average Spend",
        f"₹ {avg_spend:,}"
    )

    st.markdown("---")

    # ---------------- Download ---------------- #

    st.download_button(
        label="⬇ Download Customer Insights",
        data=df.to_csv(index=False),
        file_name="customer_insights.csv",
        mime="text/csv",
        width="stretch"
    )