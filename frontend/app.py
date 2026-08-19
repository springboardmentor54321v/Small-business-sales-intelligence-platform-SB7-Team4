import streamlit as st

# ================= Imports ================= #

from views.customer_management import customer_management_page
from views.home import home_page
from views.login import login_page
from views.dashboard import dashboard_page
from views.inventory import inventory_page
from views.customers import customers_page
from views.reports import reports_page
from views.invoice import invoice_page
from views.payments import payments_page
from views.sales_upload import sales_upload_page
from views.admin import admin_page
from views.settings import settings_page
from views.notifications import notifications_page
from views.business_overview import business_overview_page
from views.forecast_vs_actual import forecast_vs_actual_page
from views.churn_risk import churn_risk_page
from views.user_management import user_management_page
from views.signup import signup_page

# Optional theme import resolved dynamically to avoid static analysis linter warnings
apply_theme = None
try:
    import importlib
    styles_theme = importlib.import_module("styles.theme")
    apply_theme = styles_theme.apply_theme
except ModuleNotFoundError:
    pass

if not apply_theme:
    def apply_theme():
        pass


from services.auth_service import restore_auth_session

# ================= Page Configuration ================= #

st.set_page_config(
    page_title="MarketMind AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# ================= Session State ================= #

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# Automatically restore user session from browser refresh / token
if not st.session_state.logged_in:
    if restore_auth_session():
        if st.session_state.page in ["Home", "Login", "Signup"]:
            st.session_state.page = "Dashboard"


# ================= Authentication ================= #

if not st.session_state.logged_in:

    if st.session_state.page == "Home":
        home_page()

    elif st.session_state.page == "Login":
        login_page()

    elif st.session_state.page == "Signup":
        signup_page()

    else:
        st.session_state.page = "Login"
        login_page()


# ================= Application ================= #

else:

    # ================= Page Routing ================= #

    if st.session_state.page == "Dashboard":
        dashboard_page()

    elif st.session_state.page == "Inventory":
        inventory_page()

    elif st.session_state.page == "Customer Insights":
        customers_page()

    elif st.session_state.page == "Customer Management":
        customer_management_page()

    elif st.session_state.page == "User Management":
        user_management_page()

    elif st.session_state.page == "Churn Risk":
        churn_risk_page()

    elif st.session_state.page == "Reports":
        reports_page()

    elif st.session_state.page == "Invoice":
        invoice_page()

    elif st.session_state.page == "Payments":
        payments_page()

    elif st.session_state.page == "Sales Upload":
        sales_upload_page()

    elif st.session_state.page == "Settings":
        settings_page()

    elif st.session_state.page == "Notifications":
        notifications_page()

    elif st.session_state.page == "Business Overview":
        business_overview_page()

    elif st.session_state.page == "Forecast vs Actual":
        forecast_vs_actual_page()

    else:
        dashboard_page()