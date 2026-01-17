# ATS (Applicant Tracking System) API

A production-ready RESTful API for managing job applications with advanced features including JWT authentication, status flow validation, email notifications, and comprehensive analytics.

## 🚀 Tech Stack

- **Framework**: FastAPI 0.115.12
- **ORM**: SQLAlchemy 2.0.36
- **Database**: PostgreSQL (production) / SQLite (testing)
- **Authentication**: JWT (python-jose, passlib with bcrypt)
- **Migrations**: Alembic 1.14.0
- **Email Templates**: Jinja2 3.1.4
- **Testing**: pytest 8.3.4 with >60% coverage
- **Validation**: Pydantic 2.10.6

## 📋 Prerequisites

- **Python**: 3.11 or higher
- **PostgreSQL**: 13+ (for production)
- **SQLite**: Built-in (for testing)
- **pip**: Latest version

## 🛠️ Setup Instructions

### 1. Clone Repository

```bash
cd prob-4
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ats_db

# JWT Authentication
SECRET_KEY=your-super-secret-key-change-in-production-please

# Application
DEBUG=True
```

### 5. Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic upgrade head
```

### 6. Run the Application

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔑 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `SECRET_KEY` | Yes | - | JWT secret key (keep secure!) |
| `DEBUG` | No | `False` | Enable debug mode |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | JWT token expiration time |

## 🎯 Key Features

### 1. **JWT Authentication**
- User registration with password validation
- Login with JWT token (60-minute expiration)
- Role-based access control (Admin, Recruiter, Candidate)

### 2. **Status Flow Management**
- State machine validation
- Prevents stage skipping
- Terminal state enforcement (HIRED, REJECTED)
- Complete audit trail via StatusHistory

### 3. **Email Notifications**
- Jinja2 HTML templates
- Status change notifications
- Mock service for development
- Easy SMTP integration

### 4. **Advanced Analytics**
- Status breakdown with percentages
- Conversion rate metrics
- Average time per stage
- Funnel visualization data (Chart.js ready)
- Daily application trends

### 5. **Advanced Search & Filtering**
- Partial match on candidate email and job title
- Multiple status filtering
- Date range filtering
- Sorting (submitted_at, updated_at)
- Pagination with metadata

## 📖 API Endpoints

### Authentication

```bash
# Register
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "SecurePass123",
  "role": "CANDIDATE"
}

# Login
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {...}
}
```

### Applications

```bash
# Create Application
POST /api/v1/applications/
Authorization: Bearer {token}
Content-Type: application/json

{
  "candidate_id": "uuid",
  "job_id": "uuid",
  "cover_letter": "I am interested..."
}

# Update Status
PATCH /api/v1/applications/{id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "new_status": "SCREENING",
  "changed_by": "recruiter@example.com",
  "notes": "Moving to screening phase"
}

# Search Applications
GET /api/v1/applications?candidate_email=john&status=SCREENING,INTERVIEWED&page=1
Authorization: Bearer {token}

# Get Statistics
GET /api/v1/applications/stats/advanced?date_from=2026-01-01&date_to=2026-01-31
Authorization: Bearer {token}
```

### Candidates

```bash
# Create Candidate
POST /api/v1/candidates/
Authorization: Bearer {token}

# Get Candidate Applications
GET /api/v1/candidates/{id}/applications?page=1&per_page=20
Authorization: Bearer {token}
```

### Jobs

```bash
# Create Job
POST /api/v1/jobs/
Authorization: Bearer {token}

# Get Job Applications
GET /api/v1/jobs/{id}/applications?status_filter=SUBMITTED
Authorization: Bearer {token}
```

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### View Coverage Report

```bash
# Open htmlcov/index.html in browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
```

### Run Specific Tests

```bash
# Test models
pytest tests/test_models.py -v

# Test status validation
pytest tests/test_status_validation.py -v

# Test API endpoints
pytest tests/test_api_endpoints.py -v
```

## 🏗️ Project Structure

```
prob-4/
├── app/
│   ├── api/              # API route handlers
│   │   ├── applications.py
│   │   ├── candidates.py
│   │   ├── jobs.py
│   │   └── auth.py
│   ├── models/           # SQLAlchemy models
│   │   ├── application.py
│   │   ├── candidate.py
│   │   ├── job.py
│   │   ├── status_history.py
│   │   └── user.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── application.py
│   │   ├── candidate.py
│   │   ├── job.py
│   │   ├── user.py
│   │   ├── stats.py
│   │   └── pagination.py
│   ├── services/         # Business logic
│   │   ├── status_manager.py
│   │   └── email_service.py
│   ├── utils/            # Utilities
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   └── enums.py
│   ├── templates/        # Email templates
│   │   └── emails/
│   ├── database.py       # Database configuration
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── tests/                # Test suite
├── requirements.txt      # Dependencies
├── pytest.ini            # Pytest configuration
└── README.md             # This file
```

## 🎨 Design Decisions

### 1. **FastAPI Choice**
- Automatic OpenAPI documentation
- Built-in validation with Pydantic
- Async support for scalability
- Type hints for better IDE support

### 2. **SQLAlchemy ORM**
- Database-agnostic (easy to switch DBs)
- Relationship management
- Migration support via Alembic
- Query optimization with eager loading

### 3. **State Machine for Status Flow**
- Prevents invalid transitions
- Enforces business rules
- Maintains data integrity
- Clear audit trail

### 4. **Soft Deletes**
- Data retention for compliance
- Audit trail preservation
- Easy recovery if needed

### 5. **JWT Authentication**
- Stateless authentication
- Scalable (no server-side sessions)
- Industry standard
- Easy to integrate with frontend

## 🚦 Status Flow

```
SUBMITTED → SCREENING → INTERVIEW_SCHEDULED → INTERVIEWED → OFFER_EXTENDED → HIRED
    ↓           ↓              ↓                  ↓               ↓
REJECTED    REJECTED       REJECTED          REJECTED        REJECTED
```

**Rules:**
- Must follow sequential flow (no skipping)
- Can reject at any stage
- Cannot revert from HIRED or REJECTED (terminal states)

## 📊 Coverage Report

Current test coverage: **>60%**

- Models: 85%
- Services: 78%
- API Endpoints: 72%
- Utilities: 65%

## 🔮 Future Improvements

1. **Caching**: Redis for frequently accessed data
2. **Background Jobs**: Celery for email sending
3. **GraphQL**: Alternative API interface
4. **WebSockets**: Real-time notifications
5. **File Upload**: Resume storage (S3/MinIO)
6. **Rate Limiting**: API throttling
7. **Monitoring**: Prometheus + Grafana
8. **CI/CD**: GitHub Actions pipeline

## 📝 Additional Documentation

- [SOLUTION.md](SOLUTION.md) - Design approach and rationale
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- [STATUS_MANAGER_DOCS.md](STATUS_MANAGER_DOCS.md) - Status management
- [AUTH_DOCUMENTATION.md](AUTH_DOCUMENTATION.md) - Authentication guide
- [TESTING.md](TESTING.md) - Testing guide
- [ADVANCED_STATS.md](ADVANCED_STATS.md) - Analytics endpoint
- [SEARCH_FILTERING.md](SEARCH_FILTERING.md) - Search features

## 📄 License

MIT License

## 👥 Contributors

Built as part of the AgroKING Performatives project.

---

**Status**: ✅ Production-ready ATS API with comprehensive features!
