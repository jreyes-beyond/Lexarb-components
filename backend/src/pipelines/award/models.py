from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Award(Base):
    __tablename__ = 'awards'
    
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'), nullable=False)
    status = Column(Enum('DRAFT', 'REVIEW', 'FINAL', name='award_status'))
    content = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    case = relationship('Case', back_populates='awards')