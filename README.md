# 🧠 Agent-Orchestration Framework with LangChain

---

> **A Modular Multi-Agent Reasoning System**  
> LangChain • Gemini LLM • Tool-Based Reasoning • Memory-Oriented Architecture

This project implements a **multi-agent orchestration framework** using **LangChain** and **Google Gemini**.  
Instead of functioning as a traditional chatbot, the system decomposes user queries into **specialized agent responsibilities** such as planning, research, and summarization, coordinated through a central orchestration layer.

The focus of this project is on **how intelligence is structured**, not just how responses are generated.

---

## 📌 Project Highlights
---

- 🧩 **Multi-Agent Architecture** with clear separation of concerns  
- 🛠 **Tool-Based Reasoning** for deterministic operations  
- 🧠 **Per-Agent & Shared Memory** for contextual and reusable knowledge  
- 🔁 **Central Orchestration Layer** to manage agent flow  
- 📈 **Incremental, Milestone-Based System Evolution**

---

## 🧠 System Overview
```text
User Query
   │
   ▼
Planner Agent
   │   (decides execution strategy)
   ▼
Research Agent
   │   (uses tools & memory)
   ▼
Summarizer Agent
   │
   ▼
Final Answer
```

**Memory Layers**
- **Agent Memory** → short-term conversational context  
- **Shared Memory (FAISS)** → long-term reusable knowledge  

---

## 🤖 Agents Implemented
---

| Agent Name | Responsibility |
|-----------|---------------|
| **Planner Agent** | Analyzes user intent and generates a strict step-by-step execution plan |
| **Research Agent** | Executes the plan using tools, shared memory, and structured reasoning |
| **Summarizer Agent** | Converts raw research output into a clear, user-facing response |
| **Orchestrator** | Manages agent communication and execution flow |

Each agent is implemented independently to ensure **modularity, traceability, and extensibility**.

---

## 🛠 Tools Implemented
---

| Tool | Purpose |
|-----|--------|
| `greet(name)` | Returns a greeting |
| `get_weather(city)` | Fetches live weather data |
| `calculate(expression)` | Safely evaluates mathematical expressions |
| `gen_password(length)` | Generates secure random passwords |
| `get_time(tz)` | Returns current time (UTC / IST / LOCAL) |
| `read_file(path)` | Reads text-based files |
| `write_file(path, content)` | Writes content to files |
| `append_file(path, content)` | Appends content to files |
| `analyze_text(text)` | Extracts key points from large text |
| `extract_keywords(text)` | Identifies important keywords |
| `decompose_task(goal)` | Breaks a goal into structured subtasks |
| `structure_as_json()` | Converts content into structured JSON |
| `generate_markdown_table()` | Generates markdown tables |

All tools are **explicitly invoked** and never hallucinated.

---

## 🧠 Memory Design
---

### 🔹 Agent Memory
- Maintains short-term conversational context per agent  
- Isolated memory prevents cross-agent contamination  

### 🔹 Shared Memory
- Implemented using **FAISS vector store**  
- Uses **Gemini embeddings**  
- Stores reusable facts across conversations  
- Enables memory-aware decision making  

---

## 📂 Project Structure
---

```text
src/
├── faiss_index/                 # Persistent shared memory (vector store)
│
├── multi_agents/
│   ├── __init__.py
│   ├── planner_agent.py         # Planner Agent logic
│   ├── research_agent.py        # Research Agent logic
│   └── summarizer_agent.py      # Summarizer Agent logic
│
├── agents.py                    # Agent factory methods
├── orchestrator.py              # Central orchestration logic
├── memory.py                    # Per-agent memory handling
├── shared_memory.py             # FAISS-based shared memory
├── tools.py                     # Tool implementations
│
├── main.py                      # Multi-agent execution entry point
├── main_single_agent.py         # Single-agent prototype
├── test_chat_history.py         # Memory testing utilities
│
├── .env.example                 # Environment variable template
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
| Milestone 4 | Workflow automation & API layer (upcoming) |

---

## 🎯 Design Philosophy

- Separation of Concerns over monolithic agents
- Explicit Tool Usage over implicit reasoning
- Memory as a First-Class Component
- Explainability > UI Complexity

---

## 🚀 Future Enhancements

- REST API (FastAPI / Flask)
- Frontend UI for workflow triggering
- Agent performance evaluation
- Dynamic agent routing strategies

---

## 📜 License

This project is licensed under the MIT License.

---

## ✅ Final Note

This project is intentionally architecture-first.  
It demonstrates how real-world LLM agent systems are designed and orchestrated,
not just how they respond.
``


