# Screenshot Checklist for ATS API Demo

## 📸 Required Screenshots

### 1. **Swagger UI - All Endpoints** ✅
**What to capture:**
- Navigate to `http://localhost:8000/api/v1/docs`
- Expand all endpoint groups (Authentication, Applications, Candidates, Jobs)
- Show the complete API documentation

**Key elements to show:**
- All endpoint groups visible
- Status flow diagram in description
- JWT "Authorize" button
- OpenAPI metadata (title, version, contact)

**Filename:** `01_swagger_ui_overview.png`

---

### 2. **Successful Application Creation** ✅
**What to capture:**
- POST `/api/v1/applications/` endpoint in Swagger UI
- Click "Try it out"
- Fill in request body with realistic data
- Click "Execute"
- Show 201 Created response with application data

**Key elements to show:**
- Request body with candidate_id, job_id, cover_letter
- Response status: 201 Created
- Response body with generated UUID
- Location header

**Filename:** `02_application_created.png`

---

### 3. **Status Update with Validation Error** ✅
**What to capture:**
- PATCH `/api/v1/applications/{id}/status` endpoint
- Attempt invalid transition (e.g., SUBMITTED → HIRED)
- Show 400 Bad Request response

**Key elements to show:**
- Request body with invalid status
- Response status: 400 Bad Request
- Error message explaining why transition is invalid
- Allowed statuses list

**Filename:** `03_validation_error.png`

---

### 4. **Status History (Audit Trail)** ✅
**What to capture:**
- GET `/api/v1/applications/{id}` endpoint
- Show response with status_history array
- Multiple history entries showing transitions

**Key elements to show:**
- Application details
- status_history array with multiple entries
- Each entry showing: from_status, to_status, changed_by, notes, timestamp

**Filename:** `04_status_history.png`

---

### 5. **Statistics Dashboard Data** ✅
**What to capture:**
- GET `/api/v1/applications/stats/advanced` endpoint
- Show comprehensive statistics response

**Key elements to show:**
- total_applications count
- status_breakdown with percentages
- conversion_metrics (all rates)
- funnel_data (Chart.js ready)
- daily_trends data

**Filename:** `05_statistics_data.png`

---

### 6. **Test Coverage Report >60%** ✅
**What to capture:**
- Run `pytest --cov=app --cov-report=html`
- Open `htmlcov/index.html` in browser
- Show coverage summary

**Key elements to show:**
- Overall coverage percentage (>60%)
- Coverage by module (app/models, app/services, app/api)
- Color-coded coverage indicators

**Filename:** `06_test_coverage.png`

---

## 🎬 Bonus Screenshots

### 7. **Authentication Flow**
- Register user response (201 Created)
- Login response with JWT token
- Authorized request with Bearer token

**Filename:** `07_authentication_flow.png`

---

### 8. **Advanced Search**
- GET `/api/v1/applications/` with filters
- Show pagination metadata
- Multiple filter parameters (candidate_email, status, date_range)

**Filename:** `08_advanced_search.png`

---

### 9. **Code Structure**
- VS Code or IDE showing project structure
- Highlight key directories (app/models, app/services, app/api)

**Filename:** `09_code_structure.png`

---

### 10. **Docker Compose Running**
- Terminal showing `docker-compose up` output
- All services running (postgres, api, redis, pgadmin)

**Filename:** `10_docker_running.png`

---

## 📋 Screenshot Capture Instructions

### Using Swagger UI:
1. Start server: `uvicorn app.main:app --reload`
2. Navigate to: `http://localhost:8000/api/v1/docs`
3. Use browser's screenshot tool or Snipping Tool
4. Capture full page or specific sections

### Using Postman:
1. Import `ATS_API_Postman_Collection.json`
2. Run requests in order
3. Screenshot request/response panels

### For Coverage Report:
```bash
# Run tests with coverage
pytest --cov=app --cov-report=html

# Open in browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac

# Take screenshot
```

---

## ✅ Checklist

- [ ] 01_swagger_ui_overview.png
- [ ] 02_application_created.png
- [ ] 03_validation_error.png
- [ ] 04_status_history.png
- [ ] 05_statistics_data.png
- [ ] 06_test_coverage.png
- [ ] 07_authentication_flow.png (bonus)
- [ ] 08_advanced_search.png (bonus)
- [ ] 09_code_structure.png (bonus)
- [ ] 10_docker_running.png (bonus)

---

**Total Required:** 6 screenshots  
**Total with Bonus:** 10 screenshots

Save all screenshots to: `prob-4/screenshots/`
