
from agents import create_template_gemini_agent



def extract_response(result):
    """Extract the final response from the agent result."""
    
    # Handle dict with messages
    if isinstance(result, dict) and "messages" in result:
        messages = result["messages"]
        # Get the last AIMessage (which contains the final response)
        for msg in reversed(messages):
            if hasattr(msg, "content"):
                content = msg.content
                
                # Handle string content (simple case)
                if isinstance(content, str) and content:
                    return content
                
                # Handle content blocks (list of dicts with 'text' key)
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and "text" in block:
                            return block["text"]
    
    # Fallback: try to get content directly
    if hasattr(result, "content"):
        content = result.content
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    return block["text"]
    
    return str(result)


def main():
    agent = create_template_gemini_agent(model="gemini-2.5-flash", temperature=0.0)

    print("=" * 60)
    print("Gemini LangChain v1 ReAct Agent")
    print("=" * 60)
    print("Type 'exit' to quit.\n")


    thread_id = "user_session_1" # Track conversation

    while True:
        try:
            query = input("you: ").strip()
            if not query:
                continue
            if query.lower() == "exit":
                print("Goodbye!")
                break

             # Invoke agent with thread_id for memory persistence
            result = agent.invoke(
                {"messages": [{"role": "user", "content": query}]},
                config={"configurable": {"thread_id": thread_id}}
            )

            # Extract and print the response
            response = extract_response(result)
            print(f"Agent: {response}\n")

        except Exception as e:
            print(f"Agent error: {e}\n")


if __name__ == "__main__":
    main()
