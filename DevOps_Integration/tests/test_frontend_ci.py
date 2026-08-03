# pyrefly: ignore-file
# type: ignore
import sys
import os

# Adjust sys.path to include frontend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

def test_frontend_streamlit_imports():
    """Verify Streamlit is correctly installed and imported by the frontend components."""
    import streamlit as st
    assert st is not None
