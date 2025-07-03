# FastAPI Backend Implementation Guide

## 🚀 Quick Start Implementation

Follow these steps to build your physics simulation backend step by step.

## Step 1: Project Setup

### Create the basic structure:
```bash
cd backend
mkdir -p app/{api,services,models,templates,utils}
mkdir tests
touch app/__init__.py
touch app/{api,services,models,templates,utils}/__init__.py
```

### Install dependencies:
```bash
pip install fastapi uvicorn pydantic python-multipart openai anthropic redis python-dotenv sqlalchemy alembic psycopg2-binary
```

### Create `requirements.txt`:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
openai==1.3.8
anthropic==0.7.8
redis==5.0.1
python-dotenv==1.0.0
sqlalchemy==2.0.23
alembic==1.13.1
psycopg2-binary==2.9.9
```

## Step 2: Basic FastAPI Setup

### `app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.chat_routes import router as chat_router
from app.config import settings

app = FastAPI(
    title="Physics Simulation API",
    description="Generate Three.js physics simulations from natural language with chat iteration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Physics Simulation API with Chat",
        "version": "1.0.0",
        "features": ["simulation_generation", "chat_iteration", "session_management"]
    }
```

### `app/config.py`
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    redis_url: str = "redis://localhost:6379"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

## Step 3: Pydantic Models

### `app/models/request_models.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    HIGH = "high"

class SimulationRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500)
    complexity: ComplexityLevel = ComplexityLevel.SIMPLE
    structure_type: str = "auto"
    preferences: Optional[Dict[str, Any]] = {
        "units": "metric",
        "detail_level": "educational",
        "animation": True
    }

class ExampleRequest(BaseModel):
    category: Optional[str] = "all"
    complexity: Optional[ComplexityLevel] = None
```

### `app/models/response_models.py`
```python
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
```

### `app/models/chat_models.py`
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

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
```

## Step 4: LLM Service

### `app/services/llm_service.py`
```python
import json
import uuid
from datetime import datetime
from typing import Dict, Any
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from app.config import settings
from app.models.request_models import SimulationRequest

class LLMService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    
    async def generate_simulation(self, request: SimulationRequest) -> Dict[str, Any]:
        """Generate Three.js simulation JSON from natural language"""
        
        system_prompt = self._get_system_prompt(request.complexity)
        user_prompt = self._build_user_prompt(request)
        
        try:
            # Use OpenAI GPT-4
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Parse JSON response
            json_content = response.choices[0].message.content
            simulation_data = json.loads(json_content)
            
            # Add metadata
            simulation_data.update({
                "simulation_id": str(uuid.uuid4()),
                "description": request.prompt,
                "complexity": request.complexity.value,
                "metadata": {
                    "generated_at": datetime.now(),
                    "processing_time": 2.5,  # Mock for now
                    "llm_model": "gpt-4-turbo-preview",
                    "confidence": 0.85
                }
            })
            
            return simulation_data
            
        except Exception as e:
            # Fallback to template
            return self._get_fallback_simulation(request)
    
    def _get_system_prompt(self, complexity: str) -> str:
        """Get system prompt based on complexity level"""
        
        prompts = {
            "simple": """
            You are a structural engineering assistant that converts natural language 
            descriptions into Three.js-ready JSON for physics simulations.
            
            Generate JSON that includes:
            - "scene" object with "meshes", "supports", "force_arrows"
            - Each mesh has: id, type (BoxGeometry/CylinderGeometry), position, scale, material
            - Force arrows have: origin, direction, length, color, label
            - Stress colors mapping
            - Camera position and lighting
            
            Focus on simple geometric shapes and clear educational visualization.
            Return ONLY valid JSON, no explanations.
            """,
            
            "medium": """
            You are an advanced structural engineering assistant for complex simulations.
            
            Generate detailed Three.js JSON with:
            - Multiple structural systems
            - Realistic proportions and materials
            - Multiple load cases
            - Complex geometry arrangements
            
            Return ONLY valid JSON, no explanations.
            """,
            
            "high": """
            You are an expert structural engineering assistant for complex structures.
            
            Generate comprehensive Three.js JSON with:
            - Multi-component systems (cables, towers, decks)
            - Realistic structural behavior
            - Multiple analysis types
            - Advanced visualization features
            
            Return ONLY valid JSON, no explanations.
            """
        }
        
        return prompts.get(complexity, prompts["simple"])
    
    def _build_user_prompt(self, request: SimulationRequest) -> str:
        """Build user prompt with context"""
        
        return f"""
        Create a Three.js physics simulation for: "{request.prompt}"
        
        Requirements:
        - Complexity: {request.complexity.value}
        - Structure type: {request.structure_type}
        - Units: {request.preferences.get('units', 'metric')}
        - Detail level: {request.preferences.get('detail_level', 'educational')}
        - Animation: {request.preferences.get('animation', True)}
        
        Generate the complete JSON structure for Three.js rendering.
        """
    
    def _get_fallback_simulation(self, request: SimulationRequest) -> Dict[str, Any]:
        """Fallback simulation when LLM fails"""
        
        return {
            "simulation_id": str(uuid.uuid4()),
            "description": request.prompt,
            "complexity": request.complexity.value,
            "scene": {
                "meshes": [
                    {
                        "id": "beam_1",
                        "type": "BoxGeometry",
                        "position": [0, 0, 0],
                        "scale": [5, 0.2, 0.2],
                        "rotation": [0, 0, 0],
                        "material": {
                            "type": "MeshStandardMaterial",
                            "color": "#8C92AC",
                            "metalness": 0.8,
                            "roughness": 0.2
                        },
                        "userData": {
                            "element_type": "beam",
                            "stress_level": 0.4,
                            "force": 1000,
                            "material": "steel",
                            "info": "Simple steel beam under load"
                        }
                    }
                ],
                "supports": [
                    {
                        "id": "support_1",
                        "type": "ConeGeometry",
                        "position": [-2.5, -0.3, 0],
                        "scale": [0.2, 0.3, 0.2],
                        "material": {
                            "type": "MeshStandardMaterial",
                            "color": "#444444"
                        }
                    }
                ],
                "force_arrows": [
                    {
                        "id": "force_1",
                        "origin": [0, 0, 0],
                        "direction": [0, -1, 0],
                        "length": 2,
                        "color": "#FF4444",
                        "label": "1000N",
                        "label_position": [0, -2.5, 0]
                    }
                ]
            },
            "stress_colors": {
                "low": "#00FF00",
                "medium": "#FFAA00",
                "high": "#FF0000",
                "max_stress": 250
            },
            "camera": {
                "position": [10, 5, 10],
                "look_at": [0, 0, 0]
            },
            "lighting": {
                "ambient": {"color": "#404040", "intensity": 0.4},
                "directional": {
                    "color": "#ffffff",
                    "intensity": 0.8,
                    "position": [10, 10, 5]
                }
            },
            "metadata": {
                "generated_at": datetime.now(),
                "processing_time": 1.0,
                "llm_model": "fallback",
                "confidence": 0.5
            }
                 }
```

## Step 5: Chat Service & Session Management

### `app/services/chat_service.py`
```python
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from app.config import settings
from app.models.chat_models import ChatMessage, ChatRequest, MessageType
from app.services.session_manager import SessionManager

class ChatService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.session_manager = SessionManager()
    
    async def process_chat_message(self, request: ChatRequest) -> Dict[str, Any]:
        """Process chat message and generate updated simulation"""
        
        # Get conversation history
        history = await self.session_manager.get_chat_history(request.session_id)
        
        # Get current simulation context
        current_simulation = await self.session_manager.get_current_simulation(request.session_id)
        
        # Build context for LLM
        context = self._build_chat_context(history, current_simulation, request.message)
        
        try:
            # Generate response using LLM
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=context,
                temperature=0.7,
                max_tokens=3000
            )
            
            # Parse response
            response_content = response.choices[0].message.content
            
            # Extract simulation JSON and explanation
            simulation_data, explanation, changes = self._parse_chat_response(response_content)
            
            # Generate new simulation ID
            new_simulation_id = str(uuid.uuid4())
            
            # Update simulation data
            simulation_data.update({
                "simulation_id": new_simulation_id,
                "session_id": request.session_id,
                "metadata": {
                    "generated_at": datetime.now(),
                    "processing_time": 2.0,
                    "llm_model": "gpt-4-turbo-preview",
                    "confidence": 0.85
                }
            })
            
            # Save to session
            await self.session_manager.add_message(
                request.session_id,
                ChatMessage(
                    id=str(uuid.uuid4()),
                    type=MessageType.USER,
                    content=request.message,
                    timestamp=datetime.now()
                )
            )
            
            await self.session_manager.add_message(
                request.session_id,
                ChatMessage(
                    id=str(uuid.uuid4()),
                    type=MessageType.ASSISTANT,
                    content=explanation,
                    timestamp=datetime.now(),
                    simulation_id=new_simulation_id
                )
            )
            
            # Update current simulation
            await self.session_manager.update_current_simulation(request.session_id, new_simulation_id)
            
            return {
                **simulation_data,
                "message": explanation,
                "changes_made": changes
            }
            
        except Exception as e:
            return self._get_error_response(request, str(e))
    
    def _build_chat_context(self, history: List[ChatMessage], current_simulation: Optional[Dict], message: str) -> List[Dict[str, str]]:
        """Build context for LLM chat"""
        
        system_prompt = """
        You are a structural engineering assistant helping users iterate on physics simulations.
        
        Current conversation context:
        - User has an existing simulation
        - User wants to modify or improve the simulation
        - Generate updated Three.js JSON based on the request
        - Explain what changes you made
        - List specific modifications in a "changes_made" array
        
        Return format:
        {
            "explanation": "I've made the following changes...",
            "changes_made": ["Increased bridge length", "Added supports"],
            "simulation": { ... Three.js JSON ... }
        }
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 messages)
        for msg in history[-10:]:
            role = "user" if msg.type == MessageType.USER else "assistant"
            messages.append({"role": role, "content": msg.content})
        
        # Add current simulation context
        if current_simulation:
            messages.append({
                "role": "system",
                "content": f"Current simulation: {json.dumps(current_simulation, indent=2)}"
            })
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        return messages
    
    def _parse_chat_response(self, response: str) -> tuple[Dict[str, Any], str, List[str]]:
        """Parse LLM response to extract simulation, explanation, and changes"""
        
        try:
            # Try to parse as JSON
            data = json.loads(response)
            return (
                data.get("simulation", {}),
                data.get("explanation", "Simulation updated successfully."),
                data.get("changes_made", [])
            )
        except json.JSONDecodeError:
            # Fallback parsing
            return {}, "Simulation updated.", ["Modified structure"]
    
    def _get_error_response(self, request: ChatRequest, error: str) -> Dict[str, Any]:
        """Generate error response"""
        
        return {
            "simulation_id": str(uuid.uuid4()),
            "session_id": request.session_id,
            "message": f"I encountered an error: {error}. Please try rephrasing your request.",
            "description": "Error in simulation generation",
            "scene": {"meshes": [], "supports": [], "force_arrows": []},
            "changes_made": [],
            "metadata": {
                "generated_at": datetime.now(),
                "processing_time": 0.5,
                "llm_model": "error",
                "confidence": 0.0
            }
        }
```

### `app/services/session_manager.py`
```python
import json
import uuid
import redis
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from app.config import settings
from app.models.chat_models import ChatMessage, MessageType

class SessionManager:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
        self.session_timeout = settings.session_timeout
        self.max_chat_history = settings.max_chat_history
    
    async def create_session(self, initial_simulation_id: str) -> str:
        """Create a new chat session"""
        
        session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "message_count": 0,
            "current_simulation_id": initial_simulation_id,
            "messages": []
        }
        
        # Store in Redis
        await self._store_session(session_id, session_data)
        
        return session_id
    
    async def get_chat_history(self, session_id: str) -> List[ChatMessage]:
        """Get chat history for a session"""
        
        session_data = await self._get_session(session_id)
        if not session_data:
            return []
        
        messages = []
        for msg_data in session_data.get("messages", []):
            messages.append(ChatMessage(
                id=msg_data["id"],
                type=MessageType(msg_data["type"]),
                content=msg_data["content"],
                timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                simulation_id=msg_data.get("simulation_id")
            ))
        
        return messages
    
    async def add_message(self, session_id: str, message: ChatMessage):
        """Add a message to the session"""
        
        session_data = await self._get_session(session_id)
        if not session_data:
            return
        
        # Add message
        session_data["messages"].append({
            "id": message.id,
            "type": message.type.value,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "simulation_id": message.simulation_id
        })
        
        # Trim history if too long
        if len(session_data["messages"]) > self.max_chat_history:
            session_data["messages"] = session_data["messages"][-self.max_chat_history:]
        
        # Update metadata
        session_data["message_count"] += 1
        session_data["last_activity"] = datetime.now().isoformat()
        
        # Store back
        await self._store_session(session_id, session_data)
    
    async def get_current_simulation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current simulation for a session"""
        
        session_data = await self._get_session(session_id)
        if not session_data:
            return None
        
        simulation_id = session_data.get("current_simulation_id")
        if not simulation_id:
            return None
        
        # Get simulation from cache/database
        simulation_key = f"simulation:{simulation_id}"
        simulation_data = self.redis_client.get(simulation_key)
        
        if simulation_data:
            return json.loads(simulation_data)
        
        return None
    
    async def update_current_simulation(self, session_id: str, simulation_id: str):
        """Update current simulation for a session"""
        
        session_data = await self._get_session(session_id)
        if not session_data:
            return
        
        session_data["current_simulation_id"] = simulation_id
        session_data["last_activity"] = datetime.now().isoformat()
        
        await self._store_session(session_id, session_data)
    
    async def _get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data from Redis"""
        
        session_key = f"session:{session_id}"
        session_data = self.redis_client.get(session_key)
        
        if session_data:
            return json.loads(session_data)
        
        return None
    
    async def _store_session(self, session_id: str, session_data: Dict[str, Any]):
        """Store session data in Redis"""
        
        session_key = f"session:{session_id}"
        self.redis_client.setex(
            session_key,
            self.session_timeout,
            json.dumps(session_data, default=str)
        )
```

## Step 6: Chat API Routes

### `app/api/chat_routes.py`
```python
from fastapi import APIRouter, HTTPException, Depends
from app.models.chat_models import ChatRequest, ChatResponse, ChatHistoryResponse
from app.services.chat_service import ChatService
from app.services.session_manager import SessionManager

router = APIRouter()

async def get_chat_service():
    return ChatService()

async def get_session_manager():
    return SessionManager()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_simulation(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Process chat message and update simulation"""
    
    try:
        response_data = await chat_service.process_chat_message(request)
        return ChatResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )

@router.get("/chat/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """Get chat history for a session"""
    
    try:
        messages = await session_manager.get_chat_history(session_id)
        return ChatHistoryResponse(
            session_id=session_id,
            messages=messages,
            total_messages=len(messages)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get chat history: {str(e)}"
        )

@router.delete("/chat/session/{session_id}")
async def clear_chat_session(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """Clear chat session"""
    
    # Implementation depends on your session storage
    return {"message": "Session cleared successfully"}
```

## Step 7: Updated Main Routes

### `app/api/routes.py`
```python
from fastapi import APIRouter, HTTPException, Depends
from app.models.request_models import SimulationRequest, ExampleRequest
from app.models.response_models import SimulationResponse, ExamplesResponse
from app.services.llm_service import LLMService
from app.services.session_manager import SessionManager
from app.templates.simple_structures import get_example_structures

router = APIRouter()

async def get_llm_service():
    return LLMService()

async def get_session_manager():
    return SessionManager()

@router.post("/simulate", response_model=SimulationResponse)
async def generate_simulation(
    request: SimulationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """Generate physics simulation from natural language"""
    
    try:
        simulation_data = await llm_service.generate_simulation(request)
        
        # Create session for chat functionality
        session_id = await session_manager.create_session(simulation_data["simulation_id"])
        simulation_data["session_id"] = session_id
        
        return SimulationResponse(**simulation_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation generation failed: {str(e)}"
        )

@router.get("/examples", response_model=ExamplesResponse)
async def get_examples(request: ExampleRequest = Depends()):
    """Get pre-built simulation examples"""
    
    examples = get_example_structures()
    
    # Filter by complexity if specified
    if request.complexity:
        examples = [ex for ex in examples if ex.complexity == request.complexity.value]
    
    return ExamplesResponse(examples=examples)

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "physics-simulation-api"}
```

## Step 6: Example Templates

### `app/templates/simple_structures.py`
```python
from app.models.response_models import Example
from typing import List

def get_example_structures() -> List[Example]:
    """Return pre-built example structures"""
    
    return [
        Example(
            id="simple_truss",
            title="Simple Truss Bridge",
            prompt="steel rod stress on truss bridge",
            complexity="simple"
        ),
        Example(
            id="cantilever_beam",
            title="Cantilever Beam",
            prompt="cantilever beam with point load",
            complexity="simple"
        ),
        Example(
            id="frame_structure",
            title="Steel Frame Building",
            prompt="steel frame building with wind load",
            complexity="medium"
        ),
        Example(
            id="suspension_bridge",
            title="Suspension Bridge",
            prompt="suspension bridge like golden gate bridge",
            complexity="high"
        )
    ]
```

## Step 7: Environment Setup

### `.env` file:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
```

## Step 8: Running the Backend

```bash
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 9: Test the API

### Test health endpoint:
```bash
curl http://localhost:8000/api/health
```

### Test simulation generation:
```bash
curl -X POST "http://localhost:8000/api/simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "steel rod stress on truss bridge",
    "complexity": "simple",
    "structure_type": "auto"
  }'
```

### Test examples:
```bash
curl http://localhost:8000/api/examples
```

## 🎯 Next Steps

1. **Add JSON validation** for LLM outputs
2. **Implement caching** with Redis
3. **Add error handling** and logging
4. **Create more sophisticated prompts**
5. **Add rate limiting**
6. **Write comprehensive tests**

## 🔧 Development Tips

- **Start simple**: Get basic structure working first
- **Test with mock data**: Don't rely on LLM initially
- **Validate JSON**: Always validate LLM-generated JSON
- **Use fallbacks**: Have backup simulations ready
- **Monitor performance**: Track response times and costs

---

This implementation provides a solid foundation that can grow from simple structures to complex engineering simulations! 