import streamlit as st

def login_page():

    st.title("🔐 Login")

    st.write("Please sign in to continue")

    st.markdown("---")

    username = st.text_input(
        "Username",
        placeholder="Enter your username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    role = st.selectbox(
        "Select Role",
        (
            "Owner",
            "Store Manager",
            "Sales Executive",
            "Admin"
        )
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button("Login", use_container_width=True):

            if username == "" or password == "":
                st.error("Please enter Username and Password")

            else:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.page = "Dashboard"

                st.rerun()

    st.markdown("---")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()