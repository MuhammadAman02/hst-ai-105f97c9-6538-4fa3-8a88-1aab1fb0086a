"""Application configuration management."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    app_name: str = "Skin Tone Color Analyzer"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Image processing settings
    max_image_size: int = 5242880  # 5MB
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "webp"]
    temp_dir: str = "temp_images"
    
    # UI settings
    theme: str = "creative"
    show_footer: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure temp directory exists
os.makedirs(settings.temp_dir, exist_ok=True)