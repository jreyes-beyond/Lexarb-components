from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Case(Base):
    __tablename__ = 'cases'
    
    id = Column(Integer, primary_key=True)
    case_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    status = Column(Enum('DRAFT', 'ACTIVE', 'CLOSED', name='case_status'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)