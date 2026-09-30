import streamlit as st
import time
import numpy as np
from PIL import Image

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding, identify_speaker
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
)

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    student_name = student_data.get("name", "Student")

    # Top Navigation Bar
    nav_c1, nav_c2 = st.columns([3, 1], vertical_alignment="center")
    with nav_c1:
        header_dashboard()
    with nav_c2:
        if st.button("Log Out", type="secondary", key="student_logout_btn", use_container_width=True):
            st.session_state["is_logged_in"] = False
            if "student_data" in st.session_state:
                del st.session_state.student_data
            st.rerun()

    # Load enrolled subjects and attendance records
    with st.spinner("Loading student dashboard..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    total_attended_overall = 0
    total_sessions_overall = len(logs)

    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1
            total_attended_overall += 1

    overall_pct = (
        round((total_attended_overall / total_sessions_overall) * 100)
        if total_sessions_overall > 0
        else 100
    )
    pct_color = "#059669" if overall_pct >= 75 else "#D97706"

    initials = "".join([part[0].upper() for part in student_name.split() if part])[:2] or "ST"

    # Profile Ribbon
    hero_html = f"""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.4rem; margin: 1.2rem 0 1.6rem 0; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="width: 48px; height: 48px; border-radius: 12px; background: #EFF6FF; border: 1px solid #DBEAFE; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #2563EB; font-size: 1.1rem;">
{initials}
</div>
<div>
<div style="display: flex; align-items: center; gap: 8px;">
<h2 style="margin: 0; font-size: 1.4rem; color: #0F172A; font-weight: 700;">Welcome, {student_name}</h2>
<span class="badge-blue" style="font-size: 0.68rem;">ID #{student_id}</span>
</div>
<div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">
<span class="pulse-dot-green"></span> Student Attendance Portal
</div>
</div>
</div>
<div style="display: flex; gap: 20px; align-items: center;">
<div style="text-align: right;">
<div style="font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Overall Attendance</div>
<div style="font-size: 1.35rem; font-weight: 700; color: {pct_color};">{overall_pct}%</div>
</div>
<div style="text-align: right; border-left: 1px solid #E2E8F0; padding-left: 15px;">
<div style="font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Enrolled Subjects</div>
<div style="font-size: 1.35rem; font-weight: 700; color: #2563EB;">{len(subjects)}</div>
</div>
</div>
</div>
</div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

    # Subject Section Header
    sec_c1, sec_c2 = st.columns([2, 1], vertical_alignment="center")
    with sec_c1:
        st.markdown(
            """<div style="display: flex; align-items: center; gap: 8px;">
<h3 style="margin: 0; font-size: 1.25rem; color: #0F172A; font-weight: 700;">Your Enrolled Subjects</h3>
<span class="badge-gray" style="font-size: 0.72rem;">Academic Courses</span>
</div>""",
            unsafe_allow_html=True,
        )
    with sec_c2:
        if st.button("Enroll in Subject", type="primary", use_container_width=True):
            enroll_dialog()

    st.markdown("<hr style='margin: 1.2rem 0;'/>", unsafe_allow_html=True)

    if not subjects:
        empty_subjects_html = """<div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 14px; padding: 2.5rem; text-align: center; margin: 1.5rem 0;">
<h3 style="color: #0F172A; margin-bottom: 0.3rem;">No Courses Enrolled Yet</h3>
<p style="color: #64748B; max-width: 420px; margin: 0 auto 1rem auto; font-size: 0.9rem;">
You are not currently enrolled in any subjects. Click 'Enroll in Subject' above with the course code provided by your teacher.
</p>
</div>"""
        st.markdown(empty_subjects_html, unsafe_allow_html=True)
    else:
        cols = st.columns(2, gap="medium")
        for i, sub_node in enumerate(subjects):
            sub = sub_node["subjects"]
            sid = sub["subject_id"]
            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll_button(s_name=sub["name"], s_id=sid):
                if st.button(
                    f"Unenroll from {s_name}",
                    key=f"unenroll_{s_id}",
                    type="tertiary",
                    use_container_width=True,
                ):
                    unenroll_student_to_subject(student_id, s_id)
                    st.toast(f"Unenrolled from {s_name} successfully")
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=[
                        ("Total Sessions", stats["total"]),
                        ("Attended", stats["attended"]),
                    ],
                    footer_callback=unenroll_button,
                )

    footer_dashboard()

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Student Login Header
    top_c1, top_c2 = st.columns([3, 1], vertical_alignment="center")
    with top_c1:
        header_dashboard()
    with top_c2:
        if st.button("Return Home", type="secondary", key="student_back_home", use_container_width=True):
            st.session_state["login_type"] = None
            st.rerun()

    login_head_html = """<div style="text-align: center; margin: 1.5rem 0 1.2rem 0;">
<div style="display: flex; justify-content: center; gap: 8px; margin-bottom: 0.4rem;">
<span class="badge-blue">VOICE ATTENDANCE</span>
<span class="badge-green">FACIAL RECOGNITION</span>
</div>
<h2 style="font-size: 1.8rem; margin: 0.3rem 0 0.2rem 0; color: #0F172A; font-weight: 700;">
Student Attendance Verification
</h2>
<p style="color: #64748B; font-size: 0.95rem; margin: 0;">
Check in using your voice or camera face identification
</p>
</div>"""
    st.markdown(login_head_html, unsafe_allow_html=True)

    tab_voice, tab_face, tab_reg = st.tabs([
        "Voice Check-In",
        "FaceID Check-In",
        "Register as New Student"
    ])

    with tab_voice:
        with st.container(border=True):
            st.markdown(
                """<div style="margin-bottom: 0.8rem;">
<h4 style="margin: 0 0 0.2rem 0; font-size: 1.1rem; color: #0F172A; font-weight: 700;">Voice Recognition Check-In</h4>
<p style="color: #64748B; font-size: 0.88rem; margin: 0;">
Record audio of yourself saying <i>"I am present"</i>. The AI compares your vocal frequency signature against student profiles.
</p>
</div>""",
                unsafe_allow_html=True,
            )
            v_audio = st.audio_input("Microphone input: Speak 'I am present'", key="student_voice_input")

            if st.button("Verify Voice Check-In", key="btn_verify_voice", type="primary", use_container_width=True):
                if not v_audio:
                    st.warning("Please record your voice phrase before verifying.")
                else:
                    with st.spinner("Analyzing vocal frequencies and matching student profile..."):
                        all_students = get_all_students()
                        candidates_dict = {
                            s["student_id"]: s["voice_embedding"]
                            for s in all_students
                            if s.get("voice_embedding")
                        }
                        if not candidates_dict:
                            st.warning("No students have registered voice profiles yet. Please register your voice in the Register tab.")
                        else:
                            audio_bytes = v_audio.read()
                            new_emb = get_voice_embedding(audio_bytes)
                            if new_emb:
                                matched_id, score = identify_speaker(new_emb, candidates_dict, threshold=0.60)
                                if matched_id:
                                    student = next((s for s in all_students if s["student_id"] == matched_id), None)
                                    if student:
                                        st.session_state.is_logged_in = True
                                        st.session_state.user_role = "student"
                                        st.session_state.student_data = student
                                        st.toast(f"Voice verified! Welcome back, {student['name']}")
                                        time.sleep(1)
                                        st.rerun()
                                else:
                                    st.error("Voice not recognized in records. Please try speaking clearly or register your voice in the Register tab.")
                            else:
                                st.error("Could not process voice sample. Please ensure clear speech.")

    with tab_face:
        with st.container(border=True):
            st.markdown(
                """<div style="margin-bottom: 0.8rem;">
<h4 style="margin: 0 0 0.2rem 0; font-size: 1.1rem; color: #0F172A; font-weight: 700;">FaceID Camera Check-In</h4>
<p style="color: #64748B; font-size: 0.88rem; margin: 0;">
Position your face centered in the camera frame to instantly verify attendance.
</p>
</div>""",
                unsafe_allow_html=True,
            )
            photo_source = st.camera_input("Camera View", key="student_camera_input")

            if photo_source:
                img = np.array(Image.open(photo_source))
                with st.spinner("Scanning facial landmarks..."):
                    detected, all_ids, num_faces = predict_attendance(img)
                    if num_faces == 0:
                        st.warning("No face detected. Please ensure proper lighting and face the camera directly.")
                    elif num_faces > 1:
                        st.warning("Multiple faces detected. Please ensure only one person is in front of the camera.")
                    else:
                        if detected:
                            student_id = list(detected.keys())[0]
                            all_students = get_all_students()
                            student = next((s for s in all_students if s["student_id"] == student_id), None)
                            if student:
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = student
                                st.toast(f"Face verified! Welcome back, {student['name']}")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.info("Face not recognized in student records. If you are new, please register in the Register tab.")

    with tab_reg:
        with st.container(border=True):
            st.markdown(
                """<div style="margin-bottom: 1rem;">
<span class="badge-blue">NEW STUDENT ONBOARDING</span>
<h4 style="margin: 0.3rem 0 0.2rem 0; font-size: 1.15rem; color: #0F172A; font-weight: 700;">
Register Voice &amp; Face Profile
</h4>
<p style="color: #64748B; font-size: 0.88rem; margin: 0;">
Register both your facial features and voice pattern for dual-modality attendance check-in.
</p>
</div>""",
                unsafe_allow_html=True,
            )

            new_name = st.text_input("Full Name", placeholder="E.g. Alexander Vance", key="reg_student_name")

            reg_col1, reg_col2 = st.columns(2, gap="medium")
            with reg_col1:
                st.markdown("<p style='font-size: 0.88rem; font-weight: 600; color: #0F172A; margin: 0 0 4px 0;'>Face Identification Photo</p>", unsafe_allow_html=True)
                reg_photo = st.camera_input("Capture facial reference photo", key="reg_photo_input")

            with reg_col2:
                st.markdown("<p style='font-size: 0.88rem; font-weight: 600; color: #0F172A; margin: 0 0 4px 0;'>Voice Reference Sample</p>", unsafe_allow_html=True)
                reg_audio = st.audio_input("Speak: 'I am present, my name is [Your Name]'", key="reg_audio_input")

            st.markdown("<hr style='margin: 1rem 0;'/>", unsafe_allow_html=True)

            if st.button("Complete Registration & Enter Portal", type="primary", use_container_width=True, key="btn_complete_reg"):
                if not new_name.strip():
                    st.warning("Please enter your full name.")
                elif not reg_photo:
                    st.warning("Please capture a facial reference photo.")
                else:
                    with st.spinner("Processing biometric profiles and creating student record..."):
                        img = np.array(Image.open(reg_photo))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if reg_audio:
                                voice_emb = get_voice_embedding(reg_audio.read())

                            response_data = create_student(
                                new_name.strip(),
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Account registered! Welcome, {new_name}")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Could not capture clear facial features. Please retake photo with good lighting.")

    footer_dashboard()