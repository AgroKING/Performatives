# Demo Script - ATS API (2-3 Minutes)

## 🎬 Recording Setup

**Duration:** 2-3 minutes  
**Tools Needed:**
- Screen recorder (OBS Studio, Loom, or built-in)
- Terminal
- Browser (for Swagger UI)
- Code editor (VS Code)

**Resolution:** 1920x1080 recommended

---

## 📝 Script Timeline

### **[0:00-0:15] Introduction & Server Start** (15 seconds)

**Actions:**
1. Open terminal in `prob-4` directory
2. Show directory structure briefly
3. Start server

**Script:**
```bash
# Show we're in the project directory
pwd

# Start the server
uvicorn app.main:app --reload
```

**Narration:**
> "Welcome to the ATS API demonstration. This is a production-ready Applicant Tracking System built with FastAPI. Let's start the server."

**What to show:**
- Terminal output showing server starting
- "Application startup complete" message
- Server running on http://127.0.0.1:8000

---

### **[0:15-0:45] Swagger UI Tour** (30 seconds)

**Actions:**
1. Open browser to `http://localhost:8000/api/v1/docs`
2. Scroll through endpoint groups
3. Show the main description with status flow

**Narration:**
> "The API features automatic OpenAPI documentation with Swagger UI. We have four main endpoint groups: Authentication for JWT-based auth, Applications with status flow validation, Candidates, and Jobs. Notice the status flow diagram showing the state machine that prevents invalid transitions."

**What to show:**
- Expand Authentication group
- Expand Applications group
- Point out the Authorize button
- Show status flow in description

---

### **[0:45-1:15] Create Candidate & Job** (30 seconds)

**Actions:**
1. Click "Authorize" button
2. Login first (or use pre-generated token)
3. Create candidate via POST /candidates/
4. Create job via POST /jobs/

**Script (in Swagger UI):**
```json
// POST /auth/login
{
  "username": "admin",
  "password": "AdminPass123"
}

// Copy token, click Authorize, paste token

// POST /candidates/
{
  "email": "jane.smith@example.com",
  "full_name": "Jane Smith",
  "phone": "+1234567890",
  "skills": ["Python", "FastAPI", "PostgreSQL"]
}

// POST /jobs/
{
  "title": "Senior Backend Engineer",
  "department": "Engineering",
  "description": "Looking for experienced backend engineer",
  "required_skills": ["Python", "FastAPI"],
  "location": "San Francisco, CA",
  "employment_type": "Full-time",
  "salary_min": 120000,
  "salary_max": 180000
}
```

**Narration:**
> "First, I'll authenticate and get a JWT token. Now let's create a candidate and a job posting. Notice the 201 Created responses with generated UUIDs."

**What to show:**
- 201 Created responses
- Copy candidate_id and job_id

---

### **[1:15-1:45] Submit Application & Valid Status Changes** (30 seconds)

**Actions:**
1. Create application
2. Update status: SUBMITTED → SCREENING
3. Update status: SCREENING → INTERVIEW_SCHEDULED

**Script:**
```json
// POST /applications/
{
  "candidate_id": "{paste_candidate_id}",
  "job_id": "{paste_job_id}",
  "cover_letter": "I'm very interested in this position",
  "score": 85
}

// PATCH /applications/{id}/status
{
  "new_status": "SCREENING",
  "changed_by": "recruiter@example.com",
  "notes": "Candidate meets requirements"
}

// PATCH /applications/{id}/status
{
  "new_status": "INTERVIEW_SCHEDULED",
  "changed_by": "recruiter@example.com",
  "notes": "Scheduling interview"
}
```

**Narration:**
> "Now I'll submit an application and progress it through valid status changes. First to SCREENING, then to INTERVIEW_SCHEDULED. Each transition is validated by our state machine."

**What to show:**
- Application created with SUBMITTED status
- Successful status updates
- 200 OK responses

---

### **[1:45-2:05] Invalid Transition (Error Demo)** (20 seconds)

**Actions:**
1. Attempt invalid transition: INTERVIEW_SCHEDULED → HIRED

**Script:**
```json
// PATCH /applications/{id}/status
{
  "new_status": "HIRED",
  "changed_by": "recruiter@example.com",
  "notes": "Attempting to skip stages"
}
```

**Narration:**
> "Let's try an invalid transition - jumping from INTERVIEW_SCHEDULED directly to HIRED, skipping the interview and offer stages. Watch what happens."

**What to show:**
- 400 Bad Request response
- Error message explaining invalid transition
- List of allowed statuses

---

### **[2:05-2:30] Status History & Statistics** (25 seconds)

**Actions:**
1. GET /applications/{id} to show status history
2. GET /applications/stats/advanced

**Narration:**
> "Every status change is recorded in our audit trail. Here's the complete history showing who made changes and when. The API also provides comprehensive analytics with conversion rates, funnel data, and daily trends - all formatted for Chart.js visualization."

**What to show:**
- status_history array with multiple entries
- Statistics response with:
  - conversion_metrics
  - funnel_data
  - daily_trends

---

### **[2:30-2:50] Code Structure Tour** (20 seconds)

**Actions:**
1. Switch to VS Code
2. Quick tour of project structure

**Narration:**
> "The codebase follows clean architecture principles. Models for database entities, services for business logic like the StatusManager, API routers for endpoints, and comprehensive test coverage exceeding 60%."

**What to show:**
- app/models/ directory
- app/services/status_manager.py
- app/api/ directory
- tests/ directory
- Coverage report (if time)

---

### **[2:50-3:00] Closing** (10 seconds)

**Actions:**
1. Show README.md or documentation
2. End screen

**Narration:**
> "This ATS API demonstrates production-ready FastAPI development with JWT authentication, state machine validation, comprehensive testing, and automatic documentation. Thank you for watching!"

**What to show:**
- README.md in browser or editor
- Project highlights

---

## 🎯 Key Points to Emphasize

1. **JWT Authentication** - Secure, stateless auth
2. **State Machine** - Prevents invalid status transitions
3. **Audit Trail** - Complete history of changes
4. **Advanced Analytics** - Chart.js ready data
5. **Test Coverage** - >60% with pytest
6. **Auto Documentation** - OpenAPI/Swagger UI
7. **Clean Architecture** - SOLID principles

---

## 📌 Pro Tips

### Before Recording:
- [ ] Clear browser cache
- [ ] Zoom browser to 125% for readability
- [ ] Close unnecessary tabs
- [ ] Prepare test data in advance
- [ ] Test the flow once before recording

### During Recording:
- Speak clearly and at moderate pace
- Pause briefly between sections
- Highlight important responses
- Keep mouse movements smooth

### After Recording:
- Add captions/subtitles if needed
- Add intro/outro slides
- Export in 1080p
- Keep file size reasonable (<100MB)

---

## 🎥 Alternative: Quick Demo (1 minute)

If time is limited, focus on:
1. Start server (5s)
2. Show Swagger UI (10s)
3. Create application (15s)
4. Valid status update (10s)
5. Invalid status update with error (10s)
6. Show status history (10s)

---

**Ready to record? Follow this script and you'll have a compelling 2-3 minute demo!**
