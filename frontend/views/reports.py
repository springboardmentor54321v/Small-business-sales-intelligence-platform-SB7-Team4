import streamlit as st
import plotly.express as px

from components.sidebar import show_sidebar
from models.recommendation import get_recommendations
from models.forecasting import get_sales_forecast
from models.anomaly_detection import get_anomaly_alerts
from models.customer_group import get_customer_group
from models.churn import get_churn_risk


def reports_page():

    show_sidebar()

    st.title("📈 AI Reports & Analytics")
    st.caption(
        "AI-powered Forecasting, Recommendations, Anomaly Detection, Customer Segmentation & Churn Prediction"
    )

    st.markdown("---")

    # ================= User Inputs =================

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input(
            "🛒 Product Name",
            value="Staples"
        )

    with col2:
        order_date = st.text_input(
            "📅 Order Date",
            value="2011-01-04"
        )

    customer_id = st.text_input(
        "👤 Customer ID",
        value="AA-10315"
    )

    # ================= Upload Forecast CSV =================

    st.subheader("📂 Upload Sales CSV for Forecast")

    uploaded_file = st.file_uploader(
        "Upload Sales CSV",
        type=["csv"]
    )

    if uploaded_file is not None:
        forecast_df = get_sales_forecast(uploaded_file)
    else:
        forecast_df = None

    # ================= Load Other AI Models =================

    recommendation_df = get_recommendations(product_name)
    anomaly_df = get_anomaly_alerts(order_date)
    customer_group_df = get_customer_group(customer_id)
    churn_df = get_churn_risk(customer_id)

    # ================= Dashboard Metrics =================

    st.markdown("---")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "📈 Forecast",
        len(forecast_df) if forecast_df is not None else 0
    )
    c2.metric(
        "🤖 Recommendations",
        len(recommendation_df)
    )
    c3.metric(
        "🚨 Alerts",
        len(anomaly_df)
    )
    c4.metric(
        "👥 Segments",
        len(customer_group_df)
    )
    c5.metric(
        "📉 Churn",
        len(churn_df)
    )

    st.markdown("---")

    # ================= Sales Forecast =================

    st.subheader("📈 Sales Forecast")

    if forecast_df is not None and not forecast_df.empty:

        fig = px.line(
            forecast_df,
            x="Order Date",
            y="Predicted Sales",
            markers=True,
            title="30-Day Sales Forecast"
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Predicted Sales"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Please upload a sales CSV to generate the forecast.")

    st.markdown("---")

    # ================= Recommendations =================

    st.subheader("🤖 Product Recommendations")

    st.dataframe(
        recommendation_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Anomaly Detection =================

    st.subheader("🚨 Anomaly Detection")

    st.dataframe(
        anomaly_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Customer Segmentation =================

    st.subheader("👥 Customer Segmentation")

    st.dataframe(
        customer_group_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Churn Prediction =================

    st.subheader("📉 Customer Churn Prediction")

    st.dataframe(
        churn_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ================= Downloads =================

    st.subheader("⬇ Export Reports")

    col1, col2, col3 = st.columns(3)

    with col1:
        if forecast_df is not None:
            st.download_button(
                "Forecast CSV",
                forecast_df.to_csv(index=False),
                "forecast.csv",
                "text/csv",
                use_container_width=True
            )

    with col2:
        st.download_button(
            "Recommendations CSV",
            recommendation_df.to_csv(index=False),
            "recommendations.csv",
            "text/csv",
            use_container_width=True
        )

    with col3:
        st.download_button(
            "Alerts CSV",
            anomaly_df.to_csv(index=False),
            "alerts.csv",
            "text/csv",
            use_container_width=True
        )

    st.markdown("---")

    st.success("✅ AI Reports loaded successfully.")


if __name__ == "__main__":
    reports_page()