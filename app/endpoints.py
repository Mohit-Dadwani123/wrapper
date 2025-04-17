from fastapi import APIRouter, HTTPException
from app.schemas import UnifiedAgentRequest
from app.services import vapi, retell

router = APIRouter()

@router.post("/agents", summary="Create agent with unified interface")
async def create_agent(request: UnifiedAgentRequest):
    try:
        if request.provider == "vapi":
            if request.llm["type"] != "builtin":
                raise HTTPException(
                    status_code=400,
                    detail="Vapi requires 'builtin' LLM type"
                )
            result = await vapi.create_vapi_agent(request)
            
        elif request.provider == "retell":
            if request.llm["type"] != "custom":
                raise HTTPException(
                    status_code=400,
                    detail="Retell requires 'custom' LLM type"
                )
            result = await retell.create_retell_agent(request)
            
        return {
            "status": "success",
            "provider": request.provider,
            "agent_id": result.get("id") or result.get("agent_id"),
            "details": result
        }
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"{request.provider} API error: {e.response.text}"
        )