"""
Test API Endpoints

Tests all API endpoints with various scenarios.
"""

import pytest
from app.utils.enums import ApplicationStatus


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_register_user_success(self, client):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "SecurePass123",
            "role": "CANDIDATE"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "hashed_password" not in data
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email."""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",  # Already exists
            "username": "different",
            "full_name": "Different User",
            "password": "SecurePass123"
        })
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post("/api/v1/auth/register", json={
            "email": "weak@example.com",
            "username": "weakpass",
            "full_name": "Weak Pass",
            "password": "weak"  # Too short, no uppercase, no digit
        })
        
        assert response.status_code == 422
    
    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "TestPass123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 3600
        assert data["user"]["username"] == "testuser"
    
    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials."""
        response = client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "WrongPassword"
        })
        
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"


class TestApplicationEndpoints:
    """Test application endpoints."""
    
    def test_create_application_success(self, client, auth_headers, test_candidate, test_job):
        """Test creating an application."""
        response = client.post("/api/v1/applications/", headers=auth_headers, json={
            "candidate_id": str(test_candidate.id),
            "job_id": str(test_job.id),
            "cover_letter": "I am very interested..."
        })
        
        assert response.status_code == 201
        assert "Location" in response.headers
        data = response.json()
        assert data["status"] == "SUBMITTED"
    
    def test_create_application_unauthorized(self, client, test_candidate, test_job):
        """Test creating application without auth."""
        response = client.post("/api/v1/applications/", json={
            "candidate_id": str(test_candidate.id),
            "job_id": str(test_job.id)
        })
        
        assert response.status_code == 401  # No auth header
    
    def test_get_application_by_id(self, client, auth_headers, test_application):
        """Test getting application by ID."""
        response = client.get(
            f"/api/v1/applications/{test_application.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_application.id)
        assert "status_history" in data
    
    def test_get_application_not_found(self, client, auth_headers):
        """Test getting non-existent application."""
        import uuid
        response = client.get(
            f"/api/v1/applications/{uuid.uuid4()}",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_update_application_status(self, client, auth_headers, test_application):
        """Test updating application status."""
        response = client.patch(
            f"/api/v1/applications/{test_application.id}/status",
            headers=auth_headers,
            json={
                "new_status": "SCREENING",
                "changed_by": "recruiter@example.com",
                "notes": "Moving to screening"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SCREENING"
    
    def test_update_application_status_invalid_transition(self, client, auth_headers, test_application):
        """Test invalid status transition."""
        response = client.patch(
            f"/api/v1/applications/{test_application.id}/status",
            headers=auth_headers,
            json={
                "new_status": "HIRED",  # Skip stages
                "changed_by": "recruiter@example.com"
            }
        )
        
        assert response.status_code == 400
    
    def test_list_applications(self, client, auth_headers, test_application):
        """Test listing applications."""
        response = client.get("/api/v1/applications/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 1
    
    def test_list_applications_with_filters(self, client, auth_headers, test_application):
        """Test listing applications with filters."""
        response = client.get(
            "/api/v1/applications/",
            headers=auth_headers,
            params={"status": "SUBMITTED", "per_page": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(app["status"] == "SUBMITTED" for app in data["items"])
    
    def test_get_application_stats(self, client, auth_headers, test_application):
        """Test getting application statistics."""
        response = client.get("/api/v1/applications/stats/advanced", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_applications" in data
        assert "status_breakdown" in data
        assert isinstance(data["status_breakdown"], list)
        assert "conversion_metrics" in data
        assert "avg_time_per_stage" in data
        assert isinstance(data["avg_time_per_stage"], list)


class TestCandidateEndpoints:
    """Test candidate endpoints."""
    
    def test_create_candidate(self, client, auth_headers):
        """Test creating a candidate."""
        response = client.post("/api/v1/candidates/", headers=auth_headers, json={
            "email": "newcandidate@example.com",
            "full_name": "New Candidate",
            "phone": "+1234567890",
            "skills": ["Python", "FastAPI"]
        })
        
        assert response.status_code == 201
        assert "Location" in response.headers
    
    def test_get_candidate(self, client, auth_headers, test_candidate):
        """Test getting candidate by ID."""
        response = client.get(
            f"/api/v1/candidates/{test_candidate.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_candidate.email
    
    def test_get_candidate_applications(self, client, auth_headers, test_candidate, test_application):
        """Test getting candidate's applications."""
        response = client.get(
            f"/api/v1/candidates/{test_candidate.id}/applications",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "applications" in data
        assert "total" in data
        assert data["total"] >= 1


class TestJobEndpoints:
    """Test job endpoints."""
    
    def test_create_job(self, client, auth_headers):
        """Test creating a job."""
        response = client.post("/api/v1/jobs/", headers=auth_headers, json={
            "title": "Software Engineer",
            "department": "Engineering",
            "description": "Great opportunity",
            "required_skills": ["Python"],
            "location": "Remote",
            "employment_type": "Full-time",
            "salary_min": 100000,
            "salary_max": 150000
        })
        
        assert response.status_code == 201
    
    def test_get_job(self, client, auth_headers, test_job):
        """Test getting job by ID."""
        response = client.get(f"/api/v1/jobs/{test_job.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_job.title
    
    def test_get_job_applications(self, client, auth_headers, test_job, test_application):
        """Test getting job's applications."""
        response = client.get(
            f"/api/v1/jobs/{test_job.id}/applications",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "applications" in data
        assert "total" in data
    
    def test_get_job_applications_with_status_filter(self, client, auth_headers, test_job, test_application):
        """Test getting job applications with status filter."""
        response = client.get(
            f"/api/v1/jobs/{test_job.id}/applications",
            headers=auth_headers,
            params={"status_filter": "SUBMITTED"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status_filter"] == "SUBMITTED"
