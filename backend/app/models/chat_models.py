from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from .response_models import SimulationMetadata

class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    id: str
    type: MessageType
    content: str
    timestamp: datetime
    simulation_id: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1, max_length=500)
    simulation_id: Optional[str] = None

class ChatResponse(BaseModel):
    simulation_id: str
    session_id: str
    message: str
    description: str
    scene: Dict[str, Any]
    changes_made: List[str]
    metadata: SimulationMetadata

class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    total_messages: int
    
class SessionInfo(BaseModel):
    session_id: str
    created_at: datetime
    last_activity: datetime
    message_count: int
    current_simulation_id: Optional[str] = None 