import streamlit as st
import pandas as pd

from components.sidebar import show_sidebar


def forecast_vs_actual_page():

    show_sidebar()

    st.title("📈 Forecast vs Actual")
    st.caption("Milestone 3 - Day 5")

    st.markdown("---")

    # ---------------- Filters ---------------- #

    c1, c2 = st.columns(2)

    with c1:
        month = st.selectbox(
            "Select Month",
            ["All", "Jan", "Feb", "Mar", "Apr", "May"]
        )

    with c2:
        category = st.selectbox(
            "Product Category",
            [
                "All",
                "Laptop",
                "Mouse",
                "Keyboard",
                "Monitor",
                "Printer"
            ]
        )

    st.markdown("---")

    # ---------------- Sample Data ---------------- #

    df = pd.DataFrame({

        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],

        "Forecast": [120, 150, 170, 200, 220],

        "Actual": [110, 155, 165, 195, 210]

    })

    # ---------------- Filter ---------------- #

    if month != "All":
        df = df[df["Month"] == month]

    # ---------------- Chart ---------------- #

    st.subheader("Forecast vs Actual")

    st.line_chart(
        df.set_index("Month")
    )

    st.markdown("---")

    # ---------------- Drill Down ---------------- #

    st.subheader("Detailed Comparison")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.info(f"Selected Month : {month}")

    st.info(f"Selected Category : {category}")