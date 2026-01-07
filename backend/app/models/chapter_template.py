"""
Chapter Template model
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class ChapterTemplate(Base):
    """Chapter Template model for storing reusable chapter templates"""
    __tablename__ = "chapter_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    preview_image_url = Column(String(500), nullable=True)
    template_data = Column(JSON, nullable=False)  # Stores the template structure
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    is_public = Column(Boolean, default=False, nullable=False, index=True)
    usage_count = Column(Integer, default=0, nullable=False)  # Track how many times template is used
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="chapter_templates")
    
    def __repr__(self):
        return f"<ChapterTemplate {self.name} (created_by={self.created_by}, public={self.is_public})>"

