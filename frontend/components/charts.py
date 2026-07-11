import streamlit as st
import pandas as pd
import plotly.express as px


def sales_trend_chart():

    data = pd.DataFrame({
        "Day": [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ],
        "Sales": [
            12000,
            18000,
            15000,
            22000,
            28000,
            35000,
            30000
        ]
    })

    fig = px.line(
        data,
        x="Day",
        y="Sales",
        markers=True,
        title="📈 Daily Sales Trend"
    )

    fig.update_layout(
        height=400,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)


def top_products_chart():

    data = pd.DataFrame({
        "Product": [
            "Laptop",
            "Mouse",
            "Keyboard",
            "Monitor",
            "Printer"
        ],
        "Sales": [
            320,
            280,
            240,
            180,
            120
        ]
    })

    fig = px.bar(
        data,
        x="Product",
        y="Sales",
        title="🏆 Top Products"
    )

    fig.update_layout(
        height=400,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)