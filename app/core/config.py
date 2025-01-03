from typing import Dict, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Document storage settings
    DOCUMENT_STORAGE_PATH: str = "/data/documents"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_MIME_TYPES: list = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/jpeg",
        "image/png",
        "text/plain"
    ]

    # Email settings
    SMTP: Dict[str, Any] = {
        "host": "smtp.example.com",
        "port": 587,
        "use_tls": True,
        "username": "notifications@lexarb.com",
        "password": ""
    }

    class Config:
        env_file = ".env"

settings = Settings()