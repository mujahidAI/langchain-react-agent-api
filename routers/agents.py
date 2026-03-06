from fastapi import APIRouter, HTTPException
from schemas.agent_schema import AgentRequest, AgentResponse
from services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    try:
        agent_service = AgentService(
            model_name=request.model,
            temperature=request.temperature,
            max_iterations=request.max_iterations,
        )
        result = agent_service.run(request.query)
        return AgentResponse(
            result=result["result"],
            steps=result["steps"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
