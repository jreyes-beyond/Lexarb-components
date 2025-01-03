"""Integration tests for summary repository."""

import pytest
from datetime import datetime
from src.services.summarization.repository import SummaryRepository, Summary
from src.db.session import async_session

@pytest.fixture
def summary_data():
    """Create sample summary data."""
    return {
        'id': 'sum_123',
        'document_id': 'doc_123',
        'title': 'Test Summary',
        'executive_summary': 'Executive summary text',
        'detailed_summary': 'Detailed summary text',
        'key_points': ['Point 1', 'Point 2'],
        'metadata': {
            'language': 'en',
            'word_count': 100,
            'document_type': 'award'
        },
        'model_version': '1.0.0',
        'summary_stats': {
            'compression_ratio': 0.5
        },
        'confidence_scores': {
            'content_quality': 0.9
        }
    }

@pytest.fixture
async def repository():
    """Create repository instance."""
    return SummaryRepository(async_session)

@pytest.mark.asyncio
async def test_create_summary(repository, summary_data):
    """Test creating a new summary."""
    summary = await repository.create_summary(summary_data)
    
    assert summary.id == summary_data['id']
    assert summary.document_id == summary_data['document_id']
    assert summary.title == summary_data['title']
    assert summary.executive_summary == summary_data['executive_summary']
    assert summary.key_points == summary_data['key_points']
    assert summary.metadata == summary_data['metadata']

@pytest.mark.asyncio
async def test_get_summary(repository, summary_data):
    """Test retrieving a summary."""
    await repository.create_summary(summary_data)
    
    summary = await repository.get_summary(summary_data['document_id'])
    
    assert summary is not None
    assert summary.id == summary_data['id']
    assert summary.document_id == summary_data['document_id']

@pytest.mark.asyncio
async def test_update_summary(repository, summary_data):
    """Test updating a summary."""
    await repository.create_summary(summary_data)
    
    updated_data = {
        'executive_summary': 'Updated executive summary',
        'metadata': {'language': 'fr'}
    }
    
    summary = await repository.update_summary(summary_data['document_id'], updated_data)
    
    assert summary is not None
    assert summary.executive_summary == updated_data['executive_summary']
    assert summary.metadata['language'] == updated_data['metadata']['language']

@pytest.mark.asyncio
async def test_delete_summary(repository, summary_data):
    """Test deleting a summary."""
    await repository.create_summary(summary_data)
    
    result = await repository.delete_summary(summary_data['document_id'])
    assert result is True
    
    summary = await repository.get_summary(summary_data['document_id'])
    assert summary is None

@pytest.mark.asyncio
async def test_get_summaries_by_metadata(repository, summary_data):
    """Test retrieving summaries by metadata."""
    await repository.create_summary(summary_data)
    
    summaries = await repository.get_summaries_by_metadata({
        'language': 'en',
        'document_type': 'award'
    })
    
    assert len(summaries) == 1
    assert summaries[0].id == summary_data['id']
    
    # Test with non-matching metadata
    summaries = await repository.get_summaries_by_metadata({
        'language': 'es'
    })
    
    assert len(summaries) == 0