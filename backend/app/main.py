from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .api.chat_routes import router as chat_router
from .config import settings

app = FastAPI(
    title="Physics Simulation API",
    description="Generate Three.js physics simulations from natural language with chat iteration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite frontend
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
        "features": ["simulation_generation", "chat_iteration", "session_management"],
        "docs": "/docs",
        "health": "/api/health"
    } 