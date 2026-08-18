import streamlit as st


def show_cards(metrics):
    # CSS to guarantee no ellipsis or truncation on metric values
    st.markdown(
        """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            white-space: normal !important;
            word-break: break-word !important;
            overflow: visible !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricValue"] > div {
            text-overflow: unset !important;
            overflow: visible !important;
            white-space: normal !important;
        }
        [data-testid="stMetricLabel"] > div > p {
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
        }
        div[data-testid="column"] {
            background: rgba(30, 41, 59, 0.45);
            padding: 12px 14px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"₹ {metrics['Revenue']:,.2f}"
        )

    with col2:
        st.metric(
            label="📦 Total Orders",
            value=f"{metrics['Orders']:,}"
        )

    with col3:
        st.metric(
            label="🛍️ Products Sold",
            value=f"{metrics['Products Sold']:,}"
        )

    with col4:
        st.metric(
            label="🏷️ Inventory Count",
            value=f"{metrics['Inventory']:,}"
        )

    with col5:
        st.metric(
            label="⚠️ Low Stock Items",
            value=f"{metrics['Low Stock']:,}"
        )