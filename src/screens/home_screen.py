import streamlit as st
from pathlib import Path
import base64

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_background_home

def _asset_b64(filename):
    path = Path(__file__).resolve().parents[1] / "assets" / filename
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

def home_screen():
    style_background_home()
    header_home()

    st.markdown(
        """<div style="text-align: center; margin-bottom: 1.6rem;">
<p style="font-size: 0.85rem; color: #2563EB; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.2rem;">
Campus Portal Gateway
</p>
<h3 style="font-size: 1.35rem; color: #0F172A; font-weight: 700; margin: 0;">
Please choose your portal to begin
</h3>
</div>""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    stu_b64 = _asset_b64("student_mascot.jpg")
    tea_b64 = _asset_b64("teacher_mascot.jpg")

    with col1:
        with st.container(border=True):
            if stu_b64:
                st.markdown(
                    f"""<div style="text-align: center; padding: 0.5rem 0 1rem 0;">
<div style="width: 140px; height: 140px; margin: 0 auto; border-radius: 20px; overflow: hidden; border: 2px solid #DBEAFE; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);">
<img src="data:image/jpeg;base64,{stu_b64}" style="width: 100%; height: 100%; object-fit: cover;" alt="Cute Student Mascot" />
</div>
</div>""",
                    unsafe_allow_html=True,
                )

            st.markdown(
                """<div style="margin-bottom: 0.8rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; height: 32px;">
<h3 style="margin: 0; font-size: 1.35rem; color: #0F172A; font-weight: 700;">Student Portal</h3>
<span class="badge-blue">STUDENT</span>
</div>
<p style="color: #64748B; font-size: 0.92rem; line-height: 1.5; margin: 0 0 0.8rem 0; height: 52px; overflow: hidden;">
Check in to class using voice or camera FaceID, inspect your attendance ledger, and manage course enrollments.
</p>
<div style="display: flex; flex-wrap: wrap; gap: 6px; height: 34px; align-items: center; margin-bottom: 0.6rem;">
<span class="badge-blue">Voice Check-in</span>
<span class="badge-green">Instant FaceID</span>
<span class="badge-gray">Course Ledger</span>
</div>
</div>""",
                unsafe_allow_html=True,
            )

            if st.button("Enter Student Portal", key="btn_student_portal", type="primary", use_container_width=True):
                st.session_state["login_type"] = "student"
                st.rerun()

    with col2:
        with st.container(border=True):
            if tea_b64:
                st.markdown(
                    f"""<div style="text-align: center; padding: 0.5rem 0 1rem 0;">
<div style="width: 140px; height: 140px; margin: 0 auto; border-radius: 20px; overflow: hidden; border: 2px solid #DCFCE7; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);">
<img src="data:image/jpeg;base64,{tea_b64}" style="width: 100%; height: 100%; object-fit: cover;" alt="Cute Teacher Mascot" />
</div>
</div>""",
                    unsafe_allow_html=True,
                )

            st.markdown(
                """<div style="margin-bottom: 0.8rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; height: 32px;">
<h3 style="margin: 0; font-size: 1.35rem; color: #0F172A; font-weight: 700;">Teacher Portal</h3>
<span class="badge-green">FACULTY</span>
</div>
<p style="color: #64748B; font-size: 0.92rem; line-height: 1.5; margin: 0 0 0.8rem 0; height: 52px; overflow: hidden;">
Conduct classroom roll call by voice or photos, monitor student attendance ledgers, and manage course rosters.
</p>
<div style="display: flex; flex-wrap: wrap; gap: 6px; height: 34px; align-items: center; margin-bottom: 0.6rem;">
<span class="badge-blue">Voice Roll Call</span>
<span class="badge-green">Photo Scan</span>
<span class="badge-gray">Course Roster</span>
</div>
</div>""",
                unsafe_allow_html=True,
            )

            if st.button("Enter Teacher Portal", key="btn_teacher_portal", type="secondary", use_container_width=True):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    # Academic Benefit Cards - Highlighting Voice & Face
    st.markdown(
        """<div style="margin-top: 2.8rem; padding: 1.4rem; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; text-align: center;">
<div>
<div style="color: #2563EB; font-size: 1.35rem; font-weight: 700;">Voice Attendance</div>
<div style="color: #64748B; font-size: 0.85rem; margin-top: 2px;">Record class audio to recognize student voices</div>
</div>
<div>
<div style="color: #059669; font-size: 1.35rem; font-weight: 700;">Facial Recognition</div>
<div style="color: #64748B; font-size: 0.85rem; margin-top: 2px;">Scan classroom photos or live camera feed</div>
</div>
<div>
<div style="color: #0F172A; font-size: 1.35rem; font-weight: 700;">Real-Time Records</div>
<div style="color: #64748B; font-size: 0.85rem; margin-top: 2px;">Instant calculation and course database sync</div>
</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    footer_home()