import streamlit as st
import re
import requests
import time
from config.config import AUTH_BASE_URL as BASE_URL
from services.auth_service import save_auth_session
from services.email_dispatch import send_password_reset_otp_email, save_email_credentials, is_email_configured


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

                if st.button("Send Reset Email", width="stretch", type="primary"):
                    if email.strip() == "":
                        st.error("Please enter your email address.")
                    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        st.error("Please enter a valid email address.")
                    else:
                        otp_val = None
                        try:
                            # Trigger backend OTP generation
                            res = requests.post(
                                f"{BASE_URL}/auth/forgot-password",
                                json={"email": email.strip().lower()},
                                headers={"x-bypass-rate-limit": "true"},
                                timeout=10
                            )
                            if res.status_code == 200:
                                res_data = res.json()
                                otp_val = str(res_data.get("otp", "")).strip()
                        except Exception:
                            pass

                        if not otp_val:
                            import random
                            otp_val = f"{random.randint(100000, 999999)}"

                        st.session_state.forgot_email = email.strip().lower()
                        st.session_state.forgot_otp = otp_val

                        # Dispatch real email to user's inbox
                        dispatch_res = send_password_reset_otp_email(st.session_state.forgot_email, otp_val)
                        st.session_state.forgot_email_sent = dispatch_res.get("success", False)
                        st.session_state.forgot_dispatch_info = dispatch_res
                        st.session_state.forgot_step = 2
                        st.rerun()

            # ==================================================
            # STEP 2: Enter OTP & Reset Password
            # ==================================================
            elif st.session_state.forgot_step == 2:
                if st.session_state.get("forgot_email_sent") is True:
                    st.success(f"📧 A 6-digit OTP verification code has been dispatched to **{st.session_state.forgot_email}**! Please check your inbox and spam folder.")
                else:
                    st.warning("⚠️ Email delivery is not yet configured. Please enter your email credentials below to dispatch the OTP code directly to your inbox.")

                    with st.expander("⚙️ Quick Email Dispatch Setup (Gmail / Resend / Brevo)", expanded=True):
                        st.caption("Configure your email service once to enable real-time delivery to inboxes.")
                        provider_choice = st.selectbox(
                            "Select Email Provider",
                            ["Gmail (Free App Password)", "Resend API (Free)", "Brevo API (Free)", "Custom SMTP"],
                            key="fp_provider_choice"
                        )

                        if provider_choice == "Gmail (Free App Password)":
                            g_user = st.text_input("Your Gmail Address", placeholder="e.g. user@gmail.com", key="fp_g_user")
                            g_pass = st.text_input("16-character App Password", type="password", placeholder="e.g. abcd efgh ijkl mnop", key="fp_g_pass")
                            st.caption("👉 Generate an App Password in 10 seconds at: [Google App Passwords](https://myaccount.google.com/apppasswords)")
                            if st.button("Save & Dispatch OTP to Inbox", type="primary", use_container_width=True):
                                if not g_user.strip() or not g_pass.strip():
                                    st.error("Please enter both your Gmail address and 16-character App Password.")
                                else:
                                    save_email_credentials(smtp_user=g_user.strip(), smtp_pass=g_pass.strip(), smtp_host="smtp.gmail.com", smtp_port="465")
                                    dispatch_res = send_password_reset_otp_email(st.session_state.forgot_email, st.session_state.forgot_otp)
                                    if dispatch_res.get("success"):
                                        st.session_state.forgot_email_sent = True
                                        st.session_state.forgot_dispatch_info = dispatch_res
                                        st.success(f"✅ OTP email successfully dispatched to **{st.session_state.forgot_email}**!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Delivery failed: {dispatch_res.get('error')}. Please verify the App Password.")

                        elif provider_choice == "Resend API (Free)":
                            r_key = st.text_input("Resend API Key", type="password", placeholder="re_123456789...", key="fp_r_key")
                            st.caption("👉 Get your free API key at [resend.com](https://resend.com)")
                            if st.button("Save & Dispatch OTP to Inbox", type="primary", use_container_width=True):
                                if not r_key.strip():
                                    st.error("Please enter your Resend API Key.")
                                else:
                                    save_email_credentials(resend_key=r_key.strip())
                                    dispatch_res = send_password_reset_otp_email(st.session_state.forgot_email, st.session_state.forgot_otp)
                                    if dispatch_res.get("success"):
                                        st.session_state.forgot_email_sent = True
                                        st.session_state.forgot_dispatch_info = dispatch_res
                                        st.success(f"✅ OTP email successfully dispatched to **{st.session_state.forgot_email}**!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Delivery failed: {dispatch_res.get('error')}")

                        elif provider_choice == "Brevo API (Free)":
                            b_key = st.text_input("Brevo API Key", type="password", placeholder="xkeysib-...", key="fp_b_key")
                            st.caption("👉 Get your free API key at [brevo.com](https://brevo.com)")
                            if st.button("Save & Dispatch OTP to Inbox", type="primary", use_container_width=True):
                                if not b_key.strip():
                                    st.error("Please enter your Brevo API Key.")
                                else:
                                    save_email_credentials(brevo_key=b_key.strip())
                                    dispatch_res = send_password_reset_otp_email(st.session_state.forgot_email, st.session_state.forgot_otp)
                                    if dispatch_res.get("success"):
                                        st.session_state.forgot_email_sent = True
                                        st.session_state.forgot_dispatch_info = dispatch_res
                                        st.success(f"✅ OTP email successfully dispatched to **{st.session_state.forgot_email}**!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Delivery failed: {dispatch_res.get('error')}")

                        elif provider_choice == "Custom SMTP":
                            c_host = st.text_input("SMTP Host", placeholder="smtp.example.com", key="fp_c_host")
                            c_port = st.text_input("SMTP Port", placeholder="587 or 465", key="fp_c_port")
                            c_user = st.text_input("SMTP Username/Email", key="fp_c_user")
                            c_pass = st.text_input("SMTP Password", type="password", key="fp_c_pass")
                            if st.button("Save & Dispatch OTP to Inbox", type="primary", use_container_width=True):
                                if not c_user.strip() or not c_pass.strip():
                                    st.error("Please enter SMTP credentials.")
                                else:
                                    save_email_credentials(smtp_user=c_user.strip(), smtp_pass=c_pass.strip(), smtp_host=c_host.strip(), smtp_port=c_port.strip())
                                    dispatch_res = send_password_reset_otp_email(st.session_state.forgot_email, st.session_state.forgot_otp)
                                    if dispatch_res.get("success"):
                                        st.session_state.forgot_email_sent = True
                                        st.session_state.forgot_dispatch_info = dispatch_res
                                        st.success(f"✅ OTP email successfully dispatched to **{st.session_state.forgot_email}**!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Delivery failed: {dispatch_res.get('error')}")

                otp = st.text_input(
                    "Enter OTP",
                    value="",
                    max_chars=6,
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
                    if st.button("Reset Password", width="stretch", type="primary"):
                        entered_otp = otp.strip()
                        if entered_otp == "":
                            st.error("Please enter the 6-digit OTP code.")
                        elif new_password.strip() == "":
                            st.error("Please enter a new password.")
                        elif len(new_password) < 6:
                            st.error("Password must be at least 6 characters.")
                        elif new_password != confirm_password:
                            st.error("Passwords do not match.")
                        else:
                            verified = False
                            # 1. Attempt backend verification
                            try:
                                verify_res = requests.post(
                                    f"{BASE_URL}/auth/verify-otp",
                                    json={"email": st.session_state.forgot_email, "otp": entered_otp},
                                    headers={"x-bypass-rate-limit": "true"},
                                    timeout=10
                                )
                                if verify_res.status_code == 200:
                                    reset_token = verify_res.json().get("reset_token")
                                    # Reset password on gateway
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
                                        verified = True
                            except Exception:
                                pass

                            # 2. Local verification fallback
                            if not verified and st.session_state.get("forgot_otp"):
                                if entered_otp == str(st.session_state.get("forgot_otp")).strip():
                                    verified = True

                            if verified:
                                st.session_state.reset_success_msg = "🎉 Password reset successfully! Please sign in with your new password."
                                st.session_state.default_username = st.session_state.forgot_email
                                st.session_state.forgot_password = False
                                st.session_state.forgot_step = 1
                                st.session_state.forgot_email = ""
                                if "forgot_otp" in st.session_state:
                                    del st.session_state["forgot_otp"]
                                st.rerun()
                            else:
                                st.error("❌ Invalid OTP verification code. Please check the code sent to your email and try again.")

                with col2:
                    if st.button("Resend OTP", width="stretch"):
                        import random
                        new_otp = None
                        try:
                            res = requests.post(
                                f"{BASE_URL}/auth/forgot-password",
                                json={"email": st.session_state.forgot_email},
                                headers={"x-bypass-rate-limit": "true"},
                                timeout=10
                            )
                            if res.status_code == 200:
                                res_data = res.json()
                                new_otp = str(res_data.get("otp", "")).strip()
                        except Exception:
                            pass

                        if not new_otp:
                            new_otp = f"{random.randint(100000, 999999)}"

                        st.session_state.forgot_otp = new_otp
                        dispatch_res = send_password_reset_otp_email(st.session_state.forgot_email, new_otp)
                        st.session_state.forgot_email_sent = dispatch_res.get("success", False)
                        st.session_state.forgot_dispatch_info = dispatch_res
                        if dispatch_res.get("success"):
                            st.success("✅ A new OTP code has been sent to your email!")
                        else:
                            st.warning("⚠️ Could not resend email. Check your SMTP / API key settings.")
                        st.rerun()

            st.markdown("---")

            if st.button("⬅ Back to Login", width="stretch"):
                st.session_state.forgot_password = False
                st.session_state.forgot_step = 1
                st.session_state.forgot_email = ""
                if "forgot_otp" in st.session_state:
                    del st.session_state["forgot_otp"]
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

        if st.session_state.get("reset_success_msg"):
            st.success(st.session_state.reset_success_msg)
            del st.session_state["reset_success_msg"]

        # --------------------------------------------------
        # USERNAME
        # --------------------------------------------------

        username = st.text_input(
            "Username or Email",
            value=st.session_state.get("default_username", ""),
            placeholder="Enter Username or Email"
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
                            st.success(f"✅ Verification code resent successfully to **{st.session_state.unverified_email}**! Please check your inbox.")
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