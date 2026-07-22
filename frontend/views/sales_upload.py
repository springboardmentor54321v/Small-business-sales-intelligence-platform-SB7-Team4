import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar


API_URL = "http://localhost:8000/api/sales/upload"


def sales_upload_page():

    show_sidebar()

    st.title("📤 Sales Upload")

    st.write("Upload Sales Transaction CSV")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Drag & Drop your CSV file here",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            st.success("✅ File uploaded successfully!")

            st.subheader("CSV Preview")

            st.dataframe(df.head(10), use_container_width=True)

            st.markdown("---")

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

            st.subheader("Validation")

            missing_columns = []

            for column in required_columns:

                if column in df.columns:
                    st.success(f"✔ {column}")
                else:
                    st.error(f"❌ Missing: {column}")
                    missing_columns.append(column)

            st.markdown("---")

            if len(missing_columns) == 0:

                st.success("✅ CSV Validation Successful")

                if st.button("🚀 Upload Sales Data", use_container_width=True):

                    try:

                        uploaded_file.seek(0)

                        files = {
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "text/csv"
                            )
                        }

                        with st.spinner("Uploading file to backend..."):

                            response = requests.post(
                                API_URL,
                                files=files
                            )

                        if response.status_code == 200:

                            st.success("✅ Sales Data Uploaded Successfully!")

                            try:
                                st.subheader("Backend Response")
                                st.json(response.json())
                            except Exception:
                                st.write(response.text)

                            st.balloons()

                        elif response.status_code == 400:

                            st.error("❌ Invalid Request")

                            try:
                                st.json(response.json())
                            except Exception:
                                st.write(response.text)

                        elif response.status_code == 500:

                            st.error("❌ Internal Server Error")

                            try:
                                st.json(response.json())
                            except Exception:
                                st.write(response.text)

                        else:

                            st.warning(
                                f"Unexpected Response: {response.status_code}"
                            )

                            st.write(response.text)

                    except requests.exceptions.ConnectionError:

                        st.error("❌ Cannot connect to backend.")

                        st.info(
                            "Make sure the backend server is running on http://localhost:8000"
                        )

                    except Exception as e:

                        st.error(f"Upload Failed: {e}")

            else:

                st.warning("Please upload a valid CSV file.")

        except Exception as e:

            st.error(f"Error reading CSV: {e}")