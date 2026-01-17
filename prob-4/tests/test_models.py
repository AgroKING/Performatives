"""
Test SQLAlchemy Models

Tests model constraints, relationships, and methods.
"""

import pytest
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.models.status_history import StatusHistory
from app.models.user import User, UserRole
from app.utils.enums import ApplicationStatus, JobStatus
from app.utils.auth import get_password_hash


class TestCandidateModel:
    """Test Candidate model."""
    
    def test_create_candidate(self, db_session):
        """Test creating a candidate."""
        candidate = Candidate(
            email="test@example.com",
            full_name="Test User",
            skills=["Python", "FastAPI"]
        )
        db_session.add(candidate)
        db_session.commit()
        
        assert candidate.id is not None
        assert candidate.email == "test@example.com"
        assert candidate.created_at is not None
        assert candidate.deleted_at is None
    
    def test_candidate_unique_email(self, db_session):
        """Test that email must be unique."""
        candidate1 = Candidate(email="test@example.com", full_name="User 1")
        db_session.add(candidate1)
        db_session.commit()
        
        candidate2 = Candidate(email="test@example.com", full_name="User 2")
        db_session.add(candidate2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_candidate_soft_delete(self, db_session, test_candidate):
        """Test soft delete functionality."""
        assert test_candidate.deleted_at is None
        assert not test_candidate.is_deleted
        
        test_candidate.soft_delete()
        db_session.commit()
        
        assert test_candidate.deleted_at is not None
        assert test_candidate.is_deleted


class TestJobModel:
    """Test Job model."""
    
    def test_create_job(self, db_session):
        """Test creating a job."""
        job = Job(
            title="Software Engineer",
            department="Engineering",
            description="Great opportunity",
            location="Remote",
            employment_type="Full-time",
            status=JobStatus.OPEN
        )
        db_session.add(job)
        db_session.commit()
        
        assert job.id is not None
        assert job.status == JobStatus.OPEN
        assert job.is_open
    
    def test_job_soft_delete(self, db_session, test_job):
        """Test job soft delete."""
        test_job.soft_delete()
        db_session.commit()
        
        assert test_job.deleted_at is not None
        assert test_job.status == JobStatus.CLOSED
        assert not test_job.is_open


class TestApplicationModel:
    """Test Application model."""
    
    def test_create_application(self, db_session, test_candidate, test_job):
        """Test creating an application."""
        application = Application(
            candidate_id=test_candidate.id,
            job_id=test_job.id,
            status=ApplicationStatus.SUBMITTED
        )
        db_session.add(application)
        db_session.commit()
        
        assert application.id is not None
        assert application.status == ApplicationStatus.SUBMITTED
        assert application.submitted_at is not None
    
    def test_application_unique_constraint(self, db_session, test_candidate, test_job):
        """Test unique constraint on candidate_id + job_id."""
        app1 = Application(
            candidate_id=test_candidate.id,
            job_id=test_job.id,
            status=ApplicationStatus.SUBMITTED
        )
        db_session.add(app1)
        db_session.commit()
        
        app2 = Application(
            candidate_id=test_candidate.id,
            job_id=test_job.id,
            status=ApplicationStatus.SUBMITTED
        )
        db_session.add(app2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_application_relationships(self, db_session, test_application):
        """Test application relationships."""
        assert test_application.candidate is not None
        assert test_application.job is not None
        assert test_application.candidate.full_name == "John Doe"
        assert test_application.job.title == "Senior Backend Engineer"
    
    def test_application_terminal_status(self, db_session, test_application):
        """Test terminal status check."""
        assert not test_application.is_terminal_status
        
        test_application.status = ApplicationStatus.HIRED
        assert test_application.is_terminal_status
        
        test_application.status = ApplicationStatus.REJECTED
        assert test_application.is_terminal_status


class TestStatusHistoryModel:
    """Test StatusHistory model."""
    
    def test_create_status_history(self, db_session, test_application):
        """Test creating status history entry."""
        history = StatusHistory(
            application_id=test_application.id,
            from_status="SUBMITTED",
            to_status="SCREENING",
            changed_by="recruiter@example.com",
            notes="Moving to screening"
        )
        db_session.add(history)
        db_session.commit()
        
        assert history.id is not None
        assert history.changed_at is not None
        assert history.transition_description == "SUBMITTED → SCREENING"


class TestUserModel:
    """Test User model."""
    
    def test_create_user(self, db_session):
        """Test creating a user."""
        user = User(
            email="user@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password=get_password_hash("password123"),
            role=UserRole.CANDIDATE
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.role == UserRole.CANDIDATE
        assert user.is_active
    
    def test_user_unique_email(self, db_session):
        """Test user email uniqueness."""
        user1 = User(
            email="same@example.com",
            username="user1",
            full_name="User 1",
            hashed_password="hash1",
            role=UserRole.CANDIDATE
        )
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(
            email="same@example.com",
            username="user2",
            full_name="User 2",
            hashed_password="hash2",
            role=UserRole.CANDIDATE
        )
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_unique_username(self, db_session):
        """Test user username uniqueness."""
        user1 = User(
            email="user1@example.com",
            username="sameusername",
            full_name="User 1",
            hashed_password="hash1",
            role=UserRole.CANDIDATE
        )
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(
            email="user2@example.com",
            username="sameusername",
            full_name="User 2",
            hashed_password="hash2",
            role=UserRole.CANDIDATE
        )
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
