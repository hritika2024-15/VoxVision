import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    # Calculate attendance percentage if total and attended are present
    pct = None
    if stats:
        total_val = None
        att_val = None
        for item in stats:
            # item can be (icon, label, val) or (label, val)
            label = item[1] if len(item) == 3 else item[0]
            val = item[2] if len(item) == 3 else item[1]
            if "total" in label.lower() or "classes" in label.lower():
                try:
                    total_val = int(val)
                except Exception:
                    pass
            if "attended" in label.lower():
                try:
                    att_val = int(val)
                except Exception:
                    pass
        if total_val and total_val > 0 and att_val is not None:
            pct = round((att_val / total_val) * 100)

    meter_html = ""
    if pct is not None:
        meter_color = "#10B981" if pct >= 75 else ("#F59E0B" if pct >= 50 else "#EF4444")
        meter_html = f"""<div style="margin: 12px 0 10px 0;">
<div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
<span style="color: #64748B; font-weight: 600;">Attendance Rate</span>
<span style="color: {meter_color}; font-weight: 700;">{pct}%</span>
</div>
<div style="width: 100%; height: 6px; background: #E2E8F0; border-radius: 9999px; overflow: hidden;">
<div style="width: {pct}%; height: 100%; background: {meter_color}; border-radius: 9999px;"></div>
</div>
</div>"""

    stats_html = ""
    if stats:
        stats_html += '<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;">'
        for item in stats:
            label = item[1] if len(item) == 3 else item[0]
            value = item[2] if len(item) == 3 else item[1]
            stats_html += f"""<div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 4px 10px; border-radius: 8px; font-size: 0.82rem; color: #334155; display: inline-flex; align-items: center; gap: 5px;">
<span style="color: #64748B; font-size: 0.8rem;">{label}:</span> <strong style="color: #0F172A;">{value}</strong>
</div>"""
        stats_html += "</div>"

    html = f"""<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #2563EB; padding: 20px; border-radius: 14px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
<h3 style="margin: 0; color: #0F172A; font-size: 1.25rem; font-weight: 700;">{name}</h3>
<span class="badge-gray" style="font-size: 0.72rem;">Sec {section}</span>
</div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
<span style="color: #64748B; font-size: 0.82rem; font-weight: 500;">Code:</span>
<span style="background: #EFF6FF; color: #1D4ED8; border: 1px solid #DBEAFE; font-size: 0.82rem; font-weight: 600; padding: 2px 8px; border-radius: 6px;">
{code}
</span>
</div>
{meter_html}
{stats_html}
</div>"""

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()