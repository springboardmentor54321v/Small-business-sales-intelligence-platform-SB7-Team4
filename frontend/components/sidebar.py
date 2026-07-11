import streamlit as st

def show_sidebar():

    role = st.session_state.role

    st.sidebar.title("📊 MarketMind AI")
    st.sidebar.markdown("---")

    st.sidebar.write(f"### 👋 Welcome, {st.session_state.username}")
    st.sidebar.caption(f"Role: {role}")

    st.sidebar.markdown("---")

    # Role Based Menu
    menus = {
        "Owner": [
            "Dashboard",
            "Inventory",
            "Customers",
            "Reports"
        ],

        "Store Manager": [
            "Dashboard",
            "Inventory",
            "Invoice",
            "Sales Upload"
        ],

        "Sales Executive": [
            "Dashboard",
            "Customers",
            "Sales Upload",
            "Invoice"
        ],

        "Admin": [
            "Dashboard",
            "Inventory",
            "Reports",
            "Admin"
        ]
    }

    menu = menus.get(role, ["Dashboard"])

    # If current page is not available for this role
    if st.session_state.page not in menu:
        st.session_state.page = menu[0]

    selected = st.sidebar.radio(
        "Navigation",
        options=menu,
        index=menu.index(st.session_state.page)
    )

    # Change page only when user selects another page
    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.page = "Home"

        st.rerun()