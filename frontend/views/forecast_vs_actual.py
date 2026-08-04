import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import show_sidebar

def forecast_vs_actual_page():

    # ================= Sidebar ================= #

    show_sidebar()

    # ================= Header ================= #

    st.title(" Forecast vs Actual Dashboard")
    st.caption("AI-Powered Sales Forecast Analytics")

    st.write("Monitor forecast performance and compare it with actual sales.")

    st.markdown("")

    # ================= Filters ================= #

    filter1, filter2 = st.columns(2)

    with filter1:

        month = st.selectbox(

            " Select Month",

            [
                "All",
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May"
            ]

        )

    with filter2:

        category = st.selectbox(

            " Product Category",

            [
                "All",
                "Laptop",
                "Mouse",
                "Keyboard",
                "Monitor",
                "Printer"
            ]

        )

    st.markdown("")

    # ================= Sample Data ================= #

    df = pd.DataFrame({

        "Month": [

            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May"

        ],

        "Forecast": [

            120,
            150,
            170,
            200,
            220

        ],

        "Actual": [

            110,
            155,
            165,
            195,
            210

        ]

    })

    # ================= Apply Filter ================= #

    if month != "All":

        df = df[df["Month"] == month]

    # ================= KPI Calculations ================= #

    forecast_total = df["Forecast"].sum()

    actual_total = df["Actual"].sum()

    variance = actual_total - forecast_total

    accuracy = round(

        (actual_total / forecast_total) * 100,

        2

    )

    # ================= KPI Cards ================= #

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(

            " Forecast Revenue",

            f"₹{forecast_total}K"

        )

    with k2:

        st.metric(

            " Actual Revenue",

            f"₹{actual_total}K"

        )

    with k3:

        st.metric(

            " Variance",

            f"{variance:+}K"

        )

    with k4:

        st.metric(

            " Forecast Accuracy",

            f"{accuracy}%"

        )

    st.write("")
        # ================= Charts ================= #

    chart1, chart2 = st.columns([2, 1])

    # ---------------- Forecast vs Actual ---------------- #

    with chart1:

        st.subheader(" Forecast vs Actual Trend")

        fig = px.line(

            df,

            x="Month",

            y=["Forecast", "Actual"],

            markers=True,

            template="plotly_dark"

        )

        fig.update_layout(

            plot_bgcolor="#0F172A",

            paper_bgcolor="#0F172A",

            height=420,

            legend_title="Revenue",

            margin=dict(
                l=20,
                r=20,
                t=40,
                b=20
            ),

            hovermode="x unified"

        )

        fig.update_traces(

            line=dict(width=4),

            marker=dict(size=10)

        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ---------------- Variance Chart ---------------- #

    variance_df = df.copy()

    variance_df["Variance"] = (

        variance_df["Actual"]

        -

        variance_df["Forecast"]

    )

    with chart2:

        st.subheader(" Variance")

        fig = px.bar(

            variance_df,

            x="Month",

            y="Variance",
            text="Variance",
            color_discrete_sequence=["#06B6D4"],
            template="plotly_dark"

        )

        fig.update_layout(

            plot_bgcolor="#0F172A",

            paper_bgcolor="#0F172A",

            height=450,

            margin=dict(
                l=20,
                r=20,
                t=40,
                b=20
            ),

            coloraxis_showscale=False

        )

        fig.update_traces(

            textposition="outside"

        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.write("")
        # ================= Monthly Comparison ================= #

    st.subheader("📋 Monthly Performance Summary")

    comparison = df.copy()

    comparison["Variance"] = (
        comparison["Actual"] - comparison["Forecast"]
    )

    comparison["Accuracy %"] = (
        comparison["Actual"] /
        comparison["Forecast"] * 100
    ).round(2)

    st.dataframe(
        comparison,
        width="stretch",
        hide_index=True
    )

    st.write("")

    # ================= Performance Metrics ================= #

    left, right = st.columns([1, 1])

    with left:

        st.subheader(" Forecast Accuracy")

        accuracy = round(

            (
                comparison["Actual"].sum()
                /
                comparison["Forecast"].sum()
            ) * 100,

            2

        )

        st.progress(
            min(int(accuracy), 100)
        )

        st.metric(
            "Overall Accuracy",
            f"{accuracy}%"
        )

    with right:

        st.subheader(" Performance Status")

        variance_total = comparison["Variance"].sum()

        if variance_total >= 0:

            st.success(
                f"""
🟢 Excellent Performance

Revenue exceeded forecast.

Overall Variance : +{variance_total}

Business Trend : Positive
                """
            )

        else:

            st.warning(
                f"""
🟡 Needs Attention

Revenue below forecast.

Overall Variance : {variance_total}

Business Trend : Moderate
                """
            )

    st.write("")

    # ================= AI Insights ================= #

    st.subheader(" AI Insights")

    highest = comparison.loc[
        comparison["Actual"].idxmax(),
        "Month"
    ]

    lowest = comparison.loc[
        comparison["Actual"].idxmin(),
        "Month"
    ]

    positive = comparison[
        comparison["Variance"] > 0
    ]

    negative = comparison[
        comparison["Variance"] < 0
    ]

    insight1, insight2 = st.columns(2)

    with insight1:

        st.info(
            f"""
Highest Sales

Month : **{highest}**

Forecast Accuracy : **{accuracy}%**
            """
        )

    with insight2:

        st.info(
            f"""
 Lowest Sales

Month : **{lowest}**

Negative Months : **{len(negative)}**
            """
        )

    st.write("")

    st.subheader(" AI Recommendation")

    if len(negative) > len(positive):

        st.error(
            """
• Increase promotional campaigns.

• Improve inventory planning.

• Review underperforming products.

• Retrain forecasting model.

• Focus on low-performing months.
            """
        )

    else:

        st.success(
            """
• Maintain current sales strategy.

• Increase stock for top products.

• Continue AI-based forecasting.

• Expand marketing campaigns.

• Monitor monthly trends.
            """
        )

    st.write("")
        # ================= Current Filters ================= #

    st.subheader(" Current Filters")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        st.info(f" Month : {month}")

    with filter_col2:

        st.info(f" Category : {category}")

    st.write("")

    # ================= Dashboard Actions ================= #

    action1, action2 = st.columns([1, 1])

    csv = comparison.to_csv(
        index=False
    ).encode("utf-8")

    with action1:

        st.download_button(

            label="⬇ Download Forecast Report",

            data=csv,

            file_name="forecast_vs_actual_report.csv",

            mime="text/csv",

            width="stretch"

        )

    with action2:

        if st.button(

            " Refresh Dashboard",

            width="stretch"

        ):

            st.rerun()

    st.write("")

    # ================= Dashboard Summary ================= #

    st.subheader(" Dashboard Summary")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "Forecast",
            f"₹{forecast_total}K"
        )

    with s2:

        st.metric(
            "Actual",
            f"₹{actual_total}K"
        )

    with s3:

        st.metric(
            "Variance",
            f"{variance:+}K"
        )

    with s4:

        st.metric(
            "Accuracy",
            f"{accuracy}%"
        )

    st.write("")

    # ================= Business Health ================= #

    st.subheader("🩺 Business Health")

    if accuracy >= 95:

        st.success(
            """
🟢 Overall Business Status : Excellent

✔ Forecast model performing accurately

✔ Revenue tracking is healthy

✔ Business is meeting expectations
            """
        )

    elif accuracy >= 85:

        st.warning(
            """
🟡 Overall Business Status : Good

✔ Minor deviations from forecast

✔ Monitor inventory and sales

✔ Review next month's prediction
            """
        )

    else:

        st.error(
            """
🔴 Overall Business Status : Needs Attention

• Improve forecasting model

• Review sales strategy

• Increase promotional activities

• Analyze underperforming products
            """
        )

    st.write("")

    # ================= Footer ================= #

    st.caption(
        "MarketMind AI • Forecast Analytics Dashboard • Version 1.0"
    )