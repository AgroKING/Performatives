"""
Jobs API Router

RESTful endpoints for managing job postings.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.job import Job
from app.models.application import Application
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.schemas.application import ApplicationResponse
from app.utils.pagination import paginate

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new job",
    description="Post a new job opening."
)
def create_job(
    job: JobCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Create a new job posting.
    
    Returns 201 Created with Location header.
    """
    db_job = Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Set Location header
    response.headers["Location"] = f"/api/v1/jobs/{db_job.id}"
    
    return db_job


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get job by ID",
    description="Retrieve job posting details."
)
def get_job(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    """Get job by ID."""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.deleted_at.is_(None)
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {job_id} not found"
        )
    
    return job


@router.get(
    "/{job_id}/applications",
    response_model=dict,
    summary="Get job applications",
    description="List all applications for a specific job with status filtering and pagination."
)
def get_job_applications(
    job_id: UUID,
    status_filter: Optional[str] = Query(None, description="Filter by application status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all applications for a job with optional status filter and pagination.
    
    Query parameters:
    - **status_filter**: Filter by application status (e.g., "SUBMITTED", "SCREENING")
    - **skip**: Offset for pagination
    - **limit**: Max records to return
    
    Returns:
    - **applications**: List of applications
    - **total**: Total count (with filter applied)
    - **skip**: Current offset
    - **limit**: Current limit
    - **has_more**: Boolean indicating if more records exist
    """
    # Verify job exists
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.deleted_at.is_(None)
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {job_id} not found"
        )
    
    # Build query
    query = db.query(Application).filter(
        Application.job_id == job_id,
        Application.deleted_at.is_(None)
    )
    
    # Apply status filter if provided
    if status_filter:
        query = query.filter(Application.status == status_filter)
    
    # Apply pagination using utility
    query = query.options(joinedload(Application.candidate))
    applications, metadata = paginate(query, skip=skip, limit=limit)
    
    return {
        "applications": applications,
        "total": metadata.total,
        "skip": skip,
        "limit": limit,
        "has_more": metadata.has_next,
        "status_filter": status_filter
    }


@router.get(
    "/",
    response_model=List[JobResponse],
    summary="List jobs",
    description="List all job postings with optional filtering."
)
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    department: Optional[str] = Query(None, description="Filter by department"),
    status_filter: Optional[str] = Query(None, description="Filter by job status"),
    db: Session = Depends(get_db)
):
    """
    List jobs with filtering and pagination.
    
    Query parameters:
    - **skip**: Offset for pagination
    - **limit**: Max records to return
    - **department**: Filter by department name
    - **status_filter**: Filter by job status (OPEN, CLOSED, etc.)
    """
    query = db.query(Job).filter(Job.deleted_at.is_(None))
    
    # Apply filters
    if department:
        query = query.filter(Job.department == department)
    if status_filter:
        query = query.filter(Job.status == status_filter)
    
    # Apply pagination
    jobs = query.offset(skip).limit(limit).all()
    
    return jobs


@router.patch(
    "/{job_id}",
    response_model=JobResponse,
    summary="Update job",
    description="Update job posting details."
)
def update_job(
    job_id: UUID,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
):
    """Update job details."""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.deleted_at.is_(None)
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {job_id} not found"
        )
    
    # Update fields
    for field, value in job_update.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    
    return job


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete job",
    description="Soft delete a job posting."
)
def delete_job(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    """Soft delete a job."""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.deleted_at.is_(None)
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {job_id} not found"
        )
    
    job.soft_delete()
    db.commit()
    
    return None
