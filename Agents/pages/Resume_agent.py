import streamlit as st
from ai_agent.parser import (
    extract_text_from_pdf,
    build_resume_structure,
    clean_pdf_text
)

from ai_agent.Jd_parser import (
    structure_jd_with_groq,
    calculate_ats_score
)

from ai_agent.ats_optimizer import (
    optimize_resume_with_ai,
    create_docx
)

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
        st.session_state.structured_jd = structured_jd
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
    
st.divider()

st.subheader("🚀 Improve Resume with AI")

# Only show button if ATS calculation happened
if "resume_data" in st.session_state and "structured_jd" in st.session_state:

    if st.button("Optimize Resume for Better ATS Score"):

        with st.spinner("Optimizing resume..."):

            optimized_resume = optimize_resume_with_ai(
                st.session_state.resume_text,   # use raw text
                missing,                        # missing skills from ATS
                job_description                 # full JD text
            )

        # Show improved resume
        st.header("Optimized Resume")
        st.write(optimized_resume)

        # Download button
        st.download_button(
            label="Download Improved Resume",
            data=optimized_resume,
            file_name="optimized_resume.txt",
            mime="text/plain"
        )

        # Recalculate ATS score
        new_score, _, _ = calculate_ats_score(
            build_resume_structure(optimized_resume),
            st.session_state.structured_jd
        )

        st.success(f"New ATS Score: {new_score}%")
        docx_file = create_docx(optimized_resume)

        st.download_button(
            label="Download Improved Resume (DOCX)",
            data=docx_file,
            file_name="optimized_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
else:
    st.info("Upload resume and paste JD to enable optimization.")