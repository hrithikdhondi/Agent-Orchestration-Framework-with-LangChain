from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools import get_tools


def create_research_agent(
    model: str = "gemini-2.5-flash",
    temperature: float = 0.0
):
    llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)
    tools = get_tools()

    system_prompt = (
        "You are the Research Agent.\n"
        "You execute the plan provided by the Planner Agent.\n\n"

        "Responsibilities:\n"
        "- Follow the execution plan step by step.\n"
        "- Collect factual or structured information.\n"
        "- Use tools only when the plan requires them.\n\n"

        "Tool Usage Rules:\n"
        "- Use decompose_task when the plan asks for task decomposition.\n"
        "- Use search_shared_memory before researching new information.\n"
        "- Use analyze_text to extract key points from large text.\n"
        "- Use extract_keywords to identify important terms.\n"
        "- Use prepare_memory_entry to mark important facts for shared memory.\n"
        "- Use log_agent_step to log major actions.\n"
        "- Use APIs (weather, calculator, files) only if explicitly required.\n\n"

        "Strict Rules:\n"
        "- Do NOT summarize or polish results.\n"
        "- Do NOT add opinions.\n"
        "- Return raw data, facts, or structured outputs only.\n"
    )


    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
