import streamlit as st
from components.sidebar import show_sidebar

def customers_page():

    show_sidebar()

    st.title("👥 Customers")

    st.info("Customers Page")