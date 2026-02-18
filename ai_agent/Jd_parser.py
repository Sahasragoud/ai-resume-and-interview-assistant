
from groq import Groq
import json
import os
import re

from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# models = client.models.list()
# for m in models.data:
#     print(m.id)

def structure_jd_with_groq(jd_text):
    
    prompt = f"""
        You are a JSON API.
        Return ONLY valid JSON.
        Do NOT explain anything.
        Do NOT add markdown.
        Do NOT add backticks.
        Do NOT add text before or after JSON.

        Format:

        {{
        "role": "",
        "required_skills": [],
        "preferred_skills": [],
        "technologies": [],
        "responsibilities": [],
        "mindset_traits": []
        }}

        Job Description:
        {jd_text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # <-- use active model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content

    # Extract first JSON object
    json_match = re.search(r"\{[\s\S]*\}", content)

    if not json_match:
        raise ValueError("No JSON found in model response")

    json_string = json_match.group(0)

    # Clean common issues
    json_string = json_string.strip()

    # Remove trailing commas before } or ]
    json_string = re.sub(r",\s*}", "}", json_string)
    json_string = re.sub(r",\s*]", "]", json_string)

    try:
        parsed = json.loads(json_string)
    except json.JSONDecodeError as e:
        print("JSON ERROR:", e)
        print("FAILED STRING:", json_string)
        raise e

    return parsed

import re

def normalize_resume_skills(skill_sections):
    """
    Convert grouped resume skill strings into a flat clean skill list.
    """

    clean_skills = []

    for section in skill_sections:
        # Remove category name before colon
        if ":" in section:
            section = section.split(":", 1)[1]

        # Fix broken spacing
        section = re.sub(r"\s+", " ", section)

        # Split by comma
        skills = section.split(",")

        for skill in skills:
            skill = skill.strip().lower()
            if skill:
                clean_skills.append(skill)

    return clean_skills


def calculate_ats_score(resume_data, jd_data):

    # ---- Normalize Skills Properly ----
    resume_raw = resume_data.get("skills", [])
    jd_raw = jd_data.get("required_skills", [])

    resume_skills = set(normalize_resume_skills(resume_raw))
    jd_skills = set([skill.strip().lower() for skill in jd_raw])

    if not jd_skills:
        return 0

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    score = round((len(matched) / len(jd_skills)) * 100)

    return score, matched, missing
