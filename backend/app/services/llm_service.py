import json
import uuid
from datetime import datetime
from typing import Dict, Any
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from ..config import settings
from ..models.request_models import SimulationRequest

class LLMService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key) if settings.anthropic_api_key else None
    
    async def generate_simulation(self, request: SimulationRequest) -> Dict[str, Any]:
        """Generate Three.js simulation JSON from natural language"""
        
        system_prompt = self._get_system_prompt(request.complexity)
        user_prompt = self._build_user_prompt(request)
        
        try:
            if self.openai_client:
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
            else:
                # Fallback to template if no API key
                return self._get_fallback_simulation(request)
                
        except Exception as e:
            print(f"LLM generation error: {e}")
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