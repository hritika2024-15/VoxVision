import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import time

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
)
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_name = teacher_data.get("name", "Instructor")
    teacher_id = teacher_data["teacher_id"]

    # Top Navigation Bar
    nav_c1, nav_c2 = st.columns([3, 1], vertical_alignment="center")
    with nav_c1:
        header_dashboard()
    with nav_c2:
        if st.button("Log Out", type="secondary", key="teacher_logout_btn", use_container_width=True):
            st.session_state["is_logged_in"] = False
            if "teacher_data" in st.session_state:
                del st.session_state.teacher_data
            st.rerun()

    # Pre-fetch stats for the instructor summary
    subjects = get_teacher_subjects(teacher_id) or []
    total_students_count = sum(s.get("total_students", 0) for s in subjects)

    initials = "".join([part[0].upper() for part in teacher_name.split() if part])[:2] or "TC"

    # Faculty Command Summary Banner
    hero_html = f"""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.4rem; margin: 1.2rem 0 1.6rem 0; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="width: 48px; height: 48px; border-radius: 12px; background: #F0FDF4; border: 1px solid #DCFCE7; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #059669; font-size: 1.1rem;">
{initials}
</div>
<div>
<div style="display: flex; align-items: center; gap: 8px;">
<h2 style="margin: 0; font-size: 1.4rem; color: #0F172A; font-weight: 700;">Welcome, {teacher_name}</h2>
<span class="badge-green" style="font-size: 0.68rem;">Faculty Member</span>
</div>
<div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">
<span class="pulse-dot-green"></span> Instructor Portal • Ready for Attendance
</div>
</div>
</div>
<div style="display: flex; gap: 20px; align-items: center;">
<div style="text-align: right;">
<div style="font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Active Courses</div>
<div style="font-size: 1.35rem; font-weight: 700; color: #2563EB;">{len(subjects)}</div>
</div>
<div style="text-align: right; border-left: 1px solid #E2E8F0; padding-left: 15px;">
<div style="font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Total Students</div>
<div style="font-size: 1.35rem; font-weight: 700; color: #059669;">{total_students_count}</div>
</div>
</div>
</div>
</div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

    # Clean Segmented Navigation Tabs
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    t_col1, t_col2, t_col3 = st.columns(3, gap="small")

    with t_col1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "secondary"
        if st.button("Take Attendance", type=type1, use_container_width=True):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with t_col2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "secondary"
        if st.button("Manage Subjects", type=type2, use_container_width=True):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with t_col3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "secondary"
        if st.button("Attendance Records", type=type3, use_container_width=True):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.markdown("<hr style='margin: 1.4rem 0;'/>", unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance(subjects)
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects(subjects)
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()

def teacher_tab_take_attendance(subjects):
    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.markdown(
        """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
<div>
<h3 style="margin: 0; color: #0F172A; font-size: 1.3rem; font-weight: 700;">Take Class Attendance</h3>
<p style="margin: 2px 0 0 0; color: #64748B; font-size: 0.9rem;">
Choose your preferred attendance method: record classroom audio for voice attendance, or capture photos for facial recognition
</p>
</div>
<span class="badge-blue"><span class="pulse-dot-green"></span> READY</span>
</div>""",
        unsafe_allow_html=True,
    )

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if not subjects:
        st.warning("You haven't created any subjects yet. Please create one under 'Manage Subjects' to get started.")
        return

    subject_options = {f"{s['name']} ({s['subject_code']})": s["subject_id"] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom", gap="medium")

    with col1:
        selected_subject_label = st.selectbox("Select Target Course", options=list(subject_options.keys()))

    with col2:
        if st.button("Add Classroom Photos", type="secondary", use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.markdown("<hr style='margin: 1.2rem 0;'/>", unsafe_allow_html=True)

    # Dual prominent options: Voice Attendance and Face Attendance
    method_col1, method_col2 = st.columns(2, gap="large")

    with method_col1:
        with st.container(border=True):
            st.markdown(
                """<div style="margin-bottom: 0.8rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
<h4 style="margin: 0; color: #0F172A; font-size: 1.15rem; font-weight: 700;">Option A: Voice Attendance</h4>
<span class="badge-blue">VOICE ROLL CALL</span>
</div>
<p style="color: #64748B; font-size: 0.88rem; margin: 0; line-height: 1.45;">
Record classroom audio while students say "I am present". AI identifies and verifies each enrolled student's voice profile automatically.
</p>
</div>""",
                unsafe_allow_html=True,
            )
            if st.button("Start Voice Attendance", key="start_voice_btn", type="primary", use_container_width=True):
                voice_attendance_dialog(selected_subject_id)

    with method_col2:
        with st.container(border=True):
            st.markdown(
                """<div style="margin-bottom: 0.8rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
<h4 style="margin: 0; color: #0F172A; font-size: 1.15rem; font-weight: 700;">Option B: Facial Recognition</h4>
<span class="badge-green">PHOTO SCAN</span>
</div>
<p style="color: #64748B; font-size: 0.88rem; margin: 0; line-height: 1.45;">
Scan classroom photos to recognize all enrolled students simultaneously and generate instant attendance records.
</p>
</div>""",
                unsafe_allow_html=True,
            )
            has_photos = bool(st.session_state.attendance_images)
            p_c1, p_c2 = st.columns(2, gap="small")
            with p_c1:
                if st.button("Run Face Analysis", use_container_width=True, type="primary" if has_photos else "secondary", disabled=not has_photos):
                    with st.spinner("Analyzing classroom photos and identifying students..."):
                        all_detected_ids = {}

                        for idx, img in enumerate(st.session_state.attendance_images):
                            img_np = np.array(img.convert("RGB"))
                            detected, _, _ = predict_attendance(img_np)

                            if detected:
                                for sid in detected.keys():
                                    student_id = int(sid)
                                    all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                        enrolled_res = (
                            supabase.table("subject_students")
                            .select("*, students(*)")
                            .eq("subject_id", selected_subject_id)
                            .execute()
                        )
                        enrolled_students = enrolled_res.data

                        if not enrolled_students:
                            st.warning("No students currently enrolled in this subject.")
                        else:
                            results, attendance_to_log = [], []
                            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                            for node in enrolled_students:
                                student = node["students"]
                                sources = all_detected_ids.get(int(student["student_id"]), [])
                                is_present = len(sources) > 0

                                results.append(
                                    {
                                        "Name": student["name"],
                                        "ID": student["student_id"],
                                        "Source": ", ".join(sources) if is_present else "-",
                                        "Status": "Present" if is_present else "Absent",
                                    }
                                )

                                attendance_to_log.append(
                                    {
                                        "student_id": student["student_id"],
                                        "subject_id": selected_subject_id,
                                        "timestamp": current_timestamp,
                                        "is_present": bool(is_present),
                                    }
                                )

                            attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
            with p_c2:
                if st.button("Clear Photos", use_container_width=True, type="tertiary", disabled=not has_photos):
                    st.session_state.attendance_images = []
                    st.rerun()

    if st.session_state.attendance_images:
        gallery_header_html = f"""<div style="display: flex; align-items: center; gap: 8px; margin: 1.2rem 0 0.8rem 0;">
<span class="badge-blue">PHOTOS ADDED</span>
<span style="color: #0F172A; font-weight: 600; font-size: 0.95rem;">Classroom Photos ({len(st.session_state.attendance_images)})</span>
</div>"""
        st.markdown(gallery_header_html, unsafe_allow_html=True)

        gallery_cols = st.columns(4, gap="small")
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {idx+1}")
            voice_attendance_dialog(selected_subject_id)

def teacher_tab_manage_subjects(subjects):
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        st.markdown(
            """<div style="display: flex; align-items: center; gap: 8px;">
<h3 style="margin: 0; font-size: 1.3rem; color: #0F172A; font-weight: 700;">Your Created Subjects</h3>
<span class="badge-blue">Course Directory</span>
</div>""",
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("Create New Subject", type="primary", use_container_width=True):
            create_subject_dialog(teacher_id)

    st.markdown("<hr style='margin: 1.2rem 0;'/>", unsafe_allow_html=True)

    if subjects:
        cols = st.columns(2, gap="medium")
        for i, sub in enumerate(subjects):
            stats = [
                ("Students Enrolled", sub.get("total_students", 0)),
                ("Classes Held", sub.get("total_classes", 0)),
            ]

            def share_btn(s_name=sub["name"], s_code=sub["subject_code"]):
                if st.button(
                    f"Share Class Code: {s_code}",
                    key=f"share_{s_code}",
                    type="secondary",
                    use_container_width=True,
                ):
                    share_subject_dialog(s_name, s_code)

            with cols[i % 2]:
                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=stats,
                    footer_callback=share_btn,
                )
    else:
        no_course_html = """<div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 14px; padding: 2.5rem; text-align: center; margin: 1.5rem 0;">
<h3 style="color: #0F172A; margin-bottom: 0.3rem;">No Subjects Created Yet</h3>
<p style="color: #64748B; max-width: 420px; margin: 0 auto 1rem auto; font-size: 0.9rem;">
You haven't set up any subjects yet. Click 'Create New Subject' above to add your first course and generate a join code.
</p>
</div>"""
        st.markdown(no_course_html, unsafe_allow_html=True)

def teacher_tab_attendance_records():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.markdown(
        """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
<div>
<h3 style="margin: 0; color: #0F172A; font-size: 1.3rem; font-weight: 700;">Attendance Records</h3>
<p style="margin: 2px 0 0 0; color: #64748B; font-size: 0.9rem;">
Historical classroom attendance logs and student participation records
</p>
</div>
<span class="badge-green"><span class="pulse-dot-green"></span> SYNCHRONIZED</span>
</div>""",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading attendance records..."):
        records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet. Complete an attendance check-in to view history.")
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        data.append(
            {
                "ts_group": ts.split(".")[0] if ts else None,
                "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
                "Subject": r["subjects"]["name"],
                "Subject Code": r["subjects"]["subject_code"],
                "is_present": bool(r.get("is_present", False)),
            }
        )

    df = pd.DataFrame(data)

    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"])
        .agg(Present_Count=("is_present", "sum"), Total_Count=("is_present", "count"))
        .reset_index()
    )

    summary["Attendance Stats"] = (
        summary["Present_Count"].astype(str) + " / " + summary["Total_Count"].astype(str) + " Students Present"
    )

    display_df = summary.sort_values(by="ts_group", ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance Stats"]
    ]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username is already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Teacher account created successfully! Please sign in."
    except Exception:
        return False, "An unexpected error occurred."

def teacher_screen_login():
    top_c1, top_c2 = st.columns([3, 1], vertical_alignment="center")
    with top_c1:
        header_dashboard()
    with top_c2:
        if st.button("Return Home", type="secondary", key="teacher_back_home", use_container_width=True):
            st.session_state["login_type"] = None
            st.rerun()

    login_head_html = """<div style="text-align: center; margin: 1.8rem 0 1.4rem 0;">
<span class="badge-blue"><span class="pulse-dot-green"></span> TEACHER PORTAL</span>
<h2 style="font-size: 1.8rem; margin: 0.4rem 0 0.2rem 0; color: #0F172A; font-weight: 700;">
Teacher Sign In
</h2>
<p style="color: #64748B; font-size: 0.95rem; margin: 0;">
Sign in with your credentials to manage your classes and take attendance
</p>
</div>"""
    st.markdown(login_head_html, unsafe_allow_html=True)

    with st.container(border=True):
        teacher_username = st.text_input("Username", placeholder="e.g. hritikaprasad")
        teacher_pass = st.text_input("Password", type="password", placeholder="Enter your password")

        st.markdown("<hr style='margin: 1.2rem 0;'/>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2, gap="medium")

        with btnc1:
            if st.button("Sign In", type="primary", use_container_width=True):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("Welcome back")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with btnc2:
            if st.button("Create Account", type="secondary", use_container_width=True):
                st.session_state.teacher_login_type = "register"
                st.rerun()

    footer_dashboard()

def teacher_screen_register():
    top_c1, top_c2 = st.columns([3, 1], vertical_alignment="center")
    with top_c1:
        header_dashboard()
    with top_c2:
        if st.button("Return Home", type="secondary", key="teacher_reg_back_home", use_container_width=True):
            st.session_state["login_type"] = None
            st.rerun()

    reg_head_html = """<div style="text-align: center; margin: 1.8rem 0 1.4rem 0;">
<span class="badge-blue">NEW TEACHER</span>
<h2 style="font-size: 1.8rem; margin: 0.4rem 0 0.2rem 0; color: #0F172A; font-weight: 700;">
Create Teacher Account
</h2>
<p style="color: #64748B; font-size: 0.95rem; margin: 0;">
Register your teacher profile to start creating classes and taking attendance
</p>
</div>"""
    st.markdown(reg_head_html, unsafe_allow_html=True)

    with st.container(border=True):
        teacher_username = st.text_input("Username", placeholder="e.g. hritikaprasad")
        teacher_name = st.text_input("Full Name", placeholder="e.g. Hritika Prasad")
        teacher_pass = st.text_input("Password", type="password", placeholder="Create a password")
        teacher_pass_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")

        st.markdown("<hr style='margin: 1.2rem 0;'/>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2, gap="medium")

        with btnc1:
            if st.button("Register Account", type="primary", use_container_width=True):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    time.sleep(1.5)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(message)

        with btnc2:
            if st.button("Already have an account? Sign In", type="secondary", use_container_width=True):
                st.session_state.teacher_login_type = "login"
                st.rerun()

    footer_dashboard()