from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class SimulationMetadata(BaseModel):
    generated_at: datetime
    processing_time: float
    llm_model: str
    confidence: float

class SimulationResponse(BaseModel):
    simulation_id: str
    session_id: str
    description: str
    complexity: str
    scene: Dict[str, Any]
    metadata: SimulationMetadata
    
class Example(BaseModel):
    id: str
    title: str
    prompt: str
    complexity: str
    preview_image: Optional[str] = None

class ExamplesResponse(BaseModel):
    examples: List[Example] 