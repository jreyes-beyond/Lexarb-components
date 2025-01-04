import pytest
from datetime import datetime
from src.pipelines.award.services import AwardService

def test_award_creation(db_session):
    service = AwardService(db_session)
    award = service.create_draft_award(
        case_id=1,
        content='Test award content'
    )
    
    assert award.case_id == 1
    assert award.status == 'DRAFT'
    assert award.content == 'Test award content'
    assert isinstance(award.created_at, datetime)
    assert isinstance(award.updated_at, datetime)

def test_award_update(db_session):
    service = AwardService(db_session)
    award = service.create_draft_award(
        case_id=1,
        content='Initial content'
    )
    
    updated_award = service.update_award(
        award_id=award.id,
        content='Updated content',
        status='REVIEW'
    )
    
    assert updated_award.content == 'Updated content'
    assert updated_award.status == 'REVIEW'