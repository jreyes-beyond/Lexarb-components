from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.award import Award, AwardSection, AwardStatus, SectionStatus, AwardReview, SectionReview
from services.template_engine import TemplateEngine

class AwardPipeline:
    def __init__(self, db: Session, template_engine: TemplateEngine):
        self.db = db
        self.template_engine = template_engine

    async def aggregate_case_data(self, case_id: int) -> Dict:
        """
        Aggregate all relevant case data for award generation.
        """
        # Query case details and related documents
        case = self.db.query(Case).get(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")

        # Aggregate data by document categories
        documents = self.db.query(Document).filter(
            Document.case_id == case_id
        ).order_by(Document.created_at).all()

        aggregated_data = {
            "case_info": {
                "number": case.case_number,
                "filed_date": case.filed_date,
                "parties": self._get_parties(case),
                "tribunal": self._get_tribunal(case)
            },
            "procedural_history": self._aggregate_procedural_history(documents),
            "factual_background": self._aggregate_factual_background(documents),
            "legal_analysis": self._aggregate_legal_analysis(documents),
            "evidence": self._aggregate_evidence(documents),
            "decisions": self._get_decisions(case)
        }

        return aggregated_data

    async def generate_draft_award(self, case_id: int, created_by_id: int) -> Award:
        """
        Generate a draft award using aggregated case data.
        """
        # Aggregate case data
        case_data = await self.aggregate_case_data(case_id)

        # Create new award
        award = Award(
            case_id=case_id,
            title=f"Award - Case {case_data['case_info']['number']}",
            status=AwardStatus.DRAFT,
            created_by_id=created_by_id
        )
        self.db.add(award)
        self.db.flush()  # Get award ID

        # Generate sections
        sections = []
        section_order = [
            ("Introduction", "introduction.j2"),
            ("Procedural History", "procedural_history.j2"),
            ("Factual Background", "factual_background.j2"),
            ("Parties' Positions", "parties_positions.j2"),
            ("Tribunal's Analysis", "tribunal_analysis.j2"),
            ("Decision", "decision.j2")
        ]

        for order, (title, template) in enumerate(section_order):
            content = self.template_engine.render_award_section(
                template,
                case_data.get(title.lower().replace(" ", "_"), {}),
                case_data['case_info']
            )

            section = AwardSection(
                award_id=award.id,
                title=title,
                content=content,
                order=order,
                status=SectionStatus.DRAFT
            )
            sections.append(section)

        self.db.add_all(sections)
        self.db.commit()

        return award

    async def submit_for_review(self, award_id: int, reviewer_ids: List[int]) -> Award:
        """
        Submit award for review to specified reviewers.
        """
        award = self.db.query(Award).get(award_id)
        if not award:
            raise ValueError(f"Award {award_id} not found")

        # Update award status
        award.status = AwardStatus.UNDER_REVIEW

        # Create review requests
        reviews = [
            AwardReview(
                award_id=award_id,
                reviewer_id=reviewer_id,
                status="pending"
            )
            for reviewer_id in reviewer_ids
        ]
        
        self.db.add_all(reviews)
        self.db.commit()

        return award

    async def process_review(
        self,
        award_id: int,
        reviewer_id: int,
        status: str,
        comments: Optional[str] = None,
        section_reviews: Optional[Dict[int, Dict]] = None
    ) -> Award:
        """
        Process a review submission for an award.
        """
        award = self.db.query(Award).get(award_id)
        if not award:
            raise ValueError(f"Award {award_id} not found")

        # Update award review
        review = self.db.query(AwardReview).filter(
            AwardReview.award_id == award_id,
            AwardReview.reviewer_id == reviewer_id
        ).first()
        
        if not review:
            raise ValueError(f"Review not found for award {award_id} and reviewer {reviewer_id}")

        review.status = status
        review.comments = comments
        review.updated_at = datetime.utcnow()

        # Process section-specific reviews if provided
        if section_reviews:
            for section_id, review_data in section_reviews.items():
                section_review = SectionReview(
                    section_id=section_id,
                    reviewer_id=reviewer_id,
                    status=review_data.get('status', 'pending'),
                    comments=review_data.get('comments')
                )
                self.db.add(section_review)

        # Check if all reviews are complete
        all_reviews = self.db.query(AwardReview).filter(
            AwardReview.award_id == award_id
        ).all()

        if all(r.status != 'pending' for r in all_reviews):
            # If any review is rejected, mark for revision
            if any(r.status == 'rejected' for r in all_reviews):
                award.status = AwardStatus.REVISION_REQUESTED
            else:
                award.status = AwardStatus.APPROVED

        self.db.commit()
        return award

    async def finalize_award(self, award_id: int, approved_by_id: int) -> Award:
        """
        Finalize an approved award.
        """
        award = self.db.query(Award).get(award_id)
        if not award:
            raise ValueError(f"Award {award_id} not found")

        if award.status != AwardStatus.APPROVED:
            raise ValueError(f"Award {award_id} must be approved before finalization")

        award.status = AwardStatus.FINAL
        award.approved_by_id = approved_by_id
        award.finalized_at = datetime.utcnow()

        self.db.commit()
        return award

    # Private helper methods
    def _get_parties(self, case) -> Dict:
        """Extract party information from case."""
        pass  # Implementation details

    def _get_tribunal(self, case) -> Dict:
        """Extract tribunal information from case."""
        pass  # Implementation details

    def _aggregate_procedural_history(self, documents: List) -> Dict:
        """Aggregate procedural history from documents."""
        pass  # Implementation details

    def _aggregate_factual_background(self, documents: List) -> Dict:
        """Aggregate factual background from documents."""
        pass  # Implementation details

    def _aggregate_legal_analysis(self, documents: List) -> Dict:
        """Aggregate legal analysis from documents."""
        pass  # Implementation details

    def _aggregate_evidence(self, documents: List) -> Dict:
        """Aggregate evidence from documents."""
        pass  # Implementation details

    def _get_decisions(self, case) -> Dict:
        """Extract decisions from case."""
        pass  # Implementation details