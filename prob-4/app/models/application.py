"""
Application Model

Represents job applications linking candidates to jobs.
"""

from sqlalchemy import Column, String, Text, JSON, Integer, DateTime, Enum, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.database import Base
from app.utils.enums import ApplicationStatus


class Application(Base):
    """
    Application model linking candidates to jobs.
    
    Attributes:
        id: Unique identifier (UUID)
        candidate_id: Foreign key to candidates table (indexed)
        job_id: Foreign key to jobs table (indexed)
        status: Application status (indexed)
        cover_letter: Optional cover letter text
        resume_data: Parsed resume data as JSON
        score: Matching score (0-100)
        submitted_at: When application was submitted (indexed)
        created_at: Record creation timestamp (UTC)
        updated_at: Record update timestamp (UTC)
        deleted_at: Soft delete timestamp
    
    Constraints:
        - Unique constraint on (candidate_id, job_id) to prevent duplicate applications
    """
    __tablename__ = "applications"
    
    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    # Foreign Keys (indexed for JOIN performance)
    candidate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Status (indexed for filtering)
    status = Column(
        Enum(ApplicationStatus, name="application_status_enum"),
        default=ApplicationStatus.SUBMITTED,
        nullable=False,
        index=True
    )
    
    # Application Details
    cover_letter = Column(Text)
    resume_data = Column(JSON)  # Parsed resume data
    score = Column(Integer)  # Matching score (0-100)
    
    # Timestamps (UTC with timezone)
    submitted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True  # Index for date range queries
    )
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
    candidate = relationship(
        "Candidate",
        back_populates="applications",
        lazy="joined"  # Eager load candidate data
    )
    job = relationship(
        "Job",
        back_populates="applications",
        lazy="joined"  # Eager load job data
    )
    status_history = relationship(
        "StatusHistory",
        back_populates="application",
        cascade="all, delete-orphan",
        order_by="StatusHistory.changed_at",  # Order by timestamp
        lazy="select"
    )
    
    # Table Arguments
    __table_args__ = (
        # Unique constraint: one application per candidate per job
        UniqueConstraint(
            'candidate_id',
            'job_id',
            name='uq_candidate_job_application'
        ),
        # Composite indexes for common queries
        Index('idx_application_candidate', 'candidate_id'),
        Index('idx_application_job', 'job_id'),
        Index('idx_application_status', 'status'),
        Index('idx_application_submitted_at', 'submitted_at'),
        Index('idx_application_deleted', 'deleted_at'),
        # Composite index for filtering by job and status
        Index('idx_application_job_status', 'job_id', 'status'),
        # Composite index for filtering by candidate and status
        Index('idx_application_candidate_status', 'candidate_id', 'status'),
    )
    
    def __repr__(self):
        return f"<Application(id={self.id}, candidate_id={self.candidate_id}, job_id={self.job_id}, status={self.status.value})>"
    
    @property
    def is_deleted(self) -> bool:
        """Check if application is soft deleted."""
        return self.deleted_at is not None
    
    @property
    def is_terminal_status(self) -> bool:
        """Check if application is in a terminal status (HIRED or REJECTED)."""
        return self.status in [ApplicationStatus.HIRED, ApplicationStatus.REJECTED]
    
    def soft_delete(self):
        """Soft delete the application."""
        self.deleted_at = datetime.now(timezone.utc)
