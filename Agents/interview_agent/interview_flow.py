import streamlit as st
from interview_agent.question_generator import generate_questions
from interview_agent.evaluator import evaluate_answer

def start_interview(resume_data, jd_data):

    if "questions" not in st.session_state:
        st.session_state.questions = generate_questions(resume_data, jd_data)
        st.session_state.q_index = 0
        st.session_state.answers = []

    q_index = st.session_state.q_index
    questions = st.session_state.questions

    if q_index < len(questions):
        st.subheader(f"Question {q_index + 1}")
        st.write(questions[q_index])

        answer = st.text_area("Your Answer", key=f"answer_{q_index}")

        if st.button("Submit Answer"):
            score = evaluate_answer(questions[q_index], answer)
            st.session_state.answers.append({
                "question": questions[q_index],
                "answer": answer,
                "score": score
            })
            st.session_state.q_index += 1
            st.rerun()

    else:
        st.success("Interview Completed 🎉")
        st.json(st.session_state.answers)
