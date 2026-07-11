import streamlit as st
from components.sidebar import show_sidebar

def settings_page():

    show_sidebar()

    st.title("⚙ Settings")

    st.info("Settings Page")