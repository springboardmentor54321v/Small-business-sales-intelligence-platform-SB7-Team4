import streamlit as st
import pandas as pd
from components.sidebar import show_sidebar


def invoice_page():

    show_sidebar()

    st.title("🧾 Invoice Management")
    st.caption("View customer invoices")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric("🧾 Total Invoices", 240)
    col2.metric("💰 Revenue", "₹12,50,000")
    col3.metric("⏳ Pending", 18)

    st.markdown("---")

    search = st.text_input("🔍 Search Invoice")

    payment = st.selectbox(
        "Payment Status",
        ["All", "Paid", "Pending"]
    )

    df = pd.DataFrame({

        "Invoice ID":[
            "INV001","INV002","INV003","INV004","INV005",
            "INV006","INV007","INV008","INV009","INV010"
        ],

        "Customer":[
            "Ravi","Priya","Rahul","Anita","Kiran",
            "Suresh","Meena","Ajay","Neha","Arjun"
        ],

        "Date":[
            "12-07-2026","12-07-2026","11-07-2026",
            "10-07-2026","10-07-2026","09-07-2026",
            "08-07-2026","08-07-2026","07-07-2026","06-07-2026"
        ],

        "Amount":[
            5000,7200,3400,9500,1200,
            4200,6700,8800,2500,15000
        ],

        "Payment":[
            "Paid","Paid","Pending","Paid","Pending",
            "Paid","Paid","Pending","Paid","Paid"
        ]
    })

    if search:
        df = df[
            df["Invoice ID"].str.contains(search, case=False)
        ]

    if payment != "All":
        df = df[df["Payment"] == payment]

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download Invoice CSV",
        data=df.to_csv(index=False),
        file_name="invoice.csv",
        mime="text/csv"
    )