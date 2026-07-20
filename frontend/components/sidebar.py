import streamlit as st


def show_sidebar():

    role = st.session_state.get("role", "")
    username = st.session_state.get("username", "User")

    # ---------------- Header ---------------- #

    st.sidebar.title("📊 MarketMind AI")
    st.sidebar.markdown("---")

    st.sidebar.write(f"### 👋 Welcome, {username}")
    st.sidebar.caption(f"Role: {role}")

    st.sidebar.markdown("---")

    # ---------------- Menu ---------------- #

    if role == "Owner":

        nav_title = "👑 Owner Panel"

        menu = [
            "Dashboard",
            "Inventory",
            "Customer Insights",
            "Invoice",
            "Sales Upload",
            "Reports",
            "Settings"
        ]

    elif role == "Store Manager":

        nav_title = "🏬 Store Manager Panel"

        menu = [
            "Dashboard",
            "Inventory",
            "Invoice",
            "Sales Upload",
            "Settings"
        ]

    elif role == "Sales Executive":

        nav_title = "💼 Sales Executive Panel"

        menu = [
            "Dashboard",
            "Sales Upload",
            "Invoice",
            "Settings"
        ]

    elif role == "Admin":

        nav_title = "⚙️ Admin Panel"

        menu = [
            "Dashboard",
            "Inventory",
            "Customer Insights",
            "Invoice",
            "Sales Upload",
            "Reports",
            "Admin",
            "Settings"
        ]

    else:

        nav_title = "📑 Navigation"

        menu = ["Dashboard"]

    # ---------------- Navigation ---------------- #

    if st.session_state.page not in menu:
        st.session_state.page = menu[0]

    selected = st.sidebar.radio(
        nav_title,
        menu,
        index=menu.index(st.session_state.page)
    )

    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()

    st.sidebar.markdown("---")

    # ---------------- Role Badge ---------------- #

    if role == "Owner":
        st.sidebar.success("👑 Logged in as Owner")

    elif role == "Store Manager":
        st.sidebar.info("🏬 Logged in as Store Manager")

    elif role == "Sales Executive":
        st.sidebar.warning("💼 Logged in as Sales Executive")

    elif role == "Admin":
        st.sidebar.error("⚙️ Logged in as Administrator")

    st.sidebar.markdown("---")

    # ---------------- Logout ---------------- #

    if st.sidebar.button("🚪 Logout", width="stretch"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.page = "Home"

        st.rerun()