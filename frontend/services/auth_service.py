import json
import base64
import time
import streamlit as st


def save_auth_session(username: str, role: str, token: str, email: str = ""):
    """Save user authentication credentials to st.query_params to preserve login across refreshes."""
    try:
        payload = {
            "u": username,
            "r": role,
            "t": token,
            "e": email,
            "exp": int(time.time()) + (7 * 24 * 3600)  # 7 days expiration
        }
        raw_json = json.dumps(payload)
        encoded = base64.urlsafe_b64encode(raw_json.encode("utf-8")).decode("utf-8")
        st.query_params["_auth"] = encoded
    except Exception:
        pass


def restore_auth_session():
    """Restore authentication state from query params on page reload."""
    try:
        encoded = st.query_params.get("_auth")
        if not encoded:
            return False

        raw_json = base64.urlsafe_b64decode(encoded.encode("utf-8")).decode("utf-8")
        payload = json.loads(raw_json)

        # Check expiration
        if payload.get("exp", 0) < int(time.time()):
            clear_auth_session()
            return False

        st.session_state.logged_in = True
        st.session_state.username = payload.get("u", "User")
        st.session_state.role = payload.get("r", "Business Owner")
        st.session_state.token = payload.get("t", "")
        if payload.get("e"):
            st.session_state.email = payload.get("e")
        return True
    except Exception:
        clear_auth_session()
        return False


def clear_auth_session():
    """Clear authentication state from query params and session state."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.token = ""
    try:
        if "_auth" in st.query_params:
            del st.query_params["_auth"]
    except Exception:
        try:
            st.query_params.clear()
        except Exception:
            pass
