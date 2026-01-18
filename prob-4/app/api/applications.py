"""
Applications API Router

RESTful endpoints for managing job applications.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks, Response
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from app.database import get_db
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithHistory,
    StatusChangeRequest,
    ApplicationStatsResponse,
    ApplicationListResponse
)
from app.schemas.stats import AdvancedStatsResponse
from app.services.status_manager import StatusManager
from app.services.email_service import get_email_service

router = APIRouter(prefix="/applications", tags=["Applications"])

# Initialize email service
email_service = get_email_service(use_mock=True)


@router.post(
    "/",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new application",
    description="Submit a new job application. Returns 201 with Location header."
)
async def create_application(
    application: ApplicationCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Create a new job application.
    
    - **candidate_id**: UUID of the candidate
    - **job_id**: UUID of the job posting
    - **cover_letter**: Optional cover letter text
    - **resume_data**: Optional parsed resume data
    
    Returns 201 Created with Location header pointing to the new resource.
    """
    # Verify candidate exists
    candidate = db.query(Candidate).filter(
        Candidate.id == application.candidate_id,
        Candidate.deleted_at.is_(None)
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {application.candidate_id} not found"
        )
    
    # Verify job exists and is open
    job = db.query(Job).filter(
        Job.id == application.job_id,
        Job.deleted_at.is_(None)
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {application.job_id} not found"
        )
    
    # Check for duplicate application
    existing = db.query(Application).filter(
        Application.candidate_id == application.candidate_id,
        Application.job_id == application.job_id,
        Application.deleted_at.is_(None)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate has already applied to this job"
        )
    
    # Create application
    db_application = Application(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    # Set Location header
    response.headers["Location"] = f"/api/v1/applications/{db_application.id}"
    
    return db_application


@router.get(
    "/stats/advanced",
    response_model=AdvancedStatsResponse,
    summary="Get advanced application statistics",
    description="Comprehensive analytics with conversion rates, time metrics, funnel data, and daily trends."
)
def get_advanced_stats(
    job_id: Optional[UUID] = Query(None, description="Filter by job ID"),
    date_from: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get advanced application statistics optimized for Chart.js visualization.
    
    Returns:
    1. Total applications by status (breakdown)
    2. Conversion rates (Applied → Offered percentage)
    3. Average time in each stage (in days)
    4. Funnel visualization data (counts at each stage)
    5. Daily application trend (last 30 days)
    
    All data formatted for Chart.js charts.
    """
    from app.schemas.stats import (
        AdvancedStatsResponse,
        StatusBreakdown,
        ConversionMetrics,
        StageTimeMetrics,
        FunnelStage
    )
    from app.utils.enums import ApplicationStatus
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import cast, Date
    
    # Base query
    query = db.query(Application).filter(Application.deleted_at.is_(None))
    
    # Apply filters
    if job_id:
        query = query.filter(Application.job_id == job_id)
    if date_from:
        query = query.filter(cast(Application.submitted_at, Date) >= date_from)
    if date_to:
        query = query.filter(cast(Application.submitted_at, Date) <= date_to)
    
    total_applications = query.count()
    
    # 1. STATUS BREAKDOWN
    status_counts = db.query(
        Application.status,
        func.count(Application.id).label('count')
    ).filter(Application.deleted_at.is_(None))
    
    if job_id:
        status_counts = status_counts.filter(Application.job_id == job_id)
    if date_from:
        status_counts = status_counts.filter(cast(Application.submitted_at, Date) >= date_from)
    if date_to:
        status_counts = status_counts.filter(cast(Application.submitted_at, Date) <= date_to)
    
    status_counts = status_counts.group_by(Application.status).all()
    
    status_breakdown = []
    status_dict = {}
    for app_status, count in status_counts:
        percentage = (count / total_applications * 100) if total_applications > 0 else 0
        status_breakdown.append(StatusBreakdown(
            status=app_status.value,
            count=count,
            percentage=round(percentage, 2)
        ))
        status_dict[app_status.value] = count
    
    # 2. CONVERSION METRICS
    submitted_count = status_dict.get("SUBMITTED", 0) + status_dict.get("SCREENING", 0) + \
                     status_dict.get("INTERVIEW_SCHEDULED", 0) + status_dict.get("INTERVIEWED", 0) + \
                     status_dict.get("OFFER_EXTENDED", 0) + status_dict.get("HIRED", 0)
    
    screening_count = status_dict.get("SCREENING", 0) + status_dict.get("INTERVIEW_SCHEDULED", 0) + \
                     status_dict.get("INTERVIEWED", 0) + status_dict.get("OFFER_EXTENDED", 0) + \
                     status_dict.get("HIRED", 0)
    
    interview_count = status_dict.get("INTERVIEW_SCHEDULED", 0) + status_dict.get("INTERVIEWED", 0) + \
                     status_dict.get("OFFER_EXTENDED", 0) + status_dict.get("HIRED", 0)
    
    offer_count = status_dict.get("OFFER_EXTENDED", 0) + status_dict.get("HIRED", 0)
    hired_count = status_dict.get("HIRED", 0)
    
    conversion_metrics = ConversionMetrics(
        applied_to_screening=round((screening_count / submitted_count * 100), 2) if submitted_count > 0 else None,
        screening_to_interview=round((interview_count / screening_count * 100), 2) if screening_count > 0 else None,
        interview_to_offer=round((offer_count / interview_count * 100), 2) if interview_count > 0 else None,
        offer_to_hired=round((hired_count / offer_count * 100), 2) if offer_count > 0 else None,
        overall_conversion=round((hired_count / submitted_count * 100), 2) if submitted_count > 0 else None
    )
    
    # 3. AVERAGE TIME PER STAGE
    stage_time_metrics = []
    for app_status in ApplicationStatus:
        apps_in_stage = query.filter(Application.status == app_status).all()
        
        if apps_in_stage:
            days_list = [(app.updated_at - app.submitted_at).total_seconds() / 86400 for app in apps_in_stage]
            stage_time_metrics.append(StageTimeMetrics(
                stage=app_status.value,
                avg_days=round(sum(days_list) / len(days_list), 2),
                min_days=round(min(days_list), 2),
                max_days=round(max(days_list), 2),
                count=len(apps_in_stage)
            ))
    
    # 4. FUNNEL DATA (Chart.js ready)
    funnel_stages = [
        ("Applied", submitted_count, "#3B82F6"),
        ("Screening", screening_count, "#10B981"),
        ("Interview", interview_count, "#F59E0B"),
        ("Offer", offer_count, "#EF4444"),
        ("Hired", hired_count, "#8B5CF6")
    ]
    
    funnel_data = {
        "labels": [stage[0] for stage in funnel_stages],
        "values": [stage[1] for stage in funnel_stages],
        "colors": [stage[2] for stage in funnel_stages]
    }
    
    # 5. DAILY TRENDS (last 30 days or date range)
    if not date_from:
        date_from = (datetime.now(timezone.utc) - timedelta(days=30)).date()
    if not date_to:
        date_to = datetime.now(timezone.utc).date()
    
    daily_counts = db.query(
        cast(Application.submitted_at, Date).label('date'),
        func.count(Application.id).label('count')
    ).filter(
        Application.deleted_at.is_(None),
        cast(Application.submitted_at, Date) >= date_from,
        cast(Application.submitted_at, Date) <= date_to
    )
    
    if job_id:
        daily_counts = daily_counts.filter(Application.job_id == job_id)
    
    daily_counts = daily_counts.group_by(cast(Application.submitted_at, Date)).order_by('date').all()
    
    # Fill in missing dates with 0
    date_dict = {str(row.date): row.count for row in daily_counts}
    current_date = date_from
    daily_labels = []
    daily_values = []
    
    while current_date <= date_to:
        daily_labels.append(str(current_date))
        daily_values.append(date_dict.get(str(current_date), 0))
        current_date += timedelta(days=1)
    
    daily_trends = {
        "labels": daily_labels,
        "values": daily_values
    }
    
    return AdvancedStatsResponse(
        total_applications=total_applications,
        date_range={
            "from": str(date_from) if date_from else None,
            "to": str(date_to) if date_to else None
        },
        status_breakdown=status_breakdown,
        conversion_metrics=conversion_metrics,
        avg_time_per_stage=stage_time_metrics,
        funnel_data=funnel_data,
        daily_trends=daily_trends
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationWithHistory,
    summary="Get application by ID",
    description="Retrieve application with complete status history."
)
def get_application(
    application_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get application by ID with nested StatusHistory.
    
    Returns complete application details including:
    - All application fields
    - Complete status change history
    - Computed field: time_in_current_status
    """
    application = db.query(Application).options(
        joinedload(Application.candidate),
        joinedload(Application.job),
        joinedload(Application.status_history)
    ).filter(
        Application.id == application_id,
        Application.deleted_at.is_(None)
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )
    
    return application


@router.patch(
    "/{application_id}/status",
    response_model=ApplicationResponse,
    summary="Update application status",
    description="Change application status with validation and email notification."
)
async def update_application_status(
    application_id: UUID,
    status_request: StatusChangeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Update application status with validation.
    
    - Validates status transition using StatusManager
    - Creates StatusHistory entry
    - Sends email notification in background
    
    Returns 400 if transition is invalid.
    """
    # Fetch application with related data for email
    application = db.query(Application).options(
        joinedload(Application.candidate),
        joinedload(Application.job)
    ).filter(
        Application.id == application_id,
        Application.deleted_at.is_(None)
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )
    
    old_status = application.status.value
    
    # Update status using StatusManager (validates transition)
    updated_application = StatusManager.update_application_status(
        db=db,
        app_id=application_id,
        new_status=status_request.new_status,
        changed_by=status_request.changed_by,
        notes=status_request.notes
    )
    
    # Send email notification in background
    background_tasks.add_task(
        email_service.send_status_change_email,
        candidate_email=application.candidate.email,
        candidate_name=application.candidate.full_name,
        old_status=old_status,
        new_status=status_request.new_status.value,
        job_title=application.job.title,
        company_name=application.job.department,  # Using department as company
        notes=status_request.notes
    )
    
    return updated_application


@router.get(
    "/",
    response_model=ApplicationListResponse,
    summary="List applications with advanced search",
    description="Search and filter applications with pagination and metadata."
)
def list_applications(
    # Pagination
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    
    # Search filters
    candidate_email: Optional[str] = Query(None, description="Candidate email (partial match, case-insensitive)"),
    job_title: Optional[str] = Query(None, description="Job title (partial match, case-insensitive)"),
    status: Optional[str] = Query(None, description="Status filter (exact or comma-separated multiple)"),
    
    # Date range
    applied_from: Optional[date] = Query(None, description="Applied from date (YYYY-MM-DD)"),
    applied_to: Optional[date] = Query(None, description="Applied to date (YYYY-MM-DD)"),
    
    # Sorting
    sort_by: Optional[str] = Query("submitted_at", description="Sort field (submitted_at, updated_at)"),
    order: Optional[str] = Query("desc", description="Sort order (asc, desc)"),
    
    # Legacy filters (for backward compatibility)
    job_id: Optional[UUID] = Query(None, description="Filter by job ID"),
    candidate_id: Optional[UUID] = Query(None, description="Filter by candidate ID"),
    
    db: Session = Depends(get_db)
):
    """
    List applications with advanced search and filtering.
    
    **Search Filters:**
    - `candidate_email`: Partial match, case-insensitive
    - `job_title`: Partial match, case-insensitive
    - `status`: Exact match or comma-separated (e.g., "SUBMITTED,SCREENING")
    - `applied_from`, `applied_to`: Date range filter
    
    **Sorting:**
    - `sort_by`: submitted_at (default) or updated_at
    - `order`: asc or desc (default)
    
    **Pagination:**
    - `page`: Page number (1-indexed)
    - `per_page`: Items per page (max 100)
    
    **Returns:**
    - `items`: List of applications
    - `metadata`: Pagination info (total, page, per_page, total_pages, has_next, has_prev)
    """
    from sqlalchemy import cast, Date, or_
    from app.utils.pagination import paginate, calculate_skip
    
    # Build base query with joins for search
    query = db.query(Application).options(
        joinedload(Application.candidate),
        joinedload(Application.job)
    ).filter(Application.deleted_at.is_(None))
    
    # Apply search filters dynamically
    
    # Candidate email filter (partial match, case-insensitive)
    if candidate_email:
        query = query.join(Application.candidate).filter(
            Candidate.email.ilike(f"%{candidate_email}%")
        )
    
    # Job title filter (partial match, case-insensitive)
    if job_title:
        query = query.join(Application.job).filter(
            Job.title.ilike(f"%{job_title}%")
        )
    
    # Status filter (exact or multiple)
    if status:
        status_list = [s.strip() for s in status.split(",")]
        if len(status_list) == 1:
            query = query.filter(Application.status == status_list[0])
        else:
            query = query.filter(Application.status.in_(status_list))
    
    # Date range filters
    if applied_from:
        query = query.filter(cast(Application.submitted_at, Date) >= applied_from)
    if applied_to:
        query = query.filter(cast(Application.submitted_at, Date) <= applied_to)
    
    # Legacy filters (backward compatibility)
    if job_id:
        query = query.filter(Application.job_id == job_id)
    if candidate_id:
        query = query.filter(Application.candidate_id == candidate_id)
    
    # Apply sorting
    valid_sort_fields = ["submitted_at", "updated_at"]
    if sort_by not in valid_sort_fields:
        sort_by = "submitted_at"
    
    sort_column = getattr(Application, sort_by)
    if order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    # Apply pagination using utility
    skip = calculate_skip(page, per_page)
    applications, metadata = paginate(query, skip=skip, limit=per_page)
    
    return {
        "items": applications,
        "metadata": metadata.model_dump()
    }


@router.get(
    "/stats/advanced",
    response_model=AdvancedStatsResponse,
    summary="Get advanced application statistics",
    description="Comprehensive analytics with conversion rates, time metrics, funnel data, and daily trends."
)
def get_advanced_stats(
    job_id: Optional[UUID] = Query(None, description="Filter by job ID"),
    date_from: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get advanced application statistics optimized for Chart.js visualization.
    
    Returns:
    1. Total applications by status (breakdown)
    2. Conversion rates (Applied → Offered percentage)
    3. Average time in each stage (in days)
    4. Funnel visualization data (counts at each stage)
    5. Daily application trend (last 30 days)
    
    All data formatted for Chart.js charts.
    """
    from app.schemas.stats import (
        AdvancedStatsResponse,
        StatusBreakdown,
        ConversionMetrics,
        StageTimeMetrics,
        FunnelStage
    )
    from app.utils.enums import ApplicationStatus
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import cast, Date
    
    # Base query
    query = db.query(Application).filter(Application.deleted_at.is_(None))
    
    # Apply filters
    if job_id:
        query = query.filter(Application.job_id == job_id)
    if date_from:
        query = query.filter(cast(Application.submitted_at, Date) >= date_from)
    if date_to:
        query = query.filter(cast(Application.submitted_at, Date) <= date_to)
    
    total_applications = query.count()
    
    # 1. STATUS BREAKDOWN
    status_counts = db.query(
        Application.status,
        func.count(Application.id).label('count')
    ).filter(Application.deleted_at.is_(None))
    
    if job_id:
        status_counts = status_counts.filter(Application.job_id == job_id)
    if date_from:
        status_counts = status_counts.filter(cast(Application.submitted_at, Date) >= date_from)
    if date_to:
        status_counts = status_counts.filter(cast(Application.submitted_at, Date) <= date_to)
    
    status_counts = status_counts.group_by(Application.status).all()
    
    status_breakdown = []
    status_dict = {}
    for app_status, count in status_counts:
        percentage = (count / total_applications * 100) if total_applications > 0 else 0
        status_breakdown.append(StatusBreakdown(
            status=app_status.value,
            count=count,
            percentage=round(percentage, 2)
        ))
        status_dict[app_status.value] = count
    
    # 2. CONVERSION METRICS
    submitted_count = status_dict.get("SUBMITTED", 0) + status_dict.get("SCREENING", 0) + \
                     status_dict.get("INTERVIEW_SCHEDULED", 0) + status_dict.get("INTERVIEWED", 0) + \
                     status_dict.get("OFFER_EXTENDED", 0) + status_dict.get("HIRED", 0)
    
    screening_count = status_dict.get("SCREENING", 0) + status_dict.get("INTERVIEW_SCHEDULED", 0) + \
                     status_dict.get("INTERVIEWED", 0) + status_dict.get("OFFER_EXTENDED", 0) + \
                     status_dict.get("HIRED", 0)
    
    interview_count = status_dict.get("INTERVIEW_SCHEDULED", 0) + status_dict.get("INTERVIEWED", 0) + \
                     status_dict.get("OFFER_EXTENDED", 0) + status_dict.get("HIRED", 0)
    
    offer_count = status_dict.get("OFFER_EXTENDED", 0) + status_dict.get("HIRED", 0)
    hired_count = status_dict.get("HIRED", 0)
    
    conversion_metrics = ConversionMetrics(
        applied_to_screening=round((screening_count / submitted_count * 100), 2) if submitted_count > 0 else None,
        screening_to_interview=round((interview_count / screening_count * 100), 2) if screening_count > 0 else None,
        interview_to_offer=round((offer_count / interview_count * 100), 2) if interview_count > 0 else None,
        offer_to_hired=round((hired_count / offer_count * 100), 2) if offer_count > 0 else None,
        overall_conversion=round((hired_count / submitted_count * 100), 2) if submitted_count > 0 else None
    )
    
    # 3. AVERAGE TIME PER STAGE
    stage_time_metrics = []
    for app_status in ApplicationStatus:
        apps_in_stage = query.filter(Application.status == app_status).all()
        
        if apps_in_stage:
            days_list = [(app.updated_at - app.submitted_at).total_seconds() / 86400 for app in apps_in_stage]
            stage_time_metrics.append(StageTimeMetrics(
                stage=app_status.value,
                avg_days=round(sum(days_list) / len(days_list), 2),
                min_days=round(min(days_list), 2),
                max_days=round(max(days_list), 2),
                count=len(apps_in_stage)
            ))
    
    # 4. FUNNEL DATA (Chart.js ready)
    funnel_stages = [
        ("Applied", submitted_count, "#3B82F6"),
        ("Screening", screening_count, "#10B981"),
        ("Interview", interview_count, "#F59E0B"),
        ("Offer", offer_count, "#EF4444"),
        ("Hired", hired_count, "#8B5CF6")
    ]
    
    funnel_data = {
        "labels": [stage[0] for stage in funnel_stages],
        "values": [stage[1] for stage in funnel_stages],
        "colors": [stage[2] for stage in funnel_stages]
    }
    
    # 5. DAILY TRENDS (last 30 days or date range)
    if not date_from:
        date_from = (datetime.now(timezone.utc) - timedelta(days=30)).date()
    if not date_to:
        date_to = datetime.now(timezone.utc).date()
    
    daily_counts = db.query(
        cast(Application.submitted_at, Date).label('date'),
        func.count(Application.id).label('count')
    ).filter(
        Application.deleted_at.is_(None),
        cast(Application.submitted_at, Date) >= date_from,
        cast(Application.submitted_at, Date) <= date_to
    )
    
    if job_id:
        daily_counts = daily_counts.filter(Application.job_id == job_id)
    
    daily_counts = daily_counts.group_by(cast(Application.submitted_at, Date)).order_by('date').all()
    
    # Fill in missing dates with 0
    date_dict = {str(row.date): row.count for row in daily_counts}
    current_date = date_from
    daily_labels = []
    daily_values = []
    
    while current_date <= date_to:
        daily_labels.append(str(current_date))
        daily_values.append(date_dict.get(str(current_date), 0))
        current_date += timedelta(days=1)
    
    daily_trends = {
        "labels": daily_labels,
        "values": daily_values
    }
    
    return AdvancedStatsResponse(
        total_applications=total_applications,
        date_range={
            "from": str(date_from) if date_from else None,
            "to": str(date_to) if date_to else None
        },
        status_breakdown=status_breakdown,
        conversion_metrics=conversion_metrics,
        avg_time_per_stage=stage_time_metrics,
        funnel_data=funnel_data,
        daily_trends=daily_trends
    )


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete application",
    description="Soft delete an application."
)
def delete_application(
    application_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Soft delete an application.
    
    Sets deleted_at timestamp instead of hard delete.
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.deleted_at.is_(None)
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )
    
    application.soft_delete()
    db.commit()
    
    return None
