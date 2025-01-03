import pytest
from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.middleware.document_validation import DocumentValidationMiddleware

@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(DocumentValidationMiddleware)
    
    @app.post("/test/submit")
    async def test_endpoint(file: UploadFile):
        return {"filename": file.filename}
    
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_valid_file_upload(client):
    # Setup
    mock_file = ("test.pdf", b"test content", "application/pdf")
    
    # Execute
    with patch('magic.from_buffer', return_value='application/pdf'):
        response = client.post(
            "/test/submit",
            files={"file": mock_file}
        )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["filename"] == "test.pdf"

def test_file_size_too_large(client):
    # Setup
    large_content = b"x" * (100 * 1024 * 1024 + 1)  # Slightly over 100MB
    mock_file = ("large.pdf", large_content, "application/pdf")
    
    # Execute
    response = client.post(
        "/test/submit",
        files={"file": mock_file}
    )
    
    # Assert
    assert response.status_code == 413
    assert "exceeds maximum limit" in response.json()["detail"]

def test_invalid_mime_type(client):
    # Setup
    mock_file = ("test.exe", b"test content", "application/x-executable")
    
    # Execute
    with patch('magic.from_buffer', return_value='application/x-executable'):
        response = client.post(
            "/test/submit",
            files={"file": mock_file}
        )
    
    # Assert
    assert response.status_code == 415
    assert "not allowed" in response.json()["detail"]