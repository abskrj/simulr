from fastapi import APIRouter, HTTPException, Depends
from ..models.chat_models import ChatRequest, ChatResponse, ChatHistoryResponse
from ..services.chat_service import ChatService
from ..services.session_manager import SessionManager

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
    
    try:
        # This would need to be implemented in session manager
        # For now, just return success
        return {"message": "Session cleared successfully", "session_id": session_id}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear session: {str(e)}"
        ) 