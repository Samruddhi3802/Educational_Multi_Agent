def decide_action(user_input):
    user_input = user_input.lower()

    if "quiz" in user_input:
        return "quiz"
    elif "evaluate" in user_input:
        return "evaluate"
    elif "plan" in user_input:
        return "plan"
    else:
        return "teach"