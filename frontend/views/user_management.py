import streamlit as st
import requests
import re
from config.config import AUTH_BASE_URL as BASE_URL
from components.sidebar import show_sidebar

def user_management_page():
    show_sidebar()

    st.title("User Management")
    st.caption("Manage business invitations and team permissions")
    st.markdown("---")

    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    tab1, tab2 = st.tabs(["Invite New User", "Sent Invitations"])

    # ==================================================
    # TAB 1: INVITE NEW USER
    # ==================================================
    with tab1:
        st.subheader("Invite User")
        st.markdown("Invite a new member to join your business account. They will receive an email containing a secure code to register.")

        with st.form("invite_form", clear_on_submit=True):
            email = st.text_input(
                "Email Address",
                placeholder="Enter recipient's email (e.g. employee@domain.com)"
            )
            role = st.selectbox(
                "Permitted Role",
                ["Store Manager", "Sales Executive"]
            )
            
            submit = st.form_submit_button("Send Invitation", use_container_width=True)

            if submit:
                if not email.strip():
                    st.error("Please enter an email address.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
                    st.error("Please enter a valid email address.")
                else:
                    try:
                        res = requests.post(
                            f"{BASE_URL}/api/invitations",
                            json={"email": email.strip(), "role": role},
                            headers=headers,
                            timeout=10
                        )
                        if res.status_code == 201:
                            st.success(f"Invitation sent successfully to {email.strip()}!")
                            # Show simulated invitation code in development mode (if returned by backend)
                            res_data = res.json()
                            if res_data.get("code_sim"):
                                st.info(f"🔑 [SIMULATED INVITATION CODE]: **{res_data['code_sim']}**")
                        else:
                            detail = res.json().get("detail", "Failed to send invitation.")
                            st.error(f"Error: {detail}")
                    except Exception as e:
                        st.error(f"Failed to connect to gateway: {str(e)}")

    # ==================================================
    # TAB 2: SENT INVITATIONS
    # ==================================================
    with tab2:
        st.subheader("Pending & Sent Invitations")
        
        try:
            res = requests.get(
                f"{BASE_URL}/api/invitations",
                headers=headers,
                timeout=10
            )
            if res.status_code == 200:
                invitations = res.json()
                if not invitations:
                    st.info("No invitations sent yet.")
                else:
                    for inv in invitations:
                        # Color coding status
                        status_color = "#ff4b4b"
                        if inv["status"] == "PENDING":
                            status_color = "#ffaa00"
                        elif inv["status"] == "USED":
                            status_color = "#00cc66"
                        
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        with col1:
                            st.markdown(f"**{inv['email']}**")
                            st.caption(f"Role: {inv['role']}")
                        with col2:
                            st.markdown(f"<span style='color:{status_color}; font-weight:bold;'>{inv['status']}</span>", unsafe_allow_html=True)
                            st.caption(f"Expires: {inv['expires_at'][:10]}")
                        with col3:
                            if inv["status"] == "PENDING":
                                if st.button("Revoke", key=f"revoke_{inv['id']}", use_container_width=True):
                                    try:
                                        revoke_res = requests.delete(
                                            f"{BASE_URL}/api/invitations/{inv['id']}",
                                            headers=headers,
                                            timeout=10
                                        )
                                        if revoke_res.status_code == 200:
                                            st.success("Invitation revoked successfully!")
                                            st.rerun()
                                        else:
                                            detail = revoke_res.json().get("detail", "Revocation failed.")
                                            st.error(f"Error: {detail}")
                                    except Exception as e:
                                        st.error(f"Connection failed: {str(e)}")
                            else:
                                st.write("")
                        with col4:
                            st.write("")
                        st.markdown("---")
            else:
                st.error("Failed to load invitations.")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
