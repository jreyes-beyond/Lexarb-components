from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DocumentAnalysis(Base):
    __tablename__ = 'document_analyses'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    category = Column(String, nullable=False)
    summary = Column(Text)
    analysis_results = Column(JSON)
    created_at = Column(DateTime, nullable=False)
    
    document = relationship('Document', back_populates='analyses')