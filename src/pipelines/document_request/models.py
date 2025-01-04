from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'), nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, nullable=False)
    
    case = relationship('Case', back_populates='documents')