import streamlit as st
from components.sidebar import show_sidebar

def reports_page():

    show_sidebar()

    st.title("📈 Reports")

    st.info("Reports Page")