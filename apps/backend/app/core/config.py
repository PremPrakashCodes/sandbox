from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Sandbox API"
    version: str = "0.1.0"
    debug: bool = True
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database settings
    database_url: str = "postgresql://postgres:password@postgres:5432/sandbox"
    redis_url: str = "redis://redis:6379"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()