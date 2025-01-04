import pytest
from datetime import datetime
from backend.src.pipelines.document_request import DocumentService

def test_document_processing(db_session):
    service = DocumentService(db_session)
    document = service.process_document(
        case_id=1,
        file_data=b'test content',
        filename='test.txt'
    )
    
    assert document.case_id == 1
    assert document.filename == 'test.txt'
    assert document.content_type is not None
    assert isinstance(document.created_at, datetime)