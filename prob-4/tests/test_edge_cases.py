"""
Test Edge Cases

Tests duplicate applications, concurrent updates, and other edge cases.
"""

import pytest
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.utils.enums import ApplicationStatus
from app.services.status_manager import StatusManager


class TestDuplicateApplications:
    """Test duplicate application prevention."""
    
    def test_duplicate_application_database_constraint(self, db_session, test_candidate, test_job):
        """Test database prevents duplicate applications."""
        app1 = Application(
            candidate_id=test_candidate.id,
            job_id=test_job.id,
            status=ApplicationStatus.SUBMITTED
        )
        db_session.add(app1)
        db_session.commit()
        
        # Try to create duplicate
        app2 = Application(
            candidate_id=test_candidate.id,
            job_id=test_job.id,
            status=ApplicationStatus.SUBMITTED
        )
        db_session.add(app2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_duplicate_application_api_endpoint(self, client, auth_headers, test_candidate, test_job):
        """Test API prevents duplicate applications."""
        # Create first application
        response1 = client.post("/api/v1/applications/", headers=auth_headers, json={
            "candidate_id": str(test_candidate.id),
            "job_id": str(test_job.id)
        })
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post("/api/v1/applications/", headers=auth_headers, json={
            "candidate_id": str(test_candidate.id),
            "job_id": str(test_job.id)
        })
        assert response2.status_code == 400
        assert "already applied" in response2.json()["detail"].lower()
    
    def test_same_candidate_multiple_jobs(self, client, auth_headers, test_candidate, db_session):
        """Test candidate can apply to multiple jobs."""
        job1 = Job(
            title="Job 1",
            department="Dept 1",
            description="Description 1",
            location="Location 1",
            employment_type="Full-time"
        )
        job2 = Job(
            title="Job 2",
            department="Dept 2",
            description="Description 2",
            location="Location 2",
            employment_type="Full-time"
        )
        db_session.add_all([job1, job2])
        db_session.commit()
        
        # Apply to job 1
        response1 = client.post("/api/v1/applications/", headers=auth_headers, json={
            "candidate_id": str(test_candidate.id),
            "job_id": str(job1.id)
        })
        assert response1.status_code == 201
        
        # Apply to job 2 (should succeed)
        response2 = client.post("/api/v1/applications/", headers=auth_headers, json={
            "candidate_id": str(test_candidate.id),
            "job_id": str(job2.id)
        })
        assert response2.status_code == 201


class TestConcurrentUpdates:
    """Test concurrent update scenarios."""
    
    def test_rapid_status_updates(self, db_session, test_application):
        """Test rapid sequential status updates."""
        # Update 1: SUBMITTED → SCREENING
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.SCREENING,
            changed_by="user1@example.com"
        )
        
        # Update 2: SCREENING → INTERVIEW_SCHEDULED
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.INTERVIEW_SCHEDULED,
            changed_by="user2@example.com"
        )
        
        db_session.refresh(test_application)
        assert test_application.status == ApplicationStatus.INTERVIEW_SCHEDULED
        assert len(test_application.status_history) == 2


class TestInvalidTransitions:
    """Test various invalid transition scenarios."""
    
    def test_skip_multiple_stages(self, db_session, test_application):
        """Test skipping multiple stages."""
        with pytest.raises(HTTPException) as exc_info:
            StatusManager.update_application_status(
                db=db_session,
                app_id=test_application.id,
                new_status=ApplicationStatus.OFFER_EXTENDED,
                changed_by="recruiter@example.com"
            )
        
        assert exc_info.value.status_code == 400
    
    def test_backward_transition(self, db_session, test_application):
        """Test backward transition (not allowed)."""
        # Move to SCREENING
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.SCREENING,
            changed_by="recruiter@example.com"
        )
        
        # Try to go back to SUBMITTED (not in allowed transitions)
        with pytest.raises(HTTPException) as exc_info:
            StatusManager.update_application_status(
                db=db_session,
                app_id=test_application.id,
                new_status=ApplicationStatus.SUBMITTED,
                changed_by="recruiter@example.com"
            )
        
        assert exc_info.value.status_code == 400
    
    def test_transition_from_rejected(self, db_session, test_application):
        """Test that rejected applications cannot be updated."""
        # Reject application
        StatusManager.update_application_status(
            db=db_session,
            app_id=test_application.id,
            new_status=ApplicationStatus.REJECTED,
            changed_by="recruiter@example.com"
        )
        
        # Try to update (should fail)
        with pytest.raises(HTTPException) as exc_info:
            StatusManager.update_application_status(
                db=db_session,
                app_id=test_application.id,
                new_status=ApplicationStatus.SCREENING,
                changed_by="recruiter@example.com"
            )
        
        assert exc_info.value.status_code == 400
        assert "terminal" in str(exc_info.value.detail).lower()


class TestSoftDelete:
    """Test soft delete functionality."""
    
    def test_soft_deleted_application_not_listed(self, client, auth_headers, test_application, db_session):
        """Test soft-deleted applications don't appear in listings."""
        # Soft delete
        test_application.soft_delete()
        db_session.commit()
        
        # List applications
        response = client.get("/api/v1/applications/", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        app_ids = [app["id"] for app in data["items"]]
        assert str(test_application.id) not in app_ids
    
    def test_soft_deleted_application_not_found(self, client, auth_headers, test_application, db_session):
        """Test soft-deleted application returns 404."""
        # Soft delete
        test_application.soft_delete()
        db_session.commit()
        
        # Try to get
        response = client.get(
            f"/api/v1/applications/{test_application.id}",
            headers=auth_headers
        )
        assert response.status_code == 404


class TestEdgeCaseData:
    """Test edge cases with data."""
    
    def test_application_with_empty_cover_letter(self, client, auth_headers, test_candidate, test_job):
        """Test application with no cover letter."""
        response = client.post("/api/v1/applications/", headers=auth_headers, json={
            "candidate_id": str(test_candidate.id),
            "job_id": str(test_job.id),
            "cover_letter": None
        })
        
        assert response.status_code == 201
    
    def test_candidate_with_empty_skills(self, client, auth_headers):
        """Test candidate with no skills."""
        response = client.post("/api/v1/candidates/", headers=auth_headers, json={
            "email": "noskills@example.com",
            "full_name": "No Skills",
            "skills": []
        })
        
        assert response.status_code == 201
    
    def test_job_with_no_salary_range(self, client, auth_headers):
        """Test job with no salary specified."""
        response = client.post("/api/v1/jobs/", headers=auth_headers, json={
            "title": "Mystery Salary Job",
            "department": "Engineering",
            "description": "Salary TBD",
            "location": "Remote",
            "employment_type": "Full-time",
            "salary_min": None,
            "salary_max": None
        })
        
        assert response.status_code == 201
    
    def test_pagination_edge_cases(self, client, auth_headers):
        """Test pagination with edge values."""
        # Test with per_page=1 (should return 1 or 0 items)
        response = client.get(
            "/api/v1/applications/",
            headers=auth_headers,
            params={"page": 1, "per_page": 1}
        )
        assert response.status_code == 200
        
        # Test with large page value
        response = client.get(
            "/api/v1/applications/",
            headers=auth_headers,
            params={"page": 1000, "per_page": 10}
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 0
