import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar
from components.cards import show_cards
from components.charts import (
    sales_trend_chart,
    top_products_chart
)

# ---------------- API Configuration ---------------- #
from config.config import DB_BASE_URL as BASE_URL

INVENTORY_API = f"{BASE_URL}/inventory/"
REVENUE_API = f"{BASE_URL}/revenue/summary"


# ---------------- Cached Data Loader ---------------- #

@st.cache_data(ttl=180, show_spinner=False)
def load_dashboard_raw_data(base_url, inventory_url, revenue_url):
    sales = []
    inventory = []
    revenue = {}

    # 1. Fetch Sales
    page = 1
    page_size = 1000
    while True:
        url = f"{base_url}/sales/?page={page}&page_size={page_size}"
        try:
            sales_res = requests.get(url, timeout=4)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            sales_res = requests.get(url, timeout=45)
        sales_res.raise_for_status()
        page_data = sales_res.json()
        if not page_data:
            break
        sales.extend(page_data)
        if len(page_data) < page_size:
            break
        page += 1

    # 2. Fetch Inventory
    try:
        inventory_response = requests.get(inventory_url, timeout=4)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        inventory_response = requests.get(inventory_url, timeout=20)
    inventory_response.raise_for_status()
    inventory = inventory_response.json()

    # 3. Fetch Revenue
    try:
        revenue_response = requests.get(revenue_url, timeout=4)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        revenue_response = requests.get(revenue_url, timeout=20)
    revenue_response.raise_for_status()
    revenue = revenue_response.json()

    return sales, inventory, revenue


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

    st.markdown("---")

    db_error = False
    sales = []
    inventory = []
    revenue = {}

    with st.spinner("Loading Dashboard..."):
        try:
            sales, inventory, revenue = load_dashboard_raw_data(BASE_URL, INVENTORY_API, REVENUE_API)
        except Exception:
            db_error = True

    if db_error:
        st.warning("⚠️ The remote database server is currently sleeping or experiencing connection issues on Render. The dashboard will automatically update once it wakes up.")
        st.info("💡 Please wait 10-15 seconds and try refreshing the page, or verify the database service status in your Render dashboard.")
        return

    sales_df = pd.DataFrame(sales)
    inventory_df = pd.DataFrame(inventory)

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

                sales_df[col] = pd.to_numeric(
                    sales_df[col],
                    errors="coerce"
                ).fillna(0)

        numeric_inventory = [
            "stock_quantity",
            "low_stock_threshold"
        ]

        for col in numeric_inventory:

            if col in inventory_df.columns:

                inventory_df[col] = pd.to_numeric(
                    inventory_df[col],
                    errors="coerce"
                ).fillna(0)

        # ---------------- Date Conversion ---------------- #

        if "transaction_date" in sales_df.columns:

            sales_df["transaction_date"] = pd.to_datetime(
                sales_df["transaction_date"],
                errors="coerce"
            )

            sales_df = sales_df.sort_values(
                by="transaction_date",
                ascending=False
            )
                # ---------------- KPI Values ---------------- #

        total_revenue = float(
            revenue.get("total_revenue") or 0
        )

        total_outstanding = float(
            revenue.get("total_outstanding") or 0
        )

        daily_collections = float(
            revenue.get("daily_collections") or 0
        )

        total_orders = len(sales_df)

        if "quantity" in sales_df.columns:
            total_products_sold = int(
                sales_df["quantity"].sum()
            )
        else:
            total_products_sold = 0

        inventory_count = len(inventory_df)

        if (
            "stock_quantity" in inventory_df.columns
            and
            "low_stock_threshold" in inventory_df.columns
        ):

            low_stock_df = inventory_df[
                inventory_df["stock_quantity"]
                <= inventory_df["low_stock_threshold"]
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

        # ---------------- KPI Cards ---------------- #

        show_cards(metrics)

        st.markdown("---")

        # ---------------- Charts ---------------- #

        col1, col2 = st.columns(2)

        with col1:

            sales_trend_chart(sales_df)

        with col2:

            top_products_chart(sales_df)

        st.markdown("---")  
                # ---------------- Recent Sales ---------------- #

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