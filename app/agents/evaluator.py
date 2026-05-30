from app.config import llm_call

def evaluate_agent(question, answer):
    prompt = f"""
    Question: {question}
    Student Answer: {answer}

    Evaluate and give:
    - Score out of 10
    - Feedback
    """
    return llm_call(prompt)
