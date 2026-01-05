from fastapi import APIRouter
from src.Backend.app.schemas import TaskRequest, TaskResponse

# import your existing orchestrator
from src.orchestrator import run_multi_agent_workflow

router = APIRouter()

@router.post("/run", response_model=TaskResponse)
def run_task(request: TaskRequest):
    result = run_multi_agent_workflow(request.query)

    return TaskResponse(
        status="success",
        output=result
    )
