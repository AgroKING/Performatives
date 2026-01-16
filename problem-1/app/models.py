"""
Data Models for Job Matching System
FastAPI + Pydantic implementation

This module defines all input and output schemas for the job matching API.
All field names match the Input Specifications exactly.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# INPUT SCHEMAS
# ============================================================================

class Education(BaseModel):
    """
    Education qualification model.
    
    Attributes:
        degree: Type of degree (e.g., "Bachelor's", "Master's", "PhD")
        field: Field of study (e.g., "Computer Science", "Engineering")
        institution: Name of educational institution
        graduation_year: Year of graduation
    """
    degree: str = Field(..., description="Type of degree obtained")
    field: str = Field(..., description="Field of study")
    institution: str = Field(..., description="Name of institution")
    graduation_year: int = Field(..., description="Year of graduation", ge=1950, le=2030)


class Candidate(BaseModel):
    """
    Candidate profile model.
    
    Attributes:
        name: Full name of the candidate
        skills: List of technical/professional skills
        experience_years: Total years of professional experience
        education: List of educational qualifications
        preferred_locations: List of preferred work locations
        preferred_roles: List of preferred job titles/roles
        expected_salary: Expected salary (annual)
    """
    name: str = Field(..., description="Candidate's full name")
    skills: List[str] = Field(..., description="List of skills", min_length=1)
    experience_years: float = Field(..., description="Years of experience", ge=0)
    education: List[Education] = Field(..., description="Educational background")
    preferred_locations: List[str] = Field(..., description="Preferred work locations")
    preferred_roles: Optional[List[str]] = Field(default=None, description="Preferred job titles/roles")
    expected_salary: Optional[float] = Field(None, description="Expected annual salary", ge=0)


class Job(BaseModel):
    """
    Job posting model.
    
    Attributes:
        job_id: Unique identifier for the job
        title: Job title
        company: Company name
        required_skills: List of required skills (can be empty)
        experience_required: Experience requirement as string (e.g., "0-2 years", "3-5 years")
        location: Job location
        salary_range: Salary range as [min, max]
        education_required: Required education level
    """
    job_id: str = Field(..., description="Unique job identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    required_skills: List[str] = Field(default_factory=list, description="Required skills (can be empty)")
    experience_required: str = Field(..., description="Experience requirement (e.g., '0-2 years', '3-5 years')")
    location: str = Field(..., description="Job location")
    salary_range: List[float] = Field(..., description="Salary range [min, max]", min_length=2, max_length=2)
    education_required: str = Field(..., description="Required education level")
    
    @field_validator('salary_range')
    @classmethod
    def validate_salary_range(cls, v: List[float]) -> List[float]:
        """
        Validate salary range has exactly 2 values and min < max.
        
        Args:
            v: Salary range list
            
        Returns:
            Validated salary range
            
        Raises:
            ValueError: If validation fails
        """
        if len(v) != 2:
            raise ValueError('salary_range must have exactly 2 values [min, max]')
        
        min_salary, max_salary = v[0], v[1]
        
        if min_salary < 0 or max_salary < 0:
            raise ValueError('salary_range values must be non-negative')
        
        if min_salary >= max_salary:
            raise ValueError(f'salary_range min ({min_salary}) must be less than max ({max_salary})')
        
        return v


# ============================================================================
# OUTPUT SCHEMAS
# ============================================================================

class MatchBreakdown(BaseModel):
    """
    Detailed breakdown of match scoring.
    
    Attributes:
        skill_score: Skill match score (0-40)
        location_score: Location match score (0-20)
        salary_score: Salary match score (0-15)
        experience_score: Experience match score (0-15)
        role_score: Role match score (0-10)
        total_score: Total match score (0-100)
        missing_skills: List of required skills the candidate doesn't have
    """
    skill_score: float = Field(..., description="Skill match score", ge=0, le=40)
    location_score: float = Field(..., description="Location match score", ge=0, le=20)
    salary_score: float = Field(..., description="Salary match score", ge=0, le=15)
    experience_score: float = Field(..., description="Experience match score", ge=0, le=15)
    role_score: float = Field(..., description="Role match score", ge=0, le=10)
    total_score: float = Field(..., description="Total match score", ge=0, le=100)
    missing_skills: List[str] = Field(..., description="Skills candidate is missing")


class JobMatch(BaseModel):
    """
    Individual job match result.
    
    Attributes:
        job_id: Unique identifier for the job
        title: Job title
        company: Company name
        total_score: Overall match score (0-100)
        breakdown: Detailed match breakdown
    """
    job_id: str = Field(..., description="Unique job identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    total_score: float = Field(..., description="Overall match score", ge=0, le=100)
    breakdown: MatchBreakdown = Field(..., description="Detailed match breakdown")


class MatchResponse(BaseModel):
    """
    Complete API response for job matching.
    
    Attributes:
        candidate_name: Name of the candidate
        matches: List of job matches sorted by match_percentage (descending)
        total_jobs_analyzed: Total number of jobs analyzed
    """
    candidate_name: str = Field(..., description="Candidate's name")
    matches: List[JobMatch] = Field(..., description="Sorted list of job matches")
    total_jobs_analyzed: int = Field(..., description="Total jobs analyzed", ge=0)


# ============================================================================
# REQUEST SCHEMA
# ============================================================================

class MatchRequest(BaseModel):
    """
    API request schema for job matching endpoint.
    
    Attributes:
        candidate: Candidate profile
        jobs: List of job postings to match against
    """
    candidate: Candidate = Field(..., description="Candidate profile")
    jobs: List[Job] = Field(..., description="List of job postings", min_length=1)
