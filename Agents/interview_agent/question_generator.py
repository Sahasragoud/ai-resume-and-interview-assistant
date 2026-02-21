from dotenv import load_dotenv   # ✅ THIS WAS MISSING
from groq import Groq
import os

# Load environment variables
load_dotenv(dotenv_path="ai_agent/.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_questions_with_ai(stage, resume_data, jd_data, num_questions=15):

    prompt = f"""
You are an AI interviewer.

Interview Stage: {stage}

Job Description:
{jd_data}

Candidate Resume:
{resume_data}

Generate {num_questions} interview questions for the "{stage}" stage.

Rules:
- Questions must match the interview stage
- Do NOT repeat questions
- Do NOT number explanations
- Output ONLY a list of questions
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    questions = response.choices[0].message.content.split("\n")
    questions = [q.strip("- ").strip() for q in questions if q.strip()]

    return questions