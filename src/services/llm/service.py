"""LLM service implementation."""

from typing import List, Dict, Any, Optional
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
from functools import lru_cache
from .config import LLMConfig, ModelType

class LLMService:
    """Service for handling LLM operations with environment-specific configurations."""

    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize the LLM service.
        
        Args:
            config: Optional configuration settings. If not provided, default config will be used.
        """
        self.config = config or LLMConfig()
        self._init_models()

    def _init_models(self) -> None:
        """Initialize models based on environment configuration."""
        # Set device configuration
        device = 0 if torch.cuda.is_available() and not self.config.is_local else -1

        # Initialize classification pipeline
        self.classifier = pipeline(
            'text-classification',
            model=self.config.CLASSIFICATION_MODEL,
            device=device,
            max_length=self.config.MAX_LENGTH
        )

        # Initialize tokenizer and model for embeddings
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.EMBEDDING_MODEL)
        self.model = AutoModel.from_pretrained(
            self.config.EMBEDDING_MODEL,
            torchscript=self.config.is_production  # Enable TorchScript in production
        )
        
        if device >= 0:
            self.model = self.model.to(device)

        # Enable evaluation mode
        self.model.eval()

    @lru_cache(maxsize=1000)
    def get_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for input text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of embedding values
        """
        # Tokenize input
        inputs = self.tokenizer(text,
                              return_tensors='pt',
                              max_length=self.config.MAX_LENGTH,
                              truncation=True,
                              padding=True)

        # Move to appropriate device if using GPU
        if torch.cuda.is_available() and not self.config.is_local:
            inputs = {k: v.cuda() for k, v in inputs.items()}

        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)

        return embeddings[0].cpu().numpy().tolist()

    async def classify_text(self, text: str, labels: List[str]) -> Dict[str, Any]:
        """Classify text into provided categories.
        
        Args:
            text: Text to classify
            labels: List of possible classification labels
            
        Returns:
            Dictionary containing classification results
        """
        results = self.classifier(text, candidate_labels=labels)
        return {
            'labels': results['labels'],
            'scores': results['scores']
        }

    async def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """Generate a summary of the input text.
        
        Args:
            text: Text to summarize
            max_length: Optional maximum length for summary
            
        Returns:
            Summarized text
        """
        summarizer = pipeline(
            'summarization',
            model=self.config.CLASSIFICATION_MODEL,
            max_length=max_length or self.config.MAX_LENGTH
        )
        
        result = summarizer(text, max_length=max_length or self.config.MAX_LENGTH)
        return result[0]['summary_text']

    def cleanup(self) -> None:
        """Cleanup resources used by the service."""
        # Clear cache
        self.get_embeddings.cache_clear()
        
        # Free up GPU memory if applicable
        if torch.cuda.is_available():
            torch.cuda.empty_cache()