import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar

# ================= API Configuration ================= #
from config.config import DB_BASE_URL as BASE_URL

INVOICE_API = f"{BASE_URL}/invoices/"


@st.cache_data(ttl=300, show_spinner=False)
def fetch_invoices_data(api_url):
    response = requests.get(api_url, timeout=15)
    response.raise_for_status()
    return response.json()


# ================= Invoice Page ================= #

def invoice_page():

    show_sidebar()

    st.title("Invoice Management")
    st.caption("Create and Manage Customer Invoices")

    st.markdown("---")

    # ================= Create Invoice ================= #

    st.subheader(" Create Invoice")

    col1, col2 = st.columns(2)

    with col1:

        customer_id = st.text_input(
            "Customer ID",
            placeholder="JD-16150"
        )

        store_id = st.text_input(
            "Store ID",
            placeholder="115"
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
            placeholder="FUR-CH-10003861"
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
        "Create Invoice",
        width="stretch"
    ):

        try:

            with st.spinner("Creating Invoice..."):

                response = requests.post(
                    INVOICE_API,
                    json=payload,
                    timeout=30
                )

            response.raise_for_status()

            data = response.json()

            st.success("Invoice created successfully!")
            fetch_invoices_data.clear()

            st.markdown("### Invoice Details")

            left, right = st.columns(2)

            with left:

                st.metric(
                    "Invoice Number",
                    data.get("invoice_number", "-")
                )

                st.metric(
                    "Customer ID",
                    data.get("customer_id", "-")
                )

                st.metric(
                    "Store ID",
                    data.get("store_id", "-")
                )

            with right:

                amount = float(
                    data.get("total_amount", 0)
                )

                st.metric(
                    "Total Amount",
                    f"₹ {amount:,.2f}"
                )

                st.metric(
                    "Payment Status",
                    data.get("payment_status", "-")
                )

                st.metric(
                    "Invoice Status",
                    data.get("invoice_status", "-")
                )

        except requests.exceptions.Timeout:

            st.error("❌ Request timed out.")

        except requests.exceptions.ConnectionError:

            st.error("❌ Unable to connect to backend.")

        except requests.exceptions.HTTPError:

            st.error("❌ Invoice creation failed.")

            try:

                st.json(response.json())

            except Exception:

                st.write(response.text)

        except Exception as e:

            st.error(f"❌ {e}")

    st.markdown("---")
    # ================= Load Invoice Records ================= #

    try:

        with st.spinner("Loading Invoice Records..."):

            invoices = fetch_invoices_data(INVOICE_API)

        if not invoices or len(invoices) == 0:

            st.warning("No invoice records found.")
            return

        df = pd.DataFrame(invoices)

    except requests.exceptions.Timeout:

        st.error("❌ Backend request timed out.")
        return

    except requests.exceptions.ConnectionError:

        st.error("❌ Unable to connect to backend.")
        return

    except requests.exceptions.HTTPError as e:

        st.error(f"❌ API Error: {e}")
        return

    except Exception as e:

        st.error(f"❌ Unexpected Error: {e}")
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

   

    c1, c2 = st.columns(2)

    c1.metric(
        "Total Invoices",
        total_invoices
    )

    c2.metric(
        "Revenue",
        f"₹ {total_amount:,.2f}"
    )

   

    st.markdown("---")
    # ================= Search ================= #

    search = st.text_input(
        "Search Invoice"
    )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

    st.subheader("Invoice Records")

    if "payment_status" in filtered_df.columns:

        def highlight_status(value):

            value = str(value).lower()

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
            subset=["payment_status"]
        )

        st.dataframe(
            styled_df,
            width="stretch",
            hide_index=True
        )

    else:

        st.dataframe(
            filtered_df,
            width="stretch",
            hide_index=True
        )

    st.markdown("---")

    
    # ================= Download ================= #

    st.download_button(
        label="Download Invoice CSV",
        data=filtered_df.to_csv(index=False),
        file_name="invoice_records.csv",
        mime="text/csv",
        width="stretch"
    )

    st.markdown("---")

    # ================= Refresh ================= #

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Refresh",
            width="stretch"
        ):

            st.rerun()

    with col2:

        st.button(
            "Dashboard Updated",
            disabled=True,
            width="stretch"
        )

    

    st.caption(
        "MarketMind AI • Invoice Management • Version 2.0"
    )
