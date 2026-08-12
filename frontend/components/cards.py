import streamlit as st


def show_cards(metrics):

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label=" Total Revenue",
            value=f"₹{metrics['Revenue']:,.2f}"
        )

    with col2:
        st.metric(
            label=" Total Orders",
            value=metrics["Orders"]
        )

    with col3:
        st.metric(
            label=" Products Sold",
            value=metrics["Products Sold"]
        )

    with col4:
        st.metric(
            label=" Inventory Count",
            value=metrics["Inventory"]
        )

    with col5:
        st.metric(
            label="⚠ Low Stock",
            value=metrics["Low Stock"]
        )