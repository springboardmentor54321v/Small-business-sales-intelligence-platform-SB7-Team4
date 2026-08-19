import streamlit as st
import re

from components.sidebar import show_sidebar


# ============================================================
# EXISTING USERNAMES
# ============================================================

existing_users = [
    "admin",
    "owner01",
    "manager01",
    "sales01",
    "rithika"
]


# ============================================================
# SETTINGS PAGE
# ============================================================

def settings_page():

    show_sidebar()

    # ========================================================
    # HEADER
    # ========================================================

    st.title("Settings")
    st.caption("Manage your MarketMind AI account and preferences")

    st.markdown("---")

    # ========================================================
    # PROFILE
    # ========================================================

    st.subheader("Profile")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        st.text_input(
            "Username",
            value=st.session_state.get("username", ""),
            disabled=True
        )

    with profile_col2:

        st.text_input(
            "Role",
            value=st.session_state.get("role", ""),
            disabled=True
        )

    st.markdown("")

    st.info(
        "Your profile information is managed by the system."
    )

    st.markdown("---")

    # ========================================================
    # CHANGE USERNAME
    # ========================================================

    st.subheader("Change Username")

    st.caption(
        "Choose a unique username containing at least 6 characters."
    )

    username_col1, username_col2 = st.columns([3, 1])

    with username_col1:

        new_username = st.text_input(
            "New Username",
            placeholder="Enter new username",
            key="new_username"
        )

    with username_col2:

        st.markdown("<br>", unsafe_allow_html=True)

        update_username = st.button(
            "Update Username",
            width="stretch"
        )

    if update_username:

        username = new_username.strip()

        if username == "":

            st.error(
                "Please enter a username."
            )

        elif len(username) < 6:

            st.error(
                "Username must contain at least 6 characters."
            )

        elif not re.fullmatch(
            r"[A-Za-z0-9@._-]{6,}",
            username
        ):

            st.error(
                "Username can contain only letters, numbers, @ . _ -"
            )

        elif username.lower() == st.session_state.get(
            "username",
            ""
        ).lower():

            st.warning(
                "This is already your current username."
            )

        elif username.lower() in [
            u.lower() for u in existing_users
        ]:

            st.error(
                "Username already exists."
            )

        else:

            st.session_state.username = username

            st.success(
                "Username updated successfully."
            )

    st.markdown("---")

    # ========================================================
    # CHANGE PASSWORD
    # ========================================================

    st.subheader("Change Password")

    st.caption(
        "Create a new password for your MarketMind AI account."
    )

    password_col1, password_col2 = st.columns(2)

    with password_col1:

        new_password = st.text_input(
            "New Password",
            type="password",
            placeholder="Enter new password",
            key="settings_new_password"
        )

    with password_col2:

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter new password",
            key="settings_confirm_password"
        )

    st.caption(
        "Password must contain at least 6 characters."
    )

    # ========================================================
    # PASSWORD STRENGTH
    # ========================================================

    if new_password:

        if len(new_password) < 6:

            st.progress(25)

            st.error(
                "Weak Password"
            )

        elif len(new_password) < 10:

            st.progress(60)

            st.warning(
                "Medium Password"
            )

        else:

            st.progress(100)

            st.success(
                "Strong Password"
            )

    st.markdown("")

    # ========================================================
    # CHANGE PASSWORD BUTTON
    # ========================================================

    if st.button(
        "Change Password",
        width="stretch"
    ):

        if new_password.strip() == "":

            st.error(
                "Please enter a new password."
            )

        elif confirm_password.strip() == "":

            st.error(
                "Please confirm your new password."
            )

        elif len(new_password) < 6:

            st.error(
                "Password must contain at least 6 characters."
            )

        elif not re.fullmatch(
            r"[A-Za-z0-9@#$%^&*!._-]{6,}",
            new_password
        ):

            st.error(
                "Password contains invalid characters."
            )

        elif new_password != confirm_password:

            st.error(
                "New password and confirm password do not match."
            )

        else:

            st.success(
                "✅ Password changed successfully."
            )

    st.markdown("---")

    # ========================================================
    # EMAIL & NOTIFICATION SETTINGS
    # ========================================================

    st.subheader("📧 Email & Notification Dispatch")
    st.caption("Configure your SMTP or Cloud Email API service to send real-time recovery OTPs and team invitations.")

    from services.email_dispatch import is_email_configured, save_email_credentials, dispatch_real_email_with_status
    configured, provider_name = is_email_configured()

    if configured:
        st.success(f"✅ Active Email Provider: **{provider_name}**")
    else:
        st.info("ℹ️ No email provider is currently configured. Configure your credentials below.")

    with st.expander("⚙️ Configure Email Provider (Gmail / Resend / Brevo / SMTP)", expanded=not configured):
        provider_choice = st.selectbox(
            "Select Provider",
            ["Gmail (Free App Password)", "Resend API (Free)", "Brevo API (Free)", "Custom SMTP"],
            key="settings_provider_choice"
        )

        if provider_choice == "Gmail (Free App Password)":
            g_user = st.text_input("Your Gmail Address", placeholder="e.g. yourname@gmail.com", key="settings_g_user")
            g_pass = st.text_input("16-character App Password", type="password", placeholder="e.g. abcd efgh ijkl mnop", key="settings_g_pass")
            st.caption("👉 Create an App Password in 10 seconds at: [Google App Passwords](https://myaccount.google.com/apppasswords)")
            if st.button("Save Gmail Configuration", key="save_g_btn", use_container_width=True):
                if not g_user.strip() or not g_pass.strip():
                    st.error("Please enter both your Gmail address and 16-character App Password.")
                else:
                    save_email_credentials(smtp_user=g_user.strip(), smtp_pass=g_pass.strip(), smtp_host="smtp.gmail.com", smtp_port="465")
                    st.success("✅ Gmail SMTP credentials saved successfully!")
                    st.rerun()

        elif provider_choice == "Resend API (Free)":
            r_key = st.text_input("Resend API Key", type="password", placeholder="re_123456789...", key="settings_r_key")
            st.caption("👉 Get a free API key at [resend.com](https://resend.com)")
            if st.button("Save Resend API Key", key="save_r_btn", use_container_width=True):
                if not r_key.strip():
                    st.error("Please enter your Resend API Key.")
                else:
                    save_email_credentials(resend_key=r_key.strip())
                    st.success("✅ Resend API key saved successfully!")
                    st.rerun()

        elif provider_choice == "Brevo API (Free)":
            b_key = st.text_input("Brevo API Key", type="password", placeholder="xkeysib-...", key="settings_b_key")
            st.caption("👉 Get a free API key at [brevo.com](https://brevo.com)")
            if st.button("Save Brevo API Key", key="save_b_btn", use_container_width=True):
                if not b_key.strip():
                    st.error("Please enter your Brevo API Key.")
                else:
                    save_email_credentials(brevo_key=b_key.strip())
                    st.success("✅ Brevo API key saved successfully!")
                    st.rerun()

        elif provider_choice == "Custom SMTP":
            c_host = st.text_input("SMTP Host", placeholder="smtp.example.com", key="settings_c_host")
            c_port = st.text_input("SMTP Port", placeholder="587 or 465", key="settings_c_port")
            c_user = st.text_input("SMTP Username/Email", key="settings_c_user")
            c_pass = st.text_input("SMTP Password", type="password", key="settings_c_pass")
            if st.button("Save Custom SMTP", key="save_c_btn", use_container_width=True):
                if not c_user.strip() or not c_pass.strip():
                    st.error("Please enter SMTP credentials.")
                else:
                    save_email_credentials(smtp_user=c_user.strip(), smtp_pass=c_pass.strip(), smtp_host=c_host.strip(), smtp_port=c_port.strip())
                    st.success("✅ Custom SMTP credentials saved successfully!")
                    st.rerun()

    test_col1, test_col2 = st.columns([3, 1])
    with test_col1:
        test_dest = st.text_input("Send Test Email To", placeholder="Enter recipient email", key="settings_test_dest")
    with test_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Send Test", use_container_width=True):
            if not test_dest.strip():
                st.error("Please enter an email address to test.")
            else:
                test_res = dispatch_real_email_with_status(
                    test_dest.strip(),
                    "MarketMind AI - Test Email",
                    "<h3>MarketMind AI Email System Test</h3><p>Your email system is successfully configured and delivering real messages!</p>"
                )
                if test_res.get("success"):
                    st.success(f"✅ Test email successfully delivered to **{test_dest}** via {test_res.get('provider')}!")
                else:
                    st.error(f"❌ Test delivery failed: {test_res.get('error')}")

    st.markdown("---")

    # ========================================================
    # ACCOUNT INFORMATION
    # ========================================================

    st.subheader("ℹ️ Account Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.metric(
            "Account Role",
            st.session_state.get(
                "role",
                "User"
            )
        )

    with info_col2:
        st.metric(
            "Account Status",
            "Active"
        )

    st.markdown("")

    # ========================================================
    # LOGOUT
    # ========================================================

    st.subheader("Session")
    st.caption(
        "Sign out of your MarketMind AI account."
    )

    if st.button(
        "Logout",
        width="stretch"
    ):

        from services.auth_service import clear_auth_session
        clear_auth_session()
        st.session_state.page = "Home"

        st.rerun()

    st.markdown("---")

    st.caption(
        "MarketMind AI • Account Settings • Version 2.0"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    settings_page()