from pydantic import BaseModel

class TaskRequest(BaseModel):
    query: str

class TaskResponse(BaseModel):
    status: str
    output: str
