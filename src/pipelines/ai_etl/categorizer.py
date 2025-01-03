"""Document categorizer for the AI ETL pipeline."""

from typing import Dict, Any
from transformers import pipeline

class DocumentCategorizer:
    """Categorizes documents using LLaMA for content analysis."""

    def __init__(self):
        """Initialize the document categorizer."""
        self.llm = pipeline('text-classification', model='llama-3.1-8b')
        
        # Define standard award sections/categories
        self.categories = [
            'background',
            'procedural_history',
            'jurisdiction',
            'applicable_law',
            'merits',
            'damages',
            'costs',
            'decision'
        ]

    async def categorize(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Categorize a document using LLaMA for content analysis.
        
        Args:
            document: Processed document data
            
        Returns:
            Categorized document with summary and section assignments
        """
        content = document.get('content', '')
        
        # Generate document summary
        summary = self.llm(content, max_length=200)
        
        # Determine document categories
        category_scores = self.llm(
            content,
            candidate_labels=self.categories,
            multi_label=True
        )
        
        # Add categorization data to document
        document['summary'] = summary
        document['categories'] = [
            cat for cat, score in zip(category_scores['labels'], category_scores['scores'])
            if score > 0.5  # Threshold for category assignment
        ]
        document['categorized'] = True
        
        return document