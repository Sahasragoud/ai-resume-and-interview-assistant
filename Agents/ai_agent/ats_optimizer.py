from dotenv import load_dotenv
from groq import Groq
from docx import Document
import io
import os

# Load environment variables
load_dotenv(dotenv_path="ai_agent/.env")

# Debug (remove later)
print("DEBUG GROQ KEY:", os.getenv("GROQ_API_KEY"))

# Get API key safely
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=groq_key)

def create_docx(resume_text):
    document = Document()
    
    for line in resume_text.split("\n"):
        document.add_paragraph(line)
    
    buffer = io.BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer

def optimize_resume_with_ai(resume_text, missing_skills, jd_text):

    prompt = f"""
        You are a professional resume optimizer.

        Job Description:
        {jd_text}

        Current Resume:
        {resume_text}

        Missing Skills:
        {missing_skills}

        Rewrite the resume by:
        - Naturally incorporating the missing skills
        - Improving bullet points with action verbs
        - Making it ATS-friendly
        - Keeping it realistic and professional

        Return only the improved resume text.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert ATS resume optimizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content