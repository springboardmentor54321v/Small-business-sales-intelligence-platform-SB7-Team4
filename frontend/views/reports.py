import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import show_sidebar
from models.recommendation import get_recommendations
from models.forecasting import get_sales_forecast
from models.anomaly_detection import get_anomaly_alerts
from models.customer_group import get_customer_group
from models.churn import get_churn_risk


def reports_page():

    # ============================================================
    # SIDEBAR
    # ============================================================

    show_sidebar()

    # ============================================================
    # HEADER
    # ============================================================

    st.title("AI Reports & Analytics")

    st.caption(
        "AI-powered Forecasting, Recommendations, Anomaly Detection, "
        "Customer Segmentation & Churn Prediction"
    )

    st.markdown("---")

    # ============================================================
    # USER INPUTS
    # ============================================================

    col1, col2 = st.columns(2)

    with col1:

        product_name = st.text_input(
            "Product Name",
            placeholder="Enter exact product name",
            key="report_product"
        )

    with col2:

        order_date = st.text_input(
            "Order Date",
            value="2011-01-04",
            key="report_order_date"
        )

    customer_id = st.text_input(
        "Customer ID",
        value="AA-10315",
        key="report_customer"
    )

    # ============================================================
    # FORECAST CSV
    # ============================================================

    st.subheader("Sales Forecast")

    uploaded_file = None
    if "reports_uploaded_file_bytes" in st.session_state:
        r_fname = st.session_state.get("reports_uploaded_filename", "sales.csv")
        r_col_info, r_col_clear = st.columns([5, 1])
        with r_col_info:
            st.success(f"📊 Active File: **{r_fname}** (Ready for Report)")
        with r_col_clear:
            if st.button("🔄 Change CSV", key="clear_reports_csv", help="Clear uploaded CSV and choose another file", width="stretch"):
                if "reports_uploaded_file_bytes" in st.session_state:
                    del st.session_state["reports_uploaded_file_bytes"]
                if "reports_uploaded_filename" in st.session_state:
                    del st.session_state["reports_uploaded_filename"]
                st.rerun()
    else:
        uploaded_file = st.file_uploader(
            "Upload Sales CSV",
            type=["csv"],
            key="report_sales_file"
        )

        if uploaded_file is not None:
            st.session_state["reports_uploaded_file_bytes"] = uploaded_file.getvalue()
            st.session_state["reports_uploaded_filename"] = uploaded_file.name
            st.rerun()

    # ============================================================
    # GENERATE BUTTON
    # ============================================================

    st.markdown("")

    generate = st.button(
        "Generate Reports",
        width="stretch",
        type="primary"
    )

    # ============================================================
    # CALL BACKEND ONLY AFTER BUTTON CLICK
    # ============================================================

    if generate:

        # --------------------------------------------
        # Validate inputs
        # --------------------------------------------

        if not product_name.strip():

            st.warning(
                "Please enter a Product Name."
            )

            return

        if not customer_id.strip():

            st.warning(
                "Please enter a Customer ID."
            )

            return

        if not order_date.strip():

            st.warning(
                "Please enter an Order Date."
            )

            return

        # --------------------------------------------
        # Backend calls
        # --------------------------------------------

        with st.spinner(
            "Generating AI reports..."
        ):

            # ========================================
            # FORECAST
            # ========================================

            report_file_bytes = st.session_state.get("reports_uploaded_file_bytes")
            report_file_name = st.session_state.get("reports_uploaded_filename", "sales.csv")

            if report_file_bytes is not None:
                import io
                f_obj = io.BytesIO(report_file_bytes)
                f_obj.name = report_file_name
                forecast_df = get_sales_forecast(f_obj)
            elif uploaded_file is not None:
                forecast_df = get_sales_forecast(
                    uploaded_file
                )
            else:
                from services.sales_service import fetch_all_sales_df
                import io
                active_sales = fetch_all_sales_df()
                if not active_sales.empty:
                    csv_bytes = active_sales[["transaction_date", "total_amount"]].rename(
                        columns={"transaction_date": "Order Date", "total_amount": "Total amount"}
                    ).to_csv(index=False).encode("utf-8")
                    f_obj = io.BytesIO(csv_bytes)
                    f_obj.name = "platform_sales.csv"
                    forecast_df = get_sales_forecast(f_obj)
                else:
                    forecast_df = pd.DataFrame()

            # ========================================
            # RECOMMENDATIONS
            # ========================================

            recommendation_df = get_recommendations(
                product_name.strip()
            )

            # ========================================
            # ANOMALY
            # ========================================

            anomaly_df = get_anomaly_alerts(
                order_date.strip()
            )

            # ========================================
            # CUSTOMER SEGMENTATION
            # ========================================

            customer_group_df = get_customer_group(
                customer_id.strip()
            )

            # ========================================
            # CHURN
            # ========================================

            churn_df = get_churn_risk(
                customer_id.strip()
            )

        # --------------------------------------------
        # Save results in session state
        # --------------------------------------------

        st.session_state["reports_generated"] = True

        st.session_state["forecast_df"] = forecast_df

        st.session_state[
            "recommendation_df"
        ] = recommendation_df

        st.session_state[
            "anomaly_df"
        ] = anomaly_df

        st.session_state[
            "customer_group_df"
        ] = customer_group_df

        st.session_state[
            "churn_df"
        ] = churn_df

        st.success(
            "AI reports generated successfully."
        )

    # ============================================================
    # LOAD RESULTS FROM SESSION
    # ============================================================

    forecast_df = st.session_state.get(
        "forecast_df",
        pd.DataFrame()
    )

    recommendation_df = st.session_state.get(
        "recommendation_df",
        pd.DataFrame()
    )

    anomaly_df = st.session_state.get(
        "anomaly_df",
        pd.DataFrame()
    )

    customer_group_df = st.session_state.get(
        "customer_group_df",
        pd.DataFrame()
    )

    churn_df = st.session_state.get(
        "churn_df",
        pd.DataFrame()
    )

    reports_generated = st.session_state.get(
        "reports_generated",
        False
    )

    # ============================================================
    # STOP HERE IF NO REPORTS GENERATED
    # ============================================================

    if not reports_generated:

        st.info(
            "Enter the required details and click "
            "**Generate Reports**."
        )

        return

    # ============================================================
    # DASHBOARD METRICS
    # ============================================================

    st.markdown("---")

    c1, c2, c3, c4, c5 = st.columns(5)

    # Forecast count
    c1.metric(
        "Forecast",
        len(forecast_df)
    )

    # Recommendation count
    if (
        not recommendation_df.empty
        and "Error" not in recommendation_df.columns
    ):

        recommendation_count = len(
            recommendation_df
        )

    else:

        recommendation_count = 0

    c2.metric(
        "Recommendations",
        recommendation_count
    )

    # Anomaly count
    if (
        not anomaly_df.empty
        and "Error" not in anomaly_df.columns
    ):

        alert_count = len(
            anomaly_df
        )

    else:

        alert_count = 0

    c3.metric(
        "Alerts",
        alert_count
    )

    # Customer segment
    if (
        not customer_group_df.empty
        and "Error" not in customer_group_df.columns
    ):

        segment_count = len(
            customer_group_df
        )

    else:

        segment_count = 0

    c4.metric(
        "Segments",
        segment_count
    )

    # Churn
    if (
        not churn_df.empty
        and "Error" not in churn_df.columns
    ):

        churn_count = len(
            churn_df
        )

    else:

        churn_count = 0

    c5.metric(
        "📉 Churn",
        churn_count
    )

    # ============================================================
    # SALES FORECAST
    # ============================================================

    st.markdown("---")

    st.subheader("📈 Sales Forecast")

    if forecast_df.empty:

        st.info(
            "No forecast data available. "
            "Upload a valid sales CSV."
        )

    elif "Error" in forecast_df.columns:

        st.error(
            forecast_df.iloc[0]["Error"]
        )

    else:

        # --------------------------------------------
        # Date conversion
        # --------------------------------------------

        if "Order Date" in forecast_df.columns:

            forecast_df["Order Date"] = pd.to_datetime(
                forecast_df["Order Date"],
                errors="coerce"
            )

            forecast_df = forecast_df.sort_values(
                "Order Date"
            )

        # --------------------------------------------
        # Forecast calculations
        # --------------------------------------------

        if "Predicted Sales" in forecast_df.columns:

            total_forecast = forecast_df[
                "Predicted Sales"
            ].sum()

            average_forecast = forecast_df[
                "Predicted Sales"
            ].mean()

            highest_forecast = forecast_df[
                "Predicted Sales"
            ].max()

            f1, f2, f3 = st.columns(3)

            f1.metric(
                "Total Forecast",
                f"₹ {total_forecast:,.2f}"
            )

            f2.metric(
                "Average Daily Sales",
                f"₹ {average_forecast:,.2f}"
            )

            f3.metric(
                "Highest Forecast",
                f"₹ {highest_forecast:,.2f}"
            )

            # ----------------------------------------
            # Forecast chart
            # ----------------------------------------

            fig = px.line(
                forecast_df,
                x="Order Date",
                y="Predicted Sales",
                markers=True,
                title="30-Day Sales Forecast"
            )

            fig.update_layout(
                height=420,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                ),
                xaxis_title="Date",
                yaxis_title="Predicted Sales (₹)"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.warning(
                "Predicted Sales column was not returned."
            )

    # ============================================================
    # PRODUCT RECOMMENDATIONS
    # ============================================================

    st.markdown("---")

    st.subheader("Product Recommendations")

    if recommendation_df.empty:

        st.info(
            "No recommendations returned by the backend."
        )

    elif "Error" in recommendation_df.columns:

        st.error(
            recommendation_df.iloc[0]["Error"]
        )

    else:

        st.caption(
            f"Recommendations generated by the backend "
            f"for **{product_name}**."
        )

        # IMPORTANT:
        # Do NOT insert Rank here.
        #
        # get_recommendations() already creates Rank.
        #
        # This fixes:
        # ValueError: cannot insert Rank, already exists

        st.dataframe(
            recommendation_df,
            width="stretch",
            hide_index=True
        )

    # ============================================================
    # ANOMALY DETECTION
    # ============================================================

    st.markdown("---")

    st.subheader("Anomaly Detection")

    if anomaly_df.empty:

        st.info(
            "No anomaly result returned by the backend."
        )

    elif "Error" in anomaly_df.columns:

        st.error(
            anomaly_df.iloc[0]["Error"]
        )

    else:

        anomaly_display = anomaly_df.copy()

        # --------------------------------------------
        # Convert backend Anomaly value to display
        # --------------------------------------------

        if "Anomaly" in anomaly_display.columns:

            def format_anomaly(value):

                if isinstance(value, bool):

                    is_anomaly = value

                else:

                    is_anomaly = (
                        str(value).strip().lower()
                        in ["true", "1", "yes"]
                    )

                if is_anomaly:

                    return "🚨 Anomaly"

                return "✅ Normal"

            anomaly_display["Anomaly"] = (
                anomaly_display["Anomaly"]
                .apply(format_anomaly)
            )

        # --------------------------------------------
        # Format date
        # --------------------------------------------

        if "Order Date" in anomaly_display.columns:

            try:

                anomaly_display["Order Date"] = (
                    pd.to_datetime(
                        anomaly_display["Order Date"],
                        errors="coerce"
                    )
                    .dt.strftime("%d-%b-%Y")
                )

            except Exception:

                pass


        styled_anomaly = anomaly_display.style.set_properties(
            subset=["Total Sales"],
            **{"text-align": "center"}
        )

        st.dataframe(
            styled_anomaly,
            width="stretch",
            hide_index=True
        )

    # ============================================================
    # CUSTOMER SEGMENTATION
    # ============================================================

    st.markdown("---")

    st.subheader(" Customer Segmentation")

    if customer_group_df.empty:

        st.info(
            "No customer segmentation result "
            "returned by the backend."
        )

    elif "Error" in customer_group_df.columns:

        st.error(
            customer_group_df.iloc[0]["Error"]
        )

    else:

        st.caption(
            f"Customer segmentation returned by the backend "
            f"for **{customer_id}**."
        )

        st.dataframe(
            customer_group_df,
            width="stretch",
            hide_index=True
        )

    # ============================================================
    # CUSTOMER CHURN
    # ============================================================

    st.markdown("---")

    st.subheader(" Customer Churn Prediction")

    if churn_df.empty:

        st.info(
            "No churn prediction returned by the backend."
        )

    elif "Error" in churn_df.columns:

        st.error(
            churn_df.iloc[0]["Error"]
        )

    else:

        st.caption(
            f"Churn prediction returned by the backend "
            f"for **{customer_id}**."
        )

        st.dataframe(
            churn_df,
            width="stretch",
            hide_index=True
        )

    # ============================================================
    # EXPORT REPORTS
    # ============================================================

    st.markdown("---")

    st.subheader("Export Reports")

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------
    # Forecast CSV
    # --------------------------------------------

    with col1:

        if (
            not forecast_df.empty
            and "Error" not in forecast_df.columns
        ):

            st.download_button(
                label=" Forecast CSV",
                data=forecast_df.to_csv(
                    index=False
                ),
                file_name="forecast.csv",
                mime="text/csv",
                width="stretch"
            )

    # --------------------------------------------
    # Recommendations CSV
    # --------------------------------------------

    with col2:

        if (
            not recommendation_df.empty
            and "Error" not in recommendation_df.columns
        ):

            st.download_button(
                label=" Recommendations CSV",
                data=recommendation_df.to_csv(
                    index=False
                ),
                file_name="recommendations.csv",
                mime="text/csv",
                width="stretch"
            )

    # --------------------------------------------
    # Anomaly CSV
    # --------------------------------------------

    with col3:

        if (
            not anomaly_df.empty
            and "Error" not in anomaly_df.columns
        ):

            st.download_button(
                label=" Alerts CSV",
                data=anomaly_df.to_csv(
                    index=False
                ),
                file_name="alerts.csv",
                mime="text/csv",
                width="stretch"
            )

    

    st.caption(
        "MarketMind AI • AI Reports & Analytics • Version 1.0"
    )


# ================================================================
# RUN PAGE
# ================================================================

if __name__ == "__main__":
    reports_page()