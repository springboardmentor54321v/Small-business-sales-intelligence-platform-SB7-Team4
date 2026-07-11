import streamlit as st
from components.sidebar import show_sidebar

def inventory_page():

    show_sidebar()

    st.title("📦 Inventory")

    st.info("Inventory Page")