from app.config import llm_call

def quiz_agent(explanation):
    prompt = f"""
    Based on this explanation:
    {explanation}

    Generate 3 quiz questions in JSON format:
    [
      {{"question": "..."}},
      {{"question": "..."}}
    ]
    """

    return llm_call(prompt)
