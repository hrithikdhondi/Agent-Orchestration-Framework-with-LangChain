from fastapi import FastAPI
from src.Backend.app.routes import router

app = FastAPI(
    title="Agent Orchestration API",
    description="Multi-Agent Workflow Automation using LangChain",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Agent Orchestration API running"}
