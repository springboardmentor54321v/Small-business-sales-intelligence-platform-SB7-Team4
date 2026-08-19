import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar
from config.config import DB_BASE_URL as BASE_URL
from services.sales_service import (
    add_appended_sales_file,
    remove_appended_sales_file
)

UPLOAD_API = f"{BASE_URL}/api/sales/upload"


def normalize_uploaded_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to match platform standard schema."""
    df = raw_df.copy()
    col_mapping = {}
    
    aliases = {
        "transaction_date": ["transaction_date", "transaction date", "order_date", "order date", "invoice_date", "date"],
        "customer_id": ["customer_id", "customer id", "customer"],
        "product_id": ["product_id", "product id", "product"],
        "quantity": ["quantity", "qty"],
        "total_amount": ["total_amount", "total amount", "amount", "total", "sales", "sale", "revenue"],
        "unit_price": ["unit_price", "unit price", "price"],
        "discount": ["discount"],
        "payment_method": ["payment_method", "payment method", "payment"],
        "store_id": ["store_id", "store id", "store"],
        "city": ["city"],
        "state": ["state"],
        "country": ["country"]
    }
    
    for col in df.columns:
        clean_col = str(col).strip().lower().replace("-", "_").replace(" ", "_")
        for target, alias_list in aliases.items():
            if clean_col in [a.replace(" ", "_") for a in alias_list]:
                col_mapping[col] = target
                break
                
    df = df.rename(columns=col_mapping)
    
    # Numeric formatting
    for num_col in ["quantity", "unit_price", "discount", "total_amount"]:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce").fillna(0)
            
    if "total_amount" not in df.columns and "quantity" in df.columns and "unit_price" in df.columns:
        df["total_amount"] = df["quantity"] * df["unit_price"]
        
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
        
    return df


def sales_upload_page():

    show_sidebar()

    st.title(" Sales Upload")
    st.caption("Upload Sales Transactions CSV to append into backend and platform analytics")
    st.markdown("---")

    # ================= Proof of Recent Append ================= #
    if "sales_upload_proof" in st.session_state:
        proof = st.session_state["sales_upload_proof"]
        st.success(
            f"🎉 **Proof of Append**: Successfully appended **{proof['rows']:,}** records "
            f"from **'{proof['file_name']}'** (Total Sales: **₹ {proof['total']:,.2f}**). "
            f"All dashboards and analytics across the app have updated instantly!"
        )
        if st.button("Dismiss Banner", key="dismiss_proof_btn"):
            del st.session_state["sales_upload_proof"]
            st.rerun()
        st.markdown("---")

    # ================= CSV Upload Input ================= #
    has_staged_file = "sales_upload_df" in st.session_state

    if has_staged_file:
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

        # Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", f"{len(df):,}")
        c2.metric("Columns", len(df.columns))
        c3.metric("File Size", f"{file_size / 1024:.1f} KB")

        st.markdown("### 📋 Data Preview")
        st.dataframe(df.head(10), width="stretch", hide_index=True)
        st.markdown("---")

        # Validation
        st.subheader("🔍 CSV Validation")
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
        else:
            st.success(f"✅ All required sales columns verified ({', '.join(detected_fields)}).")

            c1, c2 = st.columns(2)
            missing_values = int(df.isnull().sum().sum())
            duplicate_rows = int(df.duplicated().sum())
            c1.metric("Missing Values", missing_values)
            c2.metric("Duplicate Rows", duplicate_rows)

            if missing_values > 0:
                st.warning(f"⚠ {missing_values} missing values found.")
            if duplicate_rows > 0:
                st.warning(f"⚠ {duplicate_rows} duplicate rows found.")

            st.markdown("---")

            # Upload Trigger
            if st.button("🚀 Upload & Append Sales Data", width="stretch", type="primary"):
                try:
                    norm_df = normalize_uploaded_df(df)
                    upload_csv_bytes = norm_df.to_csv(index=False).encode("utf-8")
                    file_name = st.session_state.get("sales_upload_filename", "sales.csv")

                    files = {
                        "file": (
                            file_name,
                            upload_csv_bytes,
                            "text/csv"
                        )
                    }

                    progress = st.progress(0)
                    with st.spinner("Uploading and appending sales transactions to backend..."):
                        progress.progress(50)
                        response = requests.post(UPLOAD_API, files=files, timeout=60)
                        progress.progress(100)

                    if response.ok:
                        norm_df = normalize_uploaded_df(df)
                        total_sales_added = float(norm_df["total_amount"].sum()) if "total_amount" in norm_df.columns else 0.0

                        # Register to in-memory/session state dataset for instant app-wide reflection
                        add_appended_sales_file(file_name, norm_df, total_sales_added)

                        st.session_state["sales_upload_proof"] = {
                            "file_name": file_name,
                            "rows": len(norm_df),
                            "total": total_sales_added
                        }

                        for k in ["sales_upload_df", "sales_upload_filename", "sales_upload_file_bytes", "sales_upload_size"]:
                            if k in st.session_state:
                                del st.session_state[k]

                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Upload Failed (HTTP {response.status_code})")
                        try:
                            error = response.json()
                            st.error(error.get("message", "Upload failed."))
                        except Exception:
                            st.write(response.text)

                except requests.exceptions.ConnectionError:
                    st.error("❌ Unable to connect to backend.")
                except requests.exceptions.Timeout:
                    st.error("❌ Upload timed out.")
                except Exception as e:
                    st.error(f"❌ {e}")

    else:
        uploaded_file = st.file_uploader(
            "Choose a CSV File",
            type=["csv"],
            key="sales_upload_file_widget"
        )

        if uploaded_file is not None:
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
        else:
            st.info(" Please upload a CSV file to continue.")

    # ================= Appended Sales Files History ================= #
    st.markdown("---")
    st.subheader("📁 Appended Sales Files History")
    st.caption("Manage all custom CSV files uploaded into the platform. Removing a file instantly updates analytics across all pages.")

    uploaded_history = st.session_state.get("uploaded_sales_files", [])

    if not uploaded_history:
        st.info("ℹ️ No custom appended files currently active. All dashboards are displaying base database records.")
    else:
        tot_custom_rows = sum(f.get("row_count", 0) for f in uploaded_history)
        tot_custom_sales = sum(f.get("total_amount", 0) for f in uploaded_history)

        m1, m2, m3 = st.columns(3)
        m1.metric("Active Uploaded Files", len(uploaded_history))
        m2.metric("Total Appended Rows", f"{tot_custom_rows:,}")
        m3.metric("Total Appended Sales", f"₹ {tot_custom_sales:,.2f}")

        st.markdown("")

        for idx, file_item in enumerate(uploaded_history):
            with st.container(border=True):
                col_left, col_mid, col_right = st.columns([4, 4, 2])
                with col_left:
                    st.markdown(f"📄 **{file_item['file_name']}**")
                    st.caption(f"ID: `{file_item['file_id']}` | Uploaded: {file_item['uploaded_at']}")
                with col_mid:
                    st.markdown(f"**Rows:** {file_item['row_count']:,} &nbsp;|&nbsp; **Sales Volume:** ₹ {file_item['total_amount']:,.2f}")
                with col_right:
                    if st.button("🗑️ Delete / Remove", key=f"delete_file_{file_item['file_id']}", width="stretch", type="secondary"):
                        remove_appended_sales_file(file_item["file_id"])
                        if "sales_upload_proof" in st.session_state:
                            del st.session_state["sales_upload_proof"]
                        st.toast(f"Removed '{file_item['file_name']}' from active dataset.")
                        st.rerun()