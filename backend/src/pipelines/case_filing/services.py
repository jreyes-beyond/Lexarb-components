import datetime
from typing import Optional
from .models import Case

class CaseFilingService:
    def __init__(self, session):
        self.session = session
    
    def generate_case_number(self) -> str:
        prefix = 'LX'
        year = datetime.datetime.now().year
        count = self.session.query(Case).count() + 1
        return f'{prefix}-{year}-{count:04d}'
    
    def create_case_email(self, case_number: str) -> str:
        return f'case-{case_number.lower()}@lexarb.com'
    
    def create_case(self) -> Case:
        case_number = self.generate_case_number()
        email = self.create_case_email(case_number)
        
        case = Case(
            case_number=case_number,
            email=email,
            status='DRAFT',
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        
        self.session.add(case)
        self.session.commit()
        
        return case