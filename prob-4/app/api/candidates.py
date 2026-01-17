"""
Candidates API Router

RESTful endpoints for managing candidates.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.candidate import Candidate
from app.models.application import Application
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse
from app.schemas.application import ApplicationResponse
from app.utils.pagination import paginate

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new candidate",
    description="Register a new candidate in the system."
)
def create_candidate(
    candidate: CandidateCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Create a new candidate.
    
    - **email**: Unique email address (validated)
    - **full_name**: Candidate's full name
    - **phone**: Optional phone number
    - **resume_url**: Optional resume URL
    - **skills**: List of skills
    
    Returns 201 Created with Location header.
    """
    # Check for duplicate email
    existing = db.query(Candidate).filter(
        Candidate.email == candidate.email,
        Candidate.deleted_at.is_(None)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Candidate with email {candidate.email} already exists"
        )
    
    # Create candidate
    db_candidate = Candidate(**candidate.model_dump())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    # Set Location header
    response.headers["Location"] = f"/api/v1/candidates/{db_candidate.id}"
    
    return db_candidate


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
    summary="Get candidate by ID",
    description="Retrieve candidate details."
)
def get_candidate(
    candidate_id: UUID,
    db: Session = Depends(get_db)
):
    """Get candidate by ID."""
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at.is_(None)
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {candidate_id} not found"
        )
    
    return candidate


@router.get(
    "/{candidate_id}/applications",
    response_model=dict,
    summary="Get candidate's applications",
    description="List all applications for a specific candidate with pagination."
)
def get_candidate_applications(
    candidate_id: UUID,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all applications for a candidate with pagination.
    
    Returns:
    - **applications**: List of applications
    - **total**: Total count of applications
    - **skip**: Current offset
    - **limit**: Current limit
    """
    # Verify candidate exists
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at.is_(None)
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {candidate_id} not found"
        )
    
    # Build query
    query = db.query(Application).options(
        joinedload(Application.job)
    ).filter(
        Application.candidate_id == candidate_id,
        Application.deleted_at.is_(None)
    )
    
    # Apply pagination using utility
    applications, metadata = paginate(query, skip=skip, limit=limit)
    
    return {
        "applications": applications,
        "total": metadata.total,
        "skip": skip,
        "limit": limit,
        "has_more": metadata.has_next
    }


@router.patch(
    "/{candidate_id}",
    response_model=CandidateResponse,
    summary="Update candidate",
    description="Update candidate information."
)
def update_candidate(
    candidate_id: UUID,
    candidate_update: CandidateUpdate,
    db: Session = Depends(get_db)
):
    """Update candidate details."""
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at.is_(None)
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {candidate_id} not found"
        )
    
    # Update fields
    for field, value in candidate_update.model_dump(exclude_unset=True).items():
        setattr(candidate, field, value)
    
    db.commit()
    db.refresh(candidate)
    
    return candidate


@router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete candidate",
    description="Soft delete a candidate."
)
def delete_candidate(
    candidate_id: UUID,
    db: Session = Depends(get_db)
):
    """Soft delete a candidate."""
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at.is_(None)
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {candidate_id} not found"
        )
    
    candidate.soft_delete()
    db.commit()
    
    return None
