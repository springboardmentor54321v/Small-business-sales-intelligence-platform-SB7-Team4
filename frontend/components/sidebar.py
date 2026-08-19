import streamlit as st
from services.auth_service import clear_auth_session


def show_sidebar():

    role = st.session_state.get("role", "Admin")
    username = st.session_state.get("username", "User")

    # ---------------- CSS ---------------- #

    st.markdown(
        """
        <style>

        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 300px;
            max-width: 300px;
            background: #171f32;
            border-right: 1px solid #232f48;
        }

        [data-testid="stSidebar"][aria-expanded="false"] {
            background: #171f32;
        }

        [data-testid="stSidebar"] div[data-testid="stButton"]>button {
            width: 100%;
            border: none;
            border-radius: 12px;
            background: #232f48;
            color: white;
            text-align: left;
            padding: 12px 16px;
            margin-bottom: 8px;
            font-size: 15px;
            font-weight: 500;
        }

        [data-testid="stSidebar"] div[data-testid="stButton"]>button:hover {
            background: #ff4b4b;
            color: white;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Logo ---------------- #

    st.sidebar.title("MarketMind AI")
    st.sidebar.caption("Small Business Intelligence")

    st.sidebar.divider()

    # ---------------- User ---------------- #

    st.sidebar.subheader(f"Welcome, {username}")
    st.sidebar.caption(f"Role : {role}")

    st.sidebar.divider()

    # ---------------- Menu ---------------- #

    if role in ["Owner", "Business Owner"]:
 
         menu = [
             "Dashboard",
             "Business Overview",
             "Forecast vs Actual",
             "User Management",
             "Notifications",
             "Inventory",
             "Customer Insights",
             "Churn Risk",
             "Invoice",
             "Sales Upload",
             "Reports",
             "Settings"
         ]

    elif role == "Store Manager":

        menu = [
            "Dashboard",
            "Business Overview",
            "Forecast vs Actual",
            "Notifications",
            "Inventory",
            "Invoice",
            "Sales Upload",
            "Churn Risk",
            "Settings"
        ]

    elif role == "Sales Executive":

        menu = [
            "Dashboard",
            "Notifications",
            "Sales Upload",
            "Invoice",
            "Churn Risk",
            "Settings"
        ]

    else:
        # ADMIN

        menu = [
            "Dashboard",
            "Business Overview",
            "Forecast vs Actual",
            "Notifications",
            "Inventory",
            "Customer Insights",
            "Customer Management",   # ⭐ NEW
            "Churn Risk",
            "Invoice",
            "Sales Upload",
            "Reports",
            "Settings"
        ]

    # ---------------- Default Page ---------------- #

    if "page" not in st.session_state:
        st.session_state.page = menu[0]

    st.sidebar.markdown("### Navigation")

    # ---------------- Navigation Buttons ---------------- #

    for page in menu:

        if page == st.session_state.page:

            st.sidebar.button(
                page,
                width="stretch",
                disabled=True
            )

        else:

            if st.sidebar.button(
                page,
                width="stretch"
            ):

                st.session_state.page = page
                st.rerun()

    st.sidebar.divider()

    # ---------------- Logout ---------------- #

    st.sidebar.info(
        f"Logged in as {role}"
    )

    if st.sidebar.button(
        "Logout",
        width="stretch"
    ):

        clear_auth_session()
        st.session_state.page = "Home"

        st.rerun()

    st.sidebar.divider()

    st.sidebar.caption("MarketMind AI")
    st.sidebar.caption("Version 2.0")