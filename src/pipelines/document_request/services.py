import datetime
from typing import List, Dict
from .models import Document

class DocumentService:
    def __init__(self, session):
        self.session = session
    
    def process_document(self, case_id: int, file_data: bytes, filename: str) -> Document:
        metadata = self.extract_metadata(file_data)
        
        document = Document(
            case_id=case_id,
            filename=filename,
            content_type=self.get_content_type(filename),
            metadata=metadata,
            created_at=datetime.datetime.now()
        )
        
        self.session.add(document)
        self.session.commit()
        
        return document
    
    def extract_metadata(self, file_data: bytes) -> Dict:
        # Implement metadata extraction
        return {}
    
    def get_content_type(self, filename: str) -> str:
        # Implement content type detection
        return 'application/octet-stream'