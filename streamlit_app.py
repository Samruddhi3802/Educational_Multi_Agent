import streamlit as st
import requests
import json
import re

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EduAI | Professional Dark",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DARK THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Core Background & Font */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f1f5f9;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }

    /* Custom Dark Cards */
    .css-card {
        background: #1e293b;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        color: #e2e8f0;
    }

    /* Professional Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Inputs */
    .stTextInput input {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }

    /* Buttons - Gradient Primary */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.7rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4);
    }

    /* Secondary/Clear Button */
    [data-testid="stSidebar"] .stButton>button {
        background: transparent;
        border: 1px solid #475569;
        color: #94a3b8;
    }

    /* Metrics/Info Boxes */
    .stAlert {
        background-color: #1e293b;
        border: 1px solid #1e40af;
        color: #bfdbfe;
    }

    /* Radio buttons & text visibility */
    .stMarkdown, p, li {
        color: #cbd5e1 !important;
    }

    /* Selection box improvement */
    div[data-baseweb="select"] > div {
        background-color: #0f172a;
        border-color: #334155;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC (Restored) ---
BASE_URL = "http://127.0.0.1:8000"

if 'explanation' not in st.session_state: st.session_state.explanation = ""
if 'quiz' not in st.session_state: st.session_state.quiz = []
if 'selected_q' not in st.session_state: st.session_state.selected_q = ""
if 'evaluation' not in st.session_state: st.session_state.evaluation = ""

def clean_json_response(text):
    try: return json.loads(text)
    except:
        match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
        if match:
            try: return json.loads(match.group(1))
            except: pass
    return None

def fetch_content(topic):
    try:
        with st.spinner("Agent is exploring the knowledge base..."):
            response = requests.get(f"{BASE_URL}/ask", params={"query": topic})
            if response.status_code == 200:
                data = response.json()
                res_type = data.get("type", "teaching")
                
                # Reset states
                st.session_state.explanation = ""
                st.session_state.plan = ""
                st.session_state.quiz = []
                st.session_state.selected_q = ""
                st.session_state.evaluation = ""
                st.session_state.context = ""

                if res_type == "planning":
                    st.session_state.plan = data.get("plan", "")
                else:
                    st.session_state.explanation = data.get("explanation", "")
                    st.session_state.context = data.get("context", "")
                    quiz_raw = data.get("quiz", "")
                    parsed = clean_json_response(quiz_raw)
                    if isinstance(parsed, list):
                        st.session_state.quiz = [q.get("question", q) if isinstance(q, dict) else q for q in parsed]
                    else:
                        st.session_state.quiz = [q.strip() for q in quiz_raw.split("\n") if q.strip() and "?" in q]
            else:
                st.error("Connection error.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- MAIN UI ---
with st.sidebar:
    st.markdown("Lab Settings")
    st.selectbox("Model Accuracy", ["Balanced", "High Precision", "Creative"])
    st.divider()
    if st.button("Reset Environment"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

st.markdown('<h1 class="main-header">EduAI Terminal</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #94a3b8;">Neural-accelerated study assistant.</p>', unsafe_allow_html=True)

# Search Bar Area
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input("topic", placeholder="What do you want to learn today?", label_visibility="collapsed")
with col2:
    if st.button("Initialize"):
        if topic: fetch_content(topic)

st.divider()

if st.session_state.explanation:
    col_left, col_right = st.columns([1.6, 1], gap="large")
    
    with col_left:
        st.markdown("Synthesized Insight")
        st.markdown(f'<div class="css-card">{st.session_state.explanation}</div>', unsafe_allow_html=True)
        
        if st.session_state.context:
            with st.expander("Technical Context"):
                st.info(st.session_state.context)
        
    with col_right:
        st.markdown("Neural Quiz")
        if st.session_state.quiz:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            selected = st.radio("Select a probe question:", st.session_state.quiz)
            if selected != st.session_state.selected_q:
                st.session_state.selected_q = selected
                st.session_state.evaluation = ""
            st.markdown('</div>', unsafe_allow_html=True)

def submit_answer(question, answer):
    try:
        with st.spinner("Analyzing response..."):
            response = requests.post(f"{BASE_URL}/evaluate", json={"question": question, "answer": answer})
            if response.status_code == 200:
                st.session_state.evaluation = response.json().get("evaluation", "")
            else:
                st.error("Evaluation failed.")
    except Exception:
        st.error("Connection lost.")

if st.session_state.selected_q:
    st.markdown("---")
    st.markdown(f"Question: *{st.session_state.selected_q}*")
    user_answer = st.text_area("answer", placeholder="Type your response...", height=120, label_visibility="collapsed")
    
    if st.button("Evaluate Response", key="eval_btn"):
        if user_answer.strip():
            submit_answer(st.session_state.selected_q, user_answer)
        else:
            st.warning("Please provide a response.")

    if st.session_state.evaluation:
        st.success(f"Agent Feedback: {st.session_state.evaluation}")

else:
    st.markdown("""
        <div style="text-align: center; margin-top: 5rem; opacity: 0.5;">
            <h2 style="color: #64748b;">Waiting for Input Signal...</h2>
            <p>Enter a topic above to begin data synthesis.</p>
        </div>
    """, unsafe_allow_html=True)