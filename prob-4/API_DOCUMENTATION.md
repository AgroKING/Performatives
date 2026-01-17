# API Documentation

Complete reference for all ATS API endpoints with curl examples, request/response samples, and error codes.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require JWT authentication.

**Header Format:**
```
Authorization: Bearer {access_token}
```

---

## 🔐 Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "SecurePass123",
    "role": "CANDIDATE"
  }'
```

**Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "john.doe@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "CANDIDATE",
  "is_active": true,
  "created_at": "2026-01-17T10:00:00Z",
  "last_login": null
}
```

---

### Login

Authenticate and receive JWT token.

**Endpoint:** `POST /auth/login`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "CANDIDATE",
    "is_active": true,
    "created_at": "2026-01-17T10:00:00Z",
    "last_login": "2026-01-17T11:00:00Z"
  }
}
```

---

### Get Current User

Get authenticated user information.

**Endpoint:** `GET /auth/me`

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer {access_token}"
```

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "john.doe@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "CANDIDATE",
  "is_active": true,
  "created_at": "2026-01-17T10:00:00Z",
  "last_login": "2026-01-17T11:00:00Z"
}
```

---

## 📋 Application Endpoints

### Create Application

Submit a new job application.

**Endpoint:** `POST /applications/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/applications/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "123e4567-e89b-12d3-a456-426614174001",
    "job_id": "123e4567-e89b-12d3-a456-426614174002",
    "cover_letter": "I am very interested in this position...",
    "score": 85
  }'
```

**Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174003",
  "candidate_id": "123e4567-e89b-12d3-a456-426614174001",
  "job_id": "123e4567-e89b-12d3-a456-426614174002",
  "status": "SUBMITTED",
  "cover_letter": "I am very interested in this position...",
  "score": 85,
  "submitted_at": "2026-01-17T11:00:00Z",
  "updated_at": "2026-01-17T11:00:00Z"
}
```

**Headers:**
```
Location: /api/v1/applications/123e4567-e89b-12d3-a456-426614174003
```

---

### Get Application

Retrieve application with status history.

**Endpoint:** `GET /applications/{id}`

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/applications/123e4567-e89b-12d3-a456-426614174003 \
  -H "Authorization: Bearer {access_token}"
```

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174003",
  "candidate_id": "123e4567-e89b-12d3-a456-426614174001",
  "job_id": "123e4567-e89b-12d3-a456-426614174002",
  "status": "SCREENING",
  "submitted_at": "2026-01-17T11:00:00Z",
  "updated_at": "2026-01-17T11:30:00Z",
  "status_history": [
    {
      "id": "history-uuid",
      "from_status": "SUBMITTED",
      "to_status": "SCREENING",
      "changed_by": "recruiter@example.com",
      "notes": "Moving to screening phase",
      "changed_at": "2026-01-17T11:30:00Z"
    }
  ]
}
```

---

### Update Application Status

Change application status with validation.

**Endpoint:** `PATCH /applications/{id}/status`

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/v1/applications/123e4567-e89b-12d3-a456-426614174003/status \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "new_status": "SCREENING",
    "changed_by": "recruiter@example.com",
    "notes": "Candidate meets initial requirements"
  }'
```

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174003",
  "status": "SCREENING",
  "updated_at": "2026-01-17T11:30:00Z"
}
```

---

### List Applications (Advanced Search)

Search and filter applications with pagination.

**Endpoint:** `GET /applications/`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/applications/?candidate_email=john&status=SCREENING,INTERVIEWED&page=1&per_page=20&sort_by=updated_at&order=desc" \
  -H "Authorization: Bearer {access_token}"
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "uuid",
      "candidate_id": "uuid",
      "job_id": "uuid",
      "status": "SCREENING",
      "submitted_at": "2026-01-17T10:00:00Z",
      "updated_at": "2026-01-17T11:00:00Z"
    }
  ],
  "metadata": {
    "total": 150,
    "page": 1,
    "per_page": 20,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### Get Advanced Statistics

Comprehensive analytics with Chart.js-ready data.

**Endpoint:** `GET /applications/stats/advanced`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/applications/stats/advanced?date_from=2026-01-01&date_to=2026-01-31" \
  -H "Authorization: Bearer {access_token}"
```

**Response (200 OK):**
```json
{
  "total_applications": 150,
  "date_range": {
    "from": "2026-01-01",
    "to": "2026-01-31"
  },
  "status_breakdown": [
    {"status": "SUBMITTED", "count": 50, "percentage": 33.33},
    {"status": "SCREENING", "count": 40, "percentage": 26.67}
  ],
  "conversion_metrics": {
    "applied_to_screening": 80.0,
    "screening_to_interview": 75.0,
    "interview_to_offer": 60.0,
    "offer_to_hired": 85.0,
    "overall_conversion": 30.6
  },
  "funnel_data": {
    "labels": ["Applied", "Screening", "Interview", "Offer", "Hired"],
    "values": [100, 80, 60, 40, 30],
    "colors": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
  },
  "daily_trends": {
    "labels": ["2026-01-01", "2026-01-02"],
    "values": [5, 8]
  }
}
```

---

## 👤 Candidate Endpoints

### Create Candidate

**Endpoint:** `POST /candidates/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/candidates/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@example.com",
    "full_name": "Jane Smith",
    "phone": "+1234567890",
    "skills": ["Python", "FastAPI", "PostgreSQL"]
  }'
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "email": "candidate@example.com",
  "full_name": "Jane Smith",
  "phone": "+1234567890",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "created_at": "2026-01-17T11:00:00Z"
}
```

---

### Get Candidate Applications

**Endpoint:** `GET /candidates/{id}/applications`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/candidates/123e4567-e89b-12d3-a456-426614174001/applications?page=1&per_page=20" \
  -H "Authorization: Bearer {access_token}"
```

**Response (200 OK):**
```json
{
  "applications": [...],
  "total": 5,
  "skip": 0,
  "limit": 20,
  "has_more": false
}
```

---

## 💼 Job Endpoints

### Create Job

**Endpoint:** `POST /jobs/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/jobs/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Engineer",
    "department": "Engineering",
    "description": "We are looking for...",
    "required_skills": ["Python", "FastAPI"],
    "location": "San Francisco, CA",
    "employment_type": "Full-time",
    "salary_min": 120000,
    "salary_max": 180000
  }'
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "title": "Senior Backend Engineer",
  "department": "Engineering",
  "status": "OPEN",
  "created_at": "2026-01-17T11:00:00Z"
}
```

---

### Get Job Applications

**Endpoint:** `GET /jobs/{id}/applications`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/123e4567-e89b-12d3-a456-426614174002/applications?status_filter=SUBMITTED&page=1" \
  -H "Authorization: Bearer {access_token}"
```

**Response (200 OK):**
```json
{
  "applications": [...],
  "total": 25,
  "skip": 0,
  "limit": 50,
  "has_more": false,
  "status_filter": "SUBMITTED"
}
```

---

## ⚠️ Error Codes and Meanings

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request data or business rule violation |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "detail": "Error message or detailed object"
}
```

### Common Errors

**Invalid Status Transition (400):**
```json
{
  "detail": {
    "error": "Invalid status transition",
    "message": "Invalid status transition: SUBMITTED → HIRED. Stage skipping is not permitted.",
    "current_status": "SUBMITTED",
    "requested_status": "HIRED",
    "allowed_statuses": ["SCREENING", "REJECTED"]
  }
}
```

**Unauthorized (401):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Forbidden (403):**
```json
{
  "detail": "Access denied. Required role: ['ADMIN']"
}
```

**Not Found (404):**
```json
{
  "detail": "Application with ID {id} not found"
}
```

**Validation Error (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 🔄 Authentication Flow

### Complete Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database

    Client->>API: POST /auth/register
    API->>Database: Create user
    Database-->>API: User created
    API-->>Client: 201 Created (user data)

    Client->>API: POST /auth/login
    API->>Database: Verify credentials
    Database-->>API: User found
    API->>API: Generate JWT token
    API-->>Client: 200 OK (token + user)

    Client->>API: GET /applications (with token)
    API->>API: Validate JWT
    API->>Database: Fetch applications
    Database-->>API: Applications data
    API-->>Client: 200 OK (applications)
```

### Token Usage

**1. Store token after login:**
```javascript
const response = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

const { access_token } = await response.json();
localStorage.setItem('token', access_token);
```

**2. Use token in requests:**
```javascript
const token = localStorage.getItem('token');

const response = await fetch('/api/v1/applications', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

**3. Handle token expiration:**
```javascript
if (response.status === 401) {
  // Token expired, redirect to login
  window.location.href = '/login';
}
```

---

**Documentation Version**: 1.0.0  
**Last Updated**: 2026-01-17
