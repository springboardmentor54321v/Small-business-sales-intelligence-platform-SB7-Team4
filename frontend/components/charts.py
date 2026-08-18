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
        title="📈 Daily Sales Revenue Trend"
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

    prod_col = "product_name" if "product_name" in df.columns else ("product_id" if "product_id" in df.columns else None)
    qty_col = "quantity" if "quantity" in df.columns else None

    if not prod_col or not qty_col:
        st.warning("Product columns are missing.")
        return

    df[qty_col] = pd.to_numeric(df[qty_col], errors="coerce").fillna(0)

    product_sales = (
        df.groupby(prod_col, as_index=False)[qty_col]
        .sum()
        .sort_values(qty_col, ascending=False)
        .head(5)
    )

    if product_sales.empty:
        st.info("No product data available.")
        return

    # Truncate label cleanly to avoid overlapping text
    product_sales["Product_Display"] = product_sales[prod_col].astype(str).apply(
        lambda x: x[:32] + "..." if len(x) > 32 else x
    )

    fig = px.bar(
        product_sales,
        x=qty_col,
        y="Product_Display",
        orientation="h",
        text=qty_col,
        title="🏆 Top 5 Selling Products (Units Sold)",
        color_discrete_sequence=["#2563eb"]
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Units Sold: %{x:,}"
    )

    fig.update_layout(
        height=380,
        template="plotly_white",
        xaxis_title="Quantity Sold (Units)",
        yaxis_title="Product",
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ---------------- Revenue by Category ---------------- #

def revenue_by_category_chart(sales):

    if sales is None:
        st.info("No category data available.")
        return

    df = pd.DataFrame(sales)

    if df.empty:
        st.info("No category data available.")
        return

    cat_col = "category" if "category" in df.columns else ("Category" if "Category" in df.columns else None)
    amt_col = "total_amount" if "total_amount" in df.columns else ("Total amount" if "Total amount" in df.columns else None)

    if not cat_col or not amt_col or cat_col not in df.columns:
        st.info("Category breakdown not available.")
        return

    df[amt_col] = pd.to_numeric(df[amt_col], errors="coerce").fillna(0)

    category_sales = (
        df.groupby(cat_col, as_index=False)[amt_col]
        .sum()
        .sort_values(amt_col, ascending=False)
    )

    if category_sales.empty:
        st.info("No category sales data found.")
        return

    fig = px.pie(
        category_sales,
        names=cat_col,
        values=amt_col,
        hole=0.45,
        title="📊 Revenue by Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.2f}<br>Share: %{percent}"
    )

    fig.update_layout(
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )