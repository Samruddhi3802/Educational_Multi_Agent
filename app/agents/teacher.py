from app.config import llm_call

def teacher_agent(context, user_input):
    prompt = f"""
    You are a friendly teacher. 
    
    IMPORTANT: Use the following Study Material as your primary source of information. 
    If the material contains relevant info, start your explanation by mentioning "Based on the study notes...".
    
    Study Material:
    {context}
    
    User Question:
    {user_input}
    
    Explain clearly and simply, incorporating the study material if it matches the topic.
    """
    return llm_call(prompt)
