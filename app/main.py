from fastapi import FastAPI
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from app.rag import get_context, load_data
from app.agents.teacher import teacher_agent
from app.agents.planner import planner_agent
from app.agents.evaluator import evaluate_agent
from app.agents.quiz import quiz_agent
from app.controller.agent_controller import decide_action

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_data()

@app.get("/")
def home():
    return{"message": "AI Study Assistant Running"}

@app.get("/ask")
def ask(query: str):
    action = decide_action(query)
    context = get_context(query)

    if action == "teach":
        explanation = teacher_agent(context, query)
        quiz = quiz_agent(explanation)

        return{
            "type":"teaching",
            "explanation" : explanation,
            "quiz" : quiz,
            "context": context
        }

    elif action == "quiz":
        return {"quiz" : "Ask after explanation (coming soon)"}

    elif action == "plan":
        plan = planner_agent(query)
        return {"type" : "planning", "plan" : plan}

    else:
        return {"message": "Invalid request"}

@app.post("/evaluate")
def evaluate(
    question: str = Body(...),
    answer: str = Body(...)
):
    result = evaluate_agent(question, answer)
    return {"evaluation": result}