import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app
from app.api import deps
from app.models.document import Document
from app.models.user import User

@pytest.fixture
def mock_current_user():
    return User(id=1, email="test@example.com")

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_email_service():
    return Mock()

@pytest.fixture
def client(mock_current_user, mock_db, mock_email_service):
    def override_get_current_user():
        return mock_current_user
    
    def override_get_db():
        return mock_db
    
    def override_get_email_service():
        return mock_email_service
    
    app.dependency_overrides[deps.get_current_user] = override_get_current_user
    app.dependency_overrides[deps.get_db] = override_get_db
    app.dependency_overrides[deps.get_email_service] = override_get_email_service
    
    return TestClient(app)

def test_create_document_request(client, mock_db, mock_email_service):
    # Setup
    case_id = 1
    request_data = {"description": "Please provide contract document"}
    
    # Execute
    response = client.post(f"/api/v1/cases/{case_id}/document-requests", json=request_data)
    
    # Assert
    assert response.status_code == 200
    assert "request_id" in response.json()
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_email_service.send_document_request.assert_called_once()

def test_get_pending_requests(client, mock_db):
    # Setup
    case_id = 1
    mock_documents = [
        Document(
            case_id=case_id,
            request_id="req1",
            requested_by=1,
            filename="doc1.pdf"
        ),
        Document(
            case_id=case_id,
            request_id="req2",
            requested_by=1,
            filename="doc2.pdf"
        )
    ]
    mock_db.query.return_value.filter.return_value.all.return_value = mock_documents
    
    # Execute
    response = client.get(f"/api/v1/cases/{case_id}/document-requests")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["request_id"] == "req1"
    assert data[1]["request_id"] == "req2"

def test_submit_document(client, mock_db):
    # Setup
    request_id = "test-request-id"
    mock_file = ("test.pdf", b"test content", "application/pdf")
    
    mock_document = Document(
        case_id=1,
        request_id=request_id,
        requested_by=1
    )
    mock_db.query.return_value.filter.return_value.first.return_value = mock_document
    
    # Execute
    with patch('app.services.document_processor.DocumentProcessor.process_document') as mock_process:
        mock_process.return_value = mock_document
        response = client.post(
            f"/api/v1/document-requests/{request_id}/submit",
            files={"file": mock_file}
        )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Document submitted successfully"

def test_submit_document_not_found(client, mock_db):
    # Setup
    request_id = "non-existent-id"
    mock_file = ("test.pdf", b"test content", "application/pdf")
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Execute
    response = client.post(
        f"/api/v1/document-requests/{request_id}/submit",
        files={"file": mock_file}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()