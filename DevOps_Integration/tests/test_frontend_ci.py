# pyrefly: ignore-file
# type: ignore
import sys
import os


def test_frontend_streamlit_imports():
    """Verify Streamlit is correctly installed and imported by the frontend components."""
    import streamlit as st
    assert st is not None
