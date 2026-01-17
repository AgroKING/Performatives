"""
Pytest Configuration and Fixtures

Provides test database, client, and common fixtures.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.utils.auth import get_password_hash, create_access_token
from app.utils.enums import ApplicationStatus, JobStatus, UserRole

# SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database for each test.
    
    Yields:
        Database session
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create FastAPI test client with test database.
    
    Args:
        db_session: Test database session
        
    Yields:
        TestClient instance
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("TestPass123"),
        role=UserRole.CANDIDATE,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin(db_session):
    """Create a test admin user."""
    admin = User(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        hashed_password=get_password_hash("AdminPass123"),
        role=UserRole.ADMIN,
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def test_recruiter(db_session):
    """Create a test recruiter user."""
    recruiter = User(
        email="recruiter@example.com",
        username="recruiter",
        full_name="Recruiter User",
        hashed_password=get_password_hash("RecruiterPass123"),
        role=UserRole.RECRUITER,
        is_active=True
    )
    db_session.add(recruiter)
    db_session.commit()
    db_session.refresh(recruiter)
    return recruiter


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers with JWT token."""
    access_token = create_access_token(
        data={
            "sub": str(test_user.id),
            "username": test_user.username,
            "role": test_user.role.value
        }
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def admin_headers(test_admin):
    """Create admin authentication headers."""
    access_token = create_access_token(
        data={
            "sub": str(test_admin.id),
            "username": test_admin.username,
            "role": test_admin.role.value
        }
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_candidate(db_session):
    """Create a test candidate."""
    candidate = Candidate(
        email="candidate@example.com",
        full_name="John Doe",
        phone="+1234567890",
        skills=["Python", "FastAPI", "PostgreSQL"]
    )
    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)
    return candidate


@pytest.fixture
def test_job(db_session):
    """Create a test job."""
    job = Job(
        title="Senior Backend Engineer",
        department="Engineering",
        description="We are looking for a senior backend engineer...",
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        location="San Francisco, CA",
        employment_type="Full-time",
        salary_min=120000,
        salary_max=180000,
        status=JobStatus.OPEN
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    return job


@pytest.fixture
def test_application(db_session, test_candidate, test_job):
    """Create a test application."""
    application = Application(
        candidate_id=test_candidate.id,
        job_id=test_job.id,
        status=ApplicationStatus.SUBMITTED,
        cover_letter="I am very interested in this position...",
        score=85
    )
    db_session.add(application)
    db_session.commit()
    db_session.refresh(application)
    return application
