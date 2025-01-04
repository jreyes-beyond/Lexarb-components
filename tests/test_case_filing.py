import pytest
from datetime import datetime
from src.pipelines.case_filing.services import CaseFilingService
from src.pipelines.case_filing.models import Case

def test_case_number_generation(db_session):
    service = CaseFilingService(db_session)
    case_number = service.generate_case_number()
    
    assert case_number.startswith('LX')
    assert str(datetime.now().year) in case_number

def test_case_creation(db_session):
    service = CaseFilingService(db_session)
    case = service.create_case()
    
    assert case.case_number is not None
    assert case.email is not None
    assert case.status == 'DRAFT'
    assert isinstance(case.created_at, datetime)
    assert isinstance(case.updated_at, datetime)