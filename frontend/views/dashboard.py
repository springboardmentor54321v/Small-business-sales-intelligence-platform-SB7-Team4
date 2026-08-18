import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar
from components.cards import show_cards
from components.charts import (
    sales_trend_chart,
    top_products_chart,
    revenue_by_category_chart
)

# ---------------- API Configuration ---------------- #
from config.config import DB_BASE_URL as BASE_URL

INVENTORY_API = f"{BASE_URL}/inventory/"
REVENUE_API = f"{BASE_URL}/revenue/summary"


import os
from concurrent.futures import ThreadPoolExecutor
from models.data_loader import get_active_sales_df, get_active_inventory_df, reset_to_default_dataset

# ---------------- Instant Full-History Cached Data Loader ---------------- #

def load_dashboard_raw_data(base_url, inventory_url, revenue_url):
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


# ---------------- Dashboard ---------------- #

def dashboard_page():

    show_sidebar()

    header_col, refresh_col = st.columns([5, 1])
    with header_col:
        st.title("MarketMind AI Dashboard")
        st.caption("Small Business Sales Intelligence Platform")
    with refresh_col:
        st.write("")
        if st.button("🔄 Refresh Data", help="Clear cache and fetch latest sales & inventory"):
            st.cache_data.clear()
            st.rerun()

    # Active dataset banner
    active_dataset_name = st.session_state.get("active_dataset_name", "Cleaned Primary Dataset")
    if st.session_state.get("active_sales_df") is not None:
        c_info, c_rst = st.columns([5, 1])
        with c_info:
            st.info(f"📊 **Active Dataset:** `{active_dataset_name}` ({len(st.session_state['active_sales_df']):,} records)")
        with c_rst:
            if st.button("🔄 Use Default", key="dash_reset_btn", help="Revert to primary cleaned dataset"):
                reset_to_default_dataset()
                st.rerun()

    st.markdown("---")

    db_error = False
    sales_df = pd.DataFrame()
    inventory_df = pd.DataFrame()
    revenue = {}

    with st.spinner("Loading Dashboard..."):
        try:
            sales_df, inventory_df, revenue = load_dashboard_raw_data(BASE_URL, INVENTORY_API, REVENUE_API)
        except Exception:
            db_error = True

    try:
        if sales_df.empty:
            st.warning("No Sales Data Available")
            return

        if inventory_df.empty:
            st.warning("No Inventory Data Available")
            return

        # ---------------- Numeric Conversion ---------------- #

        numeric_sales = [
            "quantity",
            "unit_price",
            "discount",
            "total_amount"
        ]

        for col in numeric_sales:
            if col in sales_df.columns:
                sales_df[col] = pd.to_numeric(sales_df[col], errors="coerce").fillna(0)

        numeric_inventory = [
            "stock_quantity",
            "low_stock_threshold"
        ]

        for col in numeric_inventory:
            if col in inventory_df.columns:
                inventory_df[col] = pd.to_numeric(inventory_df[col], errors="coerce").fillna(0)

        # ---------------- Date Conversion ---------------- #

        if "transaction_date" in sales_df.columns:
            sales_df["transaction_date"] = pd.to_datetime(sales_df["transaction_date"], errors="coerce")
            sales_df = sales_df.sort_values(by="transaction_date", ascending=False)

        # ---------------- KPI Values ---------------- #

        total_revenue = float(revenue.get("total_revenue") or sales_df["total_amount"].sum())
        total_outstanding = float(revenue.get("total_outstanding") or (total_revenue * 0.12))
        daily_collections = float(revenue.get("daily_collections") or sales_df["total_amount"].tail(30).sum())
        total_orders = len(sales_df)
        total_products_sold = int(sales_df["quantity"].sum()) if "quantity" in sales_df.columns else len(sales_df)
        inventory_count = len(inventory_df)

        if "stock_quantity" in inventory_df.columns and "low_stock_threshold" in inventory_df.columns:
            low_stock_df = inventory_df[inventory_df["stock_quantity"] <= inventory_df["low_stock_threshold"]]
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

        # ---------------- KPI Cards ---------------- #

        show_cards(metrics)

        st.markdown("---")

        # ---------------- Charts ---------------- #

        col_c1, col_c2 = st.columns([3, 2])

        with col_c1:
            sales_trend_chart(sales_df)

        with col_c2:
            revenue_by_category_chart(sales_df)

        st.markdown("---")

        top_products_chart(sales_df)

        st.markdown("---")

        # ---------------- Recent Sales ---------------- #

        st.subheader("Recent Sales")

        display_columns = [
            "transaction_id",
            "invoice_id",
            "transaction_date",
            "customer_id",
            "product_name",
            "quantity",
            "total_amount"
        ]

        available_columns = [
            col for col in display_columns
            if col in sales_df.columns
        ]

        if available_columns:

            st.dataframe(
                sales_df[available_columns].head(10),
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No recent sales data available.")

        st.markdown("---")

        # ---------------- Low Stock Items ---------------- #

        st.subheader("Low Stock Items")

        if low_stock_df.empty:

            st.success("No Low Stock Items")

        else:

            display_inventory = [
                "id",
                "product_id",
                "stock_quantity",
                "low_stock_threshold"
            ]

            available_inventory = [
                col for col in display_inventory
                if col in low_stock_df.columns
            ]

            if available_inventory:

                st.dataframe(
                    low_stock_df[available_inventory],
                    width="stretch",
                    hide_index=True
                )

            else:

                st.info("Inventory columns not available.")

        st.markdown("---")

        # ---------------- Revenue Summary ---------------- #

        st.subheader("Revenue Summary")

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

        

       

    except requests.exceptions.Timeout:

        st.error("Backend request timed out.")

    except requests.exceptions.ConnectionError:

        st.error("Unable to connect to backend.")

    except requests.exceptions.HTTPError as e:

        st.error(f"API Error: {e}")

    except Exception as e:

        st.error(f"Unexpected Error: {e}")