# Agent-Orchestration-Framework-with-LangChain
Agent Orchestration Framework (LangChain + Gemini)

This project implements a simple AI Agent System using LangChain, LangGraph, and Google Gemini.
The agent can call multiple custom tools to answer user queries more accurately.

📌 Features
Agents

create_basic_gemini_agent() – simple agent with a fixed system prompt

create_template_gemini_agent() – agent using PromptTemplate (recommended)

Tools

greet(name) – returns a greeting

get_weather(city) – fetches live weather using wttr.in

calculate(expression) – safe math calculator

gen_password(length) – generates secure passwords

get_time(tz) – returns 12-hour formatted time (UTC / IST / LOCAL)

📂 Project Files
agents.py      - agent creation (basic + template)
tools.py       - tool definitions
main.py        - interactive chatbot
demo.py        - quick test for all tools using the agent
.env.example   - API key template
requirements.txt

🔧 Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


Create a .env file:

GOOGLE_API_KEY=your_api_key_here

▶️ Run the Agent (interactive)
python main.py

🧪 Quick Tool Demo
python demo.py


This will test:

Weather

Calculator

Password generation

Time tool

✔ Week 1 & 2 Completed

Basic agent + environment setup

Tools integrated

Template-based agent

Demo script included