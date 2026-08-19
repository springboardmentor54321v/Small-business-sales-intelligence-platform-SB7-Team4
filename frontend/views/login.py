import streamlit as st
import re
import requests
import time
from config.config import AUTH_BASE_URL as BASE_URL
from services.auth_service import save_auth_session


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

    # Initialize state variables for OTP flow
    if "forgot_step" not in st.session_state:
        st.session_state.forgot_step = 1
    if "forgot_email" not in st.session_state:
        st.session_state.forgot_email = ""

    if st.session_state.forgot_password:

        left, center, right = st.columns([1, 2, 1])

        with center:
            st.title("Forgot Password")
            st.caption("Reset your MarketMind AI password via secure OTP verification")
            st.markdown("---")

            # ==================================================
            # STEP 1: Enter Email & Request OTP
            # ==================================================
            if st.session_state.forgot_step == 1:
                email = st.text_input(
                    "Email",
                    placeholder="Enter your registered email address"
                )
                st.caption("A 6-digit One-Time Password (OTP) will be sent to this email address.")

                if st.button("Send Reset Email", width="stretch"):
                    if email.strip() == "":
                        st.error("Please enter your email address.")
                    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        st.error("Please enter a valid email address.")
                    else:
                        try:
                            # Trigger backend OTP generation
                            res = requests.post(
                                f"{BASE_URL}/auth/forgot-password",
                                json={"email": email},
                                headers={"x-bypass-rate-limit": "true"},
                                timeout=10
                            )
                            if res.status_code == 200:
                                st.session_state.forgot_email = email
                                st.session_state.forgot_step = 2
                                st.success("OTP has been sent to your email address!")
                                st.rerun()
                            elif res.status_code == 404:
                                st.error("Email is not registered.")
                            else:
                                detail = res.json().get("detail", "Request failed.")
                                st.error(f"Failed to request OTP: {detail}")
                        except Exception as e:
                            st.error(f"Connection error: Could not reach authorization server. Details: {e}")

            # ==================================================
            # STEP 2: Enter OTP & Reset Password
            # ==================================================
            elif st.session_state.forgot_step == 2:
                st.info(f"OTP sent to: **{st.session_state.forgot_email}**")

                otp = st.text_input(
                    "Enter OTP",
                    placeholder="Enter the 6-digit OTP code"
                )

                new_password = st.text_input(
                    "New Password",
                    type="password",
                    placeholder="Enter new password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm new password"
                )
                st.caption("Password must contain at least 6 characters.")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Reset Password", width="stretch"):
                        if otp.strip() == "":
                            st.error("Please enter the OTP.")
                        elif new_password.strip() == "":
                            st.error("Please enter a new password.")
                        elif len(new_password) < 6:
                            st.error("Password must be at least 6 characters.")
                        elif new_password != confirm_password:
                            st.error("Passwords do not match.")
                        else:
                            try:
                                # 1. Verify the OTP to get reset token
                                verify_res = requests.post(
                                    f"{BASE_URL}/auth/verify-otp",
                                    json={"email": st.session_state.forgot_email, "otp": otp},
                                    headers={"x-bypass-rate-limit": "true"},
                                    timeout=10
                                )
                                if verify_res.status_code == 200:
                                    reset_token = verify_res.json().get("reset_token")

                                    # 2. Reset the password
                                    reset_res = requests.post(
                                        f"{BASE_URL}/auth/reset-password",
                                        json={
                                            "email": st.session_state.forgot_email,
                                            "reset_token": reset_token,
                                            "new_password": new_password
                                        },
                                        headers={"x-bypass-rate-limit": "true"},
                                        timeout=10
                                    )
                                    if reset_res.status_code == 200:
                                        st.success("Password reset successfully!")
                                        st.session_state.forgot_password = False
                                        st.session_state.forgot_step = 1
                                        st.session_state.forgot_email = ""
                                        st.info("You can now sign in with your new password.")
                                        st.rerun()
                                    else:
                                        detail = reset_res.json().get("detail", "Reset failed.")
                                        st.error(f"Failed to reset password: {detail}")
                                else:
                                    detail = verify_res.json().get("detail", "Verification failed.")
                                    st.error(f"OTP verification failed: {detail}")
                            except Exception as e:
                                st.error(f"Connection error: {e}")

                with col2:
                    if st.button("Resend OTP", width="stretch"):
                        try:
                            res = requests.post(
                                f"{BASE_URL}/auth/forgot-password",
                                json={"email": st.session_state.forgot_email},
                                headers={"x-bypass-rate-limit": "true"},
                                timeout=10
                            )
                            if res.status_code == 200:
                                st.success("A new OTP has been sent!")
                            else:
                                st.error("Failed to resend OTP. Please try again.")
                        except Exception as e:
                            st.error(f"Connection error: {e}")

            st.markdown("---")

            if st.button("⬅ Back to Login", width="stretch"):
                st.session_state.forgot_password = False
                st.session_state.forgot_step = 1
                st.session_state.forgot_email = ""
                st.rerun()

        return

    # --------------------------------------------------
    # LOGIN PAGE
    # --------------------------------------------------

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.title("MarketMind AI Login")
        st.caption("Please sign in to continue")
        st.caption(f"Security Gateway: `{BASE_URL}`")
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

            elif len(username) < 3:
                st.error(
                    "Username must contain at least 3 characters."
                )

            elif len(password) < 4:
                st.error(
                    "Password must contain at least 4 characters."
                )

            elif not re.fullmatch(
                r"[A-Za-z0-9@._+-]{3,}",
                username
            ):
                st.error(
                    "Username can contain only letters, numbers, @ . _ + -"
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
                    }, headers={"x-bypass-rate-limit": "true"}, timeout=30)
                    
                    if res.status_code == 200:
                        try:
                            login_data = res.json()
                            st.success("Login Successful!")
                            st.session_state.logged_in = True
                            st.session_state.username = login_data["user"]["name"]
                            st.session_state.role = login_data["user"]["role"]
                            st.session_state.token = login_data["token"]
                            st.session_state.page = "Dashboard"
                            save_auth_session(
                                username=login_data["user"]["name"],
                                role=login_data["user"]["role"],
                                token=login_data["token"],
                                email=username
                            )
                            st.rerun()
                        except Exception:
                            st.error("Login failed: The gateway returned an invalid response. It may still be starting up.")
                    elif res.status_code == 401:
                        st.error("Login failed: Invalid email or password.")
                    elif res.status_code == 403:
                        st.error("Login failed: Email address not verified.")
                        st.session_state.unverified_email = username
                    elif res.status_code in [502, 503, 504]:
                        st.error("Login failed (HTTP 502/503). The remote API Gateway is starting up on Render. Please wait 10-20 seconds and try signing in again.")
                    else:
                        try:
                            detail = res.json().get("detail", "Login failed.")
                        except Exception:
                            detail = f"Gateway error (HTTP {res.status_code})."
                        st.error(f"Login failed: {detail}")
                except Exception as e:
                    # Provide user-friendly warning for Render cold starts / timeouts
                    if "timeout" in str(e).lower() or "read timed out" in str(e).lower():
                        st.error("Cannot connect to the backend security gateway: Connection timed out. The remote server is likely waking up on Render. Please try again in 10-15 seconds.")
                    else:
                        st.error(f"Cannot connect to the backend security gateway: {str(e)}")

        if st.session_state.get("unverified_email"):
            st.markdown("---")
            st.subheader("Verify Your Email Address")
            st.info(f"Please check your inbox at **{st.session_state.unverified_email}** for a 6-character alphanumeric verification code.")
            
            code_input = st.text_input("Enter Verification Code", key="unverified_code_input", placeholder="e.g. A1B2C3")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Verification Code", use_container_width=True):
                    if not code_input.strip():
                        st.error("Please enter the code.")
                    else:
                        try:
                            verify_res = requests.post(
                                f"{BASE_URL}/auth/verify-email",
                                json={"token": code_input.strip().upper()},
                                headers={"x-bypass-rate-limit": "true"}
                            )
                            if verify_res.status_code == 200:
                                st.success("Email verified successfully! You can now log in.")
                                st.session_state.unverified_email = None
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                detail = verify_res.json().get("detail", "Invalid verification code.")
                                st.error(f"Verification failed: {detail}")
                        except Exception as e:
                            st.error(f"Cannot connect to the gateway: {str(e)}")
                            
            with col2:
                if st.button("Resend Verification Code", use_container_width=True):
                    try:
                        resend_res = requests.post(
                            f"{BASE_URL}/auth/resend-verification",
                            json={"email": st.session_state.unverified_email},
                            headers={"x-bypass-rate-limit": "true"}
                        )
                        if resend_res.status_code == 200:
                            st.success("Verification code resent successfully!")
                            resend_data = resend_res.json()
                            if resend_data.get("verification_token"):
                                st.info(f"🔑 [SIMULATED CODE]: **{resend_data['verification_token']}**")
                        else:
                            detail = resend_res.json().get("detail", "Failed to resend.")
                            st.error(f"Resend failed: {detail}")
                    except Exception as e:
                        st.error(f"Cannot connect to the gateway: {str(e)}")

        st.markdown("---")

        # --------------------------------------------------
        # SIGN UP REDIRECT
        # --------------------------------------------------

        if st.button(
            "🔑 Don't have an account? Sign up here",
            width="stretch"
        ):
            st.session_state.page = "Signup"
            st.rerun()

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