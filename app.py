import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import agent_engine  # your existing logic

# -------------------------------------------------
# Page configuration & theming
# -------------------------------------------------
st.set_page_config(
    page_title="Meeting‑Research Agent",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
def _load_css():
    css_path = Path(__file__).parent / "style.css"
    if css_path.is_file():
        st.markdown(css_path.read_text(), unsafe_allow_html=True)

_load_css()

# -------------------------------------------------
# Sidebar – inputs
# -------------------------------------------------
st.sidebar.header("🔧  Settings")
with st.sidebar.expander("Meeting details", expanded=True):
    topic = st.text_input("Meeting topic", "Product roadmap")
    participants = st.text_area(
        "Participants (comma‑separated)",
        "Alice, Bob, Carol",
        height=80,
    )
    duration = st.slider("Duration (minutes)", 15, 180, 60, step=5)

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
run_btn = st.sidebar.button("Generate Brief", type="primary")

# -------------------------------------------------
# Main – output
# -------------------------------------------------
if run_btn:
    with st.spinner("🧠 Generating brief…"):
        brief = agent_engine.run_ai_research_agent(
            topic=topic,
            participants=[p.strip() for p in participants.split(",") if p.strip()],
            duration=duration,
        )
    # Card with the brief
    st.markdown(
        f"""
        <div class=\"card\">
            <h2>📄 Meeting Brief</h2>
            <pre>{brief}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download (txt)",
            data=brief,
            file_name="meeting_brief.txt",
            mime="text/plain",
        )
    with col2:
        st.download_button(
            label="Download (pdf)",
            data=brief,
            file_name="meeting_brief.pdf",
            mime="application/pdf",
        )

    st.divider()
    # Rehearsal evaluator
    st.subheader("🎭  Rehearsal Evaluator")
    response = st.text_area("Your rehearsal response", height=150)
    if st.button("Evaluate", key="eval"):
        score, feedback = agent_engine.evaluate_user_rehearsal_response(response)
        st.success(f"**Score:** {score}/10")
        st.info(feedback)

    # Q&A helper
    st.subheader("❓  Q&A Helper")
    question = st.text_input("Ask a meeting‑related question")
    if st.button("Answer", key="answer"):
        answer = agent_engine.answer_in_meeting_question(question)
        st.markdown(f"<div class='answer'>{answer}</div>", unsafe_allow_html=True)
