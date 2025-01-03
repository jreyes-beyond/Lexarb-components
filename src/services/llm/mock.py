"""Mock LLM service for testing."""

from typing import List, Dict, Any, Optional
from .service import LLMService

class MockLLMService(LLMService):
    """Mock implementation of LLM service for testing purposes."""

    def __init__(self):
        """Initialize mock service without loading models."""
        pass

    def get_embeddings(self, text: str) -> List[float]:
        """Return mock embeddings.
        
        Args:
            text: Input text
            
        Returns:
            Mock embedding values
        """
        return [0.1] * 768  # Standard embedding dimension

    async def classify_text(self, text: str, labels: List[str]) -> Dict[str, Any]:
        """Return mock classification.
        
        Args:
            text: Input text
            labels: Classification labels
            
        Returns:
            Mock classification results
        """
        return {
            'labels': labels,
            'scores': [1.0 / len(labels)] * len(labels)
        }

    async def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """Return mock summary.
        
        Args:
            text: Input text
            max_length: Maximum length for summary
            
        Returns:
            Mock summary
        """
        words = text.split()
        summary_length = min(len(words), max_length or 50)
        return ' '.join(words[:summary_length])

    def cleanup(self) -> None:
        """Mock cleanup method."""
        pass