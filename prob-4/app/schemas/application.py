"""
Application Pydantic Schemas

Request and response schemas for application endpoints.
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from uuid import UUID

from app.utils.enums import ApplicationStatus
from app.schemas.status_history import StatusHistoryResponse


class ApplicationBase(BaseModel):
    """Base application schema with common fields."""
    cover_letter: Optional[str] = Field(
        None,
        max_length=5000,
        description="Candidate's cover letter",
        examples=["I am excited to apply for this position..."]
    )
    resume_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Parsed resume data as JSON",
        examples=[{"experience_years": 5, "education": "Bachelor's"}]
    )


class ApplicationCreate(ApplicationBase):
    """Schema for creating a new application."""
    candidate_id: UUID = Field(..., description="Candidate ID")
    job_id: UUID = Field(..., description="Job ID")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "candidate_id": "123e4567-e89b-12d3-a456-426614174000",
                "job_id": "123e4567-e89b-12d3-a456-426614174001",
                "cover_letter": "I am excited to apply for the Senior Backend Engineer position...",
                "resume_data": {
                    "experience_years": 5,
                    "education": "Bachelor's in Computer Science",
                    "certifications": ["AWS Certified"]
                }
            }
        }
    )


class ApplicationUpdate(BaseModel):
    """Schema for updating an application."""
    cover_letter: Optional[str] = Field(None, max_length=5000)
    resume_data: Optional[Dict[str, Any]] = None
    score: Optional[int] = Field(None, ge=0, le=100, description="Matching score (0-100)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "score": 85,
                "resume_data": {
                    "experience_years": 5,
                    "skills_matched": ["Python", "FastAPI", "PostgreSQL"]
                }
            }
        }
    )


class StatusChangeRequest(BaseModel):
    """Schema for changing application status."""
    new_status: ApplicationStatus = Field(
        ...,
        description="New status for the application"
    )
    changed_by: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="User ID or email of person making the change",
        examples=["recruiter@example.com"]
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional notes about the status change",
        examples=["Candidate showed strong technical skills in the interview"]
    )
    
    @field_validator('new_status')
    @classmethod
    def validate_status(cls, v: ApplicationStatus) -> ApplicationStatus:
        """Validate that status is a valid ApplicationStatus enum."""
        if not isinstance(v, ApplicationStatus):
            raise ValueError(f'Invalid status. Must be one of: {[s.value for s in ApplicationStatus]}')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "new_status": "SCREENING",
                "changed_by": "recruiter@example.com",
                "notes": "Candidate meets initial requirements, moving to screening phase"
            }
        }
    )


class ApplicationResponse(ApplicationBase):
    """Schema for application response."""
    id: UUID = Field(..., description="Unique application identifier")
    candidate_id: UUID = Field(..., description="Candidate ID")
    job_id: UUID = Field(..., description="Job ID")
    status: ApplicationStatus = Field(..., description="Current application status")
    score: Optional[int] = Field(None, ge=0, le=100, description="Matching score")
    submitted_at: datetime = Field(..., description="When the application was submitted")
    created_at: datetime = Field(..., description="When the record was created")
    updated_at: datetime = Field(..., description="When the record was last updated")
    deleted_at: Optional[datetime] = Field(None, description="Soft delete timestamp")
    
    @computed_field
    @property
    def time_in_current_status(self) -> float:
        """
        Compute time in current status (hours).
        
        Returns:
            Hours since last status update
        """
        now = datetime.now(timezone.utc)
        # Make updated_at timezone-aware if it isn't
        updated = self.updated_at
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        
        delta = now - updated
        return round(delta.total_seconds() / 3600, 2)  # Hours
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "candidate_id": "123e4567-e89b-12d3-a456-426614174000",
                "job_id": "123e4567-e89b-12d3-a456-426614174001",
                "status": "SCREENING",
                "cover_letter": "I am excited to apply for this position...",
                "resume_data": {"experience_years": 5},
                "score": 85,
                "submitted_at": "2026-01-17T10:00:00Z",
                "created_at": "2026-01-17T10:00:00Z",
                "updated_at": "2026-01-17T11:00:00Z",
                "deleted_at": None,
                "time_in_current_status": 1.5
            }
        }
    )


class ApplicationWithHistory(ApplicationResponse):
    """Schema for application response with status history."""
    status_history: List[StatusHistoryResponse] = Field(
        default_factory=list,
        description="Complete status change history"
    )
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "candidate_id": "123e4567-e89b-12d3-a456-426614174000",
                "job_id": "123e4567-e89b-12d3-a456-426614174001",
                "status": "SCREENING",
                "score": 85,
                "submitted_at": "2026-01-17T10:00:00Z",
                "created_at": "2026-01-17T10:00:00Z",
                "updated_at": "2026-01-17T11:00:00Z",
                "deleted_at": None,
                "time_in_current_status": 1.5,
                "status_history": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174003",
                        "application_id": "123e4567-e89b-12d3-a456-426614174002",
                        "from_status": "SUBMITTED",
                        "to_status": "SCREENING",
                        "changed_by": "recruiter@example.com",
                        "notes": "Moving to screening",
                        "changed_at": "2026-01-17T11:00:00Z"
                    }
                ]
            }
        }
    )


class ApplicationStatsResponse(BaseModel):
    """Schema for application statistics response."""
    total_applications: int = Field(..., description="Total number of applications")
    breakdown_by_status: Dict[str, int] = Field(
        ...,
        description="Count of applications by status"
    )
    avg_time_per_stage: Dict[str, float] = Field(
        ...,
        description="Average time spent in each stage (hours)"
    )
    conversion_rates: Dict[str, float] = Field(
        ...,
        description="Conversion rate from one stage to next (%)"
    )
    avg_time_to_hire: Optional[float] = Field(
        None,
        description="Average time from submission to hire (days)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_applications": 150,
                "breakdown_by_status": {
                    "SUBMITTED": 45,
                    "SCREENING": 30,
                    "INTERVIEW_SCHEDULED": 25,
                    "INTERVIEWED": 20,
                    "OFFER_EXTENDED": 15,
                    "HIRED": 10,
                    "REJECTED": 5
                },
                "avg_time_per_stage": {
                    "SUBMITTED": 24.5,
                    "SCREENING": 48.2,
                    "INTERVIEW_SCHEDULED": 72.0,
                    "INTERVIEWED": 36.5,
                    "OFFER_EXTENDED": 120.0
                },
                "conversion_rates": {
                    "SUBMITTED_to_SCREENING": 66.7,
                    "SCREENING_to_INTERVIEW": 83.3,
                    "INTERVIEW_to_OFFER": 75.0,
                    "OFFER_to_HIRED": 66.7
                },
                "avg_time_to_hire": 14.5
            }
        }
    )


class ApplicationListResponse(BaseModel):
    """Schema for paginated application list."""
    items: List[ApplicationResponse]
    metadata: Dict[str, Any]
