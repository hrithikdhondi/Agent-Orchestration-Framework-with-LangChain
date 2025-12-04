

from agents import create_template_gemini_agent, create_basic_gemini_agent

PROMPTS = [
    ("Weather", "What's the weather in Mumbai? Please use the weather tool."),
    ("Calculator", "Please use the calculator tool to compute 12 * (5 + 3)."),
    ("Password", "Generate a secure password of length 12 using the password tool."),
    ("Time", "Tell me the current time in IST using the time tool."),
]

def safe_invoke(agent, prompt):
    """Invoke the agent safely (handles CompiledStateGraph with with_config)."""
    cfg = {"thread_id": "demo_thread", "checkpoint_ns": "demo_ns", "checkpoint_id": "run1"}
    # prefer configured copy
    if hasattr(agent, "with_config"):
        try:
            agent_cfg = agent.with_config(cfg)
            return agent_cfg.invoke({"messages": [{"role": "user", "content": prompt}]})
        except Exception:
            pass
    # try invoke with config kwarg
    try:
        return agent.invoke({"messages": [{"role": "user", "content": prompt}]}, config=cfg)
    except Exception:
        pass
    # try common sync calls
    for name in ("run", "predict", "execute", "__call__"):
        if hasattr(agent, name):
            try:
                return getattr(agent, name)(prompt)
            except Exception:
                pass
    raise RuntimeError("No compatible call style for this agent")

def extract_text(result):
    """Best-effort: pull a human text answer from common agent result shapes."""
    try:
        # dict with 'messages' (langchain/langgraph)
        if isinstance(result, dict) and "messages" in result:
            msgs = result["messages"]
            for m in reversed(msgs):
                # object-like with .content
                content = None
                try:
                    content = getattr(m, "content", None)
                except Exception:
                    content = None
                if not content and isinstance(m, dict):
                    content = m.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()
                # handle ToolMessage/list-of-dicts style
                if isinstance(content, list) and content:
                    first = content[0]
                    if isinstance(first, dict) and "text" in first:
                        return first["text"]
        # string result
        if isinstance(result, str):
            return result.strip()
        # some agents return message objects or lists
        if hasattr(result, "content"):
            return getattr(result, "content") or str(result)
        # fallback to str
        return str(result)
    except Exception:
        return str(result)

def main():
    # create agent
    try:
        agent = create_template_gemini_agent()
    except Exception:
        agent = create_basic_gemini_agent()

    for label, prompt in PROMPTS:
        try:
            raw = safe_invoke(agent, prompt)
            text = extract_text(raw)
        except Exception as e:
            text = f"ERROR: {e}"
        # print single-line result
        print(f"{label}: {text}")

if __name__ == "__main__":
    main()
