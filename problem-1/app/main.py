"""
FastAPI Job Matching System - Main Application Entry Point

This module defines the FastAPI application and all API endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.models import MatchRequest, MatchResponse, JobMatch, Candidate, Job
from app.algorithm import calculate_match

# Initialize FastAPI app
app = FastAPI(
    title="Job Matching API",
    description="Intelligent job matching system using weighted scoring algorithm",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - API information and health check.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "Job Matching API is running",
        "version": "1.0.0",
        "description": "Intelligent job matching with weighted scoring",
        "endpoints": {
            "match": "POST /match - Match candidate to jobs",
            "health": "GET /health - Health check",
            "docs": "GET /docs - Interactive API documentation",
            "redoc": "GET /redoc - ReDoc documentation"
        },
        "scoring_weights": {
            "skills": "40%",
            "location": "20%",
            "salary": "15%",
            "experience": "15%",
            "role": "10%"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Service health status
    """
    return {
        "status": "healthy",
        "service": "job-matching-api",
        "version": "1.0.0"
    }


@app.post("/match", response_model=MatchResponse)
async def match_candidate_to_jobs(request: MatchRequest):
    """
    Match a candidate to multiple job postings.
    
    This endpoint calculates match scores between a candidate and a list of jobs
    using a weighted scoring algorithm:
    - Skills: 40%
    - Location: 20%
    - Salary: 15%
    - Experience: 15%
    - Role: 10%
    
    Args:
        request: MatchRequest containing candidate profile and list of jobs
        
    Returns:
        MatchResponse: Sorted list of job matches with scores and breakdowns
        
    Raises:
        HTTPException: 422 if validation fails (handled by Pydantic)
        HTTPException: 500 if internal error occurs
    """
    try:
        candidate = request.candidate
        jobs = request.jobs
        
        # Validate that we have jobs to match against
        if not jobs:
            raise HTTPException(
                status_code=400,
                detail="No jobs provided. Please include at least one job posting."
            )
        
        # Calculate match for each job
        matches: List[JobMatch] = []
        
        for job in jobs:
            try:
                match = calculate_match(candidate, job)
                matches.append(match)
            except Exception as e:
                # Log error but continue processing other jobs
                print(f"Error matching job {job.job_id}: {str(e)}")
                continue
        
        # Sort matches by total_score in descending order (best matches first)
        matches.sort(key=lambda x: x.total_score, reverse=True)
        
        # Create response
        response = MatchResponse(
            candidate_name=candidate.name,
            matches=matches,
            total_jobs_analyzed=len(jobs)
        )
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/match/example")
async def get_example_request():
    """
    Get an example request payload for the /match endpoint.
    
    This is helpful for understanding the expected input format.
    
    Returns:
        dict: Example MatchRequest payload
    """
    return {
        "candidate": {
            "name": "John Doe",
            "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "experience_years": 5.0,
            "education": [
                {
                    "degree": "Bachelor's",
                    "field": "Computer Science",
                    "institution": "MIT",
                    "graduation_year": 2018
                }
            ],
            "preferred_locations": ["San Francisco", "Remote"],
            "preferred_roles": ["Backend Engineer", "Full Stack Developer"],
            "expected_salary": 120000
        },
        "jobs": [
            {
                "job_id": "job-001",
                "title": "Senior Backend Engineer",
                "company": "TechCorp",
                "required_skills": ["Python", "FastAPI", "Docker"],
                "experience_required": "3-5 years",
                "location": "San Francisco",
                "salary_range": [100000, 150000],
                "education_required": "Bachelor's"
            },
            {
                "job_id": "job-002",
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "required_skills": ["Python", "React", "PostgreSQL"],
                "experience_required": "2-4 years",
                "location": "Remote",
                "salary_range": [90000, 130000],
                "education_required": "Bachelor's"
            }
        ]
    }


# Error handlers
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    """
    Custom handler for validation errors (422).
    
    Pydantic automatically raises 422 errors for invalid inputs,
    such as missing required fields (e.g., candidate without name).
    """
    return {
        "error": "Validation Error",
        "detail": "Invalid input data. Please check your request payload.",
        "validation_errors": exc.errors() if hasattr(exc, 'errors') else str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
