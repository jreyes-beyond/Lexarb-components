"""Document categorization service."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import spacy
from transformers import pipeline
from .models import Category, Classification, CategoryHierarchy
from .constants import DEFAULT_CATEGORIES, CONFIDENCE_THRESHOLDS

class CategorizationService:
    """Service for document categorization using AI and rule-based approaches."""

    def __init__(self):
        """Initialize the categorization service."""
        # Load spaCy model for text processing
        self.nlp = spacy.load('en_core_web_sm')
        
        # Initialize transformers pipeline for zero-shot classification
        self.classifier = pipeline(
            'zero-shot-classification',
            model='facebook/bart-large-mnli'
        )
        
        # Initialize category hierarchy
        self.categories = self._build_category_hierarchy(DEFAULT_CATEGORIES)

    def _build_category_hierarchy(self, categories_dict: Dict) -> List[CategoryHierarchy]:
        """Build category hierarchy from dictionary configuration.
        
        Args:
            categories_dict: Dictionary containing category configuration
            
        Returns:
            List of CategoryHierarchy objects
        """
        hierarchy = []
        
        for cat_id, cat_data in categories_dict.items():
            category = CategoryHierarchy(
                id=cat_id,
                name=cat_data['name'],
                description=cat_data.get('description', ''),
                keywords=cat_data.get('keywords', [])
            )
            
            if 'subcategories' in cat_data:
                category.subcategories = self._build_category_hierarchy(
                    cat_data['subcategories']
                )
                
            hierarchy.append(category)
            
        return hierarchy

    async def categorize_document(self, document: Dict[str, Any]) -> Classification:
        """Categorize a document using AI and rule-based analysis.
        
        Args:
            document: Document to categorize
            
        Returns:
            Classification result
        """
        # Extract text content
        content = document.get('content', '')
        title = document.get('title', '')
        
        # Process text with spaCy
        doc = self.nlp(content[:1000000])  # Limit for large documents
        
        # Prepare candidate labels for all categories
        all_categories = self._get_all_category_labels()
        
        # Perform zero-shot classification
        classification = self.classifier(
            content[:1000000],  # Text length limit
            candidate_labels=all_categories,
            multi_label=True
        )
        
        # Process results
        categories = []
        confidence_scores = {}
        requires_review = False
        review_reason = None
        
        for label, score in zip(classification['labels'], classification['scores']):
            confidence_scores[label] = score
            
            # Check confidence thresholds
            if score >= CONFIDENCE_THRESHOLDS['primary']:
                categories.append(label)
            elif score >= CONFIDENCE_THRESHOLDS['secondary']:
                categories.append(label)  # Include as secondary category
            elif score >= CONFIDENCE_THRESHOLDS['review']:
                requires_review = True
                review_reason = f'Low confidence score for category: {label}'
        
        # Create classification result
        result = Classification(
            document_id=document['id'],
            categories=categories,
            confidence_scores=confidence_scores,
            classification_date=datetime.utcnow(),
            requires_review=requires_review,
            review_reason=review_reason,
            metadata={
                'text_length': len(content),
                'processed_length': len(doc),
                'title_keywords': [token.text for token in self.nlp(title) if not token.is_stop]
            }
        )
        
        return result

    def _get_all_category_labels(self) -> List[str]:
        """Get all category labels from the hierarchy.
        
        Returns:
            List of category labels
        """
        labels = []
        
        def collect_labels(categories: List[CategoryHierarchy]):
            for category in categories:
                labels.append(category.name)
                if category.subcategories:
                    collect_labels(category.subcategories)
        
        collect_labels(self.categories)
        return labels

    async def batch_categorize(self, documents: List[Dict[str, Any]]) -> List[Classification]:
        """Categorize multiple documents.
        
        Args:
            documents: List of documents to categorize
            
        Returns:
            List of classification results
        """
        results = []
        for doc in documents:
            try:
                classification = await self.categorize_document(doc)
                results.append(classification)
            except Exception as e:
                # Create error classification
                results.append(Classification(
                    document_id=doc['id'],
                    categories=[],
                    confidence_scores={},
                    requires_review=True,
                    review_reason=f'Error during classification: {str(e)}'
                ))
        
        return results