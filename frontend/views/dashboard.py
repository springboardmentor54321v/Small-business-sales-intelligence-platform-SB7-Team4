import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar
from components.cards import show_cards
from components.charts import sales_trend_chart, top_products_chart

# ---------------- API Configuration ---------------- #
import os
BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

SALES_API = f"{BASE_URL}/sales/"
INVENTORY_API = f"{BASE_URL}/inventory/"



# ---------------- Dashboard ---------------- #

def dashboard_page():

    show_sidebar()

    st.title("📊 MarketMind AI Dashboard")
    st.caption("Small Business Sales Intelligence Platform")

    st.markdown("---")

    try:

        with st.spinner("Loading Dashboard..."):

            sales_response = requests.get(SALES_API, timeout=10)
            inventory_response = requests.get(INVENTORY_API, timeout=10)

        if sales_response.status_code != 200:
            st.error(f"❌ Sales API Error ({sales_response.status_code})")
            return

        if inventory_response.status_code != 200:
            st.error(f"❌ Inventory API Error ({inventory_response.status_code})")
            return

        sales = sales_response.json()
        inventory = inventory_response.json()

        sales_df = pd.DataFrame(sales)
        inventory_df = pd.DataFrame(inventory)

        # ---------------- Empty Data Check ---------------- #

        if sales_df.empty:
            st.warning("No Sales Data Available")
            return

        if inventory_df.empty:
            st.warning("No Inventory Data Available")
            return

        # ---------------- Convert Numeric Columns ---------------- #

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

        # ---------------- KPI ---------------- #

        total_revenue = float(
            sales_df["total_amount"].sum()
        )

        total_orders = len(sales_df)

        total_products_sold = int(
            sales_df["quantity"].sum()
        )

        inventory_count = len(inventory_df)

        low_stock_df = inventory_df[
            inventory_df["stock_quantity"]
            <= inventory_df["low_stock_threshold"]
        ]

        metrics = {

            "Revenue": total_revenue,

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
            sales_trend_chart(sales)

        with col2:
            top_products_chart(sales)

        st.markdown("---")

        # ---------------- Recent Sales ---------------- #

        st.subheader("🧾 Recent Sales")

        display_columns = [
            "transaction_id",
            "invoice_id",
            "transaction_date",
            "product_id",
            "quantity",
            "total_amount"
        ]

        available_columns = [
            c for c in display_columns
            if c in sales_df.columns
        ]

        st.dataframe(
            sales_df.sort_values(
                by="transaction_date",
                ascending=False
            )[available_columns].head(10),
            use_container_width=True
        )

        st.markdown("---")

        # ---------------- Low Stock ---------------- #

        st.subheader("⚠ Low Stock Items")

        if low_stock_df.empty:

            st.success("✅ No Low Stock Items")

        else:

            display_inventory = [
                "product_id",
                "stock_quantity",
                "low_stock_threshold"
            ]

            available_inventory = [
                c for c in display_inventory
                if c in low_stock_df.columns
            ]

            st.dataframe(
                low_stock_df[available_inventory],
                use_container_width=True
            )

    except requests.exceptions.Timeout:

        st.error("❌ Backend request timed out.")

    except requests.exceptions.ConnectionError:

        st.error("❌ Unable to connect to backend.")

    except Exception as e:

        st.error(f"❌ Unexpected Error: {e}")
