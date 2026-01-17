"""
Job Pydantic Schemas

Request and response schemas for job endpoints.
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.utils.enums import JobStatus


class JobBase(BaseModel):
    """Base job schema with common fields."""
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Job title",
        examples=["Senior Backend Engineer"]
    )
    department: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Department name",
        examples=["Engineering"]
    )
    description: str = Field(
        ...,
        min_length=10,
        description="Full job description",
        examples=["We are looking for a Senior Backend Engineer to join our team..."]
    )
    required_skills: List[str] = Field(
        default_factory=list,
        description="List of required skills",
        examples=[["Python", "FastAPI", "PostgreSQL", "Docker"]]
    )
    location: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Job location",
        examples=["San Francisco, CA"]
    )
    employment_type: str = Field(
        ...,
        description="Employment type",
        examples=["Full-time"]
    )
    salary_min: Optional[int] = Field(
        None,
        ge=0,
        description="Minimum salary",
        examples=[100000]
    )
    salary_max: Optional[int] = Field(
        None,
        ge=0,
        description="Maximum salary",
        examples=[150000]
    )
    
    @field_validator('required_skills')
    @classmethod
    def validate_skills(cls, v: List[str]) -> List[str]:
        """Validate required skills list."""
        if v:
            v = [skill.strip() for skill in v if skill.strip()]
            v = list(dict.fromkeys(v))  # Remove duplicates
        return v
    
    @field_validator('salary_max')
    @classmethod
    def validate_salary_range(cls, v: Optional[int], info) -> Optional[int]:
        """Validate that salary_max >= salary_min."""
        if v is not None and 'salary_min' in info.data:
            salary_min = info.data['salary_min']
            if salary_min is not None and v < salary_min:
                raise ValueError('salary_max must be greater than or equal to salary_min')
        return v
    
    @field_validator('employment_type')
    @classmethod
    def validate_employment_type(cls, v: str) -> str:
        """Validate employment type."""
        valid_types = ['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary']
        if v not in valid_types:
            raise ValueError(f'employment_type must be one of: {", ".join(valid_types)}')
        return v


class JobCreate(JobBase):
    """Schema for creating a new job."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Senior Backend Engineer",
                "department": "Engineering",
                "description": "We are looking for a Senior Backend Engineer with 5+ years of experience...",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "location": "San Francisco, CA",
                "employment_type": "Full-time",
                "salary_min": 120000,
                "salary_max": 180000
            }
        }
    )


class JobUpdate(BaseModel):
    """Schema for updating a job."""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    required_skills: Optional[List[str]] = None
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    employment_type: Optional[str] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    status: Optional[JobStatus] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Senior Backend Engineer (Updated)",
                "status": "CLOSED"
            }
        }
    )


class JobResponse(JobBase):
    """Schema for job response."""
    id: UUID = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Job posting status")
    posted_at: datetime = Field(..., description="When the job was posted")
    closed_at: Optional[datetime] = Field(None, description="When the job was closed")
    created_at: datetime = Field(..., description="When the record was created")
    updated_at: datetime = Field(..., description="When the record was last updated")
    deleted_at: Optional[datetime] = Field(None, description="Soft delete timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "title": "Senior Backend Engineer",
                "department": "Engineering",
                "description": "We are looking for a Senior Backend Engineer...",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "location": "San Francisco, CA",
                "employment_type": "Full-time",
                "salary_min": 120000,
                "salary_max": 180000,
                "status": "OPEN",
                "posted_at": "2026-01-17T10:00:00Z",
                "closed_at": None,
                "created_at": "2026-01-17T10:00:00Z",
                "updated_at": "2026-01-17T10:00:00Z",
                "deleted_at": None
            }
        }
    )
