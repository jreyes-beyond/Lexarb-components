from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class DocumentRequest(BaseModel):
    description: str

class DocumentResponse(BaseModel):
    request_id: str
    case_id: int
    requested_by: Optional[int]
    requested_at: Optional[datetime]
    filename: Optional[str]
    file_type: Optional[str]
    file_size: Optional[int]
    metadata: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True