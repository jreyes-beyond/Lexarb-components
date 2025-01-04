"""Tests for document categorization service."""

import pytest
from datetime import datetime
from src.services.categorization.service import CategorizationService
from src.services.categorization.models import Classification

@pytest.fixture
def service():
    """Create categorization service instance."""
    return CategorizationService()

@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    return [
        {
            'id': 'doc1',
            'title': 'Notice of Arbitration',
            'content': 'This is a notice of arbitration to commence proceedings...',
            'created_at': datetime.utcnow()
        },
        {
            'id': 'doc2',
            'title': 'Witness Statement of John Doe',
            'content': 'I, John Doe, hereby declare and state as follows...',
            'created_at': datetime.utcnow()
        },
        {
            'id': 'doc3',
            'title': 'Final Award',
            'content': 'The Tribunal hereby renders its final award...',
            'created_at': datetime.utcnow()
        }
    ]

@pytest.mark.asyncio
async def test_categorize_document(service, sample_documents):
    """Test single document categorization."""
    doc = sample_documents[0]
    result = await service.categorize_document(doc)
    
    assert isinstance(result, Classification)
    assert result.document_id == doc['id']
    assert len(result.categories) > 0
    assert all(isinstance(score, float) for score in result.confidence_scores.values())
    assert isinstance(result.requires_review, bool)

@pytest.mark.asyncio
async def test_batch_categorization(service, sample_documents):
    """Test batch document categorization."""
    results = await service.batch_categorize(sample_documents)
    
    assert len(results) == len(sample_documents)
    assert all(isinstance(result, Classification) for result in results)

@pytest.mark.asyncio
async def test_error_handling(service):
    """Test error handling during categorization."""
    # Document with missing required fields
    invalid_doc = {'id': 'invalid1'}
    
    result = await service.categorize_document(invalid_doc)
    
    assert result.requires_review
    assert result.review_reason is not None
    assert len(result.categories) == 0