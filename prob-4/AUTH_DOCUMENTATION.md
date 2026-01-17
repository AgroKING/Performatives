# JWT Authentication System - Complete Documentation

## ✅ Implementation Complete

### Components Created

**1. User Model** (`app/models/user.py`)
- UUID primary key
- Email (unique, indexed)
- Username (unique, indexed)
- Hashed password (bcrypt)
- Full name
- Role enum (ADMIN, RECRUITER, CANDIDATE)
- is_active flag
- Timestamps (created_at, updated_at, last_login)

**2. Authentication Utilities** (`app/utils/auth.py`)
- `verify_password()` - Bcrypt password verification
- `get_password_hash()` - Bcrypt password hashing
- `create_access_token()` - JWT token creation
- `decode_access_token()` - JWT token validation
- 60-minute token expiration

**3. User Schemas** (`app/schemas/user.py`)
- UserRegister - With password validation
- UserLogin - Username/password
- UserResponse - User details (no password)
- Token - JWT token response
- TokenData - Token payload

**4. Dependencies** (`app/utils/dependencies.py`)
- `get_current_user()` - Extract user from JWT
- `get_current_active_user()` - Verify user is active
- `RoleChecker` - Role-based access control class
- Convenience instances: `require_admin`, `require_recruiter`

**5. Auth Router** (`app/api/auth.py`)
- POST /api/v1/auth/register - Create user account
- POST /api/v1/auth/login - Get JWT token
- GET /api/v1/auth/me - Get current user

---

## 🔐 Authentication Flow

### 1. User Registration

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "SecurePass123",
  "role": "CANDIDATE"
}
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
  "created_at": "2026-01-17T11:00:00Z",
  "last_login": null
}
```

### 2. User Login

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "CANDIDATE",
    "is_active": true,
    "created_at": "2026-01-17T11:00:00Z",
    "last_login": "2026-01-17T11:30:00Z"
  }
}
```

### 3. Accessing Protected Endpoints

```bash
GET /api/v1/applications
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🎭 Role-Based Access Control

### User Roles

| Role | Permissions |
|------|-------------|
| **ADMIN** | Full access to all endpoints |
| **RECRUITER** | Manage jobs and applications |
| **CANDIDATE** | View own applications |

### Usage Examples

**Require Admin Only:**
```python
from app.utils.dependencies import require_admin

@router.delete("/jobs/{job_id}", dependencies=[Depends(require_admin)])
def delete_job(job_id: UUID):
    # Only admins can access
    ...
```

**Require Admin or Recruiter:**
```python
from app.utils.dependencies import require_recruiter

@router.patch("/applications/{id}/status", dependencies=[Depends(require_recruiter)])
def update_status(id: UUID):
    # Admins and recruiters can access
    ...
```

**Custom Role Check:**
```python
from app.utils.dependencies import RoleChecker
from app.models.user import UserRole

@router.get("/stats", dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.RECRUITER]))])
def get_stats():
    # Custom role requirements
    ...
```

---

## 🔒 Protected Endpoints

All endpoints are now protected except auth endpoints:

**Public (No Auth Required):**
- POST /api/v1/auth/register
- POST /api/v1/auth/login

**Protected (Requires JWT Token):**
- All /api/v1/applications/* endpoints
- All /api/v1/candidates/* endpoints
- All /api/v1/jobs/* endpoints
- GET /api/v1/auth/me

---

## 🛡️ Password Requirements

Passwords must meet the following criteria:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter
- ✅ At least one lowercase letter
- ✅ At least one digit

**Example Valid Passwords:**
- `SecurePass123`
- `MyP@ssw0rd`
- `Admin2026!`

---

## 🔑 JWT Token Details

**Token Payload:**
```json
{
  "sub": "user-uuid",
  "username": "johndoe",
  "role": "CANDIDATE",
  "exp": 1705492800
}
```

**Token Expiration:** 60 minutes (3600 seconds)

**Algorithm:** HS256

**Secret Key:** Configured via `SECRET_KEY` environment variable

---

## 📝 Environment Variables

Add to `.env`:
```bash
SECRET_KEY=your-super-secret-key-change-in-production
```

---

## 🧪 Testing Authentication

### 1. Register a User
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/auth/register",
    json={
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "TestPass123",
        "role": "CANDIDATE"
    }
)
print(response.json())
```

### 2. Login
```python
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "username": "testuser",
        "password": "TestPass123"
    }
)
token_data = response.json()
access_token = token_data["access_token"]
```

### 3. Access Protected Endpoint
```python
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(
    "http://localhost:8000/api/v1/applications",
    headers=headers
)
print(response.json())
```

---

## ⚠️ Error Responses

**401 Unauthorized** - Invalid or missing token:
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden** - Insufficient permissions:
```json
{
  "detail": "Access denied. Required role: ['ADMIN']"
}
```

**400 Bad Request** - Duplicate email/username:
```json
{
  "detail": "Email already registered"
}
```

---

**Status**: ✅ JWT Authentication System Complete!
