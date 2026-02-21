import streamlit as st
from interview_agent.interview_flow import start_interview

st.set_page_config(page_title="AI Interview Agent")
st.title("🎤 AI Interview Agent")

# ---- READ REAL DATA FROM SESSION ----
resume_data = st.session_state.get("resume_data")
jd_data = st.session_state.get("structured_jd")

if not resume_data or not jd_data:
    st.warning("⚠ Please upload resume and JD in Resume Agent first.")
    st.stop()

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if st.button("Start Interview"):
    st.session_state.interview_started = True

if st.session_state.interview_started:
    start_interview(resume_data, jd_data)