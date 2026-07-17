import streamlit as st
import pandas as pd
from components.sidebar import show_sidebar


def invoice_page():

    show_sidebar()

    st.title("🧾 Invoice Management")
    st.caption("Create and Manage Customer Invoices")

    st.markdown("---")

    # ---------------- Create Invoice ---------------- #

    st.subheader("➕ Create Invoice")

    customers = [
        "Ravi",
        "Priya",
        "Rahul",
        "Anita",
        "Kiran"
    ]

    products = {
        "Laptop": 50000,
        "Mouse": 800,
        "Keyboard": 1500,
        "Monitor": 12000,
        "Printer": 18000
    }

    col1, col2 = st.columns(2)

    with col1:

        customer = st.selectbox(
            "Select Customer",
            customers
        )

        product = st.selectbox(
            "Select Product",
            list(products.keys())
        )

    with col2:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        unit_price = products[product]

        st.text_input(
            "Unit Price (₹)",
            value=str(unit_price),
            disabled=True
        )

    total = quantity * unit_price

    st.metric(
        "Total Amount",
        f"₹ {total:,}"
    )

    if st.button("🧾 Create Invoice"):

        st.success("✅ Invoice Created Successfully!")
        st.balloons()

    st.markdown("---")

    # ---------------- Dashboard Metrics ---------------- #

    col1, col2, col3 = st.columns(3)

    col1.metric("🧾 Total Invoices", 240)
    col2.metric("💰 Revenue", "₹12,50,000")
    col3.metric("⏳ Pending", 18)

    st.markdown("---")

    # ---------------- Search & Filter ---------------- #

    search = st.text_input("🔍 Search Invoice")

    payment = st.selectbox(
        "Payment Status",
        [
            "All",
            "Paid",
            "Unpaid",
            "Partially Paid"
        ]
    )

    # ---------------- Sample Invoice Data ---------------- #

    df = pd.DataFrame({

        "Invoice ID": [
            "INV001",
            "INV002",
            "INV003",
            "INV004",
            "INV005",
            "INV006",
            "INV007",
            "INV008",
            "INV009",
            "INV010"
        ],

        "Customer": [
            "Ravi",
            "Priya",
            "Rahul",
            "Anita",
            "Kiran",
            "Suresh",
            "Meena",
            "Ajay",
            "Neha",
            "Arjun"
        ],

        "Date": [
            "12-07-2026",
            "12-07-2026",
            "11-07-2026",
            "10-07-2026",
            "10-07-2026",
            "09-07-2026",
            "08-07-2026",
            "08-07-2026",
            "07-07-2026",
            "06-07-2026"
        ],

        "Total Amount": [
            5000,
            7200,
            3400,
            9500,
            1200,
            4200,
            6700,
            8800,
            2500,
            15000
        ],

        "Amount Paid": [
            5000,
            0,
            1500,
            9500,
            1200,
            0,
            3000,
            8800,
            0,
            15000
        ],

        "Balance": [
            0,
            7200,
            1900,
            0,
            0,
            4200,
            3700,
            0,
            2500,
            0
        ],

        "Payment": [
            "Paid",
            "Unpaid",
            "Partially Paid",
            "Paid",
            "Paid",
            "Unpaid",
            "Partially Paid",
            "Paid",
            "Unpaid",
            "Paid"
        ]
    })
        # ---------------- Search ---------------- #

    if search:

        df = df[
            df["Invoice ID"].str.contains(search, case=False) |
            df["Customer"].str.contains(search, case=False)
        ]

    # ---------------- Filter ---------------- #

    if payment != "All":

        df = df[
            df["Payment"] == payment
        ]

    # ---------------- Invoice Table ---------------- #

    st.subheader("📋 Invoice Records")

    def highlight_payment(val):

        if val == "Paid":
            return "background-color:#d4edda;color:green;font-weight:bold;"

        elif val == "Unpaid":
            return "background-color:#f8d7da;color:red;font-weight:bold;"

        elif val == "Partially Paid":
            return "background-color:#fff3cd;color:orange;font-weight:bold;"

        return ""

    styled_df = df.style.map(
        highlight_payment,
        subset=["Payment"]
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ---------------- Invoice Summary ---------------- #

    st.subheader("📊 Invoice Summary")

    total_revenue = df["Total Amount"].sum()
    total_paid = df["Amount Paid"].sum()
    total_balance = df["Balance"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Revenue",
        f"₹ {total_revenue:,}"
    )

    c2.metric(
        "Amount Received",
        f"₹ {total_paid:,}"
    )

    c3.metric(
        "Outstanding Balance",
        f"₹ {total_balance:,}"
    )

    st.markdown("---")

    # ---------------- Download ---------------- #

    st.download_button(
        label="⬇ Download Invoice CSV",
        data=df.to_csv(index=False),
        file_name="invoice_records.csv",
        mime="text/csv",
        use_container_width=True
    )