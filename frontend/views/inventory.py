import streamlit as st
import pandas as pd
from components.sidebar import show_sidebar


def inventory_page():

    show_sidebar()

    st.title("📦 Inventory Management")
    st.caption("Manage and monitor product inventory")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric("📦 Total Products", 125)
    col2.metric("⚠ Low Stock", 12)
    col3.metric("💰 Inventory Value", "₹8,75,000")

    st.markdown("---")

    search = st.text_input("🔍 Search Product")

    status = st.selectbox(
        "Filter Status",
        ["All", "In Stock", "Low Stock"]
    )

    data = pd.DataFrame({

        "Product ID":[
            "P001","P002","P003","P004","P005",
            "P006","P007","P008","P009","P010"
        ],

        "Product":[
            "Laptop","Mouse","Keyboard","Monitor",
            "Printer","Speaker","SSD","Router",
            "Camera","Scanner"
        ],

        "Category":[
            "Electronics","Accessories","Accessories",
            "Electronics","Office","Electronics",
            "Storage","Networking","Electronics","Office"
        ],

        "Stock":[
            50,120,75,10,5,18,40,22,8,15
        ],

        "Price":[
            55000,650,1200,12000,9500,
            3500,4500,2200,38000,9000
        ]
    })

    data["Status"] = data["Stock"].apply(
        lambda x: "Low Stock" if x <= 15 else "In Stock"
    )

    if search:
        data = data[
            data["Product"].str.contains(search, case=False)
        ]

    if status != "All":
        data = data[data["Status"] == status]

    st.dataframe(data, use_container_width=True)

    st.download_button(
        "⬇ Download Inventory CSV",
        data=data.to_csv(index=False),
        file_name="inventory.csv",
        mime="text/csv"
    )