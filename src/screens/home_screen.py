import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_background_home

def home_screen():
    st.title("Welcome to VoxVision")
    st.subheader("This is the home screen of the VoxVision application. Please select your role to proceed.")

    header_home()
    style_background_home()

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Student"):
            st.session_state['login_type'] = "student"
            st.rerun()
    with col2:
        if st.button("Teacher"):
            st.session_state['login_type'] = "teacher"
            st.rerun()