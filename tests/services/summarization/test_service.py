"""Tests for document summarization service."""

import pytest
from datetime import datetime
from src.services.summarization import (
    SummarizationService,
    DocumentSummary,
    SummarizationConfig
)
from src.services.llm import MockLLMService

@pytest.fixture
def mock_llm():
    """Create mock LLM service."""
    return MockLLMService()

@pytest.fixture
def service(mock_llm):
    """Create summarization service instance."""
    return SummarizationService(llm_service=mock_llm)

@pytest.fixture
def sample_document():
    """Create sample document for testing."""
    return {
        'id': 'test123',
        'title': 'Sample Arbitration Award',
        'content': '''
        IN THE MATTER OF ARBITRATION BETWEEN
        
        Company A (Claimant)
        v.
        Company B (Respondent)
        
        FINAL AWARD
        
        The Tribunal, having considered the submissions of the parties and the evidence presented,
        hereby renders its final award in this matter.
        
        1. BACKGROUND
        This dispute arises from a contract dated January 1, 2020...
        
        2. FINDINGS
        Based on the evidence presented, the Tribunal finds that...
        ''',
        'created_at': datetime.utcnow(),
        'file_type': 'text/plain'
    }

@pytest.mark.asyncio
async def test_summarize_document(service, sample_document):
    """Test document summarization."""
    summary = await service.summarize_document(sample_document)
    
    assert isinstance(summary, DocumentSummary)
    assert summary.document_id == sample_document['id']
    assert summary.title == sample_document['title']
    assert len(summary.executive_summary) > 0
    assert len(summary.detailed_summary) > 0
    assert summary.metadata.language == 'en'
    assert summary.metadata.word_count > 0
    assert summary.metadata.sentence_count > 0
    assert isinstance(summary.summary_stats, dict)
    assert 'compression_ratio' in summary.summary_stats

@pytest.mark.asyncio
async def test_summarize_with_config(service, sample_document):
    """Test summarization with custom configuration."""
    config = SummarizationConfig(
        max_length=500,
        min_length=50,
        executive_summary_length=100,
        extract_legal_terms=True,
        extract_entities=True
    )
    
    summary = await service.summarize_document(sample_document, config)
    
    assert isinstance(summary, DocumentSummary)
    assert len(summary.executive_summary) > 0
    assert len(summary.executive_summary.split()) <= config.executive_summary_length
    assert len(summary.detailed_summary) > 0
    assert summary.metadata.legal_terms
    assert summary.metadata.named_entities

@pytest.mark.asyncio
async def test_metadata_extraction(service, sample_document):
    """Test metadata extraction functionality."""
    summary = await service.summarize_document(sample_document)
    
    assert summary.metadata.language == 'en'
    assert summary.metadata.word_count > 0
    assert summary.metadata.sentence_count > 0
    assert summary.metadata.paragraph_count > 0
    assert isinstance(summary.metadata.legal_terms, set)
    assert isinstance(summary.metadata.named_entities, dict)
    assert summary.metadata.creation_date == sample_document['created_at']
    assert summary.metadata.file_type == sample_document['file_type']

@pytest.mark.asyncio
async def test_key_points_generation(service, sample_document):
    """Test key points extraction."""
    summary = await service.summarize_document(sample_document)
    
    assert isinstance(summary.key_points, list)
    assert len(summary.key_points) > 0
    assert all(isinstance(point, str) for point in summary.key_points)

@pytest.mark.asyncio
async def test_confidence_scores(service, sample_document):
    """Test confidence score generation."""
    summary = await service.summarize_document(
        sample_document,
        config=SummarizationConfig(include_confidence_scores=True)
    )
    
    assert isinstance(summary.confidence_scores, dict)
    assert 'content_quality' in summary.confidence_scores
    assert 'summary_quality' in summary.confidence_scores
    assert all(0 <= score <= 1 for score in summary.confidence_scores.values())

@pytest.mark.asyncio
async def test_invalid_document(service):
    """Test handling of invalid documents."""
    invalid_doc = {'id': 'invalid1'}
    
    with pytest.raises(ValueError):
        await service.summarize_document(invalid_doc)

@pytest.mark.asyncio
async def test_empty_content(service, sample_document):
    """Test handling of empty content."""
    empty_doc = sample_document.copy()
    empty_doc['content'] = ''
    
    with pytest.raises(ValueError, match='Document content cannot be empty'):
        await service.summarize_document(empty_doc)

@pytest.mark.asyncio
async def test_section_detection(service, sample_document):
    """Test section detection functionality."""
    config = SummarizationConfig(section_detection=True)
    summary = await service.summarize_document(sample_document, config)
    
    assert isinstance(summary.sections, list)
    for section in summary.sections:
        assert section.section_id
        assert section.title
        assert section.content
        assert section.word_count > 0
        assert isinstance(section.importance_score, float)
        assert 0 <= section.importance_score <= 1