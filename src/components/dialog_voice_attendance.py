import streamlit as st
import pandas as pd
from datetime import datetime
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from src.components.dialog_attendance_results import show_attendance_result

@st.dialog("Voice Attendance (Audio Roll Call)")
def voice_attendance_dialog(selected_subject_id):
    st.markdown(
        """<div style="margin-bottom: 0.8rem;">
<p style="color: #475569; font-size: 0.92rem; margin: 0; line-height: 1.5;">
Record classroom audio as students speak roll call phrases (e.g. <i>"I am present"</i>). The AI voice encoder compares voice acoustic embeddings with enrolled student profiles.
</p>
</div>""",
        unsafe_allow_html=True,
    )

    audio_data = st.audio_input("Record classroom roll call audio")

    if st.button("Analyze Audio & Mark Attendance", type="primary", use_container_width=True):
        if not audio_data:
            st.warning("Please record audio before analyzing.")
            return

        with st.spinner("Processing speech audio & identifying student voices..."):
            enrolled_res = supabase.table("subject_students").select("*, students(*)").eq("subject_id", selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this course.")
                return

            candidates_dict = {
                s["students"]["student_id"]: s["students"]["voice_embedding"]
                for s in enrolled_students
                if s["students"].get("voice_embedding")
            }

            if not candidates_dict:
                st.error("No enrolled students have registered voice profiles yet.")
                return

            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node["students"]
                score = detected_scores.get(student["student_id"], 0.0)
                is_present = bool(score > 0)

                results.append({
                    "Name": student["name"],
                    "ID": student["student_id"],
                    "Confidence": f"{score:.2f}" if is_present else "-",
                    "Status": "Present" if is_present else "Absent"
                })

                attendance_to_log.append({
                    "student_id": student["student_id"],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get("voice_attendance_results"):
        st.markdown("<hr style='margin: 1.2rem 0;'/>", unsafe_allow_html=True)
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)