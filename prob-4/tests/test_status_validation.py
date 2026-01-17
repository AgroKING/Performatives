"""
Test Status Validation and Business Rules

Tests all status transition scenarios and business logic.
"""

import pytest
from fastapi import HTTPException

from app.services.status_manager import StatusManager
from app.utils.enums import ApplicationStatus, STATUS_TRANSITIONS
from app.models.application import Application


class TestStatusTransitionValidation:
    """Test status transition validation logic."""
    
    @pytest.mark.parametrize("current,new,expected_valid", [
        # Valid transitions
        (ApplicationStatus.SUBMITTED, ApplicationStatus.SCREENING, True),
        (ApplicationStatus.SUBMITTED, ApplicationStatus.REJECTED, True),
        (ApplicationStatus.SCREENING, ApplicationStatus.INTERVIEW_SCHEDULED, True),
        (ApplicationStatus.SCREENING, ApplicationStatus.REJECTED, True),
        (ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.INTERVIEWED, True),
        (ApplicationStatus.INTERVIEWED, ApplicationStatus.OFFER_EXTENDED, True),
        (ApplicationStatus.OFFER_EXTENDED, ApplicationStatus.HIRED, True),
        (ApplicationStatus.OFFER_EXTENDED, ApplicationStatus.REJECTED, True),
        
        # Invalid transitions (stage skipping)
        (ApplicationStatus.SUBMITTED, ApplicationStatus.INTERVIEWED, False),
        (ApplicationStatus.SUBMITTED, ApplicationStatus.OFFER_EXTENDED, False),
        (ApplicationStatus.SUBMITTED, ApplicationStatus.HIRED, False),
        (ApplicationStatus.SCREENING, ApplicationStatus.OFFER_EXTENDED, False),
        
        # Invalid transitions (terminal states)
        (ApplicationStatus.HIRED, ApplicationStatus.SCREENING, False),
        (ApplicationStatus.HIRED, ApplicationStatus.REJECTED, False),
        (ApplicationStatus.REJECTED, ApplicationStatus.SUBMITTED, False),
        (ApplicationStatus.REJECTED, ApplicationStatus.SCREENING, False),
        (ApplicationStatus.REJECTED, ApplicationStatus.HIRED, False),
        
        # Self-transitions
        (ApplicationStatus.SUBMITTED, ApplicationStatus.SUBMITTED, False),
        (ApplicationStatus.SCREENING, ApplicationStatus.SCREENING, False),
    ])
    def test_validate_status_transition(self, current, new, expected_valid):
        """Test status transition validation with various scenarios."""
        is_valid, error_message = StatusManager.validate_status_transition(current, new)
        
        assert is_valid == expected_valid
        
        if not expected_valid:
            assert error_message is not None
            assert len(error_message) > 0
        else:
            assert error_message is None
    
    def test_get_allowed_next_statuses(self):
        """Test getting allowed next statuses."""
        # SUBMITTED can go to SCREENING or REJECTED
        allowed = StatusManager.get_allowed_next_statuses(ApplicationStatus.SUBMITTED)
        assert "SCREENING" in allowed
        assert "REJECTED" in allowed
        assert len(allowed) == 2
        
        # HIRED has no allowed transitions (terminal)
        allowed = StatusManager.get_allowed_next_statuses(ApplicationStatus.HIRED)
        assert len(allowed) == 0
        
        # REJECTED has no allowed transitions (terminal)
        allowed = StatusManager.get_allowed_next_statuses(ApplicationStatus.REJECTED)
        assert len(allowed) == 0
    
    def test_prevent_reverting_from_rejected(self):
        """Test that rejected applications cannot be reopened."""
        is_valid, error = StatusManager.validate_status_transition(
            ApplicationStatus.REJECTED,
            ApplicationStatus.SCREENING
        )
        
        assert not is_valid
        assert "terminal state" in error.lower()
        assert "rejected" in error.lower()
    
    def test_prevent_reverting_from_hired(self):
        """Test that hired applications cannot be changed."""
        is_valid, error = StatusManager.validate_status_transition(
            ApplicationStatus.HIRED,
            ApplicationStatus.OFFER_EXTENDED
        )
        
        assert not is_valid
        assert "terminal state" in error.lower()
        assert "hired" in error.lower()
    
    def test_no_stage_skipping(self):
        """Test that stage skipping is prevented."""
        is_valid, error = StatusManager.validate_status_transition(
            ApplicationStatus.SUBMITTED,
            ApplicationStatus.INTERVIEWED
        )
        
        assert not is_valid
        assert "stage skipping" in error.lower() or "invalid" in error.lower()


class TestStatusManagerService:
    """Test StatusManager service methods."""
    
    def test_update_application_status_success(self, db_session, test_application):
        """Test successful status update."""
        updated_app = StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.SCREENING,
            changed_by="recruiter@example.com",
            notes="Moving to screening phase"
        )
        
        assert updated_app.status == ApplicationStatus.SCREENING
        assert len(updated_app.status_history) == 1
        assert updated_app.status_history[0].to_status == "SCREENING"
        assert updated_app.status_history[0].changed_by == "recruiter@example.com"
    
    def test_update_application_status_invalid_transition(self, db_session, test_application):
        """Test invalid status transition raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            StatusManager.update_application_status(
                db=db_session,
                app_id=test_application.id,
                new_status=ApplicationStatus.HIRED,  # Skip stages
                changed_by="recruiter@example.com"
            )
        
        assert exc_info.value.status_code == 400
        assert "invalid" in str(exc_info.value.detail).lower()
    
    def test_update_application_status_not_found(self, db_session):
        """Test updating non-existent application."""
        import uuid
        
        with pytest.raises(HTTPException) as exc_info:
            StatusManager.update_application_status(
                db=db_session,
                app_id=uuid.uuid4(),
                new_status=ApplicationStatus.SCREENING,
                changed_by="recruiter@example.com"
            )
        
        assert exc_info.value.status_code == 404
    
    def test_status_history_created(self, db_session, test_application):
        """Test that status history is created on update."""
        # Update status
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.SCREENING,
            changed_by="recruiter@example.com",
            notes="Test notes"
        )
        
        # Check history
        db_session.refresh(test_application)
        assert len(test_application.status_history) == 1
        
        history = test_application.status_history[0]
        assert history.from_status == "SUBMITTED"
        assert history.to_status == "SCREENING"
        assert history.notes == "Test notes"
    
    def test_multiple_status_transitions(self, db_session, test_application):
        """Test multiple sequential status transitions."""
        # SUBMITTED → SCREENING
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.SCREENING,
            changed_by="recruiter@example.com"
        )
        
        # SCREENING → INTERVIEW_SCHEDULED
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.INTERVIEW_SCHEDULED,
            changed_by="recruiter@example.com"
        )
        
        # INTERVIEW_SCHEDULED → INTERVIEWED
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.INTERVIEWED,
            changed_by="recruiter@example.com"
        )
        
        db_session.refresh(test_application)
        assert test_application.status == ApplicationStatus.INTERVIEWED
        assert len(test_application.status_history) == 3
    
    def test_bulk_validate_transitions(self):
        """Test bulk validation of transitions."""
        transitions = [
            (ApplicationStatus.SUBMITTED, ApplicationStatus.SCREENING),
            (ApplicationStatus.SUBMITTED, ApplicationStatus.HIRED),  # Invalid
            (ApplicationStatus.REJECTED, ApplicationStatus.SCREENING),  # Invalid
        ]
        
        results = StatusManager.bulk_validate_transitions(transitions)
        
        assert len(results) == 3
        assert results[0]["is_valid"] is True
        assert results[1]["is_valid"] is False
        assert results[2]["is_valid"] is False
