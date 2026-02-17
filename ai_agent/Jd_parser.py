
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

def structure_jd_with_openai(jd_text):
    
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