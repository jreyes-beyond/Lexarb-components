"""Utility functions for summarization service."""

from typing import List, Dict, Any
import re

def extract_sections(text: str) -> List[Dict[str, str]]:
    """Extract sections from document text.
    
    Args:
        text: Document text
        
    Returns:
        List of sections with titles and content
    """
    sections = []
    current_section = None
    current_content = []
    
    # Pattern for section headers (e.g., "1. BACKGROUND", "I. Introduction")
    section_pattern = re.compile(r'^\s*(?:[0-9]+\.|[A-Z]+\.|[IVXLC]+\.)?\s*([A-Z][A-Z\s]+)\s*$', re.MULTILINE)
    
    lines = text.split('\n')
    for line in lines:
        match = section_pattern.match(line)
        if match:
            # Save previous section if exists
            if current_section:
                sections.append({
                    'title': current_section,
                    'content': '\n'.join(current_content).strip()
                })
            
            current_section = match.group(1).strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Add last section
    if current_section:
        sections.append({
            'title': current_section,
            'content': '\n'.join(current_content).strip()
        })
    
    return sections

def calculate_importance_score(section: Dict[str, str], document_length: int) -> float:
    """Calculate importance score for a section.
    
    Args:
        section: Section dictionary with title and content
        document_length: Total document length in characters
        
    Returns:
        Importance score between 0 and 1
    """
    # Factors affecting importance:
    # 1. Section length relative to document
    # 2. Position in document
    # 3. Presence of key terms
    # 4. Title significance
    
    section_length = len(section['content'])
    length_score = min(section_length / document_length * 3, 1.0)
    
    # Add more scoring factors as needed
    
    return length_score