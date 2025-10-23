from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    app_name: str = "Bank Statement Parser API"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Veryfi Configuration
    veryfi_client_id: str
    veryfi_client_secret: str
    veryfi_username: str
    veryfi_api_key: str
    
    # File Upload Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = ["application/pdf", "image/jpeg", "image/png"]
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
