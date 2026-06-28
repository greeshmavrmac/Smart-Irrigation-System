import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #f4fff4 0%, #eaf8ea 100%); }
    .block-container { padding-top: 0.4rem; padding-bottom: 1.4rem; }
    .hero-banner { border-radius: 24px; overflow: hidden; margin-bottom: 14px; box-shadow: 0 10px 24px rgba(31, 83, 41, 0.14); }
    .hero-banner img { width: 100%; height: 240px; object-fit: cover; display: block; }
    .card { background: white; color: #1f2937; border-radius: 16px; padding: 14px 16px; box-shadow: 0 6px 18px rgba(31, 83, 41, 0.08); margin-bottom: 12px; border: 1px solid #e4f3e4; }
    .pill { display: inline-block; padding: 6px 10px; border-radius: 999px; background: #eaf8ea; color: #20633b; font-size: 0.82rem; font-weight: 700; margin-right: 6px; margin-top: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='hero-banner'><img src='https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1600&q=80' alt='smart irrigation landscape' /></div>", unsafe_allow_html=True)

st.markdown("<div class='card'><h2 style='margin:0 0 6px 0;'>About the Project</h2><p style='margin:0; color:#4b5563;'>This dashboard combines predictive modeling, explainable AI, and a lightweight assistant for smarter irrigation decisions.</p></div>", unsafe_allow_html=True)

cols = st.columns(2)
with cols[0]:
    st.markdown("<div class='card'><h4 style='margin:0 0 6px 0;'>🌱 Project Overview</h4><p style='margin:0; color:#4b5563;'>The app predicts irrigation needs using key farm and environmental signals such as soil moisture, humidity, temperature, and crop context.</p></div>", unsafe_allow_html=True)
with cols[1]:
    st.markdown("<div class='card'><h4 style='margin:0 0 6px 0;'>✨ Features</h4><ul style='margin:0; padding-left:18px; color:#4b5563;'><li>Prediction workflow</li><li>Model comparison dashboard</li><li>AI assistant guidance</li></ul></div>", unsafe_allow_html=True)

st.markdown("<div class='card'><h4 style='margin:0 0 6px 0;'>🧰 Technologies</h4><div><span class='pill'>Python</span><span class='pill'>Streamlit</span><span class='pill'>Scikit-Learn</span><span class='pill'>XGBoost</span><span class='pill'>Groq</span><span class='pill'>Plotly</span></div></div>", unsafe_allow_html=True)

st.markdown("<div class='card'><h4 style='margin:0 0 6px 0;'>📊 ML Models</h4><p style='margin:0; color:#4b5563;'>Random Forest, XGBoost, SVM, KNN, and MLP are compared through a compact evaluation dashboard.</p></div>", unsafe_allow_html=True)

st.markdown("<div class='card'><h4 style='margin:0 0 6px 0;'>🧾 Dataset</h4><p style='margin:0; color:#4b5563;'>The experience is built around agricultural inputs that influence irrigation decisions, including weather, soil, and crop stage.</p></div>", unsafe_allow_html=True)

st.markdown("<div class='card'><h4 style='margin:0 0 6px 0;'>🚀 Future Scope</h4><p style='margin:0; color:#4b5563;'>Planned enhancements include live weather integration, sensor data support, and deeper analytical dashboards.</p></div>", unsafe_allow_html=True)

