import pytest
from datetime import datetime
from services.award_pipeline import AwardPipeline
from models.award import Award, AwardStatus, AwardSection

@pytest.fixture
def award_pipeline(db_session, template_engine):
    return AwardPipeline(db_session, template_engine)

@pytest.fixture
def sample_case_data():
    return {
        "case_info": {
            "number": "ARB-2024-001",
            "filed_date": datetime.utcnow(),
            "parties": {
                "claimant": {"name": "Company A"},
                "respondent": {"name": "Company B"}
            },
            "tribunal": [
                {"name": "John Doe", "role": "President"},
                {"name": "Jane Smith", "role": "Co-arbitrator"}
            ]
        }
    }

async def test_generate_draft_award(award_pipeline, sample_case_data, mocker):
    # Mock data aggregation
    mocker.patch.object(
        award_pipeline,
        'aggregate_case_data',
        return_value=sample_case_data
    )

    # Generate draft award
    award = await award_pipeline.generate_draft_award(
        case_id=1,
        created_by_id=1
    )

    assert isinstance(award, Award)
    assert award.status == AwardStatus.DRAFT
    assert len(award.sections) > 0

async def test_submit_for_review(award_pipeline, db_session):
    # Create test award
    award = Award(case_id=1, created_by_id=1, title="Test Award")
    db_session.add(award)
    db_session.commit()

    # Submit for review
    updated_award = await award_pipeline.submit_for_review(
        award_id=award.id,
        reviewer_ids=[1, 2]
    )

    assert updated_award.status == AwardStatus.UNDER_REVIEW
    assert len(updated_award.reviews) == 2

async def test_process_review(award_pipeline, db_session):
    # Create test award and review
    award = Award(case_id=1, created_by_id=1, title="Test Award")
    db_session.add(award)
    db_session.commit()

    # Submit review
    updated_award = await award_pipeline.process_review(
        award_id=award.id,
        reviewer_id=1,
        status="approved",
        comments="Looks good"
    )

    assert updated_award.reviews[0].status == "approved"
    assert updated_award.reviews[0].comments == "Looks good"