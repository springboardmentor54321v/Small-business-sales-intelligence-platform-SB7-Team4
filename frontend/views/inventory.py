import streamlit as st
import pandas as pd

from components.sidebar import show_sidebar
from config.config import DB_BASE_URL as BASE_URL
from services.sales_service import fetch_inventory_df


def inventory_page():

    show_sidebar()

    head_col1, head_col2 = st.columns([5, 1])
    with head_col1:
        st.title("Inventory Management")
        st.caption("Manage and Monitor Product Inventory")
    with head_col2:
        if st.button("🔄 Refresh", key="refresh_inventory_btn", width="stretch"):
            fetch_inventory_df.clear()
            st.rerun()

    st.markdown("---")

    # ================= Load Inventory ================= #

    with st.spinner("Loading Inventory..."):
        data = fetch_inventory_df(BASE_URL)

    if data.empty:
        st.warning("No inventory data available.")
        return

    if "Status" not in data.columns:
        data["Status"] = data.apply(
            lambda row: "Low Stock"
            if row.get("stock_quantity", 0) <= row.get("low_stock_threshold", 0)
            else "In Stock",
            axis=1
        )

    # ================= Metrics ================= #

    total_products = len(data)

    low_stock = len(
        data[data["Status"] == "Low Stock"]
    )

    total_stock = int(
        data["stock_quantity"].sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Products",
        total_products
    )

    col2.metric(
        "⚠ Low Stock",
        low_stock
    )

    col3.metric(
        "Total Stock",
        total_stock
    )

    st.markdown("---")

    # ================= Search & Filter ================= #

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input("Search Product ID")

    with col2:
        status = st.selectbox(
            "Filter Status",
            ["All", "In Stock", "Low Stock"]
        )

    filtered_data = data.copy()

    if search:
        filtered_data = filtered_data[
            filtered_data["product_id"]
            .astype(str)
            .str.contains(search, case=False)
        ]

    if status != "All":
        filtered_data = filtered_data[
            filtered_data["Status"] == status
        ]

    # ================= Inventory Table ================= #

    st.subheader("Inventory Records")

    def highlight_status(val):

        if val == "Low Stock":
            return (
                "background-color:#f8d7da;"
                "color:red;"
                "font-weight:bold;"
            )

        return (
            "background-color:#d4edda;"
            "color:green;"
            "font-weight:bold;"
        )

    display_columns = [
        "id",
        "product_id",
        "stock_quantity",
        "low_stock_threshold",
        "Status"
    ]

    available_columns = [
        col for col in display_columns
        if col in filtered_data.columns
    ]

    styled_df = (
        filtered_data[available_columns]
        .style
        .map(
            highlight_status,
            subset=["Status"]
        )
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Inventory Summary ================= #

    st.subheader("Inventory Summary")

    summary = pd.DataFrame({
        "Metric": [
            "Total Products",
            "Total Stock Quantity",
            "Low Stock Items"
        ],
        "Value": [
            total_products,
            total_stock,
            low_stock
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Quick Stock Update ================= #
    with st.expander("⚙️ Update Product Stock Quantity", expanded=False):
        prod_list = data["product_id"].dropna().unique().tolist()
        if prod_list:
            u_col1, u_col2, u_col3 = st.columns([2, 1, 1])
            with u_col1:
                selected_prod = st.selectbox("Select Product ID to Update", prod_list, key="inv_update_prod_select")
            
            # Fetch current stock for selected product
            curr_row = data[data["product_id"] == selected_prod].iloc[0] if not data[data["product_id"] == selected_prod].empty else None
            curr_stock = int(curr_row["stock_quantity"]) if curr_row is not None and "stock_quantity" in curr_row else 0
            curr_thresh = int(curr_row["low_stock_threshold"]) if curr_row is not None and "low_stock_threshold" in curr_row else 10

            with u_col2:
                new_stock = st.number_input("New Stock Quantity", min_value=0, max_value=100000, value=curr_stock, step=1, key="inv_new_stock_input")
            with u_col3:
                new_thresh = st.number_input("Low Stock Threshold", min_value=0, max_value=1000, value=curr_thresh, step=1, key="inv_new_thresh_input")

            if st.button("💾 Save Stock Update", key="inv_save_update_btn", type="primary"):
                try:
                    import requests
                    payload = {"stock_quantity": int(new_stock), "low_stock_threshold": int(new_thresh)}
                    res = requests.put(f"{BASE_URL}/inventory/{selected_prod}", json=payload, timeout=15)
                    if res.ok:
                        fetch_inventory_df.clear()
                        st.success(f"✅ Stock for Product `{selected_prod}` updated to {new_stock} units!")
                        st.rerun()
                    else:
                        st.error(f"❌ Update failed (HTTP {res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"❌ Update error: {e}")

    # ================= Download ================= #

    st.download_button(
        "⬇ Download Inventory CSV",
        data=filtered_data.to_csv(index=False),
        file_name="inventory.csv",
        mime="text/csv",
        use_container_width=True
    )
