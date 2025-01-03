"""Tests for the AI ETL pipeline."""

import pytest
from datetime import datetime
from src.pipelines.ai_etl import AIETLPipeline
from src.services.llm import MockLLMService

@pytest.fixture
def mock_llm():
    """Create a mock LLM service."""
    return MockLLMService()

@pytest.fixture
def pipeline(mock_llm):
    """Create a test pipeline instance with mock LLM."""
    return AIETLPipeline(llm_service=mock_llm)

@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    return {
        'id': 'test123',
        'content': 'This is a test document for the arbitration case.',
        'created_at': datetime.utcnow()
    }

@pytest.fixture
def invalid_document():
    """Create an invalid document for testing."""
    return {
        'id': 'invalid123',
        'created_at': datetime.utcnow()
        # Missing content field
    }

@pytest.mark.asyncio
async def test_process_document(pipeline, sample_document):
    """Test processing a single document."""
    processed_doc = await pipeline.process_document(sample_document)
    
    assert processed_doc['processed'] is True
    assert processed_doc['categorized'] is True
    assert 'embeddings' in processed_doc
    assert 'categories' in processed_doc
    assert 'summary' in processed_doc
    assert 'processed_at' in processed_doc
    assert 'pipeline_version' in processed_doc

@pytest.mark.asyncio
async def test_process_invalid_document(pipeline, invalid_document):
    """Test processing an invalid document."""
    with pytest.raises(ValueError) as exc_info:
        await pipeline.process_document(invalid_document)
    
    assert "must contain 'content' field" in str(exc_info.value)
    assert invalid_document.get('processing_attempted') is True
    assert invalid_document.get('processing_failed') is True

@pytest.mark.asyncio
async def test_process_batch(pipeline):
    """Test processing multiple documents."""
    documents = [
        {'id': f'test{i}', 'content': f'Test document {i}'}
        for i in range(3)
    ]
    
    processed_docs = await pipeline.process_batch(documents)
    
    assert len(processed_docs) == 3
    for doc in processed_docs:
        assert doc['processed'] is True
        assert doc['categorized'] is True

@pytest.mark.asyncio
async def test_process_batch_with_failures(pipeline):
    """Test batch processing with some failing documents."""
    documents = [
        {'id': 'test1', 'content': 'Test document 1'},
        {'id': 'test2'},  # Invalid document
        {'id': 'test3', 'content': 'Test document 3'}
    ]
    
    processed_docs = await pipeline.process_batch(documents)
    
    assert len(processed_docs) == 3
    assert processed_docs[0]['processed'] is True
    assert processed_docs[1]['processing_failed'] is True
    assert processed_docs[2]['processed'] is True

@pytest.mark.asyncio
async def test_cleanup(pipeline):
    """Test pipeline cleanup."""
    async with pipeline as p:
        await p.process_document({'id': 'test', 'content': 'Test document'})
    
    # Pipeline should be cleaned up after context manager exit
    # No assertions needed as we're just ensuring no exceptions are raised