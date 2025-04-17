from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Literal

class Provider(str, Enum):
    """Supported AI provider options"""
    VAPI = "vapi"
    RETELL = "retell"

class LLMConfig(BaseModel):
    """Standardized LLM configuration"""
    type: Literal["builtin", "custom"]
    model: Optional[str] = Field(
        None,
        description="Required when type=builtin (Vapi)",
        example="gpt-4"
    )
    websocket_url: Optional[str] = Field(
        None,
        description="Required when type=custom (Retell)",
        example="wss://your-llm.com"
    )

class VoiceConfig(BaseModel):
    """Standardized voice configuration"""
    id: str = Field(..., example="voice-123")
    provider: Optional[str] = Field(
        None,
        description="Required for Vapi",
        example="11labs"
    )

class BehaviorConfig(BaseModel):
    """Standardized agent behavior"""
    initial_message: str = Field(
        ...,
        example="Hello! How can I help you today?"
    )
    instructions: str = Field(
        ...,
        example="You are a helpful assistant..."
    )
    allow_interruptions: bool = Field(
        default=False,
        description="Whether user can interrupt the agent"
    )
    conversation_timeout: Optional[int] = Field(
        None,
        description="In seconds",
        ge=30,
        le=3600
    )

class AgentCreateRequest(BaseModel):
    """Unified request schema for all providers"""
    provider: Provider = Field(..., example="vapi")
    agent_name: str = Field(..., min_length=2, max_length=50)
    llm: LLMConfig
    voice: VoiceConfig
    behavior: BehaviorConfig

    class Config:
        schema_extra = {
            "example": {
                "provider": "vapi",
                "agent_name": "Sales Assistant",
                "llm": {
                    "type": "builtin",
                    "model": "gpt-4"
                },
                "voice": {
                    "id": "voice-123",
                    "provider": "11labs"
                },
                "behavior": {
                    "initial_message": "Welcome!",
                    "instructions": "Help with product questions",
                    "allow_interruptions": True,
                    "conversation_timeout": 300
                }
            }
        }

class AgentResponse(BaseModel):
    """Standardized success response"""
    success: bool
    agent_id: str
    provider: str
    created_at: str
    details: Optional[dict] = None

class ErrorResponse(BaseModel):
    """Standardized error response"""
    error: str
    details: Optional[str] = None
    provider: Optional[str] = None