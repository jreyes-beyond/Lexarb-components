from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String, nullable=False)
    
    # Metadata fields
    metadata = Column(JSON, nullable=True)
    integrity_verified = Column(Boolean, default=False)
    deepfake_detection_result = Column(JSON, nullable=True)
    compliance_status = Column(JSON, nullable=True)
    
    # Document request tracking
    request_id = Column(String, nullable=True, index=True)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    requested_at = Column(DateTime, nullable=True)
    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # AI processing fields
    category = Column(String, nullable=True)
    ai_summary = Column(String, nullable=True)
    ai_processed = Column(Boolean, default=False)
    
    # Relationships
    case = relationship("Case", back_populates="documents")
    requester = relationship("User", foreign_keys=[requested_by])
    submitter = relationship("User", foreign_keys=[submitted_by])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metadata = kwargs.get("metadata", {})
        self.compliance_status = kwargs.get("compliance_status", {})
        self.deepfake_detection_result = kwargs.get("deepfake_detection_result", {})

    @property
    def is_verified(self) -> bool:
        """Check if document has passed integrity verification."""
        return self.integrity_verified

    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update document metadata."""
        if self.metadata is None:
            self.metadata = {}
        self.metadata.update(metadata)

    def mark_as_processed(self, category: str, summary: Optional[str] = None) -> None:
        """Mark document as processed by AI with category and summary."""
        self.ai_processed = True
        self.category = category
        if summary:
            self.ai_summary = summary