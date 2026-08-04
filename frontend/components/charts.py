import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------- Sales Trend ---------------- #

def sales_trend_chart(sales):

    if not sales:
        st.info("No sales data available.")
        return

    df = pd.DataFrame(sales)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    df["total_amount"] = pd.to_numeric(
        df["total_amount"],
        errors="coerce"
    ).fillna(0)

    df = df.dropna(subset=["transaction_date"])

    daily_sales = (
        df.groupby("transaction_date", as_index=False)["total_amount"]
        .sum()
        .sort_values("transaction_date")
    )

    fig = px.line(
        daily_sales,
        x="transaction_date",
        y="total_amount",
        markers=True,
        title="📈 Daily Sales Revenue"
    )

    fig.update_layout(
        height=420,
        template="plotly_white",
        xaxis_title="Transaction Date",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------- Top Products ---------------- #

def top_products_chart(sales):

    if not sales:
        st.info("No product data available.")
        return

    df = pd.DataFrame(sales)

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    ).fillna(0)

    product_sales = (
        df.groupby("product_id", as_index=False)["quantity"]
        .sum()
        .sort_values("quantity", ascending=False)
        .head(5)
    )

    fig = px.bar(
        product_sales,
        x="product_id",
        y="quantity",
        text="quantity",
        title=" Top 5 Selling Products"
    )

    fig.update_layout(
        height=420,
        template="plotly_white",
        xaxis_title="Product ID",
        yaxis_title="Quantity Sold"
    )

    st.plotly_chart(fig, use_container_width=True)