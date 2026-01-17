"""
StatusHistory Pydantic Schemas

Response schemas for status history (audit trail).
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class StatusHistoryResponse(BaseModel):
    """Schema for status history response."""
    id: UUID = Field(..., description="Unique status history identifier")
    application_id: UUID = Field(..., description="Application ID")
    from_status: str = Field(..., description="Previous status")
    to_status: str = Field(..., description="New status")
    changed_by: str = Field(..., description="User who made the change")
    notes: Optional[str] = Field(None, description="Notes about the status change")
    changed_at: datetime = Field(..., description="When the status was changed")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174003",
                "application_id": "123e4567-e89b-12d3-a456-426614174002",
                "from_status": "SUBMITTED",
                "to_status": "SCREENING",
                "changed_by": "recruiter@example.com",
                "notes": "Candidate meets initial requirements, moving to screening",
                "changed_at": "2026-01-17T11:00:00Z"
            }
        }
    )
