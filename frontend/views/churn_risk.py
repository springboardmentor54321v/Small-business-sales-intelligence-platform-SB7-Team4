import streamlit as st

from components.sidebar import show_sidebar
from models.churn import get_churn_risk


def churn_risk_page():

    # =========================================================
    # SIDEBAR
    # =========================================================

    show_sidebar()

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.title("Customer Churn Risk")

    st.caption(
        "Identify customers who may be at risk of leaving "
        "and take appropriate action."
    )

    st.markdown("---")

    # =========================================================
    # CUSTOMER INPUT
    # =========================================================

    st.subheader("Customer Analysis")

    st.write(
        "Enter a customer ID to evaluate the customer's churn risk."
    )

    customer_id = st.text_input(
        "Customer ID",
        value="AA-10315",
        placeholder="Example: AA-10315"
    )

    # =========================================================
    # ANALYZE BUTTON
    # =========================================================

    if st.button(
        "Analyze Customer",
        width="stretch"
    ):

        # -----------------------------
        # Validate input
        # -----------------------------

        if not customer_id.strip():

            st.warning(
                "Please enter a Customer ID."
            )

            return

        # -----------------------------
        # Call Churn API
        # -----------------------------

        with st.spinner(
            "Analyzing customer churn risk..."
        ):

            churn_df = get_churn_risk(
                customer_id.strip()
            )

        # =====================================================
        # ERROR HANDLING
        # =====================================================

        if churn_df is None or churn_df.empty:

            st.error(
                "No churn prediction was returned."
            )

            return

        if "Error" in churn_df.columns:

            st.error(
                str(churn_df.iloc[0]["Error"])
            )

            return

        # =====================================================
        # GET API RESULT
        # =====================================================

        result = churn_df.iloc[0]

        returned_customer = str(
            result.get(
                "Customer ID",
                customer_id.strip()
            )
        )

        risk = str(
            result.get(
                "Risk",
                "Unknown"
            )
        ).strip()

        risk_upper = risk.upper()

        # =====================================================
        # DETERMINE RISK LEVEL
        # =====================================================

        if "HIGH" in risk_upper:

            risk_title = "HIGH RISK"
            risk_icon = "🔴"
            action_message = (
                "Immediate customer follow-up is recommended. "
                "Consider a targeted retention strategy."
            )

        elif "MEDIUM" in risk_upper:

            risk_title = "MEDIUM RISK"
            risk_icon = "🟡"
            action_message = (
                "Consider targeted customer engagement "
                "and follow-up."
            )

        elif "LOW" in risk_upper:

            risk_title = "LOW RISK"
            risk_icon = "🟢"
            action_message = (
                "The customer currently shows a lower "
                "risk of churn."
            )

        else:

            risk_title = risk.upper()
            risk_icon = "⚪"
            action_message = (
                "Review the customer information and "
                "monitor future activity."
            )

        # =====================================================
        # RISK RESULT
        # =====================================================

        st.markdown("---")

        st.subheader("Churn Risk Result")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Customer",
                returned_customer
            )

        with col2:

            st.metric(
                "Risk Level",
                f"{risk_icon} {risk_title}"
            )

        # =====================================================
        # RECOMMENDED ACTION
        # =====================================================

        st.markdown("---")

        st.subheader("Recommended Action")

        if "HIGH" in risk_upper:

            st.error(
                f"🔴 **High Churn Risk**\n\n"
                f"{action_message}"
            )

        elif "MEDIUM" in risk_upper:

            st.warning(
                f"🟡 **Medium Churn Risk**\n\n"
                f"{action_message}"
            )

        elif "LOW" in risk_upper:

            st.success(
                f"🟢 **Low Churn Risk**\n\n"
                f"{action_message}"
            )

        else:

            st.info(
                f"⚪ **Churn Risk: {risk}**\n\n"
                f"{action_message}"
            )

       


# =============================================================
# PAGE ENTRY
# =============================================================

if __name__ == "__main__":

    churn_risk_page()