from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.document import DocumentRequest, DocumentResponse
from app.services.document_request import DocumentRequestService
from app.services.document_processor import DocumentProcessor
from app.core.email import EmailService

router = APIRouter()

@router.post("/cases/{case_id}/document-requests", response_model=DocumentResponse)
async def create_document_request(
    case_id: int,
    request: DocumentRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    email_service: EmailService = Depends(deps.get_email_service)
):
    """Create a new document request for a case."""
    service = DocumentRequestService(db, email_service)
    
    try:
        request_id = await service.create_document_request(
            case_id=case_id,
            requester_id=current_user.id,
            description=request.description
        )
        return {"request_id": request_id, "message": "Document request created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cases/{case_id}/document-requests", response_model=List[DocumentResponse])
async def get_pending_requests(
    case_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    email_service: EmailService = Depends(deps.get_email_service)
):
    """Get all pending document requests for a case."""
    service = DocumentRequestService(db, email_service)
    return await service.get_pending_requests(case_id)

@router.post("/document-requests/{request_id}/submit")
async def submit_document(
    request_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    email_service: EmailService = Depends(deps.get_email_service)
):
    """Submit a document in response to a document request."""
    doc_processor = DocumentProcessor()
    request_service = DocumentRequestService(db, email_service)
    
    try:
        # First find the document request to get the case_id
        existing_request = db.query(Document).filter(
            Document.request_id == request_id
        ).first()
        
        if not existing_request:
            raise HTTPException(
                status_code=404,
                detail=f"Document request {request_id} not found"
            )
        
        # Process the uploaded document
        document = await doc_processor.process_document(
            file,
            existing_request.case_id,
            current_user.id
        )
        
        # Update the document request
        await request_service.process_document_submission(request_id, document)
        
        return {"message": "Document submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))