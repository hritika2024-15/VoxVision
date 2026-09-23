from pathlib import Path

import streamlit as st


def _asset_path(filename):
    return Path(__file__).resolve().parents[1] / "assets" / filename


def header_home():
    st.image(str(_asset_path("attendance.jpg")), width=500)
    st.markdown(
        "<h1 style='text-align:center; color:#E0E3FF'>Vox<br/>Vision</h1>",
        unsafe_allow_html=True,
    )


def header_dashboard():
    st.image(str(_asset_path("attendance.jpg")), width=85)
    st.markdown(
        "<h2 style='text-align:center; color:#5865F2'>Vox<br/>Vision</h2>",
        unsafe_allow_html=True,
    )