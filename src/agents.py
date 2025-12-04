
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import get_tools
from langchain_core.prompts import PromptTemplate


# WEEk - 1
def create_basic_gemini_agent(model: str = "gemini-2.5-flash", temperature: float = 0.0):
   
    # Instantiate the Gemini-backed chat model (uses GEMINI_API_KEY env variable)
    llm = ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature
    )

    tools = get_tools()
    checkpointer = MemorySaver()  # Short-term memory: stores conversation within a session

    # Create agent using LangChain v1 API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are a helpful assistant"
            "Answer user questions accurately and use available tools when needed."
        ),
        checkpointer=checkpointer  # Modern v1 approach - memory built-in via checkpointer 
    )

    return agent

# Week 2 upgrade
basic_template = PromptTemplate(
    input_variables=["user_input"],
    template=(
        "You are a reliable AI assistant. Understand the user's query: {user_input}. "
        "Respond clearly and concisely, and use tools whenever they can produce a more accurate answer."
    )
)



# Create agent using a custom prompt template
def create_template_gemini_agent(
    model="gemini-2.5-flash",
    temperature=0.0,
    template=basic_template
):
    llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)
    tools = get_tools()
    checkpointer = MemorySaver()

    # The template becomes the system prompt
    system_prompt = template.template  

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer
    )
    return agent

