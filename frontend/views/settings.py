import streamlit as st
from components.sidebar import show_sidebar

# Dummy existing usernames
existing_users = [
    "admin",
    "owner01",
    "manager01",
    "sales01",
    "rithika"
]


def settings_page():

    show_sidebar()

    st.title("⚙️ Settings")
    st.caption("Manage your account settings")

    st.markdown("---")

    # ---------------- Profile ---------------- #

    st.subheader("👤 Profile")

    st.text_input(
        "Current Username",
        value=st.session_state.username,
        disabled=True
    )

    st.text_input(
        "Role",
        value=st.session_state.role,
        disabled=True
    )

    st.markdown("---")

    # ---------------- Username ---------------- #

    st.subheader("✏️ Change Username")

    new_username = st.text_input(
        "New Username"
    )

    if st.button("Check Username Availability"):

        if len(new_username) < 6:
            st.error("Username must contain at least 6 characters.")

        elif new_username.lower() in [user.lower() for user in existing_users]:
            st.error("❌ Username already exists.")

        else:
            st.success("✅ Username is available.")

    if st.button("Update Username"):

        if len(new_username) < 6:
            st.error("Username must contain at least 6 characters.")

        elif new_username.lower() in [user.lower() for user in existing_users]:
            st.error("❌ Username already exists.")

        else:
            st.session_state.username = new_username
            st.success("✅ Username updated successfully.")

    st.markdown("---")

    # ---------------- Password ---------------- #

    st.subheader("🔒 Change Password")

    show = st.checkbox("Show Password")

    current_password = st.text_input(
        "Current Password",
        type="default" if show else "password"
    )

    new_password = st.text_input(
        "New Password",
        type="default" if show else "password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="default" if show else "password"
    )

    st.caption("Password must contain at least 6 characters.")

    if st.button("Change Password"):

        if current_password.strip() == "":
            st.error("Please enter your current password.")

        elif len(new_password) < 6:
            st.error("Password must contain at least 6 characters.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:
            st.success("✅ Password changed successfully.")

    st.markdown("---")

    # ---------------- Logout ---------------- #

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.page = "Home"

        st.rerun()