import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar

# ================= API Configuration ================= #

BASE_URL = "BASE_URL = "https://undefined-arrest-crescent.ngrok-free.dev/docs""
UPLOAD_API = f"{BASE_URL}/api/sales/upload"


def sales_upload_page():

    show_sidebar()

    st.title("📤 Sales Upload")
    st.caption("Upload Sales Transactions CSV to the Backend")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info("📁 Please upload a CSV file to continue.")
        return

    # ================= Read CSV ================= #

    try:

        df = pd.read_csv(uploaded_file)

    except Exception as e:

        st.error(f"❌ Unable to read CSV.\n\n{e}")
        return

    st.success("✅ CSV Loaded Successfully")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows",
        len(df)
    )

    col2.metric(
        "Columns",
        len(df.columns)
    )

    col3.metric(
        "File Size",
        f"{uploaded_file.size / 1024:.1f} KB"
    )

    st.markdown("---")

    st.subheader("CSV Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Validation ================= #

    st.subheader("CSV Validation")

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

        st.error("❌ Validation Failed")

        st.write("Missing Columns:")

        st.code("\n".join(missing_columns))

        return

    st.success("✅ CSV Validation Successful")

    st.markdown("---")

    # ================= Upload ================= #

    if st.button(
        "🚀 Upload Sales Data",
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

            with st.spinner("Uploading sales data..."):

                progress.progress(30)

                response = requests.post(

                    UPLOAD_API,

                    files=files,

                    timeout=60

                )

                progress.progress(100)

            if response.ok:

                st.success("🎉 Sales Data Uploaded Successfully!")

                st.balloons()

                st.subheader("Backend Response")

                try:

                    st.json(response.json())

                except Exception:

                    st.write(response.text)

            else:

                st.error(
                    f"❌ Upload Failed (HTTP {response.status_code})"
                )

                try:

                    st.json(response.json())

                except Exception:

                    st.write(response.text)

        except requests.exceptions.ConnectionError:

            st.error("❌ Unable to connect to backend server.")

        except requests.exceptions.Timeout:

            st.error("❌ Upload timed out.")

        except Exception as e:

            st.error(f"❌ {e}")

    st.markdown("---")

    st.info(
        "Supported format: CSV with the required sales transaction columns."
    )