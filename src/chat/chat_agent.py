from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

chat_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

SYSTEM_PROMPT = """
You are a friendly conversational AI.

Rules:
- Respond naturally and briefly.
- Maintain conversation context.
- Do NOT perform tasks.
- Do NOT offer to run tools or workflows.
"""

def chat_response(user_input: str, state) -> str:
    """
    Handle normal conversation using chat memory.
    """

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add recent chat history
    for turn in state.chat_history[-10:]:
        if turn["role"] == "user":
            messages.append(HumanMessage(content=turn["content"]))
        elif turn["role"] == "assistant":
            messages.append(AIMessage(content=turn["content"]))

    # Current user message
    messages.append(HumanMessage(content=user_input))

    # LLM call
    response = chat_llm.invoke(messages)
    reply = response.content

    # Update state memory
    state.chat_history.append({"role": "user", "content": user_input})
    state.chat_history.append({"role": "assistant", "content": reply})

    return reply
