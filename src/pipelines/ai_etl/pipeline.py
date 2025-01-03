"""Main AI ETL pipeline implementation."""

from typing import List, Dict, Any
from datetime import datetime
from src.services.llm import LLMService
from .processor import DocumentProcessor
from .categorizer import DocumentCategorizer

class AIETLPipeline:
    """Main pipeline for processing and categorizing documents using AI."""

    def __init__(self, llm_service: LLMService = None):
        """Initialize the AI ETL pipeline.
        
        Args:
            llm_service: Optional LLM service instance to share across components
        """
        self.llm = llm_service or LLMService()
        self.processor = DocumentProcessor(self.llm)
        self.categorizer = DocumentCategorizer(self.llm)

    async def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single document through the pipeline.
        
        Args:
            document: Raw document data from the database
            
        Returns:
            Processed and categorized document data
            
        Raises:
            ValueError: If document is missing required fields
            RuntimeError: If processing or categorization fails
        """
        try:
            # Validate document
            if not document.get('content'):
                raise ValueError("Document must contain 'content' field")

            # Process the document content
            processed_doc = await self.processor.process(document)
            
            # Categorize the document
            categorized_doc = await self.categorizer.categorize(processed_doc)
            
            # Add metadata
            categorized_doc['processed_at'] = datetime.utcnow()
            categorized_doc['pipeline_version'] = '1.0.0'
            
            return categorized_doc
            
        except (ValueError, RuntimeError) as e:
            # Add error information to document
            document['error'] = str(e)
            document['processed_at'] = datetime.utcnow()
            document['processing_failed'] = True
            raise
        
        finally:
            # Ensure we track processing attempt
            document['processing_attempted'] = True

    async def process_batch(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of documents through the pipeline.
        
        Args:
            documents: List of raw documents from the database
            
        Returns:
            List of processed and categorized documents
        """
        processed_docs = []
        errors = []

        for doc in documents:
            try:
                processed_doc = await self.process_document(doc)
                processed_docs.append(processed_doc)
            except Exception as e:
                errors.append({
                    'document_id': doc.get('id'),
                    'error': str(e)
                })
                processed_docs.append(doc)  # Include failed document in results
        
        # If all documents failed, raise exception
        if len(errors) == len(documents):
            raise RuntimeError(f"Batch processing failed for all documents: {errors}")
        
        return processed_docs

    def cleanup(self) -> None:
        """Cleanup resources used by the pipeline."""
        self.processor.cleanup()
        self.categorizer.cleanup()
        self.llm.cleanup()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.cleanup()