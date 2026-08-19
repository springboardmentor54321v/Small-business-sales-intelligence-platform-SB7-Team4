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