import streamlit as st
import re
import requests
from config.config import BASE_URL


def login_page():

    # --------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------

    if "page" not in st.session_state:
        st.session_state.page = "Login"

    if "password_visible" not in st.session_state:
        st.session_state.password_visible = False

    if "forgot_password" not in st.session_state:
        st.session_state.forgot_password = False

    # --------------------------------------------------
    # FORGOT PASSWORD PAGE
    # --------------------------------------------------

    if st.session_state.forgot_password:

        left, center, right = st.columns([1, 2, 1])

        with center:

            st.title("Forgot Password")
            st.caption("Reset your MarketMind AI password")

            st.markdown("---")

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Enter new password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter new password"
            )

            st.caption(
                "Password must contain at least 6 characters."
            )

            # --------------------------------------------------
            # RESET PASSWORD
            # --------------------------------------------------

            if st.button(
                "Reset Password",
                width="stretch"
            ):

                if username.strip() == "":
                    st.error("Please enter your username.")

                elif new_password.strip() == "":
                    st.error("Please enter a new password.")

                elif confirm_password.strip() == "":
                    st.error("Please confirm your password.")

                elif len(new_password) < 6:
                    st.error(
                        "Password must contain at least 6 characters."
                    )

                elif new_password != confirm_password:
                    st.error(
                        "New password and confirm password do not match."
                    )

                elif not re.fullmatch(
                    r"[A-Za-z0-9@#$%^&*!._-]{6,}",
                    new_password
                ):
                    st.error(
                        "Password contains invalid characters."
                    )

                else:

                    # --------------------------------------------------
                    # DEMO PASSWORD RESET
                    # --------------------------------------------------

                    st.session_state.reset_username = username
                    st.session_state.reset_password = new_password

                    st.success(
                        "Password reset successfully!"
                    )

                    st.info(
                        "You can now go back to Login and sign in "
                        "with your new password."
                    )

            st.markdown("---")

            if st.button(
                "⬅ Back to Login",
                width="stretch"
            ):

                st.session_state.forgot_password = False
                st.rerun()

        return

    # --------------------------------------------------
    # LOGIN PAGE
    # --------------------------------------------------

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.title("MarketMind AI Login")
        st.caption("Please sign in to continue")

        st.markdown("---")

        # --------------------------------------------------
        # USERNAME
        # --------------------------------------------------

        username = st.text_input(
            "Username",
            placeholder="Enter Username"
        )

        # --------------------------------------------------
        # PASSWORD
        # --------------------------------------------------

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Password"
        )

        st.caption(
            "Password must contain at least 6 characters."
        )

        # --------------------------------------------------
        # ROLE
        # --------------------------------------------------

        role = st.selectbox(
            "Select Role",
            (
                "Owner",
                "Store Manager",
                "Sales Executive",
                "Admin"
            )
        )

        # --------------------------------------------------
        # FORGOT PASSWORD
        # --------------------------------------------------

        if st.button(
            "Forgot Password?",
            width="stretch"
        ):

            st.session_state.forgot_password = True
            st.rerun()

        st.markdown("")

        # --------------------------------------------------
        # SIGN IN
        # --------------------------------------------------

        if st.button(
            "Sign In",
            width="stretch"
        ):

            if username.strip() == "" or password.strip() == "":
                st.error(
                    "Please enter Username and Password."
                )

            elif len(username) < 6:
                st.error(
                    "Username must contain at least 6 characters."
                )

            elif len(password) < 6:
                st.error(
                    "Password must contain at least 6 characters."
                )

            elif not re.fullmatch(
                r"[A-Za-z0-9@._-]{6,}",
                username
            ):
                st.error(
                    "Username can contain only letters, numbers, @ . _ -"
                )

            elif not re.fullmatch(
                r"[A-Za-z0-9@#$%^&*!._-]{6,}",
                password
            ):
                st.error(
                    "Password contains invalid characters."
                )

            else:
                try:
                    res = requests.post(f"{BASE_URL}/auth/login", json={
                        "email": username,
                        "password": password
                    }, headers={"x-bypass-rate-limit": "true"})
                    
                    if res.status_code == 200:
                        login_data = res.json()
                        st.success("Login Successful!")
                        st.session_state.logged_in = True
                        st.session_state.username = login_data["user"]["name"]
                        st.session_state.role = login_data["user"]["role"]
                        st.session_state.token = login_data["token"]
                        st.session_state.page = "Dashboard"
                        st.rerun()
                    elif res.status_code == 401:
                        st.error("Login failed: Invalid email or password.")
                    elif res.status_code == 403:
                        st.error("Login failed: Email address not verified.")
                    else:
                        detail = res.json().get("detail", "Login failed.")
                        st.error(f"Login failed: {detail}")
                except Exception as e:
                    st.error(f"Cannot connect to the backend security gateway: {str(e)}")

        st.markdown("---")

        # --------------------------------------------------
        # BACK TO HOME
        # --------------------------------------------------

        if st.button(
            "⬅ Back to Home",
            width="stretch"
        ):

            st.session_state.page = "Home"
            st.rerun()


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    login_page()