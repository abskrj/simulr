from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    HIGH = "high"
 b 
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"

class SimulationRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500)
    complexity: ComplexityLevel = ComplexityLevel.SIMPLE
    provider: LLMProvider = LLMProvider.OPENAI
    structure_type: str = "auto"
    preferences: Optional[Dict[str, Any]] = {
        "units": "metric",
        "detail_level": "educational",
        "animation": True
    }

class ExampleRequest(BaseModel):
    category: Optional[str] = "all"
    complexity: Optional[ComplexityLevel] = None 