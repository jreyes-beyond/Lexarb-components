"""Configuration settings for the AI ETL pipeline."""

from typing import Dict, Any
from pydantic import BaseSettings

class AIPipelineSettings(BaseSettings):
    """Settings for the AI ETL pipeline."""
    
    # Model settings
    ROBERTA_MODEL: str = 'roberta-base'
    LLAMA_MODEL: str = 'llama-3.1-8b'
    
    # Processing settings
    MAX_BATCH_SIZE: int = 10
    MAX_DOCUMENT_LENGTH: int = 512
    CATEGORY_THRESHOLD: float = 0.5
    
    # Database settings
    RAW_DB_COLLECTION: str = 'raw_documents'
    PREP_DB_COLLECTION: str = 'processed_documents'
    
    class Config:
        env_prefix = 'AI_PIPELINE_'