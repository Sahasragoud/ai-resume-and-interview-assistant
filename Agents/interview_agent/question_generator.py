def generate_questions(resume_data, jd_data):
    questions = []

    # From JD skills
    for skill in jd_data.get("required_skills", []):
        questions.append(f"Explain your experience with {skill}.")

    # From resume projects
    for project in resume_data.get("projects", []):
        name = project.get("name", "a project")
        questions.append(f"Explain the architecture of your project {name}.")

    # From internships
    for intern in resume_data.get("internships", []):
        role = intern.get("role", "your internship")
        questions.append(f"What were your responsibilities as a {role}?")

    return questions