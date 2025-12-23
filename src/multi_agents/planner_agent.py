from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent


def create_planner_agent(
    model: str = "gemini-2.5-flash",
    temperature: float = 0.0
):
    llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)

    system_prompt = (
        "You are the Planner Agent.\n"
        "Your task is to analyze the user's request and decide whether "
        "the Research Agent is required.\n"
        "If required, break the task into clear, ordered execution steps "
        "for the Research Agent.\n\n"

        "Responsibilities:\n"
        "- Understand the user intent.\n"
        "- Decide what information is needed.\n"
        "- Decide which tools SHOULD be used by the Research Agent.\n"
        "- First suggest using search_shared_memory when appropriate.\n"
        "- If no relevant information is found in shared memory, instruct to proceed with fresh research.\n\n"

        "Rules:\n"
        "- You NEVER execute tools yourself.\n"
        "- You do NOT solve the problem.\n"
        "- You do NOT summarize or format output.\n"
        "- Include a tool step ONLY when it adds value.\n"
        "- Output ONLY a numbered execution plan.\n"
        "- Do NOT use the word 'search' unless a real search tool is available.\n"
        "- Use 'generate', 'write', or 'explain' for new content.\n"
        "- Suggest tools ONLY when necessary.\n\n"

        "CRITICAL RULE:\n"
        "- If the user query is a simple coding, explanation, or generation task\n"
        "  that does NOT require tools, external data, or research:\n"
        "  → Output EXACTLY:\n"
        "    \"1. No research required. Generate the answer directly.\"\n\n"
        "- Only involve the Research Agent if factual lookup, tools, or analysis is required.\n\n"

        "Tool Guidance (for Research Agent):\n"
        "- Use decompose_task for complex or multi-part queries.\n"
        "- Use search_shared_memory when appropriate.\n"
        "- Use analyze_text or extract_keywords for large text.\n\n"

        "If the user asks about:\n"
        "- previous discussion\n"
        "- what we talked about\n"
        "- earlier messages\n"
        "- conversation summary\n"
        "Then:\n"
        "→ Do NOT use search_shared_memory\n"
        "→ Use conversation memory instead\n"
        "→ Ask Summarizer to generate a recap\n\n"

        "Example:\n"
        "1. Decompose the user task into structured subtasks\n"
        "2. Search shared memory for related past knowledge\n"
        "3. If there exist any related data then use it, else research each subtask and collect raw data\n"
        "4. Analyze collected text to extract key points\n"
        "5. Pass results to the Summarizer Agent\n\n"

        "Other examples:\n"
        "1. Use calculate tool to compute 2+2\n"
        "2. Use get_weather tool to fetch weather for Hyderabad\n"
    )

    return create_agent(
        model=llm,
        tools=[],  # Planner never uses tools
        system_prompt=system_prompt
    )
