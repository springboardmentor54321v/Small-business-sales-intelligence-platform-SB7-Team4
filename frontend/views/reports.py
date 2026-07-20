import streamlit as st
import plotly.express as px

from components.sidebar import show_sidebar
from models.recommendation import get_recommendations
from models.forecasting import get_sales_forecast
from models.anomaly_detection import get_anomaly_alerts


def reports_page():

    show_sidebar()

    st.title("📈 AI Reports & Analytics")
    st.caption("Sales Forecast, Product Recommendations & Anomaly Alerts")

    st.markdown("---")

    # ---------------- Sales Forecast ---------------- #

    st.subheader("📈 Sales Forecast")

    forecast_df = get_sales_forecast()

    fig = px.line(
        forecast_df,
        x="Month",
        y="Predicted Sales",
        markers=True,
        title="Monthly Sales Forecast"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("---")

    # ---------------- Recommendations ---------------- #

    st.subheader("🤖 AI Product Recommendations")

    recommendation_df = get_recommendations()

    st.dataframe(
        recommendation_df,
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # ---------------- Anomaly Detection ---------------- #

    st.subheader("🚨 Anomaly Alerts")

    anomaly_df = get_anomaly_alerts()

    st.dataframe(
        anomaly_df,
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # ---------------- Download Reports ---------------- #

    st.download_button(
        "⬇ Download Recommendations",
        recommendation_df.to_csv(index=False),
        "recommendations.csv",
        "text/csv",
        width="stretch"
    )

    st.download_button(
        "⬇ Download Forecast",
        forecast_df.to_csv(index=False),
        "forecast.csv",
        "text/csv",
        width="stretch"
    )

    st.download_button(
        "⬇ Download Alerts",
        anomaly_df.to_csv(index=False),
        "alerts.csv",
        "text/csv",
        width="stretch"
    )