"""Main AI ETL pipeline implementation."""

from typing import List, Dict, Any
from datetime import datetime
from .processor import DocumentProcessor
from .categorizer import DocumentCategorizer

class AIETLPipeline:
    """Main pipeline for processing and categorizing documents using AI."""

    def __init__(self):
        """Initialize the AI ETL pipeline."""
        self.processor = DocumentProcessor()
        self.categorizer = DocumentCategorizer()

    async def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single document through the pipeline.
        
        Args:
            document: Raw document data from the database
            
        Returns:
            Processed and categorized document data
        """
        # Process the document content
        processed_doc = await self.processor.process(document)
        
        # Categorize the document
        categorized_doc = await self.categorizer.categorize(processed_doc)
        
        # Add metadata
        categorized_doc['processed_at'] = datetime.utcnow()
        
        return categorized_doc

    async def process_batch(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of documents through the pipeline.
        
        Args:
            documents: List of raw documents from the database
            
        Returns:
            List of processed and categorized documents
        """
        processed_docs = []
        for doc in documents:
            processed_doc = await self.process_document(doc)
            processed_docs.append(processed_doc)
        
        return processed_docs