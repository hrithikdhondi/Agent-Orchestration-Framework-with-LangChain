from src.orchestrator import run_multi_agent_workflow


def run_task(query: str, mode: str):
    """
    Dispatch task execution based on mode.
    """

    if mode == "COMPLEX_TASK":
        return run_multi_agent_workflow(query)

    raise ValueError(f"Unknown mode: {mode}")
