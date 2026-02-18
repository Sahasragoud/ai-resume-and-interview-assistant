import streamlit as st
from parser import (
    extract_text_from_pdf,
    build_resume_structure,
    clean_pdf_text
)


from Jd_parser import structure_jd_with_groq,calculate_ats_score

st.set_page_config(page_title="AI Resume & Interview Assistant")

st.title("AI Resume & Interview Assistant")

# ------------------ RESUME UPLOAD ------------------

st.header("📄 Resume Upload")

uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_resume is not None:
    resume_text = extract_text_from_pdf(uploaded_resume)
    
    resume_text = clean_pdf_text(resume_text)

    # Store globally for later use
    st.session_state.resume_text = resume_text
    st.session_state.resume_data = build_resume_structure(resume_text)

    st.subheader("Extracted Resume Text:")
    st.write(resume_text)

    st.subheader("Structured Resume Data")
    st.json(st.session_state.resume_data)


# ------------------ JOB DESCRIPTION ------------------

st.header("📄 Job Description")

job_description = st.text_area("Paste the Job Description here")

if job_description and "resume_text" in st.session_state:

    # ----------------- STRUCTURE JD -----------------
    with st.spinner("Structuring JD using AI..."):
        structured_jd = structure_jd_with_groq(job_description)

    try:

        st.subheader("Structured JD")
        st.json(structured_jd)

    except Exception as e:
        st.error("Failed to parse JD structure.")
        st.write(e)

    # ----------------- ATS MATCHING -----------------
    
    score, matched, missing = calculate_ats_score(
    st.session_state.resume_data,
    structured_jd
    )


    st.subheader("ATS Score:")
    st.write(f"{score}%")

    st.subheader("Matched skills:")
    st.write(matched)

    st.subheader("Missing skills:")
    st.write(missing)

elif job_description:
    st.warning("⚠ Please upload resume first.")

