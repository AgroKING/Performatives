"""
Skill Gap Analysis & Learning Roadmap System
Pydantic Data Models (Python Alternative)
"""

from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
#error free till now


SkillCategory = Literal['Frontend', 'Backend', 'DevOps', 'Database']
DifficultyLevel = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
SeniorityLevel = Literal['Junior', 'Mid', 'Senior', 'Lead', 'Principal']
ImportanceLevel = Literal['Critical', 'High', 'Medium', 'Low']


class Skill(BaseModel):
    """Represents a single skill in the taxonomy"""
    id: str = Field(..., description="Unique skill identifier")
    name: str = Field(..., description="Skill name")
    category: SkillCategory
    difficulty: DifficultyLevel = Field(..., ge=1, le=10)
    typical_learning_time_weeks: int = Field(..., gt=0)
    prerequisites: List[str] = Field(default_factory=list, description="List of prerequisite skill IDs")
    description: str
    tags: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "fe-005",
                "name": "React",
                "category": "Frontend",
                "difficulty": 7,
                "typical_learning_time_weeks": 6,
                "prerequisites": ["fe-003"],
                "description": "Component-based JavaScript library for building UIs",
                "tags": ["framework", "library", "spa"]
            }
        }

#error free again
class CandidateSkill(BaseModel):
    """Represents a skill that a candidate possesses with proficiency level"""
    skill_id: str
    proficiency_level: int = Field(..., ge=1, le=10)
    years_of_experience: float = Field(..., ge=0)
    last_used: Optional[datetime] = None
    certified: bool = False


class Candidate(BaseModel):
    """Represents a candidate's current skill profile"""
    id: str
    name: str
    email: EmailStr
    current_skills: List[CandidateSkill]
    experience_years: float = Field(..., ge=0)
    created_at: datetime
    updated_at: datetime

#no errors
class RoleSkillRequirement(BaseModel):
    """Represents a skill requirement for a specific role"""
    skill_id: str
    minimum_proficiency: int = Field(..., ge=1, le=10)
    importance: ImportanceLevel


class SalaryRange(BaseModel):
    """Salary range for a role"""
    min: int = Field(..., gt=0)
    max: int = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)


class TargetRole(BaseModel):
    """Represents a target role with required skills"""
    id: str
    title: str
    description: str
    seniority_level: SeniorityLevel
    required_skills: List[RoleSkillRequirement]
    optional_skills: List[RoleSkillRequirement] = Field(default_factory=list)
    min_experience_years: int = Field(..., ge=0)
    salary_range: Optional[SalaryRange] = None


class CategoryInfo(BaseModel):
    """Information about a skill category"""
    name: str
    description: str
    skill_count: int
#no errors

class SkillTaxonomy(BaseModel):
    """Complete skill taxonomy structure"""
    version: str
    last_updated: datetime
    categories: dict[SkillCategory, CategoryInfo]
    skills: List[Skill]


class SkillGap(BaseModel):
    """Represents a gap between current and required skill level"""
    skill_id: str
    current_proficiency: int = Field(..., ge=0, le=10)
    required_proficiency: int = Field(..., ge=1, le=10)
    gap_score: int = Field(..., description="Difference between required and current")
    priority: ImportanceLevel

#class declaration
class LearningPathStep(BaseModel):
    """Represents a step in the learning path"""
    order: int = Field(..., ge=1)
    skill_id: str
    estimated_weeks: int = Field(..., gt=0)
    prerequisites_met: bool
    reason: str

#more class declaration
class LearningRoadmap(BaseModel):
    """Learning roadmap generated for a candidate"""
    candidate_id: str
    target_role_id: str
    generated_at: datetime
    skill_gaps: List[SkillGap]
    estimated_total_weeks: int = Field(..., ge=0)
    learning_path: List[LearningPathStep]
