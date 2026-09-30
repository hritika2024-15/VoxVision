import streamlit as st
from pathlib import Path
import base64

def _asset_b64(filename):
    path = Path(__file__).resolve().parents[1] / "assets" / filename
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

def header_home():
    b64_hero = _asset_b64("hero_classroom.jpg")
    img_tag = ""
    if b64_hero:
        img_tag = f"""<div style="position: relative; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(37, 99, 235, 0.12); border: 3px solid #FFFFFF;">
<img src="data:image/jpeg;base64,{b64_hero}" style="width: 100%; height: auto; display: block;" alt="Classroom Voice and Face Attendance" />
<div style="position: absolute; top: 12px; left: 12px; background: rgba(37, 99, 235, 0.92); color: #FFFFFF; padding: 5px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.02em; box-shadow: 0 4px 12px rgba(37,99,235,0.25);">
Voice Input: Active
</div>
<div style="position: absolute; bottom: 12px; right: 12px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px); padding: 6px 14px; border-radius: 9999px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); font-size: 0.78rem; font-weight: 700; color: #047857; display: flex; align-items: center; gap: 6px;">
<span class="pulse-dot-green"></span> Voice &amp; Face: 100% Present
</div>
</div>"""

    hero_html = f"""<div style="background: linear-gradient(135deg, #F0F7FF 0%, #F5FBF7 50%, #FFFDF5 100%); border: 1px solid #DBEAFE; border-radius: 24px; padding: 2.2rem 2.5rem; margin-bottom: 2.4rem; box-shadow: 0 8px 30px rgba(37, 99, 235, 0.05);">
<div style="display: flex; justify-content: space-between; align-items: center; gap: 30px; flex-wrap: wrap;">
<div style="flex: 1 1 420px; min-width: 300px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.8rem;">
<span class="badge-blue">VOICE ATTENDANCE</span>
<span class="badge-green">FACIAL RECOGNITION</span>
<span class="badge-gray">CAMPUS ACTIVE</span>
</div>
<h1 style="margin: 0 0 0.6rem 0; font-size: 2.7rem; font-weight: 800; color: #0F172A; line-height: 1.15; letter-spacing: -0.03em;">
Attendance by <span style="color: #2563EB;">Voice</span> &amp; <span style="color: #059669;">Face</span>
</h1>
<p style="margin: 0 0 1.2rem 0; font-size: 1.05rem; color: #475569; line-height: 1.6; font-weight: 400;">
Effortless classroom roll call. Students check in by speaking "I am present" or through camera facial verification. VoxVision instantly identifies voices and faces in seconds so learning begins immediately.
</p>
<div style="display: flex; flex-wrap: wrap; gap: 8px;">
<span class="badge-blue" style="font-size: 0.8rem; padding: 4px 12px;">Acoustic Voice Roll Call</span>
<span class="badge-green" style="font-size: 0.8rem; padding: 4px 12px;">Multi-Student FaceID</span>
<span class="badge-gray" style="font-size: 0.8rem; padding: 4px 12px;">Automatic Course Sync</span>
</div>
</div>
<div style="flex: 1 1 380px; min-width: 300px; max-width: 480px;">
{img_tag}
</div>
</div>
</div>"""

    st.markdown(hero_html, unsafe_allow_html=True)

def header_dashboard():
    st.markdown(
        """<div style="display: flex; align-items: center; padding: 0.2rem 0;">
<div>
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.35rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">
Vox<span style="color: #2563EB;">Vision</span>
</span>
<span class="badge-green" style="font-size: 0.68rem; padding: 2px 7px;">ACTIVE</span>
</div>
<div style="font-size: 0.78rem; color: #64748B; font-weight: 500;">Voice &amp; Face Attendance Portal</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )