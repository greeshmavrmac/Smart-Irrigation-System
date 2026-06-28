import streamlit as st


@st.cache_data(show_spinner=False)
def get_home_assets():
    return {
        "sidebar_image": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=800&q=70",
        "hero_image": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1200&q=70",
    }


st.set_page_config(
    page_title="Smart Irrigation Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #f4fff4 0%, #eaf8ea 100%); }
    .block-container { padding-top: 0.4rem; padding-bottom: 1.4rem; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #163d23 0%, #2e6f3d 100%); }
    [data-testid="stSidebarContent"] { padding: 0.85rem; }
    .sidebar-card {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.16);
        border-radius: 18px;
        padding: 12px;
        color: white;
        margin-bottom: 10px;
    }
    .sidebar-card img { width: 100%; height: 108px; object-fit: cover; border-radius: 12px; margin-bottom: 8px; }
    .sidebar-footer { margin-top: 8px; color: #eaf8ea; font-size: 0.9rem; }
    .hero-banner { border-radius: 24px; overflow: hidden; margin-bottom: 14px; box-shadow: 0 10px 24px rgba(31, 83, 41, 0.14); }
    .hero-banner img { width: 100%; height: 280px; object-fit: cover; display: block; }
    .card { background: white; color: #1f2937; border-radius: 18px; padding: 14px 16px; box-shadow: 0 6px 18px rgba(31, 83, 41, 0.08); margin-bottom: 12px; border: 1px solid #e4f3e4; }
    .feature-card { background: linear-gradient(135deg, #ffffff, #f4fff4); border: 1px solid #dcefdc; border-radius: 16px; padding: 14px; min-height: 120px; color: #1f2937; }
    .pill { display: inline-block; padding: 6px 10px; border-radius: 999px; background: #eaf8ea; color: #20633b; font-size: 0.82rem; font-weight: 700; margin-right: 6px; margin-top: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

assets = get_home_assets()
st.sidebar.markdown(
    f"""
    <div class="sidebar-card">
        <img src="{assets['sidebar_image']}" alt="smart irrigation" />
        <h3 style="margin:0 0 4px 0;">🌱 Smart Irrigation</h3>
        <p style="margin:0; font-size:0.92rem;">Clean AI dashboard for modern farming.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("<div class='sidebar-footer'>Compact and professional for laptop dashboards.</div>", unsafe_allow_html=True)

st.markdown(f"<div class='hero-banner'><img src='{assets['hero_image']}' alt='smart irrigation landscape' /></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="card">
        <h2 style="margin:0 0 6px 0; font-size:1.5rem;">Smart Irrigation Intelligence</h2>
        <p style="margin:0; color:#4b5563;">A compact AI dashboard for irrigation forecasting, model comparison, and farm guidance.</p>
        <div><span class="pill">🌾 Forecasting</span><span class="pill">🤖 AI Assistant</span><span class="pill">📊 Comparison</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(4)
features = [
    ("Prediction", "Estimate irrigation need with live field inputs."),
    ("AI Assistant", "Get clear agricultural advice from Groq."),
    ("Model Comparison", "Compare major irrigation models at a glance."),
    ("About", "Understand the project workflow and stack."),
]
for col, (title, text) in zip(cols, features):
    with col:
        st.markdown(f"<div class='feature-card'><h4 style='margin:0 0 6px 0;'>{title}</h4><p style='margin:0; color:#4b5563;'>{text}</p></div>", unsafe_allow_html=True)
