import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------- Sales Trend ---------------- #

def sales_trend_chart(sales):

    if sales is None:
        st.info("No sales data available.")
        return

    df = pd.DataFrame(sales)

    if df.empty:
        st.info("No sales data available.")
        return

    if "transaction_date" not in df.columns or "total_amount" not in df.columns:
        st.warning("Required columns are missing.")
        return

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    df["total_amount"] = pd.to_numeric(
        df["total_amount"],
        errors="coerce"
    ).fillna(0)

    df = df.dropna(subset=["transaction_date"])

    # Filter out future outlier dates dynamically (e.g. 2026/2027 test entries)
    if len(df) > 5:
        years = df["transaction_date"].dt.year
        q3_year = years.quantile(0.75)
        df = df[df["transaction_date"].dt.year <= q3_year + 2]

    if df.empty:
        st.info("No valid sales data available.")
        return

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
        title="Daily Sales Revenue"
    )

    fig.update_layout(
        height=420,
        template="plotly_white",
        xaxis_title="Transaction Date",
        yaxis_title="Revenue (₹)"
    )
    fig.update_xaxes(rangeslider_visible=True)

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ---------------- Top Products ---------------- #

def top_products_chart(sales):

    if sales is None:
        st.info("No product data available.")
        return

    df = pd.DataFrame(sales)

    if df.empty:
        st.info("No product data available.")
        return

    if "product_id" not in df.columns or "quantity" not in df.columns:
        st.warning("Required columns are missing.")
        return

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

    if product_sales.empty:
        st.info("No product data available.")
        return

    fig = px.bar(
        product_sales,
        x="product_id",
        y="quantity",
        text="quantity",
        title="Top 5 Selling Products"
    )

    fig.update_layout(
        height=420,
        template="plotly_white",
        xaxis_title="Product ID",
        yaxis_title="Quantity Sold"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )