"""
Base class for SQLAlchemy models
"""
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all database models"""
    __name__: str
    
    # Generate __tablename__ automatically from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Common timestamp columns
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

