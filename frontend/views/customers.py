import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from components.sidebar import show_sidebar

# ---------------- API Configuration ---------------- #
from config.config import DB_BASE_URL as BASE_URL

SALES_API = f"{BASE_URL}/sales/"


def customers_page():

    show_sidebar()

    st.title(" Customer Insights")
    st.caption("Customer Segmentation & Business Insights")

    st.markdown("---")

    # ---------------- Load Sales Data ---------------- #

    try:

        with st.spinner("Loading Customer Insights..."):

            response = requests.get(
                SALES_API,
                timeout=10
            )

        response.raise_for_status()

        sales = response.json()

        sales_df = pd.DataFrame(sales)

    except requests.exceptions.Timeout:

        st.error("❌ Backend request timed out.")
        return

    except requests.exceptions.ConnectionError:

        st.error("❌ Unable to connect to backend.")
        return

    except requests.exceptions.HTTPError as e:

        st.error(f"❌ API Error: {e}")
        return

    except Exception as e:

        st.error(f"❌ Unexpected Error: {e}")
        return

    if sales_df.empty:

        st.warning("No Sales Data Available")
        return

    # ---------------- Prepare Customer Data ---------------- #

    sales_df["total_amount"] = pd.to_numeric(
        sales_df["total_amount"],
        errors="coerce"
    ).fillna(0)

    customer_df = (

        sales_df

        .groupby("customer_id")

        .agg(

            Orders=("transaction_id", "count"),

            Total_Spend=("total_amount", "sum")

        )

        .reset_index()

    )

    customer_df.rename(

        columns={

            "customer_id": "Customer"

        },

        inplace=True

    )

    # ---------------- Customer Segmentation ---------------- #

    def segment_customer(amount):

        if amount >= 10000:

            return "High Value"

        elif amount >= 5000:

            return "Loyal"

        else:

            return "Occasional"

    customer_df["Segment"] = customer_df[
        "Total_Spend"
    ].apply(segment_customer)

    df = customer_df.copy()

    # ---------------- Dashboard Cards ---------------- #

    loyal = len(

        df[
            df["Segment"] == "Loyal"
        ]

    )

    high = len(

        df[
            df["Segment"] == "High Value"
        ]

    )

    occasional = len(

        df[
            df["Segment"] == "Occasional"
        ]

    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        " Loyal Customers",
        loyal
    )

    c2.metric(
        " High Value",
        high
    )

    c3.metric(
        " Occasional",
        occasional
    )

    st.markdown("---")
        # ---------------- Search ---------------- #

    search = st.text_input(
        " Search Customer"
    )

    if search:

        df = df[
            df["Customer"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

   

    # ---------------- Customer Distribution ---------------- #
    st.subheader(" Customer Distribution")
    segment_count = (

        df

        .groupby("Segment")

        .size()

        .reset_index(name="Customers")

    )


    pie = px.pie(

        segment_count,

        names="Segment",

        values="Customers",

        hole=0.45,
        title="Customer Segmentation"

    )

    pie.update_traces(
        textinfo="percent+label"
    )

    pie.update_layout(
        height=500
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    

    # ---------------- Customer Table ---------------- #

    st.subheader(" Customer Insights")

    display_df = df.rename(

        columns={

            "Total_Spend": "Total Spend"

        }

    )

    st.dataframe(

        display_df,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")
        # ---------------- Business Summary ---------------- #

    st.subheader("Business Summary")

    total_customers = len(df)

    total_orders = int(
        df["Orders"].sum()
    )

    total_revenue = float(
        df["Total_Spend"].sum()
    )

    avg_spend = 0

    if total_customers > 0:

        avg_spend = total_revenue / total_customers

    c1, c2 = st.columns(2)

    c3, c4 = st.columns(2)

    c1.metric(
        " Total Customers",
        total_customers
    )

    c2.metric(
        " Total Orders",
        total_orders
    )

    c3.metric(
        " Revenue",
        f"₹ {total_revenue:,.2f}"
    )

    c4.metric(
        " Average Spend",
        f"₹ {avg_spend:,.2f}"
    )

    st.markdown("---")

    # ---------------- Top Customers ---------------- #

    st.subheader(" Top 10 Customers")

    top_customers = df.sort_values(
        by="Total_Spend",
        ascending=False
    ).head(10)

    st.dataframe(
        top_customers.rename(
            columns={
                "Total_Spend": "Total Spend"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ---------------- Download ---------------- #

    csv = df.rename(
        columns={
            "Total_Spend": "Total Spend"
        }
    ).to_csv(index=False).encode("utf-8")

    st.download_button(

        label="⬇ Download Customer Insights",

        data=csv,

        file_name="customer_insights.csv",

        mime="text/csv",

        use_container_width=True

    )

    
