import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from ..config import settings
from ..models.chat_models import ChatMessage, ChatRequest, MessageType
from .session_manager import SessionManager

class ChatService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
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
            if self.openai_client:
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
            else:
                # Fallback when no OpenAI key
                simulation_data, explanation, changes = self._get_fallback_response(request, current_simulation)
            
            # Generate new simulation ID
            new_simulation_id = str(uuid.uuid4())
            
            # Update simulation data
            simulation_data.update({
                "simulation_id": new_simulation_id,
                "session_id": request.session_id,
                "metadata": {
                    "generated_at": datetime.now(),
                    "processing_time": 2.0,
                    "llm_model": "gpt-4-turbo-preview" if self.openai_client else "fallback",
                    "confidence": 0.85 if self.openai_client else 0.5
                }
            })
            
            # Save messages to session
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
            await self.session_manager.store_simulation(new_simulation_id, simulation_data)
            
            return {
                **simulation_data,
                "message": explanation,
                "changes_made": changes
            }
            
        except Exception as e:
            print(f"Chat processing error: {e}")
            return self._get_error_response(request, str(e))
    
    def _build_chat_context(self, history: List[ChatMessage], current_simulation: Optional[Dict], message: str) -> List[Dict[str, str]]:
        """Build context for LLM chat"""
        
        system_prompt = """
        You are a structural engineering assistant helping users iterate on physics simulations.
        
        Context:
        - User has an existing simulation they want to modify
        - Generate updated Three.js JSON based on their request
        - Explain what changes you made
        - List specific modifications in a "changes_made" array
        
        Return format:
        {
            "explanation": "I've made the following changes to your simulation...",
            "changes_made": ["Increased bridge length from 5m to 8m", "Added 2 additional supports"],
            "simulation": { 
                "scene": {
                    "meshes": [...],
                    "supports": [...],
                    "force_arrows": [...]
                },
                "stress_colors": {...},
                "camera": {...},
                "lighting": {...}
            }
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
                "content": f"Current simulation structure: {json.dumps(current_simulation.get('scene', {}), indent=2)}"
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
            # Fallback parsing - try to extract JSON block
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    return (
                        data.get("simulation", {}),
                        data.get("explanation", "Simulation updated successfully."),
                        data.get("changes_made", [])
                    )
                except:
                    pass
            
            # Final fallback
            return {}, "Simulation updated based on your request.", ["Modified structure"]
    
    def _get_fallback_response(self, request: ChatRequest, current_simulation: Optional[Dict]) -> tuple[Dict[str, Any], str, List[str]]:
        """Generate fallback response when LLM is unavailable"""
        
        # Simple modifications based on common requests
        message = request.message.lower()
        
        if current_simulation and "scene" in current_simulation:
            modified_scene = current_simulation["scene"].copy()
            changes = []
            
            # Simple keyword-based modifications
            if "longer" in message or "extend" in message:
                # Make beams longer
                for mesh in modified_scene.get("meshes", []):
                    if mesh.get("type") == "BoxGeometry":
                        mesh["scale"][0] *= 1.5  # Increase length
                        changes.append("Extended structural elements")
            
            elif "support" in message or "column" in message:
                # Add more supports
                support_count = len(modified_scene.get("supports", []))
                modified_scene.setdefault("supports", []).append({
                    "id": f"support_{support_count + 1}",
                    "type": "ConeGeometry",
                    "position": [0, -0.3, 0],
                    "scale": [0.2, 0.3, 0.2],
                    "material": {
                        "type": "MeshStandardMaterial",
                        "color": "#444444"
                    }
                })
                changes.append("Added additional support structure")
            
            elif "force" in message or "load" in message:
                # Modify forces
                for force in modified_scene.get("force_arrows", []):
                    force["length"] *= 1.2
                    force["label"] = f"{int(float(force['label'].replace('N', '')) * 1.2)}N"
                changes.append("Modified load conditions")
            
            return {
                "scene": modified_scene,
                "stress_colors": current_simulation.get("stress_colors", {}),
                "camera": current_simulation.get("camera", {}),
                "lighting": current_simulation.get("lighting", {})
            }, f"I've updated your simulation based on your request: '{request.message}'", changes
        
        # If no current simulation, return basic structure
        return {
            "scene": {
                "meshes": [
                    {
                        "id": "beam_1",
                        "type": "BoxGeometry",
                        "position": [0, 0, 0],
                        "scale": [6, 0.2, 0.2],
                        "material": {
                            "type": "MeshStandardMaterial",
                            "color": "#8C92AC"
                        }
                    }
                ],
                "supports": [],
                "force_arrows": []
            }
        }, "Created a new simulation based on your request.", ["Generated new structure"]
    
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