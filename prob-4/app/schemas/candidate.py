"""
Candidate Pydantic Schemas

Request and response schemas for candidate endpoints.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class CandidateBase(BaseModel):
    """Base candidate schema with common fields."""
    email: EmailStr = Field(
        ...,
        description="Candidate's email address",
        examples=["john.doe@example.com"]
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Candidate's full name",
        examples=["John Doe"]
    )
    phone: Optional[str] = Field(
        None,
        pattern=r'^\+?1?\d{9,15}$',
        description="Phone number in E.164 format",
        examples=["+1234567890"]
    )
    resume_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to candidate's resume",
        examples=["https://example.com/resumes/john-doe.pdf"]
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of candidate's skills",
        examples=[["Python", "FastAPI", "PostgreSQL", "Docker"]]
    )
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v: List[str]) -> List[str]:
        """Validate skills list."""
        if v:
            # Remove duplicates and empty strings
            v = [skill.strip() for skill in v if skill.strip()]
            v = list(dict.fromkeys(v))  # Remove duplicates while preserving order
        return v
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        """Validate full name."""
        v = v.strip()
        if not v:
            raise ValueError('Full name cannot be empty')
        return v


class CandidateCreate(CandidateBase):
    """Schema for creating a new candidate."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "alice.smith@example.com",
                "full_name": "Alice Smith",
                "phone": "+1234567890",
                "resume_url": "https://example.com/resumes/alice-smith.pdf",
                "skills": ["Python", "FastAPI", "React", "PostgreSQL"]
            }
        }
    )


class CandidateUpdate(BaseModel):
    """Schema for updating a candidate."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    resume_url: Optional[str] = Field(None, max_length=500)
    skills: Optional[List[str]] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Alice M. Smith",
                "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker"]
            }
        }
    )


class CandidateResponse(CandidateBase):
    """Schema for candidate response."""
    id: UUID = Field(..., description="Unique candidate identifier")
    created_at: datetime = Field(..., description="When the candidate was created")
    updated_at: datetime = Field(..., description="When the candidate was last updated")
    deleted_at: Optional[datetime] = Field(None, description="Soft delete timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "alice.smith@example.com",
                "full_name": "Alice Smith",
                "phone": "+1234567890",
                "resume_url": "https://example.com/resumes/alice-smith.pdf",
                "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
                "created_at": "2026-01-17T10:00:00Z",
                "updated_at": "2026-01-17T10:00:00Z",
                "deleted_at": None
            }
        }
    )
