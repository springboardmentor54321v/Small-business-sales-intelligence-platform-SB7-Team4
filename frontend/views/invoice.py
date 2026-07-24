import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar

# ================= API Configuration ================= #

BASE_URL = "BASE_URL = "https://undefined-arrest-crescent.ngrok-free.dev""

INVOICE_API = f"{BASE_URL}/invoices/"


def invoice_page():

    show_sidebar()

    st.title("🧾 Invoice Management")
    st.caption("Create and Manage Customer Invoices")

    st.markdown("---")

    # ================= Create Invoice ================= #

    st.subheader("➕ Create Invoice")

    col1, col2 = st.columns(2)

    with col1:

        customer_id = st.text_input(
            "Customer ID",
            placeholder="RH-19495"
        )

        store_id = st.text_input(
            "Store ID",
            value="STORE001"
        )

        created_by = st.number_input(
            "Created By User ID",
            min_value=1,
            value=1
        )

    with col2:

        invoice_date = st.date_input(
            "Invoice Date"
        )

        due_date = st.date_input(
            "Due Date"
        )

    notes = st.text_area(
        "Notes",
        placeholder="Enter invoice notes..."
    )

    st.markdown("### Invoice Item")

    item_col1, item_col2 = st.columns(2)

    with item_col1:

        product_id = st.text_input(
            "Product ID",
            placeholder="OFF-AP-10004246"
        )

    with item_col2:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

    payload = {

        "customer_id": customer_id,

        "store_id": store_id,

        "created_by_user_id": created_by,

        "invoice_date": str(invoice_date),

        "due_date": str(due_date),

        "notes": notes,

        "items": [

            {

                "product_id": product_id,

                "quantity": quantity

            }

        ]

    }

    if st.button(
        "🧾 Create Invoice",
        use_container_width=True
    ):

        try:

            with st.spinner("Creating Invoice..."):

                response = requests.post(
                    INVOICE_API,
                    json=payload,
                    timeout=30
                )

            if response.status_code in [200, 201]:

                st.success("✅ Invoice Created Successfully")

                try:

                    st.json(response.json())

                except Exception:

                    st.write(response.text)

            else:

                st.error(
                    f"Failed (HTTP {response.status_code})"
                )

                try:

                    st.json(response.json())

                except Exception:

                    st.write(response.text)

        except requests.exceptions.ConnectionError:

            st.error("❌ Unable to connect to backend.")

        except requests.exceptions.Timeout:

            st.error("❌ Request timed out.")

        except Exception as e:

            st.error(str(e))

    st.markdown("---")

    # ================= Load Invoice Records ================= #

    try:

        response = requests.get(
            INVOICE_API,
            timeout=10
        )

        response.raise_for_status()

        invoices = response.json()

        df = pd.DataFrame(invoices)

    except Exception as e:

        st.error(f"Unable to load invoices: {e}")
        return

    if df.empty:

        st.warning("No invoice records found.")
        return
        # ================= Dashboard Metrics ================= #

    total_invoices = len(df)

    total_amount = 0

    if "total_amount" in df.columns:

        df["total_amount"] = pd.to_numeric(
            df["total_amount"],
            errors="coerce"
        ).fillna(0)

        total_amount = df["total_amount"].sum()

    pending = 0

    if "status" in df.columns:

        pending = len(
            df[
                df["status"]
                .astype(str)
                .str.lower()
                != "paid"
            ]
        )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🧾 Total Invoices",
        total_invoices
    )

    c2.metric(
        "💰 Revenue",
        f"₹ {total_amount:,.2f}"
    )

    c3.metric(
        "⏳ Pending",
        pending
    )

    st.markdown("---")

    # ================= Search ================= #

    search = st.text_input(
        "🔍 Search Invoice"
    )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False
                ).any(),
                axis=1
            )
        ]

    st.subheader("📋 Invoice Records")

    if "status" in filtered_df.columns:

        def highlight_status(val):

            value = str(val).lower()

            if value == "paid":

                return (
                    "background-color:#d4edda;"
                    "color:green;"
                    "font-weight:bold;"
                )

            elif value == "pending":

                return (
                    "background-color:#fff3cd;"
                    "color:orange;"
                    "font-weight:bold;"
                )

            elif value == "unpaid":

                return (
                    "background-color:#f8d7da;"
                    "color:red;"
                    "font-weight:bold;"
                )

            return ""

        styled_df = filtered_df.style.map(
            highlight_status,
            subset=["status"]
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # ================= Invoice Summary ================= #

    st.subheader("📊 Invoice Summary")

    summary = pd.DataFrame({

        "Metric": [

            "Total Invoices",

            "Revenue",

            "Pending"

        ],

        "Value": [

            total_invoices,

            f"₹ {total_amount:,.2f}",

            pending

        ]

    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Download ================= #

    st.download_button(

        "⬇ Download Invoice CSV",

        data=filtered_df.to_csv(index=False),

        file_name="invoice_records.csv",

        mime="text/csv",

        use_container_width=True

    )

    st.success(
        "✅ Invoice records loaded successfully from the backend."
    )