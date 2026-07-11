import streamlit as st

def show_cards():

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Total Revenue",
            value="₹12,45,000",
            delta="+8.5%"
        )

    with col2:
        st.metric(
            label="🛒 Orders",
            value="1,256",
            delta="+5%"
        )

    with col3:
        st.metric(
            label="👥 Customers",
            value="542",
            delta="+12"
        )

    with col4:
        st.metric(
            label="📦 Products",
            value="128",
            delta="+3"
        )