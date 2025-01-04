import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.pipelines.case_filing.models import Case
from backend.src.pipelines.document_request.models import Document

client = TestClient(app)

def test_mock_case_flow():
    # 1. Create new case
    case_data = {
        "case_number": "LX-2024-0127",
        "claimant": "TechVision Systems Inc.",
        "respondent": "GlobalNet Solutions Ltd.",
        "dispute_nature": "Breach of Software Development Agreement",
        "amount": 2500000,
        "applicable_law": "English Law",
        "seat": "London, UK",
        "language": "English",
        "arbitrators": 3
    }
    
    response = client.post("/api/cases/", json=case_data)
    assert response.status_code == 201
    case_id = response.json()["id"]
    
    # 2. Upload initial documents
    files = [
        ("files", ("notice.pdf", open("backend/tests/mock_data/notice.pdf", "rb"))),
        ("files", ("agreement.pdf", open("backend/tests/mock_data/agreement.pdf", "rb"))),
        ("files", ("specs.pdf", open("backend/tests/mock_data/specs.pdf", "rb")))
    ]
    response = client.post(f"/api/cases/{case_id}/documents", files=files)
    assert response.status_code == 201
    
    # 3. Test document request
    request_data = {
        "description": "Technical specifications and related documents",
        "deadline": "2024-02-13",
        "requested_documents": [
            "Original technical specifications",
            "Specification revisions",
            "Change request logs",
            "Related communications"
        ]
    }
    response = client.post(f"/api/cases/{case_id}/document-requests", json=request_data)
    assert response.status_code == 201
    
    # 4. Test AI document processing
    document_id = response.json()["documents"][0]["id"]
    response = client.post(f"/api/documents/{document_id}/analyze")
    assert response.status_code == 200
    analysis = response.json()
    
    # Verify AI analysis results
    assert "document_type" in analysis
    assert "relevance" in analysis
    assert "award_sections" in analysis
    
    # 5. Test award section generation
    response = client.get(f"/api/cases/{case_id}/award-sections")
    assert response.status_code == 200
    sections = response.json()
    
    # Verify award sections
    assert "Background of Dispute" in sections
    assert "Technical Requirements" in sections
    assert "Timeline of Events" in sections

def test_document_integrity():
    # Test document metadata analysis
    response = client.post("/api/documents/verify", 
        files={"file": open("backend/tests/mock_data/specs.pdf", "rb")})
    assert response.status_code == 200
    verification = response.json()
    
    # Verify integrity checks
    assert verification["integrity_check"]["digital_signature"] == "Valid"
    assert verification["compliance_status"]["gdpr_compliance"] == True