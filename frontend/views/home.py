import streamlit as st

def home_page():

    st.title("MarketMind AI")

    st.subheader("Small Business Sales Intelligence Platform")

    st.markdown("---")

    st.markdown("""
### Welcome!

MarketMind AI helps businesses:

- Analyze Sales
- Manage Inventory
- Manage Customers
- Generate Reports
- AI Powered Insights
""")

    col1, col2, col3 = st.columns([2,1,2])

    with col2:
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

    st.markdown("---")

    st.caption("© 2026 MarketMind AI")