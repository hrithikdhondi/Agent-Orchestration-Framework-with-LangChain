from multi_agents import (
    create_planner_agent,
    create_research_agent,
    create_summarizer_agent,
    create_email_compose_agent
)

from memory import AgentMemory
from shared_memory import SharedKnowledgeBase
import uuid


def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict)
        )
    return str(content)

DIRECT_GENERATION = "__DIRECT_GENERATION__"

def run_multi_agent_workflow(user_query: str):
    print(f"🔍 Processing: {user_query}")

    # =========================
    # INITIALIZE MEMORY
    # =========================
    agent_memory = AgentMemory()
    shared_memory = SharedKnowledgeBase()

    session_id = str(uuid.uuid4())[:8]

    # =========================
    # EMAIL INTENT CHECK
    # =========================
    email_intent = any(
        phrase in user_query.lower()
        for phrase in [
            "write an email",
            "compose an email",
            "draft an email",
            "send an email",
            "email to",
            "mail to"
        ]
    )

    # =========================
    # SHARED MEMORY LOOKUP
    # =========================
    try:
        shared_context = shared_memory.get_context(user_query)
    except Exception:
        shared_context = "Shared memory unavailable."

    # =========================
    # AGENT IDS
    # =========================
    planner_id = f"{session_id}-planner"
    researcher_id = f"{session_id}-researcher"
    summarizer_id = f"{session_id}-summarizer"
    email_id = f"{session_id}-email"

    # =========================
    # CREATE AGENTS
    # =========================
    planner = create_planner_agent()
    researcher = create_research_agent()
    summarizer = create_summarizer_agent()
    email_agent = create_email_compose_agent()

    # =========================
    # PLANNER
    # =========================
    planner_history = agent_memory.get_agent_memory(planner_id)

    planner_context = f"""
Previous conversations: {planner_history.messages[-3:] if planner_history.messages else 'None'}
Shared knowledge: {shared_context}

User Query: {user_query}

Plan execution steps for Research Agent.
"""

    planner_result = planner.invoke({
        "messages": [{"role": "user", "content": planner_context}]
    })

    plan = extract_text(planner_result["messages"][-1].content).strip()

    agent_memory.add_message(planner_id, "user", user_query)
    agent_memory.add_message(planner_id, "assistant", plan)

    print(f"Planner output:\n{plan}")

    # =========================
    # DECIDE RESEARCH
    # =========================
    skip_research = any(
        phrase in plan.lower()
        for phrase in [
            "no research required",
            "research not required",
            "research not needed",
            "generate the answer directly"
        ]
    )

    # =========================
    # RESEARCHER (ONLY IF NEEDED)
    # =========================
    if skip_research:
        raw_data = DIRECT_GENERATION
    else:
        researcher_history = agent_memory.get_agent_memory(researcher_id)

        researcher_context = f"""
Previous research: {researcher_history.messages[-2:] if researcher_history.messages else 'None'}
Shared knowledge: {shared_context}

Execution Plan: {plan}

Execute research steps and return raw data only.
"""

        researcher_result = researcher.invoke({
            "messages": [{"role": "user", "content": researcher_context}]
        })

        raw_data = extract_text(
            researcher_result["messages"][-1].content
        )

        agent_memory.add_message(researcher_id, "user", plan)
        agent_memory.add_message(researcher_id, "assistant", raw_data)

    if not skip_research:
        print("Researcher output:")
        print(raw_data)


    # =========================
    # SUMMARIZER
    # =========================
    if raw_data == DIRECT_GENERATION:
        summarizer_context = f"""
User Query: {user_query}

Generate the final answer directly.
"""
    else:
        summarizer_context = f"""
Original Query: {user_query}
Shared Knowledge: {shared_context}
Research Data: {raw_data}

Create polished final answer.
"""

    summarizer_result = summarizer.invoke({
        "messages": [{"role": "user", "content": summarizer_context}]
    })

    final_answer = extract_text(
        summarizer_result["messages"][-1].content
    )

    # =========================
    # EMAIL AGENT (OPTIONAL)
    # =========================
    if email_intent:
        email_context = f"""
Final summarized content:
{final_answer}

Convert the above into a professional email.
Use square-bracket placeholders where details are missing.
"""

        email_result = email_agent.invoke({
            "messages": [{"role": "user", "content": email_context}]
        })

        final_answer = extract_text(
            email_result["messages"][-1].content
        )

        agent_memory.add_message(email_id, "user", final_answer)
        agent_memory.add_message(email_id, "assistant", final_answer)

    # =========================
    # SAVE MEMORY (ONLY WHEN USEFUL)
    # =========================
    agent_memory.add_message(summarizer_id, "user", raw_data)
    agent_memory.add_message(summarizer_id, "assistant", final_answer)

    if not email_intent and not skip_research:
        shared_memory.save_fact(
            f"Q: {user_query[:50]}... | "
            f"Key facts: {raw_data[:150]}... | "
            f"Summary: {final_answer[:100]}..."
        )

    return final_answer