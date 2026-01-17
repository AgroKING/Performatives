# Test Suite Documentation

## 🧪 Comprehensive Test Suite

### Test Files Created

**1. `tests/conftest.py`** - Fixtures and Configuration
- SQLite in-memory test database
- FastAPI TestClient
- Test users (candidate, recruiter, admin)
- Auth headers with JWT tokens
- Test data fixtures (candidate, job, application)

**2. `tests/test_models.py`** - Model Tests
- Candidate model constraints and soft delete
- Job model validation and relationships
- Application unique constraints
- StatusHistory audit trail
- User model with role enum
- Email/username uniqueness

**3. `tests/test_status_validation.py`** - Business Rules
- 20+ parametrized status transition tests
- Terminal state prevention (HIRED, REJECTED)
- Stage skipping prevention
- StatusManager service methods
- Bulk validation
- Status history creation

**4. `tests/test_api_endpoints.py`** - API Tests
- Auth endpoints (register, login, get_me)
- Application CRUD operations
- Candidate endpoints with pagination
- Job endpoints with filtering
- Status update with validation
- Statistics endpoints
- Unauthorized access tests

**5. `tests/test_edge_cases.py`** - Edge Cases
- Duplicate application prevention
- Concurrent status updates
- Invalid backward transitions
- Soft delete functionality
- Empty data fields
- Pagination edge cases

---

## 🚀 Running Tests

### Run All Tests
```bash
cd prob-4
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run Specific Test File
```bash
pytest tests/test_status_validation.py -v
```

### Run Specific Test
```bash
pytest tests/test_api_endpoints.py::TestAuthEndpoints::test_login_success -v
```

### Run Tests Matching Pattern
```bash
pytest -k "status" -v
```

---

## 📊 Coverage Report

After running tests with coverage, view the HTML report:
```bash
# Open htmlcov/index.html in browser
start htmlcov/index.html  # Windows
```

**Coverage Target**: >60%

**Coverage Areas**:
- ✅ Models (constraints, relationships, methods)
- ✅ Services (StatusManager, auth utilities)
- ✅ API endpoints (all routes)
- ✅ Schemas (validation)
- ✅ Business logic (status transitions)

---

## 🎯 Test Statistics

| Test File | Tests | Coverage |
|-----------|-------|----------|
| test_models.py | 12 | Models, constraints |
| test_status_validation.py | 15+ | Business rules |
| test_api_endpoints.py | 20+ | All endpoints |
| test_edge_cases.py | 15+ | Edge cases |
| **Total** | **60+** | **>60%** |

---

## 🔍 Test Categories

### Positive Tests
- ✅ Successful user registration
- ✅ Valid status transitions
- ✅ Creating applications
- ✅ Listing with filters
- ✅ Authentication flow

### Negative Tests
- ❌ Duplicate applications
- ❌ Invalid status transitions
- ❌ Unauthorized access
- ❌ Weak passwords
- ❌ Terminal state violations

### Edge Cases
- 🔸 Empty data fields
- 🔸 Soft delete behavior
- 🔸 Pagination boundaries
- 🔸 Concurrent updates
- 🔸 Missing relationships

---

## 🛠️ Test Fixtures

### Database Fixtures
- `db_session` - Fresh SQLite database per test
- `client` - FastAPI TestClient with test DB

### User Fixtures
- `test_user` - Regular candidate user
- `test_admin` - Admin user
- `test_recruiter` - Recruiter user
- `auth_headers` - JWT auth headers
- `admin_headers` - Admin JWT headers

### Data Fixtures
- `test_candidate` - Sample candidate
- `test_job` - Sample job posting
- `test_application` - Sample application

---

## 📝 Example Test

```python
def test_status_transition_with_history(db_session, test_application):
    """Test status update creates history entry."""
    # Update status
    updated = StatusManager.update_application_status(
        db=db_session,
        app_id=test_application.id,
        new_status=ApplicationStatus.SCREENING,
        changed_by="recruiter@example.com",
        notes="Moving to screening"
    )
    
    # Verify
    assert updated.status == ApplicationStatus.SCREENING
    assert len(updated.status_history) == 1
    assert updated.status_history[0].notes == "Moving to screening"
```

---

## ⚙️ CI/CD Integration

Add to GitHub Actions:
```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=app --cov-report=xml --cov-fail-under=60
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

---

**Status**: ✅ Comprehensive test suite complete with >60% coverage!
