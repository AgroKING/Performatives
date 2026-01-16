"""
Comprehensive Unit Tests for Job Matching System

Test Cases:
1. Perfect Match - All criteria match (score ~100)
2. Partial Match - Only some criteria match (weighted score)
3. Edge Cases - Empty skills, null values, missing fields

Run with: pytest tests/test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Candidate, Job, Education, MatchRequest
from app.algorithm import calculate_match

# Initialize test client
client = TestClient(app)


# ============================================================================
# TEST 1: PERFECT MATCH
# ============================================================================

def test_perfect_match():
    """
    Test a perfect match scenario where candidate meets all job requirements.
    Expected score: ~100 (all weights satisfied)
    """
    # Create candidate with all matching criteria
    candidate = Candidate(
        name="Alice Perfect",
        skills=["Python", "FastAPI", "Docker", "PostgreSQL"],
        experience_years=5.0,
        education=[
            Education(
                degree="Bachelor's",
                field="Computer Science",
                institution="MIT",
                graduation_year=2018
            )
        ],
        preferred_locations=["San Francisco", "Remote"],
        preferred_roles=["Senior Backend Engineer", "Backend Developer"],
        expected_salary=120000
    )
    
    # Create job that perfectly matches candidate
    job = Job(
        job_id="job-perfect-001",
        title="Senior Backend Engineer",
        company="TechCorp",
        required_skills=["Python", "FastAPI", "Docker", "PostgreSQL"],
        experience_required="3-5 years",
        location="San Francisco",
        salary_range=[100000, 150000],
        education_required="Bachelor's"
    )
    
    # Calculate match
    match = calculate_match(candidate, job)
    
    # Assertions
    assert match.job_id == "job-perfect-001"
    assert match.total_score == 100.0, f"Expected 100, got {match.total_score}"
    assert match.breakdown.skill_score == 40.0, "All skills match"
    assert match.breakdown.location_score == 20.0, "Location matches"
    assert match.breakdown.salary_score == 15.0, "Salary in range"
    assert match.breakdown.experience_score == 15.0, "Experience fits range"
    assert match.breakdown.role_score == 10.0, "Role matches"
    assert len(match.breakdown.missing_skills) == 0, "No missing skills"


# ============================================================================
# TEST 2: PARTIAL MATCH
# ============================================================================

def test_partial_match_location_only():
    """
    Test partial match where only location matches, skills don't.
    Expected score: 20 (location) + 15 (salary) + 15 (experience) + 10 (role) = 60
    Skills: 0/4 = 0 points
    """
    candidate = Candidate(
        name="Bob Partial",
        skills=["Java", "Spring", "MySQL"],  # Different skills
        experience_years=4.0,
        education=[
            Education(
                degree="Bachelor's",
                field="Computer Science",
                institution="Stanford",
                graduation_year=2019
            )
        ],
        preferred_locations=["Remote"],
        preferred_roles=["Backend Engineer"],
        expected_salary=110000
    )
    
    job = Job(
        job_id="job-partial-001",
        title="Backend Engineer",
        company="StartupXYZ",
        required_skills=["Python", "FastAPI", "Docker", "PostgreSQL"],  # No match
        experience_required="3-5 years",
        location="Remote",
        salary_range=[100000, 130000],
        education_required="Bachelor's"
    )
    
    match = calculate_match(candidate, job)
    
    # Assertions
    assert match.breakdown.skill_score == 0.0, "No skills match"
    assert match.breakdown.location_score == 20.0, "Location matches"
    assert match.breakdown.salary_score == 15.0, "Salary in range"
    assert match.breakdown.experience_score == 15.0, "Experience fits"
    assert match.breakdown.role_score == 10.0, "Role matches"
    assert match.total_score == 60.0, f"Expected 60, got {match.total_score}"
    assert len(match.breakdown.missing_skills) == 4, "All 4 skills missing"


def test_partial_match_skills_only():
    """
    Test partial match where 50% of skills match, nothing else.
    Expected score: 20 (50% of 40) + 0 + 0 + 0 + 0 = 20
    """
    candidate = Candidate(
        name="Charlie Skills",
        skills=["Python", "Django"],  # 2 out of 4 match
        experience_years=1.0,  # Too junior
        education=[
            Education(
                degree="Bachelor's",
                field="Computer Science",
                institution="UCLA",
                graduation_year=2022
            )
        ],
        preferred_locations=["New York"],  # Different location
        preferred_roles=["Frontend Developer"],  # Different role
        expected_salary=80000  # Too low
    )
    
    job = Job(
        job_id="job-skills-001",
        title="Senior Backend Engineer",
        company="BigTech",
        required_skills=["Python", "FastAPI", "Docker", "PostgreSQL"],
        experience_required="5-7 years",
        location="San Francisco",
        salary_range=[120000, 160000],
        education_required="Bachelor's"
    )
    
    match = calculate_match(candidate, job)
    
    # Assertions
    assert match.breakdown.skill_score == 10.0, "25% of skills match (1/4 = Python only)"
    assert match.breakdown.location_score == 0.0, "Location doesn't match"
    assert match.breakdown.salary_score == 0.0, "Salary too low"
    assert match.breakdown.experience_score == 0.0, "Experience too low"
    assert match.breakdown.role_score == 0.0, "Role doesn't match"
    assert match.total_score == 10.0, f"Expected 10, got {match.total_score}"
    assert len(match.breakdown.missing_skills) == 3, "3 skills missing"


# ============================================================================
# TEST 3: EDGE CASES
# ============================================================================

def test_empty_required_skills():
    """
    Test edge case: Job has no required skills.
    Should give full 40 points for skills (no division by zero).
    """
    candidate = Candidate(
        name="Diana Edge",
        skills=["Python", "FastAPI"],
        experience_years=3.0,
        education=[
            Education(
                degree="Bachelor's",
                field="Computer Science",
                institution="Berkeley",
                graduation_year=2020
            )
        ],
        preferred_locations=["Remote"],
        preferred_roles=["Developer"],
        expected_salary=100000
    )
    
    job = Job(
        job_id="job-edge-001",
        title="Developer",
        company="FlexCorp",
        required_skills=[],  # Empty skills list
        experience_required="2-4 years",
        location="Remote",
        salary_range=[90000, 120000],
        education_required="Bachelor's"
    )
    
    match = calculate_match(candidate, job)
    
    # Assertions
    assert match.breakdown.skill_score == 40.0, "Empty skills = full points"
    assert match.breakdown.location_score == 20.0
    assert match.breakdown.salary_score == 15.0
    assert match.breakdown.experience_score == 15.0
    assert match.breakdown.role_score == 10.0
    assert match.total_score == 100.0
    assert len(match.breakdown.missing_skills) == 0


def test_no_expected_salary():
    """
    Test edge case: Candidate has no expected salary (None).
    Should give full 15 points for salary (flexible).
    """
    candidate = Candidate(
        name="Eve Flexible",
        skills=["Python"],
        experience_years=2.0,
        education=[
            Education(
                degree="Bachelor's",
                field="Computer Science",
                institution="Harvard",
                graduation_year=2021
            )
        ],
        preferred_locations=["Anywhere"],
        preferred_roles=None,  # No role preference
        expected_salary=None  # No salary expectation
    )
    
    job = Job(
        job_id="job-flex-001",
        title="Junior Developer",
        company="StartupABC",
        required_skills=["Python"],
        experience_required="1-3 years",
        location="Boston",
        salary_range=[70000, 90000],
        education_required="Bachelor's"
    )
    
    match = calculate_match(candidate, job)
    
    # Assertions
    assert match.breakdown.skill_score == 40.0, "All skills match"
    assert match.breakdown.location_score == 20.0, "'Anywhere' matches"
    assert match.breakdown.salary_score == 15.0, "No expectation = flexible"
    assert match.breakdown.experience_score == 15.0
    assert match.breakdown.role_score == 10.0, "No preference = flexible"
    assert match.total_score == 100.0


def test_no_preferred_locations():
    """
    Test edge case: Candidate has no location preference.
    Should give full 20 points (flexible).
    """
    candidate = Candidate(
        name="Frank NoLoc",
        skills=["JavaScript", "React"],
        experience_years=3.0,
        education=[
            Education(
                degree="Bachelor's",
                field="Computer Science",
                institution="Yale",
                graduation_year=2020
            )
        ],
        preferred_locations=[],  # Empty list
        preferred_roles=["Frontend Developer"],
        expected_salary=95000
    )
    
    job = Job(
        job_id="job-noloc-001",
        title="Frontend Developer",
        company="WebCorp",
        required_skills=["JavaScript", "React"],
        experience_required="2-4 years",
        location="Seattle",
        salary_range=[90000, 110000],
        education_required="Bachelor's"
    )
    
    match = calculate_match(candidate, job)
    
    # Assertions
    assert match.breakdown.location_score == 20.0, "No preference = flexible"
    assert match.total_score == 100.0


# ============================================================================
# API ENDPOINT TESTS
# ============================================================================

def test_match_endpoint_success():
    """
    Test POST /match endpoint with valid data.
    """
    request_data = {
        "candidate": {
            "name": "Test Candidate",
            "skills": ["Python", "FastAPI"],
            "experience_years": 3.0,
            "education": [
                {
                    "degree": "Bachelor's",
                    "field": "Computer Science",
                    "institution": "MIT",
                    "graduation_year": 2020
                }
            ],
            "preferred_locations": ["Remote"],
            "preferred_roles": ["Backend Engineer"],
            "expected_salary": 100000
        },
        "jobs": [
            {
                "job_id": "job-001",
                "title": "Backend Engineer",
                "company": "TechCo",
                "required_skills": ["Python", "FastAPI"],
                "experience_required": "2-4 years",
                "location": "Remote",
                "salary_range": [90000, 120000],
                "education_required": "Bachelor's"
            },
            {
                "job_id": "job-002",
                "title": "Frontend Engineer",
                "company": "WebCo",
                "required_skills": ["React", "TypeScript"],
                "experience_required": "3-5 years",
                "location": "New York",
                "salary_range": [95000, 125000],
                "education_required": "Bachelor's"
            }
        ]
    }
    
    response = client.post("/match", json=request_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_name"] == "Test Candidate"
    assert data["total_jobs_analyzed"] == 2
    assert len(data["matches"]) == 2
    
    # Verify sorting (descending by total_score)
    assert data["matches"][0]["total_score"] >= data["matches"][1]["total_score"]


def test_match_endpoint_missing_name():
    """
    Test POST /match endpoint with missing candidate name.
    Should return 422 Validation Error.
    """
    request_data = {
        "candidate": {
            # "name" is missing - required field
            "skills": ["Python"],
            "experience_years": 3.0,
            "education": [],
            "preferred_locations": ["Remote"]
        },
        "jobs": [
            {
                "job_id": "job-001",
                "title": "Developer",
                "company": "TechCo",
                "required_skills": ["Python"],
                "experience_required": "2-4 years",
                "location": "Remote",
                "salary_range": [90000, 120000],
                "education_required": "Bachelor's"
            }
        ]
    }
    
    response = client.post("/match", json=request_data)
    
    # Assertions
    assert response.status_code == 422, "Should return 422 for missing required field"


def test_match_endpoint_invalid_salary_range():
    """
    Test POST /match endpoint with invalid salary range (min >= max).
    Should return 422 Validation Error.
    """
    request_data = {
        "candidate": {
            "name": "Test User",
            "skills": ["Python"],
            "experience_years": 3.0,
            "education": [],
            "preferred_locations": ["Remote"]
        },
        "jobs": [
            {
                "job_id": "job-001",
                "title": "Developer",
                "company": "TechCo",
                "required_skills": ["Python"],
                "experience_required": "2-4 years",
                "location": "Remote",
                "salary_range": [120000, 90000],  # Invalid: min > max
                "education_required": "Bachelor's"
            }
        ]
    }
    
    response = client.post("/match", json=request_data)
    
    # Assertions
    assert response.status_code == 422, "Should return 422 for invalid salary range"


def test_match_endpoint_no_jobs():
    """
    Test POST /match endpoint with empty jobs list.
    Should return 400 Bad Request.
    """
    request_data = {
        "candidate": {
            "name": "Test User",
            "skills": ["Python"],
            "experience_years": 3.0,
            "education": [],
            "preferred_locations": ["Remote"]
        },
        "jobs": []  # Empty jobs list
    }
    
    response = client.post("/match", json=request_data)
    
    # Assertions
    assert response.status_code == 422, "Should return 422 for empty jobs list (Pydantic validation)"


def test_health_endpoint():
    """
    Test GET /health endpoint.
    """
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint():
    """
    Test GET / endpoint.
    """
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "endpoints" in data
    assert "scoring_weights" in data


def test_example_endpoint():
    """
    Test GET /match/example endpoint.
    """
    response = client.get("/match/example")
    
    assert response.status_code == 200
    data = response.json()
    assert "candidate" in data
    assert "jobs" in data


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
