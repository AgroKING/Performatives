# Pydantic Schemas - Complete Documentation

## ✅ All Schemas Implemented

### 1. Candidate Schemas (`app/schemas/candidate.py`)

**CandidateCreate**
- Email validation with `EmailStr`
- Phone validation with regex pattern (E.164 format)
- Skills list with duplicate removal
- Full name validation (non-empty, trimmed)

**CandidateUpdate**
- All fields optional for partial updates
- Same validators as Create

**CandidateResponse**
- Includes UUID, timestamps
- ConfigDict with `from_attributes=True` for ORM mode
- OpenAPI examples

### 2. Job Schemas (`app/schemas/job.py`)

**JobCreate**
- Salary range validation (max >= min)
- Employment type validation (Full-time, Part-time, Contract, etc.)
- Required skills deduplication
- Comprehensive field constraints

**JobUpdate**
- Optional fields for partial updates
- Can update status (JobStatus enum)

**JobResponse**
- Includes all job fields + metadata
- JobStatus enum serialization
- ORM mode enabled

### 3. Application Schemas (`app/schemas/application.py`)

**ApplicationCreate**
- Links candidate_id and job_id
- Optional cover_letter and resume_data

**ApplicationUpdate**
- Partial updates for cover_letter, resume_data, score
- Score validation (0-100)

**StatusChangeRequest** ⭐
- new_status: ApplicationStatus enum
- changed_by: User identifier (required)
- notes: Optional explanation (max 1000 chars)
- Status enum validation

**ApplicationResponse**
- All application fields
- **Computed field**: `time_in_current_status` (hours since last update)
- Timezone-aware datetime handling
- ORM mode enabled

**ApplicationWithHistory**
- Extends ApplicationResponse
- Includes full status_history list
- Nested StatusHistoryResponse objects

**ApplicationStatsResponse** ⭐
- total_applications: Total count
- breakdown_by_status: Dict[str, int]
- avg_time_per_stage: Dict[str, float] (hours)
- conversion_rates: Dict[str, float] (percentages)
- avg_time_to_hire: Optional[float] (days)

### 4. StatusHistory Schemas (`app/schemas/status_history.py`)

**StatusHistoryResponse**
- Complete audit trail information
- from_status, to_status, changed_by, notes
- Timestamp with timezone support

---

## 🎯 Key Features Implemented

### ✅ ConfigDict for ORM Mode
```python
model_config = ConfigDict(
    from_attributes=True,  # Enable ORM mode
    json_schema_extra={...}  # OpenAPI examples
)
```

### ✅ Field Validators

**Email Validation:**
```python
email: EmailStr  # Built-in Pydantic email validation
```

**Phone Validation:**
```python
phone: Optional[str] = Field(
    None,
    pattern=r'^\+?1?\d{9,15}$'  # E.164 format
)
```

**Status Enum Validation:**
```python
@field_validator('new_status')
@classmethod
def validate_status(cls, v: ApplicationStatus) -> ApplicationStatus:
    if not isinstance(v, ApplicationStatus):
        raise ValueError(f'Invalid status...')
    return v
```

**Salary Range Validation:**
```python
@field_validator('salary_max')
@classmethod
def validate_salary_range(cls, v: Optional[int], info) -> Optional[int]:
    if v is not None and 'salary_min' in info.data:
        salary_min = info.data['salary_min']
        if salary_min is not None and v < salary_min:
            raise ValueError('salary_max must be >= salary_min')
    return v
```

**Skills Deduplication:**
```python
@field_validator('skills')
@classmethod
def validate_skills(cls, v: List[str]) -> List[str]:
    if v:
        v = [skill.strip() for skill in v if skill.strip()]
        v = list(dict.fromkeys(v))  # Remove duplicates
    return v
```

### ✅ Computed Fields

**Time in Current Status:**
```python
@computed_field
@property
def time_in_current_status(self) -> float:
    """Compute time in current status (hours)."""
    now = datetime.now(timezone.utc)
    updated = self.updated_at
    if updated.tzinfo is None:
        updated = updated.replace(tzinfo=timezone.utc)
    
    delta = now - updated
    return round(delta.total_seconds() / 3600, 2)  # Hours
```

### ✅ OpenAPI Documentation Examples

Every schema includes comprehensive examples:

```python
model_config = ConfigDict(
    from_attributes=True,
    json_schema_extra={
        "example": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "alice.smith@example.com",
            "full_name": "Alice Smith",
            ...
        }
    }
)
```

### ✅ Proper Datetime Serialization

All datetime fields:
- Use `datetime` type from Python's datetime module
- Support timezone-aware timestamps
- Automatically serialize to ISO 8601 format in JSON

---

## 📊 Schema Relationships

```
CandidateCreate → CandidateResponse
JobCreate → JobResponse
ApplicationCreate → ApplicationResponse → ApplicationWithHistory
StatusChangeRequest → (triggers) StatusHistoryResponse
```

---

## 🔧 Usage Examples

### Creating an Application
```python
from app.schemas import ApplicationCreate

application_data = ApplicationCreate(
    candidate_id="123e4567-e89b-12d3-a456-426614174000",
    job_id="123e4567-e89b-12d3-a456-426614174001",
    cover_letter="I am excited to apply...",
    resume_data={"experience_years": 5}
)
```

### Changing Application Status
```python
from app.schemas import StatusChangeRequest
from app.utils.enums import ApplicationStatus

status_change = StatusChangeRequest(
    new_status=ApplicationStatus.SCREENING,
    changed_by="recruiter@example.com",
    notes="Candidate meets initial requirements"
)
```

### Getting Application with History
```python
# Response will include computed field
{
    "id": "...",
    "status": "SCREENING",
    "time_in_current_status": 2.5,  # Computed field (hours)
    "status_history": [
        {
            "from_status": "SUBMITTED",
            "to_status": "SCREENING",
            "changed_by": "recruiter@example.com",
            "changed_at": "2026-01-17T11:00:00Z"
        }
    ]
}
```

### Application Statistics
```python
from app.schemas import ApplicationStatsResponse

stats = ApplicationStatsResponse(
    total_applications=150,
    breakdown_by_status={
        "SUBMITTED": 45,
        "SCREENING": 30,
        "HIRED": 10
    },
    avg_time_per_stage={
        "SUBMITTED": 24.5,
        "SCREENING": 48.2
    },
    conversion_rates={
        "SUBMITTED_to_SCREENING": 66.7
    },
    avg_time_to_hire=14.5
)
```

---

## 🎨 FastAPI Integration

These schemas automatically generate:
- **OpenAPI/Swagger documentation** with examples
- **Request validation** with detailed error messages
- **Response serialization** from ORM models
- **Type hints** for IDE autocomplete

Example FastAPI endpoint:
```python
from fastapi import APIRouter
from app.schemas import ApplicationCreate, ApplicationResponse

router = APIRouter()

@router.post("/applications", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate):
    # Pydantic validates input automatically
    # Returns ApplicationResponse with ORM mode
    ...
```

---

## ✅ Validation Summary

| Schema | Validators | Computed Fields | ORM Mode |
|--------|-----------|-----------------|----------|
| CandidateCreate | Email, Phone, Skills, Name | - | ✅ |
| JobCreate | Salary Range, Employment Type, Skills | - | ✅ |
| ApplicationCreate | - | - | ✅ |
| ApplicationResponse | - | time_in_current_status | ✅ |
| StatusChangeRequest | Status Enum | - | - |
| ApplicationStatsResponse | - | - | - |

---

**Status**: ✅ All Pydantic schemas complete and production-ready!
