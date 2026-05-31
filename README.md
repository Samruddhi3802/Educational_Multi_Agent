# EduAI — Multi-Agent Study Assistant with RAG

An intelligent educational assistant powered by **multi-agent AI** and **Retrieval-Augmented Generation (RAG)**. It combines a FastAPI backend with a beautiful Streamlit frontend to deliver personalized explanations, quizzes, and study plans on any topic — grounded in a knowledge base.

---

## What It Does

Ask any academic question and a team of specialized AI agents handles it:

| Agent | Role |
|---|---|
| Teacher Agent | Explains the topic using RAG-retrieved context |
| Quiz Agent | Generates quiz questions based on the explanation |
| Planner Agent | Creates a personalized study plan for complex topics |
| Evaluator Agent | Evaluates your quiz answers with detailed feedback |
| Controller Agent | Decides which agent to invoke based on query intent |

The system uses **RAG (Retrieval-Augmented Generation)** — it first retrieves relevant chunks from a knowledge base, then passes them to the appropriate agent for a grounded, accurate response.

---

## Project Structure

```
Multi_Agent_With_RAG/
├── streamlit_app.py     # Streamlit frontend (dark-themed UI)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── .env.example         # Template for environment variables
├── data/                # Knowledge base documents (PDFs, text files)
└── app/
    ├── main.py          # FastAPI backend server
    ├── config.py        # LLM client configuration (Groq)
    ├── rag.py           # RAG pipeline — load, chunk & retrieve data
    ├── agents/
    │   ├── teacher.py   # Teacher agent logic
    │   ├── quiz.py      # Quiz generation agent
    │   ├── planner.py   # Study planner agent
    │   └── evaluator.py # Answer evaluation agent
    └── controller/
        └── agent_controller.py  # Routes queries to the right agent
```

---

## Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (dark-themed, modern UI)
- **Backend:** FastAPI + Uvicorn
- **AI / LLM:** [Groq](https://groq.com/) (LLaMA 3.3-70B via Groq SDK)
- **RAG:** Custom retrieval pipeline using local knowledge base
- **Language:** Python 3.9+

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Multi_Agent_With_RAG
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# macOS/Linux
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Open `.env` and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com/)

### 5. Add Your Knowledge Base (Optional)

Place your study materials (`.txt`, `.pdf` files) inside the `data/` folder. The RAG pipeline will automatically load and index them.

### 6. Start the FastAPI Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at **http://localhost:8000**

### 7. Start the Streamlit Frontend

Open a **new terminal** (with the same virtual environment activated):

```bash
streamlit run streamlit_app.py
```

Frontend will open automatically at **http://localhost:8501**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/ask?query=<topic>` | Ask a question (routes to teacher/planner) |
| `POST` | `/evaluate` | Evaluate a quiz answer |

**Example — Ask a Question:**
```bash
GET http://localhost:8000/ask?query=Explain gradient descent
```

**Response (Teaching mode):**
```json
{
  "type": "teaching",
  "explanation": "Gradient descent is an optimization algorithm...",
  "quiz": "[{\"question\": \"What is the role of learning rate?\"}, ...]",
  "context": "Retrieved context from knowledge base..."
}
```

**Example — Evaluate Answer:**
```bash
POST http://localhost:8000/evaluate
Content-Type: application/json

{
  "question": "What is the role of learning rate?",
  "answer": "It controls the step size during parameter updates."
}
```

---

## How RAG Works Here

1. **Load** — Documents from `data/` are loaded at server startup
2. **Chunk** — Text is split into retrievable segments
3. **Retrieve** — For each query, the most relevant chunks are fetched
4. **Generate** — The retrieved context is passed to the appropriate agent along with the query
5. **Respond** — The agent produces a grounded, accurate answer

---

## Requirements

- Python 3.9+
- Groq API Key (free tier available)
- Study materials in `data/` folder (optional — agents can work from internal knowledge too)

---

