# StatusManager Service - Documentation

## Overview

The `StatusManager` service class enforces all business rules for application status transitions in the ATS system.

## Business Rules Enforced

### 1. ✅ Status Flow Validation
```
SUBMITTED → SCREENING → INTERVIEW_SCHEDULED → INTERVIEWED → OFFER_EXTENDED → HIRED
     ↓           ↓              ↓                  ↓               ↓
  REJECTED    REJECTED       REJECTED          REJECTED        REJECTED
```

### 2. ✅ Terminal States
- **HIRED**: Cannot transition to any other status
- **REJECTED**: Cannot transition to any other status (no reopening)

### 3. ✅ No Stage Skipping
- Must follow sequential flow
- Cannot skip from SUBMITTED directly to INTERVIEWED
- Returns 400 error with clear message

### 4. ✅ Audit Trail
- Every status change creates a `StatusHistory` entry
- Tracks: from_status, to_status, changed_by, notes, timestamp

### 5. ✅ Validation Before Commit
- All validation happens before database commit
- Rollback on any error
- No partial updates

---

## API Reference

### Methods

#### `get_allowed_next_statuses(current_status)`

Get list of allowed next statuses from current status.

**Parameters:**
- `current_status` (ApplicationStatus): Current application status

**Returns:**
- `List[str]`: List of allowed status values

**Example:**
```python
from app.services import StatusManager
from app.utils.enums import ApplicationStatus

allowed = StatusManager.get_allowed_next_statuses(ApplicationStatus.SUBMITTED)
# Returns: ['SCREENING', 'REJECTED']
```

---

#### `validate_status_transition(current_status, new_status)`

Validate if status transition is allowed.

**Parameters:**
- `current_status` (ApplicationStatus): Current status
- `new_status` (ApplicationStatus): Desired new status

**Returns:**
- `Tuple[bool, Optional[str]]`: (is_valid, error_message)

**Example:**
```python
is_valid, error = StatusManager.validate_status_transition(
    ApplicationStatus.SUBMITTED,
    ApplicationStatus.INTERVIEWED  # Invalid: skips SCREENING
)
# Returns: (False, "Invalid status transition: SUBMITTED → INTERVIEWED...")
```

---

#### `update_application_status(db, app_id, new_status, changed_by, notes)`

Update application status with full validation and audit trail.

**Parameters:**
- `db` (Session): Database session
- `app_id` (UUID): Application ID
- `new_status` (ApplicationStatus): Desired new status
- `changed_by` (str): User ID or email
- `notes` (Optional[str]): Optional notes

**Returns:**
- `Application`: Updated application object

**Raises:**
- `HTTPException(404)`: Application not found
- `HTTPException(400)`: Invalid status transition
- `HTTPException(500)`: Database error

**Example:**
```python
from app.services import StatusManager
from app.utils.enums import ApplicationStatus

updated_app = StatusManager.update_application_status(
    db=db,
    app_id=application_id,
    new_status=ApplicationStatus.SCREENING,
    changed_by="recruiter@example.com",
    notes="Candidate meets initial requirements"
)
```

---

## Usage Examples

### Example 1: Valid Transition

```python
from app.services import StatusManager
from app.utils.enums import ApplicationStatus
from app.database import SessionLocal

db = SessionLocal()

# Update status from SUBMITTED to SCREENING
try:
    application = StatusManager.update_application_status(
        db=db,
        app_id="123e4567-e89b-12d3-a456-426614174002",
        new_status=ApplicationStatus.SCREENING,
        changed_by="recruiter@example.com",
        notes="Moving to screening phase"
    )
    print(f"Status updated to: {application.status.value}")
except HTTPException as e:
    print(f"Error: {e.detail}")
```

**Output:**
```
Status updated to: SCREENING
```

---

### Example 2: Invalid Transition (Stage Skipping)

```python
# Try to skip from SUBMITTED to INTERVIEWED
try:
    application = StatusManager.update_application_status(
        db=db,
        app_id="123e4567-e89b-12d3-a456-426614174002",
        new_status=ApplicationStatus.INTERVIEWED,
        changed_by="recruiter@example.com"
    )
except HTTPException as e:
    print(f"Error {e.status_code}: {e.detail}")
```

**Output:**
```
Error 400: {
    "error": "Invalid status transition",
    "message": "Invalid status transition: SUBMITTED → INTERVIEWED. Allowed transitions from SUBMITTED: SCREENING, REJECTED. Stage skipping is not permitted.",
    "current_status": "SUBMITTED",
    "requested_status": "INTERVIEWED",
    "allowed_statuses": ["SCREENING", "REJECTED"]
}
```

---

### Example 3: Prevent Reverting from REJECTED

```python
# Try to change status from REJECTED
try:
    application = StatusManager.update_application_status(
        db=db,
        app_id="rejected_app_id",
        new_status=ApplicationStatus.SCREENING,
        changed_by="recruiter@example.com"
    )
except HTTPException as e:
    print(f"Error: {e.detail['message']}")
```

**Output:**
```
Error: Cannot change status from REJECTED (terminal state). Rejected applications cannot be reopened.
```

---

### Example 4: Get Allowed Next Statuses

```python
from app.utils.enums import ApplicationStatus

# Get allowed transitions from SCREENING
allowed = StatusManager.get_allowed_next_statuses(ApplicationStatus.SCREENING)
print(f"From SCREENING, can transition to: {allowed}")
```

**Output:**
```
From SCREENING, can transition to: ['INTERVIEW_SCHEDULED', 'REJECTED']
```

---

### Example 5: Bulk Validation

```python
transitions = [
    (ApplicationStatus.SUBMITTED, ApplicationStatus.SCREENING),  # Valid
    (ApplicationStatus.SUBMITTED, ApplicationStatus.INTERVIEWED),  # Invalid
    (ApplicationStatus.REJECTED, ApplicationStatus.SCREENING),  # Invalid
]

results = StatusManager.bulk_validate_transitions(transitions)

for result in results:
    print(f"{result['current_status']} → {result['new_status']}: {result['is_valid']}")
    if not result['is_valid']:
        print(f"  Error: {result['error_message']}")
```

**Output:**
```
SUBMITTED → SCREENING: True
SUBMITTED → INTERVIEWED: False
  Error: Invalid status transition: SUBMITTED → INTERVIEWED...
REJECTED → SCREENING: False
  Error: Cannot change status from REJECTED (terminal state)...
```

---

## Error Handling

### Error Response Format

All validation errors return HTTP 400 with detailed information:

```json
{
    "error": "Invalid status transition",
    "message": "Detailed error message explaining why transition failed",
    "current_status": "SUBMITTED",
    "requested_status": "INTERVIEWED",
    "allowed_statuses": ["SCREENING", "REJECTED"]
}
```

### Error Types

| Error Code | Scenario | Message |
|------------|----------|---------|
| 404 | Application not found | "Application with ID {id} not found" |
| 400 | Self-transition | "Status is already {status}. No change needed." |
| 400 | Terminal state (HIRED) | "Cannot change status from HIRED (terminal state)..." |
| 400 | Terminal state (REJECTED) | "Cannot change status from REJECTED (terminal state)..." |
| 400 | Stage skipping | "Invalid status transition... Stage skipping is not permitted." |
| 500 | Database error | "Failed to update application status: {error}" |

---

## State Machine Diagram

```
┌─────────────┐
│  SUBMITTED  │
└──────┬──────┘
       │
       ├─→ SCREENING ────────┐
       │                     │
       │   ┌─────────────────┘
       │   │
       │   ├─→ INTERVIEW_SCHEDULED ─────┐
       │   │                            │
       │   │   ┌────────────────────────┘
       │   │   │
       │   │   ├─→ INTERVIEWED ──────────┐
       │   │   │                         │
       │   │   │   ┌─────────────────────┘
       │   │   │   │
       │   │   │   ├─→ OFFER_EXTENDED ───┐
       │   │   │   │                     │
       │   │   │   │   ┌─────────────────┘
       │   │   │   │   │
       │   │   │   │   ├─→ HIRED (Terminal)
       │   │   │   │   │
       │   │   │   │   └─→ REJECTED (Terminal)
       │   │   │   │
       │   │   │   └─→ REJECTED (Terminal)
       │   │   │
       │   │   └─→ REJECTED (Terminal)
       │   │
       │   └─→ REJECTED (Terminal)
       │
       └─→ REJECTED (Terminal)
```

---

## Integration with FastAPI

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import StatusManager
from app.schemas import StatusChangeRequest, ApplicationResponse

router = APIRouter()

@router.post("/applications/{app_id}/status", response_model=ApplicationResponse)
def update_status(
    app_id: UUID,
    request: StatusChangeRequest,
    db: Session = Depends(get_db)
):
    """Update application status with validation."""
    application = StatusManager.update_application_status(
        db=db,
        app_id=app_id,
        new_status=request.new_status,
        changed_by=request.changed_by,
        notes=request.notes
    )
    return application
```

---

## Testing

```python
import pytest
from app.services import StatusManager
from app.utils.enums import ApplicationStatus

def test_valid_transition():
    is_valid, error = StatusManager.validate_status_transition(
        ApplicationStatus.SUBMITTED,
        ApplicationStatus.SCREENING
    )
    assert is_valid is True
    assert error is None

def test_invalid_stage_skipping():
    is_valid, error = StatusManager.validate_status_transition(
        ApplicationStatus.SUBMITTED,
        ApplicationStatus.INTERVIEWED
    )
    assert is_valid is False
    assert "Stage skipping is not permitted" in error

def test_terminal_state_rejected():
    is_valid, error = StatusManager.validate_status_transition(
        ApplicationStatus.REJECTED,
        ApplicationStatus.SCREENING
    )
    assert is_valid is False
    assert "terminal state" in error
```

---

**Status**: ✅ Production-ready with comprehensive validation and error handling!
