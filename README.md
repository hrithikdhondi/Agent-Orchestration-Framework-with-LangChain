# Agent-Orchestration-Framework-with-LangChain
Agent Orchestration Framework (LangChain + Gemini)

This project implements a simple AI Agent System using LangChain, LangGraph, and Google Gemini.
The agent can call multiple custom tools to answer user queries more accurately.

**📌 Features:**

Agents

create_basic_gemini_agent() – simple agent with a fixed system prompt

create_template_gemini_agent() – agent using PromptTemplate (recommended)



**Tools:**

greet(name) – returns a greeting

get_weather(city) – fetches live weather using wttr.in

calculate(expression) – safe math calculator

gen_password(length) – generates secure passwords

get_time(tz) – returns 12-hour formatted time (UTC / IST / LOCAL)


**📂 Project Files:**

agents.py      - agent creation (basic + template)

tools.py       - tool definitions

main.py        - interactive chatbot

demo.py        - quick test for all tools using the agent

.env.example   - API key template

requirements.txt


**🔧 Setup:**

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt


**Create a .env file:**
GOOGLE_API_KEY=your_api_key_here


**▶️ Run the Agent (interactive):**
python main.py


**🧪 Quick Tool Demo:**
python demo.py


**This will test:**

Weather

Calculator

Password generation

Time tool

**✔ Milestone 1 Completed**

Basic agent + environment setup

Tools integrated

Template-based agent

Demo script included

📌 Milestone 2: Tool Integration & API Calling

Objective:
Extend the LangChain agent with custom tools, API access, and robust error handling.

Key Updates:

Integrated multiple custom tools using LangChain @tool

Added log_tool decorator for Thought–Action–Observation logging

Implemented error handling for:

Invalid user inputs

API failures (timeouts, bad responses)

Unsafe or invalid calculations

Guided the agent via prompts to use tools appropriately

Outcome:
A reliable tool-enabled agent with transparent execution and graceful error recovery.

If you want a 1-paragraph version or bullet-only ultra-short, I can trim it more.


📌 Milestone 3: Multi-Agent Orchestration & Memory Management
Overview

In Milestone 3, the project was extended into a multi-agent system where specialized agents collaborate to solve tasks using planning, execution, and summarization. The focus is on agent coordination, memory usage, and controlled tool invocation.

Agents Implemented

Planner Agent
Analyzes the user query and decides whether research is required. It generates a numbered execution plan and skips research for simple tasks.

Research Agent
Executes the Planner’s instructions step-by-step. It uses tools only when explicitly instructed and returns raw data without summarization.

Summarizer Agent
Converts raw research data into a clear, user-friendly final response without fetching new information.

Memory Architecture

Per-Agent Memory: Each agent maintains its own conversation history for context-aware reasoning.

Shared Memory: A FAISS-based vector store stores important facts and provides relevant past knowledge to guide future decisions.