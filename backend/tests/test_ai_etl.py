import pytest
from datetime import datetime
from backend.src.pipelines.ai_etl import AIETLService

class MockLLMClient:
    def analyze(self, content):
        return 'test_category'
    
    def summarize(self, content):
        return 'test_summary'
    
    def extract_key_points(self, content):
        return ['test point 1', 'test point 2']

def test_document_analysis(db_session):
    llm_client = MockLLMClient()
    service = AIETLService(db_session, llm_client)
    
    analysis = service.analyze_document(
        document_id=1,
        content='Test document content'
    )
    
    assert analysis.document_id == 1
    assert analysis.category == 'test_category'
    assert analysis.summary == 'test_summary'
    assert isinstance(analysis.analysis_results, dict)
    assert isinstance(analysis.created_at, datetime)