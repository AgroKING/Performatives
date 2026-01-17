"""
Job Model

Represents job postings in the ATS system.
"""

from sqlalchemy import Column, String, Text, JSON, Integer, DateTime, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.database import Base
from app.utils.enums import JobStatus


class Job(Base):
    """
    Job posting model.
    
    Attributes:
        id: Unique identifier (UUID)
        title: Job title
        department: Department name
        description: Full job description
        required_skills: JSON array of required skills
        location: Job location
        employment_type: Full-time, Part-time, Contract, etc.
        salary_min: Minimum salary
        salary_max: Maximum salary
        status: Job posting status (DRAFT, OPEN, CLOSED, CANCELLED)
        posted_at: When job was posted
        closed_at: When job was closed
        created_at: Record creation timestamp (UTC)
        updated_at: Record update timestamp (UTC)
        deleted_at: Soft delete timestamp
    """
    __tablename__ = "jobs"
    
    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    # Core Fields
    title = Column(String(255), nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    required_skills = Column(JSON, default=list)  # ["Python", "FastAPI"]
    location = Column(String(255), nullable=False)
    employment_type = Column(String(50), nullable=False)  # Full-time, Part-time, Contract
    
    # Salary Range
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    
    # Status
    status = Column(
        Enum(JobStatus, name="job_status_enum"),
        default=JobStatus.OPEN,
        nullable=False,
        index=True  # Index for filtering by status
    )
    
    # Timestamps (UTC with timezone)
    posted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    closed_at = Column(DateTime(timezone=True), nullable=True)
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
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_job_title', 'title'),
        Index('idx_job_department', 'department'),
        Index('idx_job_status', 'status'),
        Index('idx_job_deleted', 'deleted_at'),
        Index('idx_job_posted_at', 'posted_at'),  # For date range queries
    )
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', department='{self.department}', status={self.status.value})>"
    
    @property
    def is_deleted(self) -> bool:
        """Check if job is soft deleted."""
        return self.deleted_at is not None
    
    @property
    def is_open(self) -> bool:
        """Check if job is currently open for applications."""
        return self.status == JobStatus.OPEN and not self.is_deleted
    
    def soft_delete(self):
        """Soft delete the job."""
        self.deleted_at = datetime.now(timezone.utc)
        self.status = JobStatus.CLOSED
