import streamlit as st
from interview_agent.question_generator import generate_questions_with_ai
from interview_agent.evaluator import evaluate_answer

STAGES = [
    "Warm-up",
    "Skill-based",
    "Behavioral",
    "Situational",
    "Wrap-up"
]

def start_interview(resume_data, jd_data):

    if "stage_index" not in st.session_state:
        st.session_state.stage_index = 0
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.session_state.questions = []

        # Generate first stage questions
        st.session_state.questions = generate_questions_with_ai(
            STAGES[0], resume_data, jd_data, num_questions=15
        )

    stage = STAGES[st.session_state.stage_index]
    questions = st.session_state.questions

    st.subheader(f"🟢 Stage: {stage}")

    if st.session_state.q_index < len(questions):
        question = questions[st.session_state.q_index]
        st.write(question)

        answer = st.text_area("Your Answer", key=f"{stage}_{st.session_state.q_index}")

        if st.button("Submit Answer"):
            score = evaluate_answer(question, answer)

            st.session_state.answers.append({
                "stage": stage,
                "question": question,
                "answer": answer,
                "score": score
            })

            st.session_state.q_index += 1
            st.rerun()

    else:
        # Move to next stage
        st.session_state.stage_index += 1
        st.session_state.q_index = 0

        if st.session_state.stage_index < len(STAGES):
            next_stage = STAGES[st.session_state.stage_index]

            with st.spinner(f"Generating {next_stage} questions..."):
                st.session_state.questions = generate_questions_with_ai(
                    next_stage, resume_data, jd_data, num_questions=15
                )

            st.rerun()
        else:
            st.success("🎉 Interview Completed!")
            st.json(st.session_state.answers)