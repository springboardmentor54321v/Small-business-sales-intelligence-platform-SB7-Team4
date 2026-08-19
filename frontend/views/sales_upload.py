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

    uploaded_file = st.file_uploader(
        "Choose a CSV File",
        type=["csv"]
    )

    if uploaded_file is None:

        st.info(
            " Please upload a CSV file to continue."
        )

        return

    # ================= Read CSV ================= #

    try:

        df = pd.read_csv(
            uploaded_file
        )

    except Exception as e:

        st.error(
            f"❌ Unable to read CSV.\n\n{e}"
        )

        return

    st.success(
        " CSV Loaded Successfully"
    )

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
        f"{uploaded_file.size / 1024:.1f} KB"
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

    required_columns = [

        "transaction_id",
        "invoice_id",
        "transaction_date",
        "customer_id",
        "product_id",
        "store_id",
        "quantity",
        "unit_price",
        "discount",
        "total_amount",
        "payment_method"

    ]

    missing_columns = [

        col
        for col in required_columns
        if col not in df.columns

    ]

    if missing_columns:

        st.error("❌ CSV Validation Failed")

        st.write("Missing Columns:")

        st.code("\n".join(missing_columns))

        return

    st.success(" Required columns found.")

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
        use_container_width=True
    ):

        try:

            uploaded_file.seek(0)

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
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