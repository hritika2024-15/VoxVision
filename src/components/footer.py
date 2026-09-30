import streamlit as st

def footer_home():
    st.markdown(
        """<div style="margin-top: 3.5rem; padding-top: 1.5rem; border-top: 1px solid #E2E8F0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.9rem; font-weight: 700; color: #0F172A;">
Vox<span style="color: #2563EB;">Vision</span>
</span>
<span style="color: #CBD5E1;">•</span>
<span style="font-size: 0.8rem; color: #64748B;">Smart Classroom Attendance Platform</span>
</div>
<p style="font-size: 0.78rem; color: #94A3B8; margin: 0;">
Streamlining education with fast facial recognition and voice check-in
</p>
</div>""",
        unsafe_allow_html=True,
    )

def footer_dashboard():
    st.markdown(
        """<div style="margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid #E2E8F0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; font-weight: 700; color: #0F172A;">
Vox<span style="color: #2563EB;">Vision</span>
</span>
<span class="badge-blue" style="font-size: 0.65rem; padding: 1px 6px;">Campus Portal</span>
</div>
<p style="font-size: 0.75rem; color: #94A3B8; margin: 0;">
Secure Attendance Session
</p>
</div>""",
        unsafe_allow_html=True,
    )