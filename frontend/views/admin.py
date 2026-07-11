import streamlit as st
from components.sidebar import show_sidebar

def admin_page():

    show_sidebar()

    st.title("⚙ Admin")

    st.info("Admin Page")