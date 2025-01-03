import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from app.services.document_request import DocumentRequestService
from app.models.document import Document
from app.models.case import Case

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_email_service():
    return Mock()

@pytest.fixture
def document_request_service(mock_db, mock_email_service):
    return DocumentRequestService(mock_db, mock_email_service)

def test_create_document_request(document_request_service, mock_db, mock_email_service):
    # Setup
    case_id = 1
    requester_id = 2
    description = "Please provide contract document"
    
    mock_case = Case(id=case_id, email="case@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_case
    
    # Execute
    request_id = document_request_service.create_document_request(
        case_id=case_id,
        requester_id=requester_id,
        description=description
    )
    
    # Assert
    assert request_id is not None
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_email_service.send_document_request.assert_called_once_with(
        case_email="case@example.com",
        request_id=request_id,
        description=description
    )

def test_process_document_submission(document_request_service, mock_db):
    # Setup
    request_id = "test-request-id"
    mock_existing_doc = Document(
        case_id=1,
        request_id=request_id,
        requested_by=2,
        requested_at=datetime.utcnow()
    )
    mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_doc
    
    new_document = Document(
        filename="test.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/path/to/file",
        metadata={"key": "value"}
    )
    
    # Execute
    document_request_service.process_document_submission(request_id, new_document)
    
    # Assert
    assert mock_existing_doc.filename == "test.pdf"
    assert mock_existing_doc.file_type == "application/pdf"
    assert mock_existing_doc.storage_path == "/path/to/file"
    assert mock_existing_doc.metadata == {"key": "value"}
    mock_db.commit.assert_called_once()

def test_get_pending_requests(document_request_service, mock_db):
    # Setup
    case_id = 1
    mock_documents = [
        Document(case_id=case_id, request_id="req1"),
        Document(case_id=case_id, request_id="req2")
    ]
    mock_db.query.return_value.filter.return_value.all.return_value = mock_documents
    
    # Execute
    result = document_request_service.get_pending_requests(case_id)
    
    # Assert
    assert len(result) == 2
    assert all(doc.case_id == case_id for doc in result)