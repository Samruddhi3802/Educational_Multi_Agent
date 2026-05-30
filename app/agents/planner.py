from app.config import llm_call

def planner_agent(topic):
    prompt = f"""
    Create a study plan for:
    {topic}

    Include:
    - Next topics
    - Practice tips
    """

    return llm_call(prompt)