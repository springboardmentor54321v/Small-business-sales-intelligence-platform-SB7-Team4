import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from components.sidebar import show_sidebar
from models.forecasting import get_forecast_backtest


# ============================================================
# FORECAST VS ACTUAL PAGE
# ============================================================

def forecast_vs_actual_page():

    # ========================================================
    # SIDEBAR
    # ========================================================

    show_sidebar()

    # ========================================================
    # HEADER
    # ========================================================

    st.title("Forecast vs Actual")

    st.caption(
        "Compare AI-predicted sales with actual historical sales"
    )

    st.markdown("---")

    # ========================================================
    # INFORMATION
    # ========================================================

    st.info(
        "Upload your daily sales CSV to compare "
        "Actual Sales vs AI Predicted Sales."
    )

    from models.data_loader import get_active_sales_df, set_active_sales_df

    active_df = get_active_sales_df()
    active_name = st.session_state.get("active_dataset_name", "Default Dataset (All 4 Years)")

    st.info(f"📊 **Current Active Dataset:** `{active_name}` ({len(active_df):,} records)")

    # ========================================================
    # UPLOAD CSV OR USE ACTIVE DATASET
    # ========================================================

    uploaded_file = st.file_uploader(
        "Upload a New Sales CSV (or use currently active dataset)",
        type=["csv"]
    )

    source_data = None
    if uploaded_file is not None:
        source_data = uploaded_file
        # Also auto-update active dataset
        try:
            temp_df = pd.read_csv(uploaded_file)
            set_active_sales_df(temp_df, uploaded_file.name)
            uploaded_file.seek(0)
        except Exception:
            pass
    elif not active_df.empty:
        source_data = active_df
    else:
        st.info("Please upload your sales CSV file.")
        return

    # ========================================================
    # RUN BACKTEST
    # ========================================================

    with st.spinner("Generating Forecast vs Actual analysis..."):
        result = get_forecast_backtest(source_data)

    # ========================================================
    # CHECK ERROR
    # ========================================================

    if result["error"] is not None:

        st.error(
            result["error"]
        )

        return

    df = result["results"]

    metrics = result["metrics"]

    

    # ========================================================
    # CHECK DATA
    # ========================================================

    if df.empty:

        st.warning(
            "No Forecast vs Actual data was returned."
        )

        return

    # ========================================================
    # DATE CONVERSION
    # ========================================================

    if "Order Date" in df.columns:

        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce"
        )

    # ========================================================
    # NUMERIC CONVERSION
    # ========================================================

    if "Actual Sales" in df.columns:

        df["Actual Sales"] = pd.to_numeric(
            df["Actual Sales"],
            errors="coerce"
        )

    if "Predicted Sales" in df.columns:

        df["Predicted Sales"] = pd.to_numeric(
            df["Predicted Sales"],
            errors="coerce"
        )

    df = df.dropna(
        subset=[
            "Order Date",
            "Actual Sales",
            "Predicted Sales"
        ]
    )

    df = df.sort_values(
        "Order Date"
    ).reset_index(
        drop=True
    )

    
    # ========================================================
    # EVALUATION METRICS
    # ========================================================

    st.subheader(
        "Model Evaluation"
    )

    mae = metrics.get(
        "MAE",
        0
    )

    rmse = metrics.get(
        "RMSE",
        0
    )

    mape = metrics.get(
        "MAPE",
        0
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "MAE",
        f"₹ {float(mae):,.2f}"
    )

    k2.metric(
        "RMSE",
        f"₹ {float(rmse):,.2f}"
    )

    k3.metric(
        "MAPE",
        f"{float(mape):,.2f}%"
    )

    k4.metric(
        "Days Compared",
        len(df)
    )

    st.markdown("---")

    # ========================================================
    # FORECAST VS ACTUAL CHART
    # ========================================================

    st.subheader(
        "Actual Sales vs Predicted Sales"
    )

    fig = go.Figure()

    # Actual Sales
    fig.add_trace(
        go.Scatter(
            x=df["Order Date"],
            y=df["Actual Sales"],
            mode="lines+markers",
            name="Actual Sales",
            line=dict(
                width=3
            ),
            marker=dict(
                size=7
            )
        )
    )

    # Predicted Sales
    fig.add_trace(
        go.Scatter(
            x=df["Order Date"],
            y=df["Predicted Sales"],
            mode="lines+markers",
            name="Predicted Sales",
            line=dict(
                width=3,
                dash="dash"
            ),
            marker=dict(
                size=7
            )
        )
    )

    fig.update_layout(
        title="Forecast vs Actual Sales",
        xaxis_title="Date",
        yaxis_title="Sales (₹)",
        template="plotly_dark",
        height=500,
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("---")

    # ========================================================
    # COMPARISON TABLE
    # ========================================================

    st.subheader(
        "Forecast vs Actual Details"
    )

    display_df = df.copy()

    display_df["Actual Sales"] = (
        display_df["Actual Sales"]
        .round(2)
    )

    display_df["Predicted Sales"] = (
        display_df["Predicted Sales"]
        .round(2)
    )

    display_df["Difference"] = (
        display_df["Actual Sales"]
        - display_df["Predicted Sales"]
    ).round(2)

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # ========================================================
    # QUICK INSIGHTS
    # ========================================================

    st.subheader(
        "Forecast Insights"
    )

    average_actual = (
        df["Actual Sales"]
        .mean()
    )

    average_predicted = (
        df["Predicted Sales"]
        .mean()
    )

    highest_actual = (
        df["Actual Sales"]
        .max()
    )

    highest_predicted = (
        df["Predicted Sales"]
        .max()
    )

    i1, i2 = st.columns(2)

    with i1:

        st.info(
            f"""
### Actual Sales

**Average:** ₹ {average_actual:,.2f}

**Highest:** ₹ {highest_actual:,.2f}
"""
        )

    with i2:

        st.info(
            f"""
### Predicted Sales

**Average:** ₹ {average_predicted:,.2f}

**Highest:** ₹ {highest_predicted:,.2f}
"""
        )

    st.markdown("---")

    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.subheader(
        "⬇ Export Analysis"
    )

    csv = df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )

    st.download_button(
        "Download Forecast vs Actual CSV",
        data=csv,
        file_name="forecast_vs_actual.csv",
        mime="text/csv",
        width="stretch"
    )

    
    

    st.caption(
        "MarketMind AI • Forecast vs Actual"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    forecast_vs_actual_page()