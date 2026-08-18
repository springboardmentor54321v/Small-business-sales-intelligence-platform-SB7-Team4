import streamlit as st
import pandas as pd
import requests

from components.sidebar import show_sidebar
from models.data_loader import set_active_sales_df, reset_to_default_dataset, get_active_sales_df

# ================= API Configuration ================= #
from config.config import DB_BASE_URL as BASE_URL

UPLOAD_API = f"{BASE_URL}/api/sales/upload"


# ================= Sales Upload Page ================= #

def sales_upload_page():

    show_sidebar()

    st.title("📤 Sales Dataset Upload")
    st.caption("Upload sales CSV dataset to update metrics, charts, and forecasts throughout the app")

    active_name = st.session_state.get("active_dataset_name", "Default Dataset (All 4 Years)")
    st.info(f"📊 **Current Active Dataset:** `{active_name}`")

    col_btn1, col_btn2 = st.columns([2, 2])
    with col_btn2:
        if st.session_state.get("active_sales_df") is not None:
            if st.button("🔄 Reset to Default Dataset", key="reset_dataset_btn", width="stretch"):
                reset_to_default_dataset()
                st.success("Reset back to default multi-year dataset!")
                st.rerun()

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Choose a CSV File (Supports raw sales transactions or daily sales summaries)",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info("💡 Please upload a CSV file (such as `sales_forecast_fixed.csv` or `dataset.csv`) to update all app metrics.")
        return

    # ================= Read CSV ================= #

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Unable to read CSV: {e}")
        return

    st.success("✅ CSV Loaded Successfully")

    # Inspect columns
    col_names = [str(c).strip().lower() for c in df.columns]
    has_date = any(k in col_names for k in ["order date", "order_date", "date", "transaction_date"])
    has_amount = any(k in col_names for k in ["total amount", "total_amount", "sales", "amount", "revenue", "totalsales"])

    if not (has_date and has_amount):
        st.error("❌ CSV Validation Failed: Dataset must contain at least a Date column (`Order Date` / `transaction_date`) and a Sales column (`Total amount` / `sales`).")
        st.write("Found columns:", df.columns.tolist())
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows / Observations", f"{len(df):,}")
    c2.metric("Columns", len(df.columns))
    
    # Calculate revenue preview
    amt_col = [c for c in df.columns if str(c).strip().lower() in ["total amount", "total_amount", "sales", "amount", "revenue", "totalsales"]][0]
    total_rev = float(pd.to_numeric(df[amt_col], errors="coerce").fillna(0.0).sum())
    c3.metric("Total Revenue Preview", f"₹ {total_rev:,.2f}")
    c4.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")

    st.markdown("---")

    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(10), width="stretch", hide_index=True)

    st.markdown("---")

    # ================= Activate Dataset ================= #

    if st.button("🚀 Apply Dataset to Dashboard & Entire Application", type="primary", width="stretch"):
        with st.spinner("Applying dataset and updating all dashboards..."):
            norm_df = set_active_sales_df(df, uploaded_file.name)
            
            # Also try to upload to backend API if reachable
            try:
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                requests.post(UPLOAD_API, files=files, timeout=3.0)
            except Exception:
                pass

        st.balloons()
        st.success(f"🎉 Dataset `{uploaded_file.name}` applied successfully! All {len(norm_df):,} records and ₹ {norm_df['total_amount'].sum():,.2f} total revenue are now live.")
        
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("📊 Go to Dashboard", type="secondary", width="stretch"):
                st.session_state.page = "Dashboard"
                st.rerun()
        with col_nav2:
            if st.button("📈 Go to Business Overview", type="secondary", width="stretch"):
                st.session_state.page = "Business Overview"
                st.rerun()