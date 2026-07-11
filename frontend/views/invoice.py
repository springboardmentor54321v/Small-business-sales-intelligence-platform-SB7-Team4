import streamlit as st
from components.sidebar import show_sidebar

def invoice_page():

    show_sidebar()

    st.title("🧾 Invoice")

    st.info("Invoice Page")