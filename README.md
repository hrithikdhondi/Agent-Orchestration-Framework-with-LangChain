# 🧠 Agent-Orchestration Framework with LangChain

---

> **A Modular Multi-Agent Reasoning & Workflow System**  
> LangChain • Gemini LLM • Tool-Based Reasoning • Memory-Oriented Architecture • Intelligent Routing

This project implements an **advanced multi-agent orchestration framework** using **LangChain** and **Google Gemini**.  
Unlike a traditional chatbot, the system dynamically **routes user input**, orchestrates **specialized agents**, and executes **multi-step workflows** such as research, summarization, and professional email composition.

The focus of this project is on **how intelligence is structured, routed, and orchestrated**, not just how responses are generated.

---

## 📌 Project Highlights
---

- 🧩 **True Multi-Agent Architecture** with strict role separation  
- 🧠 **Planner → Researcher → Summarizer → Email Agent** workflows  
- 🛠 **Explicit Tool-Based Reasoning** (no hallucinated tool use)  
- 🔁 **Central Orchestrator** coordinating agents and memory  
- 🧭 **Intelligent Input Router** (CHAT / CLARIFY / COMPLEX_TASK)  
- 🧠 **Per-Agent Memory + Shared FAISS Memory**  
- 🌐 **Backend–Frontend Ready Architecture**  
- 📈 **Milestone-Based System Evolution**

---

## 🧠 High-Level System Overview
---

```text
User Input
   │
   ▼
Input Router
   │
   ├── CHAT ─────────► Chat Agent (Conversational LLM)
   │
   ├── CLARIFY ──────► Follow-up Question
   │
   └── COMPLEX_TASK
           │
           ▼
     Orchestrator
           │
           ▼
     Planner Agent
           │   (decides execution plan)
           ▼
     Research Agent
           │   (tools + shared memory)
           ▼
     Summarizer Agent
           │
           ├──► Email Compose Agent (if email intent)
           │
           ▼
       Final Answer
```
## 🧠 Memory Layers
---

- **Session Memory**
  - Maintains short-term chat context
  - Used by the Chat Agent and Input Router
  - Resettable via the `clear` command

- **Agent Memory**
  - Isolated memory per agent
  - Prevents cross-agent contamination
  - Stores intermediate reasoning and outputs

- **Shared Memory (FAISS Vector Store)**
  - Long-term, persistent knowledge storage
  - Powered by Gemini embeddings
  - Enables memory-aware reasoning across sessions
  - Stores reusable facts and summarized insights

---

## 🤖 Agents Implemented
---

| Agent Name | Responsibility |
|-----------|---------------|
| **Planner Agent** | Analyzes intent and generates a strict execution plan |
| **Research Agent** | Executes the plan using tools and shared memory |
| **Summarizer Agent** | Converts raw research into user-facing output |
| **Email Compose Agent** | Formats finalized content into professional emails |
| **Chat Agent** | Handles casual conversational interactions |
| **Orchestrator** | Controls agent execution flow and memory lifecycle |

---

## 🧭 Intelligent Routing
---

The system does **not treat every user input as a task**.

Each input is classified into one of the following modes:

- **CHAT**
  - Casual conversation
  - Greetings, acknowledgements, opinions
  - No agent orchestration

- **CLARIFY**
  - Task intent exists
  - Required information is missing
  - System asks exactly one follow-up question

- **COMPLEX_TASK**
  - Multi-step reasoning required
  - Tool usage or memory access
  - Full multi-agent orchestration

This routing design mirrors **production-grade LLM systems**.

---

## 🛠 Tools Implemented
---

| Tool | Purpose |
|-----|--------|
| `greet(name)` | Returns a greeting |
| `get_weather(city)` | Fetches live weather data |
| `calculate(expression)` | Safe mathematical evaluation |
| `gen_password(length)` | Secure password generation |
| `get_time(tz)` | Current time (UTC / IST / LOCAL) |
| `read_file(path)` | Read text-based files |
| `write_file(path, content)` | Write content to files |
| `append_file(path, content)` | Append content to files |
| `analyze_text(text)` | Extract key points |
| `extract_keywords(text)` | Keyword extraction |
| `decompose_task(goal)` | Task decomposition |
| `search_shared_memory(query)` | Shared memory lookup |
| `prepare_memory_entry(content)` | Prepare memory entries |
| `structure_as_json()` | Structured JSON output |
| `generate_markdown_table()` | Markdown table generation |

All tools are **explicitly invoked** and **never hallucinated**.

---

## 📂 Project Structure
---

```text
src/
├── Backend/
│   └── app/
│       ├── main.py              # API entry point
│       ├── routes.py            # Backend routes
│       └── schemas.py           # Request/response schemas
│
├── Frontend/
│   └── app.py                   # Frontend interface
│
├── chat/
│   └── chat_agent.py            # Conversational chat agent
│
├── multi_agents/
│   ├── planner_agent.py         # Planner Agent
│   ├── research_agent.py        # Research Agent
│   ├── summarizer_agent.py      # Summarizer Agent
│   └── email_compose_agent.py   # Email formatting agent
│
├── router/
│   ├── input_router.py          # CHAT / CLARIFY / TASK routing
│   ├── task_router.py           # Task dispatcher
│   └── state.py                 # Session state
│
├── faiss_index/                 # Persistent shared memory
│
├── orchestrator.py              # Central agent orchestration
├── memory.py                    # Per-agent memory
├── shared_memory.py             # FAISS-based shared memory
├── tools.py                     # Tool implementations
│
├── main.py                      # Main execution entry
├── main_single_agent.py         # Single-agent prototype
├── test_chat_history.py         # Memory testing
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1️⃣ Install Dependencies
~~~bash
pip install -r requirements.txt
~~~

### 2️⃣ Configure Environment Variables
~~~bash
cp .env.example .env
~~~

Add your Gemini API key in `.env`:
~~~bash
GEMINI_API_KEY=your_api_key_here
~~~

### 3️⃣ Run the Multi-Agent System
~~~bash
python src/main.py
~~~

### 💬 Commands
- Type a query to start
- `clear` → reset memory
- `exit` → quit the program

---

## 📈 Project Evolution

| Milestone | Description |
|----------|-------------|
| Milestone 1 | Single-agent setup with basic prompts |
| Milestone 2 | Tool integration and safe execution |
| Milestone 3 | Multi-agent orchestration with memory |
| Milestone 4 | Intelligent routing, workflow automation & API layer |

---

## 🎯 Design Philosophy

- Architecture-first over UI-first
- Explicit reasoning over implicit behavior
- Routing before execution
- Memory as a first-class component
- Explainability over black-box responses

---

## 📜 License

This project is licensed under the MIT License.

---

## ✅ Final Note

This project is intentionally architecture-first.  
It demonstrates how real-world LLM agent systems are designed and orchestrated,
not just how they respond.
``
