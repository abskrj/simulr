from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    redis_url: str = "redis://localhost:6379"
    database_url: str = "sqlite:///./simulation.db"
    log_level: str = "INFO"
    session_timeout: int = 3600  # 1 hour in seconds
    max_chat_history: int = 50   # Maximum messages per session
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 