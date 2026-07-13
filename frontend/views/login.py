import streamlit as st
import re


def login_page():

    st.title("🔐 MarketMind AI Login")
    st.write("Please sign in to continue")

    st.markdown("---")

    # Username
    username = st.text_input(
        "Username",
        placeholder="Enter Username"
    )

    # Password
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter Password"
    )

    # Show Password (Below Password)
    show_password = st.checkbox("Show Password")

    if show_password and password:
        st.caption(f"Entered Password: {password}")

    # Forgot Password
    if st.button("Forgot Password?"):
        st.info(
            "Password reset functionality will be available in the next release."
        )

    # Password Instructions
    st.caption(
        "🔒 Password must contain at least 6 characters. "
        "Letters, numbers and special characters are allowed."
    )

    # Role
    role = st.selectbox(
        "Select Role",
        (
            "Owner",
            "Store Manager",
            "Sales Executive",
            "Admin"
        )
    )

    st.markdown("")

    # Sign In Button
    if st.button("🔑 Sign In", use_container_width=True):

        if username.strip() == "" or password.strip() == "":
            st.error("Please enter Username and Password.")

        elif len(username) < 6:
            st.error("Username must contain at least 6 characters.")

        elif len(password) < 6:
            st.error("Password must contain at least 6 characters.")

        elif not re.fullmatch(r"[A-Za-z0-9@._-]{6,}", username):
            st.error(
                "Username can contain only letters, numbers and @ . _ -"
            )

        elif not re.fullmatch(r"[A-Za-z0-9@#$%^&*!._-]{6,}", password):
            st.error(
                "Password contains invalid characters."
            )

        else:

            st.success("✅ Login Successful!")

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.page = "Dashboard"

            st.rerun()

    st.markdown("---")

    if st.button("⬅ Back to Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()