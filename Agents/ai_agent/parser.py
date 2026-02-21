import PyPDF2
import re

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from uploaded PDF resume.
    """
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    return text


def clean_pdf_text(text):
    # Fix broken hyphen words
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text


def normalize_line(line):
    # Remove extra spaces and convert to lowercase
    return re.sub(r'\s+', ' ', line).strip().lower()

def split_into_sections(text):

    section_keywords = {
        "education": ["education"],
        "skills": ["technical skills", "skills"],
        "internships": ["internships", "experience"],
        "projects": ["projects"],
        "certifications": ["certificates", "certifications"],
        "coding_profiles": ["coding profiles"]
    }

    sections = {key: [] for key in section_keywords}
    current_section = None

    lines = text.split("\n")

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        normalized = normalize_line(clean_line)

        # Detect section header
        for section, keywords in section_keywords.items():
            if any(keyword in normalized for keyword in keywords) and len(normalized) < 30:
                current_section = section
                break
        else:
            if current_section:
                sections[current_section].append(clean_line)

    return sections


def structure_projects(project_lines):

    projects = []
    current = {}

    for line in project_lines:

        # Detect new project
        if "GITHUB" in line:
            if current:
                projects.append(current)
                current = {}

            current["name"] = line
            current["description"] = []

        elif line.startswith("•"):
            current.setdefault("description", []).append(line)

    if current:
        projects.append(current)

    return projects

def structure_internships(internship_lines):

    internships = []
    current = {}

    for line in internship_lines:

        # Detect new internship (company line)
        if "OCTOBER" in line or "MARCH" in line or "JUNE" in line:
            if current:
                internships.append(current)
                current = {}

            current["company_duration"] = line
            current["description"] = []

        # Detect role
        elif "INTERN" in line or "ENGINEERING" in line:
            current["role"] = line

        # Bullet points
        elif line.startswith("•"):
            current.setdefault("description", []).append(line)

    if current:
        internships.append(current)

    return internships



def build_resume_structure(text):
    resume_text = clean_pdf_text(text)
    resume_text = resume_text.upper()  # optional if resume headers are uppercase

    sections = split_into_sections(resume_text)

    resume_data = {
        "education": sections.get("education", ""),
        "skills": sections.get("skills", ""),
        "internships": structure_internships(sections.get("internships", [])),
        "projects":  structure_projects(sections.get("projects", [])),
        "certifications": sections.get("certifications", ""),
        "coding_profiles": sections.get("coding_profiles", "")
    }

    return resume_data

