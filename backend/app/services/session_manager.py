import json
import uuid
import redis
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..config import settings
from ..models.chat_models import ChatMessage, MessageType

class SessionManager:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.redis_url)
            # Test connection
            self.redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            # Fallback to in-memory storage
            self.redis_client = None
            self._memory_store = {}
        
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
        
        # Store in Redis or memory
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
        
        # Get simulation from cache
        simulation_key = f"simulation:{simulation_id}"
        
        if self.redis_client:
            simulation_data = self.redis_client.get(simulation_key)
            if simulation_data:
                return json.loads(simulation_data)
        else:
            # Memory fallback
            return self._memory_store.get(simulation_key)
        
        return None
    
    async def update_current_simulation(self, session_id: str, simulation_id: str):
        """Update current simulation for a session"""
        
        session_data = await self._get_session(session_id)
        if not session_data:
            return
        
        session_data["current_simulation_id"] = simulation_id
        session_data["last_activity"] = datetime.now().isoformat()
        
        await self._store_session(session_id, session_data)
    
    async def store_simulation(self, simulation_id: str, simulation_data: Dict[str, Any]):
        """Store simulation data"""
        
        simulation_key = f"simulation:{simulation_id}"
        
        if self.redis_client:
            self.redis_client.setex(
                simulation_key,
                self.session_timeout,
                json.dumps(simulation_data, default=str)
            )
        else:
            # Memory fallback
            self._memory_store[simulation_key] = simulation_data
    
    async def _get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        
        session_key = f"session:{session_id}"
        
        if self.redis_client:
            session_data = self.redis_client.get(session_key)
            if session_data:
                return json.loads(session_data)
        else:
            # Memory fallback
            return self._memory_store.get(session_key)
        
        return None
    
    async def _store_session(self, session_id: str, session_data: Dict[str, Any]):
        """Store session data"""
        
        session_key = f"session:{session_id}"
        
        if self.redis_client:
            self.redis_client.setex(
                session_key,
                self.session_timeout,
                json.dumps(session_data, default=str)
            )
        else:
            # Memory fallback
            self._memory_store[session_key] = session_data 