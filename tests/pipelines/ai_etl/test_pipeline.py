"""Tests for the AI ETL pipeline."""

import pytest
from datetime import datetime
from src.pipelines.ai_etl import AIETLPipeline

@pytest.fixture
def pipeline():
    """Create a test pipeline instance."""
    return AIETLPipeline()

@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    return {
        'id': 'test123',
        'content': 'This is a test document for the arbitration case.',
        'created_at': datetime.utcnow()
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