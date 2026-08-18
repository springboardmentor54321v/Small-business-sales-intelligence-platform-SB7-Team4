import streamlit as st
import pandas as pd
import requests
import plotly.express as px

from components.sidebar import show_sidebar
from components.cards import show_cards


# ============================================================
# API Configuration
# ============================================================
from config.config import DB_BASE_URL as BASE_URL

INVENTORY_API = f"{BASE_URL}/inventory/"
REVENUE_API = f"{BASE_URL}/revenue/summary"


import os
from concurrent.futures import ThreadPoolExecutor
from models.data_loader import get_active_sales_df, get_active_inventory_df, reset_to_default_dataset

# ============================================================
# Instant Full-History Business Overview Data Loader
# ============================================================

def load_business_overview_raw_data(base_url, inventory_url, revenue_url):
    # 1. Primary: Use active dataset (uploaded CSV if present, otherwise default)
    sales_df = get_active_sales_df()
    inventory_df = get_active_inventory_df()

    if not sales_df.empty:
        revenue = {
            "total_revenue": float(sales_df["total_amount"].sum()),
            "total_outstanding": float(sales_df["total_amount"].sum() * 0.12),
            "daily_collections": float(sales_df["total_amount"].tail(30).sum())
        }
        return sales_df, inventory_df, revenue

    # 2. Remote API Fallback
    try:
        def _fetch_sales():
            url = f"{base_url}/sales/?page=1&page_size=2000"
            r = requests.get(url, timeout=3.5)
            r.raise_for_status()
            return pd.DataFrame(r.json())

        def _fetch_inv():
            r = requests.get(inventory_url, timeout=3.5)
            r.raise_for_status()
            return pd.DataFrame(r.json())

        def _fetch_rev():
            r = requests.get(revenue_url, timeout=3.5)
            r.raise_for_status()
            return r.json()

        with ThreadPoolExecutor(max_workers=3) as executor:
            f_s = executor.submit(_fetch_sales)
            f_i = executor.submit(_fetch_inv)
            f_r = executor.submit(_fetch_rev)
            return f_s.result(), f_i.result(), f_r.result()
    except Exception:
        pass

    return sales_df, inventory_df, {}


# ============================================================
# Business Overview Page
# ============================================================

def business_overview_page():

    show_sidebar()

    header_col, refresh_col = st.columns([5, 1])
    with header_col:
        st.title(" Business Overview")
        st.caption("Complete Business Performance Dashboard")
    with refresh_col:
        st.write("")
        if st.button("🔄 Refresh Data", key="refresh_bo_btn", help="Clear cache and fetch latest sales & inventory"):
            st.cache_data.clear()
            st.rerun()

    # Active dataset banner
    active_dataset_name = st.session_state.get("active_dataset_name", "Default Dataset (All 4 Years)")
    if st.session_state.get("active_sales_df") is not None:
        c_info, c_rst = st.columns([5, 1])
        with c_info:
            st.info(f"📊 **Active Dataset:** `{active_dataset_name}` ({len(st.session_state['active_sales_df']):,} records)")
        with c_rst:
            if st.button("🔄 Use Default", key="bo_reset_btn", help="Revert to 51k-row default dataset"):
                reset_to_default_dataset()
                st.rerun()

    st.markdown("---")

    db_error = False
    sales_df = pd.DataFrame()
    inventory_df = pd.DataFrame()
    revenue = {}

    with st.spinner("Loading Business Overview..."):
        try:
            sales_df, inventory_df, revenue = load_business_overview_raw_data(BASE_URL, INVENTORY_API, REVENUE_API)
        except Exception:
            db_error = True

    try:
        if sales_df.empty:
            st.warning("No Sales Data Available")
            return

        if inventory_df.empty:
            st.warning("No Inventory Data Available")
            return

        # ---------------- Numeric Columns ---------------- #

        sales_numeric = [

            "quantity",

            "unit_price",

            "discount",

            "total_amount"

        ]

        for col in sales_numeric:

            if col in sales_df.columns:

                sales_df[col] = pd.to_numeric(

                    sales_df[col],

                    errors="coerce"

                ).fillna(0)

        inventory_numeric = [

            "stock_quantity",

            "low_stock_threshold"

        ]

        for col in inventory_numeric:

            if col in inventory_df.columns:

                inventory_df[col] = pd.to_numeric(

                    inventory_df[col],

                    errors="coerce"

                ).fillna(0)

        if "transaction_date" in sales_df.columns:

            sales_df["transaction_date"] = pd.to_datetime(

                sales_df["transaction_date"],

                errors="coerce"

            )
        # ============================================================
        # KPI Calculations
        # ============================================================

        total_revenue = float(
            revenue.get(
                "total_revenue",
                0
            )
        )

        total_outstanding = float(
            revenue.get(
                "total_outstanding",
                0
            )
        )

        daily_collections = float(
            revenue.get(
                "daily_collections",
                0
            )
        )

        total_orders = len(
            sales_df
        )

        if "quantity" in sales_df.columns:

            total_products_sold = int(
                sales_df["quantity"].sum()
            )

        else:

            total_products_sold = 0

        inventory_count = len(
            inventory_df
        )

        if (
            "stock_quantity" in inventory_df.columns
            and
            "low_stock_threshold" in inventory_df.columns
        ):

            low_stock_df = inventory_df[

                inventory_df["stock_quantity"]

                <=

                inventory_df["low_stock_threshold"]

            ]

        else:

            low_stock_df = pd.DataFrame()

        metrics = {

            "Revenue": total_revenue,

            "Outstanding": total_outstanding,

            "Today's Collection": daily_collections,

            "Orders": total_orders,

            "Products Sold": total_products_sold,

            "Inventory": inventory_count,

            "Low Stock": len(low_stock_df)

        }

        # ============================================================
        # KPI Cards
        # ============================================================

        show_cards(metrics)

        st.markdown("---")

        st.subheader(
            "Revenue Overview"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "Total Revenue",

            f"₹ {total_revenue:,.2f}"

        )

        c2.metric(

            "Outstanding",

            f"₹ {total_outstanding:,.2f}"

        )

        c3.metric(

            "Today's Collection",

            f"₹ {daily_collections:,.2f}"

        )

        st.markdown("---")
                # ============================================================
        # Top Selling Products
        # ============================================================

        st.subheader("Top Selling Products")

        if (
            "product_id" in sales_df.columns
            and
            "quantity" in sales_df.columns
        ):

            top_products = (

                sales_df

                .groupby(
                    "product_id",
                    as_index=False
                )["quantity"]

                .sum()

                .sort_values(
                    "quantity",
                    ascending=False
                )

                .head(10)

            )

            fig = px.bar(

                top_products,

                x="quantity",

                y="product_id",

                orientation="h",

                text="quantity",

                color="quantity",

                color_continuous_scale="Blues"

            )

            fig.update_layout(

                height=500,

                template="plotly_white",

                xaxis_title="Quantity Sold",

                yaxis_title="Product"

            )

            st.plotly_chart(

                fig,

                width="stretch"

            )

        else:

            st.info(
                "Top product data not available."
            )

        st.markdown("---")


        # ============================================================
        # Revenue By Category
        # ============================================================

        st.subheader("Revenue By Category")

        if (
            "category" in sales_df.columns
            and
            "total_amount" in sales_df.columns
        ):

            category_df = (

                sales_df

                .groupby(
                    "category",
                    as_index=False
                )["total_amount"]

                .sum()

                .sort_values(
                    "total_amount",
                    ascending=False
                )

            )

            fig = px.pie(

                category_df,

                names="category",

                values="total_amount",

                hole=0.45,

                color_discrete_sequence=px.colors.qualitative.Set3

            )

            fig.update_layout(

                height=450,

                template="plotly_white"

            )

            st.plotly_chart(

                fig,

                width="stretch"

            )

        else:

            st.info(
                "Category information not available."
            )

        st.markdown("---")
        # ============================================================
        # Product Drill Down
        # ============================================================

        st.subheader("Product Drill Down")

        if (
            "product_id" in sales_df.columns
            and
            not sales_df.empty
        ):

            products = sorted(
                sales_df["product_id"]
                .dropna()
                .astype(str)
                .unique()
            )

            selected_product = st.selectbox(
                "Select Product",
                products
            )

            product_df = sales_df[
                sales_df["product_id"].astype(str)
                == selected_product
            ]

            # ---------------- KPI Cards ---------------- #

            revenue_value = product_df[
                "total_amount"
            ].sum()

            quantity_value = int(
                product_df["quantity"].sum()
            )

            order_count = len(product_df)

            stock_left = "N/A"

            if (
                "product_id" in inventory_df.columns
                and
                "stock_quantity" in inventory_df.columns
            ):

                stock = inventory_df[
                    inventory_df["product_id"]
                    .astype(str)
                    == selected_product
                ]

                if not stock.empty:

                    stock_left = int(
                        stock.iloc[0]["stock_quantity"]
                    )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Revenue",
                f"₹ {revenue_value:,.2f}"
            )

            c2.metric(
                "Units Sold",
                quantity_value
            )

            c3.metric(
                "Orders",
                order_count
            )

            c4.metric(
                "Stock Left",
                stock_left
            )

            st.markdown("---")

           

            # ---------------- Recent Transactions ---------------- #

            st.subheader(
                "Recent Transactions"
            )

            columns = [

                "transaction_date",

                "invoice_id",

                "customer_id",

                "quantity",

                "total_amount"

            ]

            available_columns = [

                col

                for col in columns

                if col in product_df.columns

            ]

            if available_columns:

                st.dataframe(

                    product_df[
                        available_columns
                    ].sort_values(
                        by="transaction_date",
                        ascending=False
                    ),

                    width="stretch",

                    hide_index=True

                )

            else:

                st.info(
                    "Transaction details not available."
                )

        else:

            st.info(
                "Product information not available."
            )

        st.markdown("---")
        # ============================================================
        # Customer Insights
        # ============================================================

        
        st.subheader("👥 Top 10 Customers by Revenue")

        cust_col = "customer_name" if "customer_name" in sales_df.columns else ("Customer Name" if "Customer Name" in sales_df.columns else "customer_id")

        customer_df = (
            sales_df.groupby(cust_col, as_index=False)
            .agg(
                Revenue=("total_amount", "sum"),
                Orders=("invoice_id", "nunique")
            )
            .sort_values("Revenue", ascending=False)
            .head(10)
        )

        if customer_df.empty:
            st.info("No customer data available.")
        else:
            fig = px.bar(
                customer_df,
                x="Revenue",
                y=cust_col,
                orientation="h",
                text="Revenue",
                title="Top 10 Customers by Total Spend",
                color_discrete_sequence=["#6366f1"]
            )

            fig.update_traces(
                texttemplate="₹%{text:,.2f}",
                textposition="outside"
            )

            fig.update_layout(
                template="plotly_white",
                height=450,
                xaxis_title="Revenue (₹)",
                yaxis_title="Customer",
                yaxis=dict(autorange="reversed")
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

            st.dataframe(
                customer_df.rename(columns={cust_col: "Customer Name", "Revenue": "Total Revenue (₹)", "Orders": "Total Orders"}),
                width="stretch",
                hide_index=True
            )

        # ============================================================
        # Business Alerts
        # ============================================================

        st.subheader("Business Alerts")

        if len(low_stock_df) > 0:

            st.warning(

                f"{len(low_stock_df)} products are below the stock threshold."

            )

        else:

            st.success(
                "No low stock products."
            )

        if total_outstanding > 0:

            st.warning(

                f"Outstanding Payments : ₹ {total_outstanding:,.2f}"

            )

        else:

            st.success(
                "No outstanding payments."
            )

        st.markdown("---")


        # ============================================================
        # Recent Sales
        # ============================================================

        st.subheader("Recent Sales")

        display_columns = [

            "transaction_id",

            "invoice_id",

            "transaction_date",

            "customer_id",

            "product_id",

            "quantity",

            "total_amount"

        ]

        available_columns = [

            col

            for col in display_columns

            if col in sales_df.columns

        ]

        if available_columns:

            st.dataframe(

                sales_df

                .sort_values(
                    by="transaction_date",
                    ascending=False
                )[available_columns]

                .head(10),

                width="stretch",

                hide_index=True

            )

        else:

            st.info(
                "No recent sales available."
            )

        st.markdown("---")


        # ============================================================
        # Revenue Summary
        # ============================================================

        st.subheader("Revenue Summary")

        summary = pd.DataFrame({

            "Metric": [

                "Revenue",

                "Outstanding",

                "Today's Collection",

                "Orders",

                "Products Sold",

                "Inventory",

                "Low Stock"

            ],

            "Value": [

                f"₹ {total_revenue:,.2f}",

                f"₹ {total_outstanding:,.2f}",

                f"₹ {daily_collections:,.2f}",

                f"{total_orders:,}",

                f"{total_products_sold:,}",

                f"{inventory_count:,}",

                f"{len(low_stock_df):,}"

            ]

        })

        st.dataframe(

            summary,

            width="stretch",

            hide_index=True

        )

        st.markdown("---")


        # ============================================================
        # Export Report
        # ============================================================

        st.subheader("Export Report")

        csv = sales_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            label="Download Business Report",

            data=csv,

            file_name="business_overview_report.csv",

            mime="text/csv",

            width="stretch"

        )

       

        st.caption(
            "MarketMind AI • Business Overview • Version 2.0"
        )
    # ============================================================
    # Exception Handling
    # ============================================================

    except requests.exceptions.Timeout:

        st.error(
            "Backend request timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to the backend server."
        )

    except requests.exceptions.HTTPError as e:

        st.error(
            f"API Error: {e}"
        )

        try:

            error_response = e.response.json()

            st.json(error_response)

        except Exception:

            if e.response is not None:

                st.code(e.response.text)

    except ValueError as e:

        st.error(
            f"Data Processing Error: {e}"
        )

    except KeyError as e:

        st.error(
            f"Missing Required Column: {e}"
        )

    except Exception as e:

        st.exception(e)