"""
StatusManager Service

Enforces business rules for application status transitions.

Business Rules:
1. Status flow: SUBMITTED → SCREENING → INTERVIEW_SCHEDULED → INTERVIEWED → OFFER_EXTENDED → HIRED
2. Can transition to REJECTED from any non-terminal state
3. Cannot revert from REJECTED (terminal state)
4. Cannot revert from HIRED (terminal state)
5. No stage skipping allowed
6. All transitions logged in StatusHistory
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from uuid import UUID

from app.models.application import Application
from app.models.status_history import StatusHistory
from app.utils.enums import ApplicationStatus, STATUS_TRANSITIONS


class StatusValidationError(Exception):
    """Custom exception for status validation errors."""
    
    def __init__(self, message: str, current_status: str, new_status: str):
        self.message = message
        self.current_status = current_status
        self.new_status = new_status
        super().__init__(self.message)


class StatusManager:
    """
    Service class for managing application status transitions.
    
    Enforces all business rules and maintains audit trail.
    """
    
    @staticmethod
    def get_allowed_next_statuses(current_status: ApplicationStatus) -> List[str]:
        """
        Get list of allowed next statuses from current status.
        
        Args:
            current_status: Current application status
            
        Returns:
            List of allowed status values (as strings)
            
        Example:
            >>> StatusManager.get_allowed_next_statuses(ApplicationStatus.SUBMITTED)
            ['SCREENING', 'REJECTED']
        """
        allowed = STATUS_TRANSITIONS.get(current_status, [])
        return [s.value for s in allowed]
    
    @staticmethod
    def validate_status_transition(
        current_status: ApplicationStatus,
        new_status: ApplicationStatus
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate if status transition is allowed.
        
        Args:
            current_status: Current application status
            new_status: Desired new status
            
        Returns:
            Tuple of (is_valid, error_message)
            - (True, None) if transition is valid
            - (False, error_message) if transition is invalid
            
        Business Rules Enforced:
        1. No self-transitions (status must change)
        2. No reverting from terminal states (HIRED, REJECTED)
        3. No skipping stages (must follow defined flow)
        4. Only allowed transitions from STATUS_TRANSITIONS dict
        """
        # Rule 1: No self-transitions
        if current_status == new_status:
            return False, f"Status is already {current_status.value}. No change needed."
        
        # Rule 2: Cannot transition from terminal states
        if current_status == ApplicationStatus.HIRED:
            return False, (
                f"Cannot change status from HIRED (terminal state). "
                f"Application has been finalized."
            )
        
        if current_status == ApplicationStatus.REJECTED:
            return False, (
                f"Cannot change status from REJECTED (terminal state). "
                f"Rejected applications cannot be reopened."
            )
        
        # Rule 3 & 4: Check if transition is in allowed list
        allowed_transitions = STATUS_TRANSITIONS.get(current_status, [])
        
        if new_status not in allowed_transitions:
            allowed_statuses = [s.value for s in allowed_transitions]
            
            if not allowed_statuses:
                return False, (
                    f"No transitions allowed from {current_status.value} (terminal state)."
                )
            
            return False, (
                f"Invalid status transition: {current_status.value} → {new_status.value}. "
                f"Allowed transitions from {current_status.value}: {', '.join(allowed_statuses)}. "
                f"Stage skipping is not permitted."
            )
        
        # Transition is valid
        return True, None
    
    @staticmethod
    def update_application_status(
        db: Session,
        app_id: UUID,
        new_status: ApplicationStatus,
        changed_by: str,
        notes: Optional[str] = None
    ) -> Application:
        """
        Update application status with validation and audit trail.
        
        Args:
            db: Database session
            app_id: Application UUID
            new_status: Desired new status
            changed_by: User ID or email making the change
            notes: Optional notes about the status change
            
        Returns:
            Updated Application object
            
        Raises:
            HTTPException(404): If application not found
            HTTPException(400): If status transition is invalid
            HTTPException(500): If database error occurs
            
        Process:
        1. Fetch application from database
        2. Validate status transition (before DB commit)
        3. Update application status
        4. Create StatusHistory entry
        5. Commit transaction
        6. Return updated application
        """
        # Step 1: Fetch application
        application = db.query(Application).filter(
            Application.id == app_id
        ).first()
        
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {app_id} not found"
            )
        
        # Check if application is soft-deleted
        if application.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {app_id} has been deleted"
            )
        
        current_status = application.status
        
        # Step 2: Validate transition (BEFORE DB commit)
        is_valid, error_message = StatusManager.validate_status_transition(
            current_status=current_status,
            new_status=new_status
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid status transition",
                    "message": error_message,
                    "current_status": current_status.value,
                    "requested_status": new_status.value,
                    "allowed_statuses": StatusManager.get_allowed_next_statuses(current_status)
                }
            )
        
        try:
            # Step 3: Update application status
            old_status = application.status
            application.status = new_status
            application.updated_at = datetime.now(timezone.utc)
            
            # Step 4: Create StatusHistory entry (audit trail)
            history_entry = StatusHistory(
                application_id=application.id,
                from_status=old_status.value,
                to_status=new_status.value,
                changed_by=changed_by,
                notes=notes,
                changed_at=datetime.now(timezone.utc)
            )
            
            db.add(history_entry)
            
            # Step 5: Commit transaction
            db.commit()
            db.refresh(application)
            
            # Step 6: Return updated application
            return application
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update application status: {str(e)}"
            )
    
    @staticmethod
    def get_status_flow_diagram() -> str:
        """
        Get ASCII diagram of status flow.
        
        Returns:
            String representation of status flow
        """
        return """
        Application Status Flow:
        
        SUBMITTED
            ├─→ SCREENING
            │       ├─→ INTERVIEW_SCHEDULED
            │       │       ├─→ INTERVIEWED
            │       │       │       ├─→ OFFER_EXTENDED
            │       │       │       │       ├─→ HIRED (Terminal)
            │       │       │       │       └─→ REJECTED (Terminal)
            │       │       │       └─→ REJECTED (Terminal)
            │       │       └─→ REJECTED (Terminal)
            │       └─→ REJECTED (Terminal)
            └─→ REJECTED (Terminal)
        
        Rules:
        - Must follow sequential flow (no skipping)
        - Can reject at any stage
        - Cannot revert from HIRED or REJECTED
        """
    
    @staticmethod
    def get_status_statistics(db: Session, job_id: Optional[UUID] = None) -> dict:
        """
        Get statistics about status transitions.
        
        Args:
            db: Database session
            job_id: Optional job ID to filter by
            
        Returns:
            Dictionary with status statistics
        """
        from sqlalchemy import func
        
        query = db.query(
            Application.status,
            func.count(Application.id).label('count')
        )
        
        if job_id:
            query = query.filter(Application.job_id == job_id)
        
        # Filter out soft-deleted applications
        query = query.filter(Application.deleted_at.is_(None))
        
        results = query.group_by(Application.status).all()
        
        return {
            status.value: count
            for status, count in results
        }
    
    @staticmethod
    def bulk_validate_transitions(
        transitions: List[Tuple[ApplicationStatus, ApplicationStatus]]
    ) -> List[dict]:
        """
        Validate multiple status transitions at once.
        
        Args:
            transitions: List of (current_status, new_status) tuples
            
        Returns:
            List of validation results with details
        """
        results = []
        
        for current, new in transitions:
            is_valid, error_message = StatusManager.validate_status_transition(current, new)
            results.append({
                "current_status": current.value,
                "new_status": new.value,
                "is_valid": is_valid,
                "error_message": error_message,
                "allowed_next": StatusManager.get_allowed_next_statuses(current)
            })
        
        return results
