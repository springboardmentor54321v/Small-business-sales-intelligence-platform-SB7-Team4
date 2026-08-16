import streamlit as st
import requests
import re
import time
from config.config import AUTH_BASE_URL as BASE_URL

def mask_email(email: str) -> str:
    """Mask email address for privacy."""
    try:
        name, domain = email.split("@")
        if len(name) <= 2:
            return f"{name[0]}*@{domain}"
        return f"{name[0]}{'*' * (len(name) - 2)}{name[-1]}@{domain}"
    except Exception:
        return "******"

def signup_page():
    # Initialize signup session states
    if "signup_step" not in st.session_state:
        st.session_state.signup_step = 1
    if "signup_email" not in st.session_state:
        st.session_state.signup_email = ""
    if "signup_code" not in st.session_state:
        st.session_state.signup_code = ""
    if "signup_session_token" not in st.session_state:
        st.session_state.signup_session_token = ""
    if "signup_token" not in st.session_state:
        st.session_state.signup_token = ""
    if "otp_resend_cooldown" not in st.session_state:
        st.session_state.otp_resend_cooldown = 0

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.title("Create Your MarketMind AI Account")
        st.caption("Complete registration via your business invitation")
        st.markdown("---")

        # ==================================================
        # STEP 1: VERIFY INVITATION
        # ==================================================
        if st.session_state.signup_step == 1:
            email = st.text_input(
                "Email Address",
                placeholder="Enter your invited email address"
            )
            code = st.text_input(
                "Invitation Code",
                placeholder="Enter your 12-character invitation code"
            )

            if st.button("Verify Invitation", use_container_width=True):
                if not email.strip() or not code.strip():
                    st.error("Please fill in all fields.")
                else:
                    try:
                        res = requests.post(
                            f"{BASE_URL}/auth/signup/verify-invitation",
                            json={
                                "email": email.strip(),
                                "code": code.strip().upper()
                            },
                            timeout=10
                        )
                        if res.status_code == 200:
                            res_data = res.json()
                            st.session_state.signup_email = email.strip()
                            st.session_state.signup_code = code.strip().upper()
                            st.session_state.signup_session_token = res_data["session_token"]
                            st.session_state.signup_step = 2
                            st.success("Invitation verified successfully! Email OTP sent.")
                            
                            # Show simulated OTP in development mode
                            if res_data.get("otp_sim"):
                                st.info(f"🔑 [SIMULATED OTP]: **{res_data['otp_sim']}**")
                            st.rerun()
                        else:
                            detail = res.json().get("detail", "Invalid or expired invitation.")
                            st.error(f"Verification failed: {detail}")
                    except Exception as e:
                        st.error(f"Cannot connect to the gateway: {str(e)}")

            st.markdown("---")
            if st.button("⬅ Back to Login", use_container_width=True):
                st.session_state.page = "Login"
                st.rerun()

        # ==================================================
        # STEP 2: VERIFY OTP
        # ==================================================
        elif st.session_state.signup_step == 2:
            st.info(f"We've sent a 6-digit verification code to: **{mask_email(st.session_state.signup_email)}**")
            
            otp = st.text_input(
                "Enter OTP Verification Code",
                placeholder="Enter the 6-digit OTP code"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Verify Code", use_container_width=True):
                    if not otp.strip():
                        st.error("Please enter the verification code.")
                    elif len(otp.strip()) != 6 or not otp.strip().isdigit():
                        st.error("OTP must be a 6-digit code.")
                    else:
                        try:
                            res = requests.post(
                                f"{BASE_URL}/auth/signup/verify-otp",
                                json={
                                    "email": st.session_state.signup_email,
                                    "otp": otp.strip(),
                                    "session_token": st.session_state.signup_session_token
                                },
                                timeout=10
                            )
                            if res.status_code == 200:
                                res_data = res.json()
                                st.session_state.signup_token = res_data["signup_token"]
                                st.session_state.signup_step = 3
                                st.success("Email verified successfully!")
                                st.rerun()
                            else:
                                detail = res.json().get("detail", "Invalid verification code.")
                                st.error(f"Verification failed: {detail}")
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")

            with col2:
                # Resend OTP with cooldown logic
                current_time = time.time()
                cooldown_remaining = int(st.session_state.otp_resend_cooldown - current_time)
                
                if cooldown_remaining > 0:
                    st.button(f"Resend Code ({cooldown_remaining}s)", disabled=True, use_container_width=True)
                else:
                    if st.button("Resend Code", use_container_width=True):
                        try:
                            res = requests.post(
                                f"{BASE_URL}/auth/signup/verify-invitation",
                                json={
                                    "email": st.session_state.signup_email,
                                    "code": st.session_state.signup_code
                                },
                                timeout=10
                            )
                            if res.status_code == 200:
                                res_data = res.json()
                                st.session_state.signup_session_token = res_data["session_token"]
                                st.session_state.otp_resend_cooldown = time.time() + 60
                                st.success("A new verification code has been sent!")
                                if res_data.get("otp_sim"):
                                    st.info(f"🔑 [SIMULATED OTP]: **{res_data['otp_sim']}**")
                                st.rerun()
                            else:
                                detail = res.json().get("detail", "Resend failed.")
                                st.error(f"Resend failed: {detail}")
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")

            st.markdown("---")
            if st.button("⬅ Cancel Signup", use_container_width=True):
                st.session_state.signup_step = 1
                st.session_state.page = "Login"
                st.rerun()

        # ==================================================
        # STEP 3: CREATE ACCOUNT
        # ==================================================
        elif st.session_state.signup_step == 3:
            st.success("Verification complete. Please set your account credentials below.")

            name = st.text_input("Full Name", placeholder="Enter your full name")
            phone = st.text_input("Phone Number", placeholder="Enter your phone number")
            password = st.text_input("Password", type="password", placeholder="Enter a secure password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")

            if st.button("Create Account", use_container_width=True):
                if not name.strip() or not phone.strip() or not password.strip():
                    st.error("Please fill in all required fields.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    try:
                        res = requests.post(
                            f"{BASE_URL}/auth/signup/complete",
                            json={
                                "email": st.session_state.signup_email,
                                "signup_token": st.session_state.signup_token,
                                "name": name.strip(),
                                "phone": phone.strip(),
                                "password": password
                            },
                            timeout=10
                        )
                        if res.status_code == 200:
                            st.success("Account created successfully! You can now log in.")
                            
                            # Clean up signup states
                            st.session_state.signup_step = 1
                            st.session_state.signup_email = ""
                            st.session_state.signup_code = ""
                            st.session_state.signup_session_token = ""
                            st.session_state.signup_token = ""
                            
                            st.session_state.page = "Login"
                            st.rerun()
                        else:
                            detail = res.json().get("detail", "Signup completion failed.")
                            st.error(f"Failed to create account: {detail}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")

            st.markdown("---")
            if st.button("⬅ Cancel Signup", use_container_width=True):
                st.session_state.signup_step = 1
                st.session_state.page = "Login"
                st.rerun()
