"""API routes for document summarization."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_session
from src.services.summarization import (
    SummarizationService,
    DocumentSummary,
    SummarizationConfig,
    SummaryRepository
)

router = APIRouter(prefix="/api/v1/summarization", tags=["summarization"])

@router.post("/documents/{document_id}/summary", response_model=DocumentSummary)
async def create_document_summary(
    document_id: str,
    config: Optional[SummarizationConfig] = None,
    session: AsyncSession = Depends(get_session)
):
    """Generate summary for a document.
    
    Args:
        document_id: Document identifier
        config: Optional summarization configuration
        session: Database session
        
    Returns:
        Generated document summary
    """
    try:
        # Initialize services
        summary_service = SummarizationService()
        repository = SummaryRepository(session)
        
        # Get document from storage (implement document retrieval)
        document = await get_document(document_id, session)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Generate summary
        summary = await summary_service.summarize_document(document, config)
        
        # Store summary
        await repository.create_summary(summary.dict())
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}/summary", response_model=DocumentSummary)
async def get_document_summary(
    document_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get existing summary for a document.
    
    Args:
        document_id: Document identifier
        session: Database session
        
    Returns:
        Document summary if exists
    """
    repository = SummaryRepository(session)
    summary = await repository.get_summary(document_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    return DocumentSummary(**summary.__dict__)

@router.put("/documents/{document_id}/summary", response_model=DocumentSummary)
async def update_document_summary(
    document_id: str,
    config: SummarizationConfig,
    session: AsyncSession = Depends(get_session)
):
    """Update summary for a document.
    
    Args:
        document_id: Document identifier
        config: New summarization configuration
        session: Database session
        
    Returns:
        Updated document summary
    """
    try:
        # Initialize services
        summary_service = SummarizationService()
        repository = SummaryRepository(session)
        
        # Get document
        document = await get_document(document_id, session)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Generate new summary
        summary = await summary_service.summarize_document(document, config)
        
        # Update in database
        updated_summary = await repository.update_summary(
            document_id,
            summary.dict()
        )
        
        if not updated_summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        
        return DocumentSummary(**updated_summary.__dict__)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}/summary", status_code=204)
async def delete_document_summary(
    document_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Delete summary for a document.
    
    Args:
        document_id: Document identifier
        session: Database session
    """
    repository = SummaryRepository(session)
    result = await repository.delete_summary(document_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Summary not found")

@router.get("/summaries/search", response_model=List[DocumentSummary])
async def search_summaries(
    document_type: Optional[str] = None,
    language: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    """Search summaries by metadata.
    
    Args:
        document_type: Optional document type filter
        language: Optional language filter
        session: Database session
        
    Returns:
        List of matching summaries
    """
    repository = SummaryRepository(session)
    
    # Build metadata filter
    metadata_filter = {}
    if document_type:
        metadata_filter['document_type'] = document_type
    if language:
        metadata_filter['language'] = language
    
    summaries = await repository.get_summaries_by_metadata(metadata_filter)
    return [DocumentSummary(**summary.__dict__) for summary in summaries]

async def get_document(document_id: str, session: AsyncSession) -> dict:
    """Get document from storage.
    
    Args:
        document_id: Document identifier
        session: Database session
        
    Returns:
        Document data if found
    """
    # TODO: Implement document retrieval from storage
    # This is a placeholder implementation
    return {
        'id': document_id,
        'content': 'Document content...',
        'title': 'Document title'
    }