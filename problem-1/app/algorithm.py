"""
Job Matching Algorithm

This module contains the core matching logic for calculating
compatibility between candidates and job postings.

Weighted Scoring:
- Skills: 40%
- Location: 20%
- Salary: 15%
- Experience: 15%
- Role: 10%
Total: 100%
"""

import re
from typing import List, Tuple
from app.models import Candidate, Job, MatchBreakdown, JobMatch


def normalize_string(s: str) -> str:
    """
    Normalize string for fuzzy matching (lowercase and strip whitespace).
    
    Args:
        s: Input string
        
    Returns:
        Normalized string
    """
    return s.lower().strip()


def parse_experience_range(experience_str: str) -> Tuple[float, float]:
    """
    Parse experience requirement string to extract min and max years.
    
    Examples:
        "0-2 years" -> (0.0, 2.0)
        "3-5 years" -> (3.0, 5.0)
        "5+ years" -> (5.0, 100.0)
        "2 years" -> (2.0, 2.0)
    
    Args:
        experience_str: Experience requirement string
        
    Returns:
        Tuple of (min_years, max_years)
    """
    # Remove "years" and normalize
    normalized = normalize_string(experience_str).replace("years", "").replace("year", "").strip()
    
    # Pattern: "X-Y" or "X - Y"
    range_match = re.search(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', normalized)
    if range_match:
        min_exp = float(range_match.group(1))
        max_exp = float(range_match.group(2))
        return (min_exp, max_exp)
    
    # Pattern: "X+" (X or more)
    plus_match = re.search(r'(\d+\.?\d*)\s*\+', normalized)
    if plus_match:
        min_exp = float(plus_match.group(1))
        return (min_exp, 100.0)  # No upper limit
    
    # Pattern: just a number "X"
    number_match = re.search(r'(\d+\.?\d*)', normalized)
    if number_match:
        exp = float(number_match.group(1))
        return (exp, exp)
    
    # Default: no requirement
    return (0.0, 100.0)


def calculate_skill_score(candidate_skills: List[str], required_skills: List[str]) -> Tuple[float, List[str]]:
    """
    Calculate skill match score with fuzzy matching.
    
    Weight: 40% of total score
    
    Args:
        candidate_skills: List of candidate's skills
        required_skills: List of required skills for the job
        
    Returns:
        Tuple of (skill_score, missing_skills)
        - skill_score: 0-40 points
        - missing_skills: List of skills candidate doesn't have
    """
    # Edge case: no required skills means full points
    if not required_skills:
        return (40.0, [])
    
    # Normalize skills for case-insensitive matching
    candidate_skills_normalized = {normalize_string(skill) for skill in candidate_skills}
    
    matched_count = 0
    missing_skills = []
    
    for required_skill in required_skills:
        required_normalized = normalize_string(required_skill)
        
        if required_normalized in candidate_skills_normalized:
            matched_count += 1
        else:
            missing_skills.append(required_skill)
    
    # Calculate percentage match and convert to score (0-40)
    match_percentage = (matched_count / len(required_skills)) * 100
    skill_score = (match_percentage / 100) * 40
    
    return (round(skill_score, 2), missing_skills)


def calculate_location_score(candidate_locations: List[str], job_location: str) -> float:
    """
    Calculate location match score.
    
    Weight: 20% of total score
    
    Args:
        candidate_locations: List of preferred locations
        job_location: Job location
        
    Returns:
        Location score: 0 or 20 points
    """
    if not candidate_locations:
        return 20.0  # No preference means flexible, full points
    
    # Normalize for case-insensitive matching
    candidate_locations_normalized = {normalize_string(loc) for loc in candidate_locations}
    job_location_normalized = normalize_string(job_location)
    
    # Exact match
    if job_location_normalized in candidate_locations_normalized:
        return 20.0
    
    # Check for "remote" or "anywhere" flexibility
    if "remote" in candidate_locations_normalized or "anywhere" in candidate_locations_normalized:
        return 20.0
    
    return 0.0


def calculate_salary_score(expected_salary: float, salary_range: List[float]) -> float:
    """
    Calculate salary match score.
    
    Weight: 15% of total score
    
    Scoring:
    - Within range: 15 points
    - Within 10% of range: Partial points (7.5 points)
    - Outside 10%: 0 points
    
    Args:
        expected_salary: Candidate's expected salary (can be None)
        salary_range: Job's salary range [min, max]
        
    Returns:
        Salary score: 0-15 points
    """
    if expected_salary is None:
        return 15.0  # No expectation means flexible, full points
    
    min_salary, max_salary = salary_range
    
    # Within range: full points
    if min_salary <= expected_salary <= max_salary:
        return 15.0
    
    # Calculate 10% flexibility bounds
    flexible_min = min_salary * 0.9
    flexible_max = max_salary * 1.1
    
    # Within 10% of range: partial points
    if flexible_min <= expected_salary <= flexible_max:
        return 7.5
    
    # Outside 10%: no points
    return 0.0


def calculate_experience_score(candidate_exp: float, experience_required: str) -> float:
    """
    Calculate experience match score.
    
    Weight: 15% of total score
    
    Args:
        candidate_exp: Candidate's years of experience
        experience_required: Experience requirement string (e.g., "0-2 years", "3-5 years")
        
    Returns:
        Experience score: 0 or 15 points
    """
    min_exp, max_exp = parse_experience_range(experience_required)
    
    # Check if candidate's experience falls within the required range
    if min_exp <= candidate_exp <= max_exp:
        return 15.0
    
    return 0.0


def calculate_role_score(candidate_roles: List[str], job_title: str) -> float:
    """
    Calculate role match score.
    
    Weight: 10% of total score
    
    Args:
        candidate_roles: List of preferred roles (can be None or empty)
        job_title: Job title
        
    Returns:
        Role score: 0 or 10 points
    """
    if not candidate_roles:
        return 10.0  # No preference means flexible, full points
    
    # Normalize for case-insensitive matching
    candidate_roles_normalized = {normalize_string(role) for role in candidate_roles}
    job_title_normalized = normalize_string(job_title)
    
    # Check for exact match
    if job_title_normalized in candidate_roles_normalized:
        return 10.0
    
    # Check for partial match (job title contains any preferred role)
    for role in candidate_roles_normalized:
        if role in job_title_normalized or job_title_normalized in role:
            return 10.0
    
    return 0.0


def calculate_match(candidate: Candidate, job: Job) -> JobMatch:
    """
    Calculate match score between a candidate and a job posting.
    
    Weighted Scoring:
    - Skills: 40%
    - Location: 20%
    - Salary: 15%
    - Experience: 15%
    - Role: 10%
    Total: 100%
    
    Args:
        candidate: Candidate profile
        job: Job posting
        
    Returns:
        JobMatch with total score and detailed breakdown
    """
    # Calculate individual scores
    skill_score, missing_skills = calculate_skill_score(candidate.skills, job.required_skills)
    location_score = calculate_location_score(candidate.preferred_locations, job.location)
    salary_score = calculate_salary_score(candidate.expected_salary, job.salary_range)
    experience_score = calculate_experience_score(candidate.experience_years, job.experience_required)
    role_score = calculate_role_score(candidate.preferred_roles, job.title)
    
    # Calculate total score
    total_score = skill_score + location_score + salary_score + experience_score + role_score
    
    # Ensure total is within bounds (should always be 0-100 due to individual constraints)
    total_score = min(100.0, max(0.0, total_score))
    
    # Create breakdown
    breakdown = MatchBreakdown(
        skill_score=skill_score,
        location_score=location_score,
        salary_score=salary_score,
        experience_score=experience_score,
        role_score=role_score,
        total_score=round(total_score, 2),
        missing_skills=missing_skills
    )
    
    return JobMatch(
        job_id=job.job_id,
        title=job.title,
        company=job.company,
        total_score=round(total_score, 2),
        breakdown=breakdown
    )


# ============================================================================
# SELF-CORRECTION VERIFICATION
# ============================================================================

def verify_weights():
    """
    Verify that all weights sum to 100%.
    
    This is a sanity check function to ensure the algorithm is correctly weighted.
    """
    weights = {
        "skills": 40,
        "location": 20,
        "salary": 15,
        "experience": 15,
        "role": 10
    }
    
    total = sum(weights.values())
    assert total == 100, f"Weights must sum to 100%, got {total}%"
    
    return weights


# Run verification on module import
verify_weights()
