from langchain_google_genai import ChatGoogleGenerativeAI
import json

# Cheap + fast model for routing
router_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0
)

# -------- EMAIL HEURISTICS -------- #

EMAIL_KEYWORDS = (
    "email",
    "mail",
    "compose",
    "draft",
)

EMAIL_CONTEXT_HINTS = (
    "to ",
    "about ",
    "regarding ",
    "for ",
    "manager",
    "hr",
    "client",
    "team",
    "meeting",
    "project",
    "internship",
    "delay",
)

# -------- SYSTEM PROMPT -------- #

ROUTER_SYSTEM_PROMPT = """
You are an INPUT ROUTER for an AI system.

Your job is to decide HOW the system should respond to the user.

Choose exactly ONE mode:

CHAT
- Casual conversation
- Greetings, opinions, acknowledgements
- No task execution required

CLARIFY
- User wants a task done
- Required information is missing
- Ask ONE clear follow-up question

COMPLEX_TASK
- Any executable task
- Email writing
- Multi-step reasoning
- Tool usage, memory, or orchestration required

Rules:
- If it is normal conversation → CHAT
- If task intent exists but info is missing → CLARIFY
- All executable tasks → COMPLEX_TASK

Respond ONLY in valid JSON.
"""

# -------- ROUTER FUNCTION -------- #

def route_input(user_input: str, state):
    """
    Decide how the system should handle the user input.
    """

    text = user_input.lower()

    # 1️⃣ Resume paused task (highest priority)
    if state.pending_task:
        return {"mode": "RESUME"}

    # -------- EMAIL FAST-PATH -------- #
    is_email = any(k in text for k in EMAIL_KEYWORDS)
    has_context = (
        any(h in text for h in EMAIL_CONTEXT_HINTS)
        or len(text.split()) > 5
    )

    if is_email and not has_context:
        return {
            "mode": "CLARIFY",
            "question": "Who is the email for and what is it about?"
        }

    if is_email and has_context:
        return {"mode": "COMPLEX_TASK"}

    # -------- LLM-BASED ROUTING -------- #
    prompt = f"""
{ROUTER_SYSTEM_PROMPT}

User message:
\"\"\"{user_input}\"\"\"

JSON Response Format:
{{
  "mode": "CHAT | CLARIFY | COMPLEX_TASK",
  "question": "<only if mode is CLARIFY>"
}}
"""

    response = router_llm.invoke(prompt)
    content = response.content.strip()

    try:
        decision = json.loads(content)
    except Exception:
        # Safe fallback
        return {"mode": "COMPLEX_TASK"}

    mode = decision.get("mode")

    if mode == "CLARIFY":
        return {
            "mode": "CLARIFY",
            "question": decision.get("question", "Could you clarify?")
        }

    if mode not in ("CHAT", "COMPLEX_TASK"):
        return {"mode": "COMPLEX_TASK"}

    return {"mode": mode}
