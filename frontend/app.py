import streamlit as st

from views.home import home_page
from views.login import login_page
from views.dashboard import dashboard_page
from views.inventory import inventory_page
from views.customers import customers_page
from views.reports import reports_page
from views.invoice import invoice_page
from views.sales_upload import sales_upload_page
from views.admin import admin_page
from views.settings import settings_page

st.set_page_config(
    page_title="MarketMind AI",
    page_icon="📊",
    layout="wide"
)

# ---------------- Session ---------------- #

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- Authentication ---------------- #

if not st.session_state.logged_in:

    if st.session_state.page == "Home":
        home_page()

    elif st.session_state.page == "Login":
        login_page()

    else:
        st.session_state.page = "Login"
        login_page()

# ---------------- Application ---------------- #

else:

    if st.session_state.page == "Dashboard":
        dashboard_page()

    elif st.session_state.page == "Inventory":
        inventory_page()

    elif st.session_state.page == "Customer Insights":
        customers_page()

    elif st.session_state.page == "Reports":
        reports_page()

    elif st.session_state.page == "Invoice":
        invoice_page()

    elif st.session_state.page == "Sales Upload":
        sales_upload_page()

    elif st.session_state.page == "Admin":
        admin_page()

    elif st.session_state.page == "Settings":
        settings_page()

    else:
        dashboard_page()