from fastapi import APIRouter, HTTPException, Depends
from ..models.request_models import SimulationRequest, ExampleRequest
from ..models.response_models import SimulationResponse, ExamplesResponse
from ..services.llm_service import LLMService
from ..services.session_manager import SessionManager
from ..templates.simple_structures import get_example_structures

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
        
        # Store the simulation
        await session_manager.store_simulation(simulation_data["simulation_id"], simulation_data)
        
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
    return {
        "status": "healthy", 
        "service": "physics-simulation-api",
        "version": "1.0.0"
    } 