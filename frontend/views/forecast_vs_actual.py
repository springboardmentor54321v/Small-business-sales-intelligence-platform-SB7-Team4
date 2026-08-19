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

    # ========================================================
    # UPLOAD CSV / SESSION STATE
    # ========================================================

    if "forecast_backtest_result" in st.session_state:
        result = st.session_state["forecast_backtest_result"]
        filename = st.session_state.get("forecast_backtest_filename", "daily_sales.csv")

        col_info, col_clear = st.columns([5, 1])
        with col_info:
            st.success(f"📊 Active File: **{filename}** (Analysis loaded)")
        with col_clear:
            if st.button("🔄 Upload New CSV", help="Remove saved analysis and upload a new CSV", width="stretch"):
                del st.session_state["forecast_backtest_result"]
                if "forecast_backtest_filename" in st.session_state:
                    del st.session_state["forecast_backtest_filename"]
                st.rerun()
    else:
        uploaded_file = st.file_uploader(
            "Upload Sales CSV",
            type=["csv"],
            key="forecast_vs_actual_uploader"
        )

        if uploaded_file is None:
            col_hint, col_plat = st.columns([3, 2])
            with col_hint:
                st.info("Upload a sales CSV or run analysis directly on platform data.")
            with col_plat:
                if st.button("📊 Analyze Platform Sales Data", help="Run Forecast vs Actual on current platform dataset", width="stretch", type="primary"):
                    from services.sales_service import fetch_all_sales_df
                    import io
                    active_sales = fetch_all_sales_df()
                    if not active_sales.empty:
                        csv_bytes = active_sales[["transaction_date", "total_amount"]].rename(
                            columns={"transaction_date": "Order Date", "total_amount": "Total amount"}
                        ).to_csv(index=False).encode("utf-8")
                        f_obj = io.BytesIO(csv_bytes)
                        f_obj.name = "platform_sales.csv"
                        with st.spinner("Generating Forecast vs Actual from platform data..."):
                            result = get_forecast_backtest(f_obj)
                        if result["error"] is not None:
                            st.error(result["error"])
                            return
                        st.session_state["forecast_backtest_result"] = result
                        st.session_state["forecast_backtest_filename"] = "Platform Active Sales"
                        st.rerun()
                    else:
                        st.warning("No sales transactions found in platform database.")
            return

        with st.spinner("Generating Forecast vs Actual analysis..."):
            result = get_forecast_backtest(uploaded_file)

        if result["error"] is not None:
            st.error(result["error"])
            return

        st.session_state["forecast_backtest_result"] = result
        st.session_state["forecast_backtest_filename"] = uploaded_file.name
        st.rerun()

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