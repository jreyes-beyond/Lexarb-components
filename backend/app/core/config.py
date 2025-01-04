from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LexArb"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # MongoDB
    MONGODB_URL: str
    MONGODB_DB: str
    
    # Redis
    REDIS_URL: str
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # LLM
    LLM_MODEL_PATH: str
    ROBERTA_MODEL_PATH: str
    
    # Storage
    STORAGE_PATH: str = "storage"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    def get_mongodb_url(self) -> str:
        return f"{self.MONGODB_URL}/{self.MONGODB_DB}"

settings = Settings()