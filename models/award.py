from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class AwardStatus(enum.Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    PENDING_PARTY_REVIEW = "pending_party_review"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"
    FINAL = "final"

class SectionStatus(enum.Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    NEEDS_REVISION = "needs_revision"
    APPROVED = "approved"

class Award(Base):
    __tablename__ = "awards"

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(Enum(AwardStatus), default=AwardStatus.DRAFT, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    finalized_at = Column(DateTime, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    case = relationship("Case", back_populates="awards")
    sections = relationship("AwardSection", back_populates="award", order_by="AwardSection.order")
    reviews = relationship("AwardReview", back_populates="award")
    created_by = relationship("User", foreign_keys=[created_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])

    def __repr__(self):
        return f"<Award(id={self.id}, case_id={self.case_id}, status={self.status})>"

class AwardSection(Base):
    __tablename__ = "award_sections"

    id = Column(Integer, primary_key=True)
    award_id = Column(Integer, ForeignKey("awards.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    status = Column(Enum(SectionStatus), default=SectionStatus.DRAFT, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    ai_generated = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    award = relationship("Award", back_populates="sections")
    reviews = relationship("SectionReview", back_populates="section")
    documents = relationship("Document", secondary="section_documents")

    def __repr__(self):
        return f"<AwardSection(id={self.id}, title={self.title}, status={self.status})>"

class AwardReview(Base):
    __tablename__ = "award_reviews"

    id = Column(Integer, primary_key=True)
    award_id = Column(Integer, ForeignKey("awards.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # approved, rejected, pending
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    award = relationship("Award", back_populates="reviews")
    reviewer = relationship("User")

    def __repr__(self):
        return f"<AwardReview(id={self.id}, award_id={self.award_id}, status={self.status})>"

class SectionReview(Base):
    __tablename__ = "section_reviews"

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("award_sections.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # approved, rejected, pending
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    section = relationship("AwardSection", back_populates="reviews")
    reviewer = relationship("User")

    def __repr__(self):
        return f"<SectionReview(id={self.id}, section_id={self.section_id}, status={self.status})>"

# Association table for sections and documents
section_documents = Table(
    "section_documents",
    Base.metadata,
    Column("section_id", Integer, ForeignKey("award_sections.id"), primary_key=True),
    Column("document_id", Integer, ForeignKey("documents.id"), primary_key=True)
)