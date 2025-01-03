from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from .base import Base

class CaseStatus(PyEnum):
    DRAFT = "draft"
    FILED = "filed"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Case(Base):
    """...[content from case-model artifact]"""
    # [Rest of the Case model implementation]
