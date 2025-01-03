from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.case import Case
from app.core.email import EmailService

class DocumentRequestService:
    def __init__(self, db: Session, email_service: EmailService):
        self.db = db
        self.email_service = email_service

    async def create_document_request(self, case_id: int, requester_id: int, description: str) -> str:
        """Create a new document request and notify relevant parties."""
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Get case details
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if not case:
            raise ValueError(f"Case {case_id} not found")
        
        # Create document placeholder
        document = Document(
            case_id=case_id,
            request_id=request_id,
            requested_by=requester_id,
            requested_at=datetime.utcnow()
        )
        self.db.add(document)
        
        # Send email notification
        await self.email_service.send_document_request(
            case_email=case.email,
            request_id=request_id,
            description=description
        )
        
        self.db.commit()
        return request_id

    async def process_document_submission(self, request_id: str, document: Document) -> None:
        """Process a document submitted in response to a request."""
        # Update existing document record
        existing_doc = self.db.query(Document).filter(
            Document.request_id == request_id
        ).first()
        
        if existing_doc:
            existing_doc.filename = document.filename
            existing_doc.file_type = document.file_type
            existing_doc.file_size = document.file_size
            existing_doc.storage_path = document.storage_path
            existing_doc.metadata = document.metadata
            existing_doc.submitted_at = datetime.utcnow()
            
            self.db.commit()

    async def get_pending_requests(self, case_id: int) -> List[Document]:
        """Get list of pending document requests for a case."""
        return self.db.query(Document).filter(
            Document.case_id == case_id,
            Document.request_id.isnot(None),
            Document.storage_path.is_(None)
        ).all()