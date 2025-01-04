import datetime
from typing import Optional
from .models import Award

class AwardService:
    def __init__(self, session):
        self.session = session
    
    def create_draft_award(self, case_id: int, content: str) -> Award:
        award = Award(
            case_id=case_id,
            status='DRAFT',
            content=content,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        
        self.session.add(award)
        self.session.commit()
        
        return award
    
    def update_award(self, award_id: int, content: str, status: Optional[str] = None) -> Award:
        award = self.session.query(Award).get(award_id)
        
        if content is not None:
            award.content = content
        
        if status is not None:
            award.status = status
        
        award.updated_at = datetime.datetime.now()
        self.session.commit()
        
        return award