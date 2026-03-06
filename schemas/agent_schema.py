from pydantic import BaseModel


class AgentRequest(BaseModel):
    query: str
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.0
    max_iterations: int = 5


class AgentResponse(BaseModel):
    result: str
    steps: list[str]
