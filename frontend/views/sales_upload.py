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
    """Normalize column names and clean rows to match platform standard schema."""
    df = raw_df.dropna(how="all").copy()
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
    
    # Clean string columns
    for str_col in ["customer_id", "product_id"]:
        if str_col in df.columns:
            df[str_col] = df[str_col].astype(str).str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    # Numeric formatting
    for num_col in ["quantity", "unit_price", "discount", "total_amount"]:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
            
    if "total_amount" not in df.columns and "quantity" in df.columns and "unit_price" in df.columns:
        df["total_amount"] = df["quantity"] * df["unit_price"]
        
    if "unit_price" not in df.columns and "quantity" in df.columns and "total_amount" in df.columns:
        df["unit_price"] = (df["total_amount"] / df["quantity"].replace(0, 1)).round(2)
    elif "unit_price" not in df.columns:
        df["unit_price"] = 0.0

    if "discount" not in df.columns:
        df["discount"] = 0.0

    if "payment_method" not in df.columns:
        df["payment_method"] = "Card"

    if "store_id" not in df.columns:
        df["store_id"] = "1"
        
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    # Drop any corrupt/blank rows
    df = df.dropna(subset=["transaction_date", "customer_id", "product_id", "quantity", "total_amount"])
    df = df[df["quantity"] > 0]
    df = df[df["total_amount"] >= 0]
    df = df.reset_index(drop=True)

    return df


def sales_upload_page():

    show_sidebar()

    st.title(" Sales Upload")
    st.caption("Upload Sales Transactions CSV to append into backend and platform analytics")
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
                    if norm_df.empty:
                        st.error("❌ No valid sales rows found in the CSV file.")
                        return

                    file_name = st.session_state.get("sales_upload_filename", "sales.csv")
                    total_sales_added = float(norm_df["total_amount"].sum()) if "total_amount" in norm_df.columns else 0.0

                    # 1. Register to active session state immediately for 100% instant platform update
                    add_appended_sales_file(file_name, norm_df, total_sales_added)

                    # Clean staging upload states
                    for k in ["sales_upload_df", "sales_upload_filename", "sales_upload_file_bytes", "sales_upload_size"]:
                        if k in st.session_state:
                            del st.session_state[k]

                    # 2. Sync with remote backend database
                    try:
                        upload_csv_bytes = norm_df.to_csv(index=False).encode("utf-8")
                        files = {"file": (file_name, upload_csv_bytes, "text/csv")}
                        requests.post(UPLOAD_API, files=files, timeout=20)
                    except Exception:
                        pass

                    st.balloons()
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Upload processing error: {e}")

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