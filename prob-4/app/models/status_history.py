"""
StatusHistory Model

Audit trail for application status changes.
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.database import Base


class StatusHistory(Base):
    """
    Status history model for audit trail.
    
    Tracks all status changes for applications with complete audit information.
    This table is append-only and should never be updated or deleted.
    
    Attributes:
        id: Unique identifier (UUID)
        application_id: Foreign key to applications table (indexed)
        from_status: Previous status
        to_status: New status (indexed)
        changed_by: User ID or system identifier who made the change
        notes: Optional notes explaining the status change
        changed_at: When the status change occurred (indexed, UTC)
    """
    __tablename__ = "status_history"
    
    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    # Foreign Key (indexed for JOIN performance)
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Status Transition
    from_status = Column(String(50), nullable=False)
    to_status = Column(String(50), nullable=False, index=True)
    
    # Audit Information
    changed_by = Column(String(255), nullable=False)  # User ID or "system"
    notes = Column(Text)  # Optional explanation for the change
    
    # Timestamp (UTC with timezone)
    changed_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True  # Index for time-based queries
    )
    
    # Relationships
    application = relationship(
        "Application",
        back_populates="status_history",
        lazy="joined"  # Eager load application data
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_status_history_application', 'application_id'),
        Index('idx_status_history_to_status', 'to_status'),
        Index('idx_status_history_changed_at', 'changed_at'),
        # Composite index for filtering by application and date
        Index('idx_status_history_app_date', 'application_id', 'changed_at'),
        # Composite index for status transition queries
        Index('idx_status_history_transition', 'from_status', 'to_status'),
    )
    
    def __repr__(self):
        return f"<StatusHistory(id={self.id}, application_id={self.application_id}, {self.from_status} -> {self.to_status}, changed_at={self.changed_at})>"
    
    @property
    def transition_description(self) -> str:
        """Get human-readable transition description."""
        return f"{self.from_status} → {self.to_status}"
