#!/usr/bin/env python3
"""
FastAPI Server Runner

Usage:
    python run.py

Environment Variables:
    OPENAI_API_KEY=your_openai_api_key_here
    ANTHROPIC_API_KEY=your_anthropic_api_key_here
    DATABASE_URL=sqlite:///./simulation.db
    REDIS_URL=redis://localhost:6379
    LOG_LEVEL=INFO
    SESSION_TIMEOUT=3600
    MAX_CHAT_HISTORY=50
"""

import uvicorn
import os

if __name__ == "__main__":
    # Check for environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. LLM features will use fallback responses.")
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 