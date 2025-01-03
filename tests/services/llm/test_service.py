"""Tests for LLM service."""

import pytest
from src.services.llm import LLMService, LLMConfig, ModelType
from src.services.llm.mock import MockLLMService

@pytest.fixture
def config():
    """Create test configuration."""
    return LLMConfig(
        ENVIRONMENT='local',
        CLASSIFICATION_MODEL=ModelType.DISTILBERT,
        EMBEDDING_MODEL=ModelType.DISTILBERT
    )

@pytest.fixture
def mock_service():
    """Create mock LLM service."""
    return MockLLMService()

@pytest.fixture
def real_service(config):
    """Create real LLM service with test configuration."""
    return LLMService(config)

def test_embeddings_mock(mock_service):
    """Test mock embedding generation."""
    text = "Test document"
    embeddings = mock_service.get_embeddings(text)
    
    assert len(embeddings) == 768
    assert all(isinstance(x, float) for x in embeddings)

@pytest.mark.asyncio
async def test_classification_mock(mock_service):
    """Test mock text classification."""
    text = "Test document"
    labels = ['category1', 'category2']
    
    result = await mock_service.classify_text(text, labels)
    
    assert 'labels' in result
    assert 'scores' in result
    assert len(result['labels']) == len(labels)
    assert len(result['scores']) == len(labels)

@pytest.mark.asyncio
async def test_summarization_mock(mock_service):
    """Test mock text summarization."""
    text = "This is a test document that needs to be summarized."
    max_length = 5
    
    summary = await mock_service.summarize(text, max_length)
    
    assert isinstance(summary, str)
    assert len(summary.split()) <= max_length

@pytest.mark.integration
def test_embeddings_real(real_service):
    """Test real embedding generation."""
    text = "Test document"
    embeddings = real_service.get_embeddings(text)
    
    assert len(embeddings) > 0
    assert all(isinstance(x, float) for x in embeddings)

@pytest.mark.integration
@pytest.mark.asyncio
async def test_classification_real(real_service):
    """Test real text classification."""
    text = "Test document"
    labels = ['category1', 'category2']
    
    result = await real_service.classify_text(text, labels)
    
    assert 'labels' in result
    assert 'scores' in result
    assert len(result['labels']) == len(labels)
    assert all(isinstance(x, float) for x in result['scores'])