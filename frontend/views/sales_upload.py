import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar

# ================= API Configuration ================= #
from config.config import DB_BASE_URL as BASE_URL

UPLOAD_API = f"{BASE_URL}/api/sales/upload"


# ================= Sales Upload Page ================= #

def sales_upload_page():

    show_sidebar()

    st.title(" Sales Upload")

    st.caption(
        "Upload Sales Transactions CSV to the Backend"
    )

    st.markdown("---")

    if "sales_upload_df" in st.session_state:
        df = st.session_state["sales_upload_df"]
        filename = st.session_state.get("sales_upload_filename", "sales.csv")
        file_size = st.session_state.get("sales_upload_size", 0)

        col_info, col_clear = st.columns([5, 1])
        with col_info:
            st.success(f"📊 Active File: **{filename}** (Ready to validate & upload)")
        with col_clear:
            if st.button("🔄 Choose Different CSV", help="Remove loaded CSV and select a new file", width="stretch"):
                for k in ["sales_upload_df", "sales_upload_filename", "sales_upload_file_bytes", "sales_upload_size"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
    else:
        uploaded_file = st.file_uploader(
            "Choose a CSV File",
            type=["csv"],
            key="sales_upload_file_widget"
        )

        if uploaded_file is None:
            st.info(" Please upload a CSV file to continue.")
            return

        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["sales_upload_df"] = df
            st.session_state["sales_upload_filename"] = uploaded_file.name
            st.session_state["sales_upload_file_bytes"] = uploaded_file.getvalue()
            st.session_state["sales_upload_size"] = uploaded_file.size
            st.rerun()
        except Exception as e:
            st.error(f"❌ Unable to read CSV.\n\n{e}")
            return

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        len(df)
    )

    c2.metric(
        "Columns",
        len(df.columns)
    )

    c3.metric(
        "File Size",
        f"{file_size / 1024:.1f} KB"
    )

    st.markdown("---")

    st.subheader(
        " CSV Preview"
    )

    st.dataframe(
        df.head(10),
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # ================= CSV Validation ================= #

    st.subheader(" CSV Validation")

    COLUMN_ALIASES = {
        "Transaction Date": ["transaction_date", "transaction date", "order_date", "order date", "invoice_date", "date"],
        "Customer ID": ["customer_id", "customer id", "customer"],
        "Product ID": ["product_id", "product id", "product"],
        "Quantity": ["quantity", "qty"],
        "Sales / Total Amount": ["total_amount", "total amount", "amount", "total", "sales", "sale", "revenue"]
    }

    norm_cols = [str(c).strip().lower().replace("-", "_").replace(" ", "_") for c in df.columns]
    missing_fields = []
    detected_fields = []

    for field_name, aliases in COLUMN_ALIASES.items():
        found = False
        for a in aliases:
            if a.replace(" ", "_") in norm_cols:
                found = True
                detected_fields.append(field_name)
                break
        if not found:
            missing_fields.append(field_name)

    if missing_fields:
        st.error("❌ CSV Validation Failed: Required business fields missing.")
        st.write("Missing Required Fields:")
        st.code("\n".join(missing_fields))
        st.info("💡 Supported formats: Superstore CSV (Order Date, Customer ID, Product ID, Quantity, Sales) or Standard Sales CSV.")
        return

    st.success(f"✅ All required sales columns verified ({', '.join(detected_fields)}).")

    c1, c2 = st.columns(2)

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    c1.metric(
        "Missing Values",
        missing_values
    )

    c2.metric(
        "Duplicate Rows",
        duplicate_rows
    )

    if missing_values > 0:

        st.warning(
            f"⚠ {missing_values} missing values found."
        )

    if duplicate_rows > 0:

        st.warning(
            f"⚠ {duplicate_rows} duplicate rows found."
        )

    st.markdown("---")
        # ================= Upload ================= #

    if st.button(
        "Upload Sales Data",
        width="stretch"
    ):

        try:

            file_bytes = st.session_state.get("sales_upload_file_bytes")
            file_name = st.session_state.get("sales_upload_filename", "sales.csv")

            if file_bytes is None and uploaded_file is not None:
                uploaded_file.seek(0)
                file_bytes = uploaded_file.getvalue()
                file_name = uploaded_file.name

            if not file_bytes:
                st.error("No file data available to upload.")
                return

            files = {
                "file": (
                    file_name,
                    file_bytes,
                    "text/csv"
                )
            }

            progress = st.progress(0)

            with st.spinner("Uploading Sales Data..."):

                progress.progress(50)

                response = requests.post(
                    UPLOAD_API,
                    files=files,
                    timeout=60
                )

                progress.progress(100)

            if response.ok:

                from services.sales_service import clear_sales_cache
                clear_sales_cache()

                for k in ["sales_upload_df", "sales_upload_filename", "sales_upload_file_bytes", "sales_upload_size"]:
                    if k in st.session_state:
                        del st.session_state[k]

                st.balloons()

                st.success(
                    " Sales Data Uploaded Successfully!"
                )

            else:

                st.error(
                    f"❌ Upload Failed (HTTP {response.status_code})"
                )

                try:

                    error = response.json()

                    st.error(
                        error.get(
                            "message",
                            "Upload failed."
                        )
                    )

                except Exception:

                    st.write(
                        response.text
                    )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Unable to connect to backend."
            )

        except requests.exceptions.Timeout:

            st.error(
                "❌ Upload timed out."
            )

        except Exception as e:

            st.error(
                f"❌ {e}"
            )