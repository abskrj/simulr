# Physics Simulation Backend - FastAPI

## 🎯 Overview

FastAPI backend that processes natural language simulation requests and returns Three.js-ready JSON using LLM models. Designed for scalability from simple trusses to complex structures like Golden Gate Bridge.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│                Client Request               │
├─────────────────────────────────────────────┤
│                FastAPI Layer                │
├─────────────────────────────────────────────┤
│              LLM Service Layer              │
├─────────────────────────────────────────────┤
│            JSON Validation Layer            │
├─────────────────────────────────────────────┤
│              Response Formatter             │
└─────────────────────────────────────────────┘
```

## 📋 API Endpoints

### **POST /api/simulate**
Primary endpoint for generating physics simulations.

**Request:**
```json
{
  "prompt": "steel rod stress on truss bridge",
  "complexity": "simple",
  "structure_type": "auto",
  "preferences": {
    "units": "metric",
    "detail_level": "educational",
    "animation": true
  }
}
```

**Response:**
```json
{
  "simulation_id": "uuid-string",
  "session_id": "uuid-string",
  "description": "Steel rod stress on truss bridge",
  "complexity": "simple",
  "scene": {
    "meshes": [...],
    "forces": [...],
    "supports": [...]
  },
  "metadata": {
    "generated_at": "2024-01-01T12:00:00Z",
    "processing_time": 2.3,
    "llm_model": "gpt-4",
    "confidence": 0.85
  }
}
```

### **POST /api/chat**
Chat endpoint for iterating on existing simulations.

**Request:**
```json
{
  "session_id": "uuid-string",
  "message": "make the bridge longer and add more supports",
  "simulation_id": "uuid-string"
}
```

**Response:**
```json
{
  "simulation_id": "new-uuid-string",
  "session_id": "uuid-string",
  "message": "I've made the bridge longer and added additional supports at the quarter points.",
  "description": "Extended steel truss bridge with additional supports",
  "scene": {
    "meshes": [...],
    "forces": [...],
    "supports": [...]
  },
  "changes_made": [
    "Increased bridge length from 10m to 15m",
    "Added 2 additional support columns",
    "Recalculated stress distribution"
  ],
  "metadata": {
    "generated_at": "2024-01-01T12:05:00Z",
    "processing_time": 1.8,
    "llm_model": "gpt-4",
    "confidence": 0.88
  }
}
```

### **GET /api/chat/history/{session_id}**
Get chat history for a simulation session.

**Response:**
```json
{
  "session_id": "uuid-string",
  "messages": [
    {
      "id": "msg-1",
      "type": "user",
      "content": "steel rod stress on truss bridge",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "id": "msg-2",
      "type": "assistant",
      "content": "I've created a simple truss bridge simulation showing stress distribution.",
      "simulation_id": "sim-1",
      "timestamp": "2024-01-01T12:00:30Z"
    },
    {
      "id": "msg-3",
      "type": "user",
      "content": "make the bridge longer",
      "timestamp": "2024-01-01T12:05:00Z"
    }
  ]
}
```

### **GET /api/examples**
Returns pre-built simulation examples.

**Response:**
```json
{
  "examples": [
    {
      "id": "simple_truss",
      "title": "Simple Truss Bridge",
      "prompt": "steel rod stress on truss bridge",
      "complexity": "simple",
      "preview_image": "base64_or_url"
    },
    {
      "id": "golden_gate",
      "title": "Golden Gate Bridge (Simplified)",
      "prompt": "suspension bridge like golden gate bridge",
      "complexity": "medium",
      "preview_image": "base64_or_url"
    }
  ]
}
```

### **GET /api/materials**
Returns available material properties.

### **GET /api/health**
Health check endpoint.

## 🤖 LLM Integration

### **Service Architecture**
```python
class LLMService:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)
    
    async def generate_simulation(self, prompt: str, complexity: str) -> dict:
        """Generate Three.js simulation JSON from natural language"""
        
    async def validate_output(self, json_data: dict) -> bool:
        """Validate generated JSON structure"""
```

### **Prompt Engineering**
```python
SYSTEM_PROMPTS = {
    "simple": """
    You are a structural engineering assistant that converts natural language 
    descriptions into Three.js-ready JSON for physics simulations.
    
    Focus on:
    - Simple geometric shapes (boxes, cylinders, cones)
    - Clear force vectors
    - Educational visualization
    - Color-coded stress levels
    
    Return valid JSON only.
    """,
    
    "complex": """
    You are an advanced structural engineering assistant that creates detailed
    Three.js simulations for complex structures.
    
    Focus on:
    - Multi-component systems
    - Realistic proportions
    - Multiple load cases
    - Dynamic visualizations
    
    Return valid JSON only.
    """
}
```

## 📊 JSON Format Specifications

### **Simple Structures (MVP)**
```json
{
  "simulation_id": "uuid",
  "description": "User prompt description",
  "complexity": "simple",
  "structure_type": "truss_bridge",
  
  "scene": {
    "meshes": [
      {
        "id": "beam_1",
        "type": "BoxGeometry",
        "position": [x, y, z],
        "scale": [length, width, height],
        "rotation": [rx, ry, rz],
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
          "info": "Description for info panel"
        }
      }
    ],
    
    "supports": [
      {
        "id": "support_1",
        "type": "ConeGeometry",
        "position": [0, -0.2, 0],
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
        "origin": [x, y, z],
        "direction": [dx, dy, dz],
        "length": 2,
        "color": "#FF4444",
        "label": "1000N",
        "label_position": [x, y, z]
      }
    ]
  },
  
  "stress_colors": {
    "low": "#00FF00",
    "medium": "#FFAA00",
    "high": "#FF0000",
    "max_stress": 250
  },
  
  "animation": {
    "deformation": [
      {
        "mesh_id": "beam_1",
        "keyframes": [
          { "time": 0, "scale": [5, 0.1, 0.1] },
          { "time": 1, "scale": [5, 0.09, 0.1] }
        ]
      }
    ]
  },
  
  "camera": {
    "position": [10, 5, 10],
    "look_at": [0, 0, 0]
  },
  
  "lighting": {
    "ambient": { "color": "#404040", "intensity": 0.4 },
    "directional": { 
      "color": "#ffffff", 
      "intensity": 0.8,
      "position": [10, 10, 5]
    }
  }
}
```

### **Complex Structures (Future)**
```json
{
  "simulation_id": "golden_gate_bridge",
  "complexity": "high",
  "total_elements": 1500,
  
  "structure_systems": {
    "suspension_system": {
      "main_cables": [...],
      "suspender_cables": [...],
      "anchorages": [...]
    },
    "tower_system": {
      "towers": [...],
      "foundations": [...]
    },
    "deck_system": {
      "deck_sections": [...],
      "trusses": [...]
    }
  },
  
  "load_cases": {
    "dead_load": {...},
    "live_load": {...},
    "wind_load": {...}
  },
  
  "analysis_results": {
    "modal_analysis": {...},
    "stress_analysis": {...},
    "deflection_analysis": {...}
  }
}
```

## 🔧 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # API endpoints
│   │   ├── chat_routes.py      # Chat endpoints
│   │   └── dependencies.py     # Dependency injection
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py      # LLM integration
│   │   ├── chat_service.py     # Chat conversation service
│   │   ├── session_manager.py  # Session management
│   │   ├── json_validator.py   # JSON validation
│   │   └── simulation_cache.py # Caching layer
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py   # Pydantic request models
│   │   ├── response_models.py  # Pydantic response models
│   │   ├── chat_models.py      # Chat-related models
│   │   └── simulation_models.py # Simulation data models
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   └── session.py          # Database session
│   ├── templates/
│   │   ├── simple_structures.py # Simple structure templates
│   │   └── complex_structures.py # Complex structure templates
│   └── utils/
│       ├── __init__.py
│       ├── json_utils.py       # JSON utilities
│       └── math_utils.py       # Math utilities
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_chat.py
│   ├── test_llm_service.py
│   └── test_json_validation.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🚀 Getting Started

### **Installation**
```bash
cd backend
pip install -r requirements.txt
```

### **Required Dependencies**
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
psycopg2-binary==2.9.9  # For PostgreSQL
```

### **Environment Variables**
```bash
# .env file
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
DATABASE_URL=sqlite:///./simulation.db
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
SESSION_TIMEOUT=3600  # 1 hour in seconds
MAX_CHAT_HISTORY=50   # Maximum messages per session
```

## 💬 Chat & Iteration System

### **How Chat Works**
1. **Initial Simulation**: User creates simulation, gets `session_id`
2. **Chat Context**: All subsequent messages maintain conversation history
3. **Iteration**: User can modify simulation with natural language
4. **Memory**: System remembers previous states and changes made
5. **Continuous Improvement**: Each iteration builds on previous versions

### **Chat Flow**
```
User: "steel rod stress on truss bridge"
  ↓
System: Creates simulation + session_id
  ↓
User: "make the bridge longer"
  ↓
System: Modifies existing simulation, remembers context
  ↓
User: "add wind load analysis"
  ↓
System: Adds wind load to the longer bridge
```

### **Session Management**
- **Session ID**: Unique identifier for conversation
- **Context Window**: Maintains last 10 messages for context
- **Simulation History**: Tracks all simulation versions
- **Expiration**: Sessions expire after 1 hour of inactivity
- **Persistence**: Chat history stored in database

### **Running the Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔮 Future Extensibility

### **Complexity Levels**
- **Simple**: Basic trusses, beams, simple bridges
- **Medium**: Multi-story buildings, complex bridges
- **High**: Skyscrapers, suspension bridges, detailed analysis

### **Structure Types**
- **Bridges**: Truss, beam, suspension, cable-stayed
- **Buildings**: Frame, shear wall, tube, outrigger
- **Towers**: Communication, wind turbine, observation
- **Industrial**: Crane, conveyor, storage tanks

### **Analysis Types**
- **Static**: Basic stress/strain analysis
- **Dynamic**: Modal analysis, time-history
- **Nonlinear**: Large deformation, material nonlinearity
- **Specialized**: Fatigue, buckling, seismic

### **LLM Model Support**
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude-3, Claude-2
- **Local**: Llama, Mistral (future)
- **Specialized**: Engineering-trained models

## 📊 Performance Considerations

### **Caching Strategy**
- **Redis**: Cache common simulations
- **Database**: Store simulation history
- **CDN**: Cache static assets

### **Rate Limiting**
- **Per-user limits**: Prevent abuse
- **LLM quota management**: Cost control
- **Response time monitoring**: Performance tracking

### **Scalability**
- **Horizontal scaling**: Multiple FastAPI instances
- **Load balancing**: Distribute requests
- **Database sharding**: Handle large datasets

## 🧪 Testing Strategy

### **Unit Tests**
- LLM service mocking
- JSON validation
- API endpoint testing

### **Integration Tests**
- End-to-end simulation generation
- Database operations
- Cache functionality

### **Performance Tests**
- Response time benchmarks
- Concurrent request handling
- Memory usage monitoring

## 🔒 Security Considerations

### **API Security**
- **Rate limiting**: Prevent abuse
- **Input validation**: Sanitize user input
- **CORS**: Configure allowed origins

### **LLM Security**
- **Prompt injection**: Prevent malicious prompts
- **Output validation**: Verify generated JSON
- **API key management**: Secure credential storage

---

**Next Steps:**
1. Implement basic FastAPI structure
2. Create LLM service integration
3. Add JSON validation layer
4. Build example endpoints
5. Add caching and optimization 