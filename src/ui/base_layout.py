import streamlit as st

def style_futuristic_theme():
    st.markdown(
        """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

/* Reset and Base Canvas - Clean Light Theme */
#MainMenu, footer, header {
    visibility: hidden !important;
    height: 0 !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

.stApp {
    background-color: #F8FAFC !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.04) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.03) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(241, 245, 249, 0.8) 0px, transparent 50%) !important;
    background-attachment: fixed !important;
    color: #1E293B !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1160px !important;
    margin: 0 auto !important;
}

/* Headings & Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #0F172A !important;
    letter-spacing: -0.025em !important;
    font-weight: 700 !important;
}

h1 {
    font-size: 2.2rem !important;
    color: #0F172A !important;
    line-height: 1.2 !important;
}

h2 {
    font-size: 1.65rem !important;
    color: #0F172A !important;
    margin-top: 0.4rem !important;
    margin-bottom: 0.6rem !important;
}

h3 {
    font-size: 1.25rem !important;
    color: #1E293B !important;
}

p, label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #475569;
    font-size: 0.95rem;
}

strong, b {
    color: #0F172A !important;
}

/* Icons */
[data-testid="stIconMaterial"], 
[class*="material-symbols"],
.material-symbols-rounded,
.material-symbols-outlined {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
    font-style: normal !important;
    font-weight: normal !important;
    display: inline-block !important;
    line-height: 1 !important;
}

/* Streamlit Containers & Dividers */
hr {
    border-color: #E2E8F0 !important;
    margin: 1.6rem 0 !important;
}

[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.02) !important;
    padding: 1.5rem !important;
}

[data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
}

[data-testid="column"] > [data-testid="stVerticalBlock"] {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}

[data-testid="column"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}

/* Professional Academic Button System */
button,
button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: #2563EB !important;
    color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.01em !important;
    border-radius: 10px !important;
    border: 1px solid #1D4ED8 !important;
    padding: 0.6rem 1.3rem !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25) !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"] *,
button[data-testid="stBaseButton-primary"] * {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background: #1D4ED8 !important;
    border-color: #1E40AF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
}

button[kind="secondary"],
button[data-testid="stBaseButton-secondary"] {
    background: #FFFFFF !important;
    color: #1E293B !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    border-radius: 10px !important;
    border: 1px solid #CBD5E1 !important;
    padding: 0.6rem 1.3rem !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"] *,
button[data-testid="stBaseButton-secondary"] * {
    color: #1E293B !important;
    font-weight: 600 !important;
}

button[kind="secondary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    background: #F8FAFC !important;
    border-color: #94A3B8 !important;
    color: #0F172A !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
}

button[kind="secondary"]:hover *,
button[data-testid="stBaseButton-secondary"]:hover * {
    color: #0F172A !important;
}

button[kind="tertiary"],
button[data-testid="stBaseButton-tertiary"] {
    background: #F1F5F9 !important;
    color: #475569 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    border-radius: 10px !important;
    border: 1px solid #E2E8F0 !important;
    padding: 0.55rem 1.1rem !important;
    transition: all 0.15s ease !important;
}

button[kind="tertiary"]:hover,
button[data-testid="stBaseButton-tertiary"]:hover {
    background: #E2E8F0 !important;
    color: #0F172A !important;
    border-color: #CBD5E1 !important;
}

/* Form Inputs & Fields */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    color: #0F172A !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 0.85rem !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
}

[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stCameraInput"] label,
[data-testid="stFileUploader"] label {
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}

/* Streamlit Alerts & Messages */
[data-testid="stAlert"] {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

[data-testid="stAlert"][data-test-color="info"] {
    border-left: 4px solid #2563EB !important;
    background: #EFF6FF !important;
}

[data-testid="stAlert"][data-test-color="warning"] {
    border-left: 4px solid #F59E0B !important;
    background: #FFFBEB !important;
}

[data-testid="stAlert"][data-test-color="success"] {
    border-left: 4px solid #10B981 !important;
    background: #ECFDF5 !important;
}

[data-testid="stAlert"][data-test-color="error"] {
    border-left: 4px solid #EF4444 !important;
    background: #FEF2F2 !important;
}

/* Streamlit Dialog Styling */
[data-testid="stDialog"] [role="dialog"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 18px !important;
    box-shadow: 0 20px 40px -8px rgba(15, 23, 42, 0.18) !important;
}

[data-testid="stDialog"] h2 {
    color: #0F172A !important;
}

/* Camera Input Clean Frame */
[data-testid="stCameraInput"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
}

/* Dataframe Table Clean Skin */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #E2E8F0 !important;
    background: #FFFFFF !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

/* Educational Badges & Chips */
.badge-blue {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 9999px;
    letter-spacing: 0.02em;
}

.badge-green {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    color: #047857;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 9999px;
}

.badge-gray {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    color: #475569;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 9999px;
}

.pulse-dot-green {
    width: 7px;
    height: 7px;
    background: #10B981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 6px #10B981;
}
</style>""",
        unsafe_allow_html=True,
    )

def style_background_home():
    style_futuristic_theme()

def style_background_dashboard():
    style_futuristic_theme()

def style_base_layout():
    style_futuristic_theme()