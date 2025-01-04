import pytest
from datetime import datetime
from src.pipelines.ai_etl.services import AIETLService

class MockLLMClient:
    def analyze(self, content):
        return 'test_category'
    
    def summarize(self, content):
        return 'test_summary'

def test_document_analysis(db_session):
    llm_client = MockLLMClient()
    service = AIETLService(db_session, llm_client)
    
    analysis = service.analyze_document(
        document_id=1,
        content='Test document content'
    )
    
    assert analysis.document_id == 1
    assert analysis.category is not None
    assert analysis.summary is not None
    assert isinstance(analysis.created_at, datetime)