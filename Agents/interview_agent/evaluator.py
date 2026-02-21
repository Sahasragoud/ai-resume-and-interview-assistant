def evaluate_answer(question, answer):
    if not answer or len(answer.strip()) < 20:
        return 2
    elif len(answer) < 60:
        return 5
    else:
        return 8
