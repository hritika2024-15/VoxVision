import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_background_home

def home_screen():
    st.title("Welcome to VoxVision")
    st.subheader("This is the home screen of the VoxVision application. Please select your role to proceed.")

    header_home()
    style_background_home()

    spacer_left, buttons, spacer_right = st.columns([1, 2, 1])

    with buttons:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Student", use_container_width=True):
                st.session_state['login_type'] = "student"
                st.rerun()
        with col2:
            if st.button("Teacher", use_container_width=True):
                st.session_state['login_type'] = "teacher"
                st.rerun()