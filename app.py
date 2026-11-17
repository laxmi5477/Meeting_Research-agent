import streamlit as st
import os
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
import agent_engine  # existing engine functions

# Load environment variables (API keys, etc.)
load_dotenv()

# -------------------------------------------------
# Page configuration & theming
# -------------------------------------------------
st.set_page_config(
    page_title="Meeting‑Research Agent",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS – wrap it in a <style> tag so Streamlit treats it as CSS
def _load_css():
    css_path = Path(__file__).parent / "style.css"
    if css_path.is_file():
        css = css_path.read_text()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

_load_css()

# -------------------------------------------------
# Header (title + tagline)
# -------------------------------------------------
st.title("Meeting Research Agent")
st.caption("Turn any topic into an actionable, evidence‑backed meeting brief.")

# -------------------------------------------------
# Sidebar – configuration & inputs
# -------------------------------------------------
st.sidebar.header("🔧  Settings")

# Research mode selector (Mock or Live)
mode = st.sidebar.selectbox(
    "Research mode",
    options=["Mock (no API)", "Live (Gemini + Web)"],
    index=0,
    help="Mock mode returns demo data without calling Gemini. Live mode requires a valid GEMINI_API_KEY.",
)

# Show API‑key status (do not reveal the value)
if mode == "Live (Gemini + Web)":
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        st.sidebar.success("✅ Gemini API key detected")
    else:
        st.sidebar.warning("⚠️ GEMINI_API_KEY not set – live mode will fall back to mock data")

with st.sidebar.expander("Meeting details", expanded=True):
    topic = st.text_input("Meeting topic", "Product roadmap")
    participants = st.text_area(
        "Participants (comma‑separated)",
        "Alice, Bob, Carol",
        height=80,
    )
    meeting_purpose = st.text_input("Meeting purpose / objective", "Discuss upcoming product features")
    meeting_date = st.date_input("Meeting date", datetime.date.today() + datetime.timedelta(days=7))
    depth = st.slider("Research depth (minutes)", min_value=5, max_value=180, value=30, step=5)

st.sidebar.divider()
st.sidebar.checkbox("Dark mode", key="dark_mode")
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        :root {--background:#1e1e1e; --text:#f0f0f0; --card:#2a2a2a;}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.header("🚀  Run")
run_btn = st.sidebar.button("Generate Research Brief", type="primary")

# -------------------------------------------------
# Main – output handling (persist across reruns)
# -------------------------------------------------
if "brief" not in st.session_state:
    st.session_state.brief = None

if run_btn:
    with st.spinner("🧠 Generating brief…"):
        brief = agent_engine.run_research(
            topic=topic,
            participants=[p.strip() for p in participants.split(",") if p.strip()],
            meeting_date=meeting_date,
            meeting_purpose=meeting_purpose,
            mode=mode,
        )
        st.session_state.brief = brief

if st.session_state.brief:
    brief = st.session_state.brief
    st.subheader("📄 Meeting Brief")
    # If the brief is a dict (structured), display each key in an expander
    if isinstance(brief, dict):
        for key, value in brief.items():
            display_key = key.replace('_', ' ').title()
            if isinstance(value, (list, dict)):
                with st.expander(display_key):
                    st.json(value)
            else:
                st.write(f"**{display_key}:** {value}")
    else:
        # Raw text – show inside a styled card
        st.markdown(f"<div class=\"card\"><pre>{brief}</pre></div>", unsafe_allow_html=True)

    # Download buttons (txt & json if applicable)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download (txt)",
            data=str(brief),
            file_name="meeting_brief.txt",
            mime="text/plain",
        )
    with col2:
        data_json = json.dumps(brief, indent=2) if isinstance(brief, dict) else str(brief)
        st.download_button(
            label="Download (json)",
            data=data_json,
            file_name="meeting_brief.json",
            mime="application/json",
        )

    st.divider()
    # ---------------- Rehearsal evaluator ----------------
    st.subheader("🎭  Rehearsal Evaluator")
    response = st.text_area("Your rehearsal response", height=150)
    if st.button("Evaluate", key="eval"):
        # Provide a simple dummy objection scenario for the evaluator
        scenario = "Price objection"
        eval_result = agent_engine.evaluate_rehearsal(brief, scenario, response)
        if isinstance(eval_result, dict):
            st.success(f"**Score:** {eval_result.get('score', '?')}/10")
            st.info(eval_result.get('feedback', ''))
        else:
            st.info(eval_result)

    # ---------------- Q&A helper ----------------
    st.subheader("❓  Q&A Helper")
    question = st.text_input("Ask a meeting‑related question")
    if st.button("Answer", key="answer"):
        answer = agent_engine.answer_question(brief, question)
        st.markdown(f"<div class='answer'>{answer}</div>", unsafe_allow_html=True)
