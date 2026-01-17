"""
Candidate Model

Represents job candidates in the ATS system.
"""

from sqlalchemy import Column, String, JSON, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.database import Base


class Candidate(Base):
    """
    Candidate model for storing applicant information.
    
    Attributes:
        id: Unique identifier (UUID)
        email: Unique email address (indexed)
        full_name: Candidate's full name
        phone: Contact phone number
        resume_url: URL to resume file
        skills: JSON array of skills
        created_at: Timestamp when record was created (UTC)
        updated_at: Timestamp when record was last updated (UTC)
        deleted_at: Soft delete timestamp (NULL if active)
    """
    __tablename__ = "candidates"
    
    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    # Core Fields
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True  # Index for fast email lookups
    )
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    resume_url = Column(String(500))
    skills = Column(JSON, default=list)  # ["Python", "FastAPI", "SQL"]
    
    # Timestamps (UTC with timezone)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    # Soft Delete
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    applications = relationship(
        "Application",
        back_populates="candidate",
        cascade="all, delete-orphan",
        lazy="select"  # Load on access
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_candidate_email', 'email'),  # Explicit email index
        Index('idx_candidate_deleted', 'deleted_at'),  # For filtering active records
    )
    
    def __repr__(self):
        return f"<Candidate(id={self.id}, name='{self.full_name}', email='{self.email}')>"
    
    @property
    def is_deleted(self) -> bool:
        """Check if candidate is soft deleted."""
        return self.deleted_at is not None
    
    def soft_delete(self):
        """Soft delete the candidate."""
        self.deleted_at = datetime.now(timezone.utc)
