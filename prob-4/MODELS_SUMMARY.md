# ATS Database Models - Summary

## ✅ Completed Implementation

### Models Created
1. **Candidate** - `app/models/candidate.py`
2. **Job** - `app/models/job.py`
3. **Application** - `app/models/application.py`
4. **StatusHistory** - `app/models/status_history.py`

### Key Features

#### ✅ All Requirements Met
- [x] Four tables with proper relationships
- [x] Foreign keys with CASCADE delete
- [x] back_populates for bidirectional relationships
- [x] Indexes on: job_id, candidate_id, status, submitted_at (applied_at)
- [x] Timezone-aware timestamps (UTC)
- [x] Soft delete capability (deleted_at field)
- [x] Unique constraint on (candidate_id, job_id)
- [x] Proper __repr__ methods
- [x] Table args for performance optimization

#### Database Configuration
- **File**: `app/database.py`
- SQLAlchemy engine with connection pooling
- SessionLocal for dependency injection
- Base class for all models

#### Enums
- **File**: `app/utils/enums.py`
- ApplicationStatus enum (7 states)
- JobStatus enum (4 states)
- STATUS_TRANSITIONS dict for state machine

#### Alembic Migrations
- **Config**: `alembic.ini`
- **Environment**: `alembic/env.py`
- **Initial Migration**: `alembic/versions/001_initial.py`

### Indexes Created

**Candidates:**
- idx_candidate_email (email)
- idx_candidate_deleted (deleted_at)

**Jobs:**
- idx_job_title (title)
- idx_job_department (department)
- idx_job_status (status)
- idx_job_deleted (deleted_at)
- idx_job_posted_at (posted_at)

**Applications:**
- idx_application_candidate (candidate_id)
- idx_application_job (job_id)
- idx_application_status (status)
- idx_application_submitted_at (submitted_at)
- idx_application_deleted (deleted_at)
- idx_application_job_status (job_id, status) - Composite
- idx_application_candidate_status (candidate_id, status) - Composite

**StatusHistory:**
- idx_status_history_application (application_id)
- idx_status_history_to_status (to_status)
- idx_status_history_changed_at (changed_at)
- idx_status_history_app_date (application_id, changed_at) - Composite
- idx_status_history_transition (from_status, to_status) - Composite

### Relationships

```
Candidate (1) ----< (N) Application (N) >---- (1) Job
                           |
                           |
                           v
                    (1) Application (1) ----< (N) StatusHistory
```

### Usage Example

```python
from app.database import SessionLocal
from app.models import Candidate, Job, Application
from app.utils.enums import ApplicationStatus

# Create session
db = SessionLocal()

# Create candidate
candidate = Candidate(
    email="john@example.com",
    full_name="John Doe",
    skills=["Python", "FastAPI", "PostgreSQL"]
)
db.add(candidate)
db.commit()

# Create application
application = Application(
    candidate_id=candidate.id,
    job_id=job.id,
    status=ApplicationStatus.SUBMITTED
)
db.add(application)
db.commit()

# Query with relationships
app_with_data = db.query(Application).filter(
    Application.id == application.id
).first()

print(app_with_data.candidate.full_name)  # "John Doe"
print(app_with_data.job.title)  # Job title
print(app_with_data.status_history)  # List of status changes
```

### Running Migrations

```bash
# Initialize Alembic (already done)
alembic init alembic

# Run migration
alembic upgrade head

# Rollback
alembic downgrade -1

# Create new migration
alembic revision --autogenerate -m "description"
```

---

**Status**: ✅ Production-ready database models complete!
