from fastapi import FastAPI
from app.api.endpoints import router as agent_router

app = FastAPI(
    title="Unified Agent API",
    description="Single endpoint for Vapi.ai and Retell.ai"
)

app.include_router(agent_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)