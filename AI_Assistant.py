import time
import streamlit as st

try:
    from utils.llm import farmer_chat
except ModuleNotFoundError:
    from pages.utils.llm import farmer_chat

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #f4fff4 0%, #eaf8ea 100%); }
    .block-container { padding-top: 0.4rem; padding-bottom: 1.4rem; }
    .hero-banner { border-radius: 24px; overflow: hidden; margin-bottom: 14px; box-shadow: 0 10px 24px rgba(31, 83, 41, 0.14); }
    .hero-banner img { width: 100%; height: 240px; object-fit: cover; display: block; }
    .card { background: white; color: #1f2937; border-radius: 16px; padding: 14px 16px; box-shadow: 0 6px 18px rgba(31, 83, 41, 0.08); margin-bottom: 12px; border: 1px solid #e4f3e4; }
    .chat-shell { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
    .bubble-user { max-width: 82%; margin-left: auto; background: linear-gradient(135deg, #2e7d32, #4caf50); color: white; border-radius: 14px 14px 4px 14px; padding: 10px 12px; }
    .bubble-assistant { max-width: 82%; margin-right: auto; background: white; color: #1f2937; border: 1px solid #dfeedd; border-radius: 14px 14px 14px 4px; padding: 10px 12px; }
    .bubble-label { font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; opacity: 0.85; }
    .typing { display: inline-flex; gap: 4px; align-items: center; padding: 8px 10px; background: #f7fff7; border: 1px solid #dfeedd; border-radius: 999px; }
    .typing span { width: 7px; height: 7px; border-radius: 50%; background: #2e7d32; animation: blink 1s infinite ease-in-out; }
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink { 0%, 80%, 100% { transform: scale(0.75); opacity: 0.5; } 40% { transform: scale(1); opacity: 1; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='hero-banner'><img src='https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1600&q=80' alt='ai agriculture assistant' /></div>", unsafe_allow_html=True)

st.markdown("<div class='card'><h2 style='margin:0 0 6px 0;'>AI Agriculture Assistant</h2><p style='margin:0; color:#4b5563;'>Ask practical irrigation and crop questions and keep the conversation flowing.</p></div>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<div class='card'><h4 style='margin:0 0 6px 0;'>💬 Conversation</h4><p style='margin:0; color:#4b5563;'>Suggested questions are available below.</p></div>", unsafe_allow_html=True)

suggestions = [
    "Should I irrigate today?",
    "Explain my prediction.",
    "How can I save water?",
    "Best irrigation method for rice?",
    "How does rainfall affect irrigation?",
]

cols = st.columns(3)
for idx, suggestion in enumerate(suggestions):
    with cols[idx % 3]:
        if st.button(suggestion, width="stretch", key=f"suggest_{idx}"):
            st.session_state.pending_prompt = suggestion

clear_col, _ = st.columns([1, 5])
with clear_col:
    if st.button("🗑️ Clear Chat", width="stretch"):
        st.session_state.chat_history = []
        st.session_state.pending_prompt = ""


def render_message(role, content):
    bubble_class = "bubble-user" if role == "user" else "bubble-assistant"
    label = "You" if role == "user" else "Assistant"
    safe_content = str(content).replace("\n", "<br>")
    st.markdown(f"<div class='{bubble_class}'><div class='bubble-label'>{label}</div>{safe_content}</div>", unsafe_allow_html=True)

st.markdown("<div class='chat-shell'>", unsafe_allow_html=True)
for message in st.session_state.chat_history:
    render_message(message["role"], message["content"])
st.markdown("</div>", unsafe_allow_html=True)


def handle_prompt(prompt):
    if not prompt:
        return
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    render_message("user", prompt)
    with st.spinner("Thinking..."):
        response = farmer_chat(prompt)
    render_message("assistant", response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = ""
    handle_prompt(prompt)

prompt = st.chat_input("Ask about irrigation, crops, soil, or weather...")
if prompt:
    handle_prompt(prompt)

