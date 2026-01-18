# 🏗️ Full-Stack Integration Strategy for Performatives

## 📊 Current State Analysis

### Existing Projects

| Project | Type | Tech Stack | Purpose | Port | Status |
|---------|------|------------|---------|------|--------|
| **prob-3** | Frontend | React 19 + Vite | Job Discovery Dashboard | 5173 | ✅ Standalone |
| **problem-1** | Backend API | FastAPI + Python | Job Matching Engine | 8000 | ✅ Standalone |
| **prob-4** | Backend API | FastAPI + SQLAlchemy | ATS with Auth | 8000 | ✅ Standalone |
| **problem-5** | Full-Stack | Next.js 14 | Skill Gap Analyzer | 3000 | ✅ Standalone |

### Key Observations

**Strengths:**
- ✅ All projects are production-ready
- ✅ Clear separation of concerns
- ✅ Well-documented APIs
- ✅ Docker-ready

**Challenges:**
- ⚠️ No shared authentication
- ⚠️ Duplicate skill matching logic (problem-1 & problem-5)
- ⚠️ No unified data layer
- ⚠️ Different ports/domains

---

## 🎯 Integration Approaches (Simplest First)

### **OPTION 1: Reverse Proxy Integration** ⭐ RECOMMENDED (Simplest)

**Concept:** Use a reverse proxy (Nginx/Traefik) to unify all services under one domain

```
┌─────────────────────────────────────────────────┐
│         Unified Domain: app.performatives.com    │
└─────────────────────────────────────────────────┘
                        │
                   [Nginx/Traefik]
                        │
        ┌───────────────┼───────────────┬──────────────┐
        │               │               │              │
    /dashboard      /api/match      /api/ats      /api/skills
        │               │               │              │
    prob-3         problem-1         prob-4       problem-5
   (React)        (FastAPI)        (FastAPI)      (Next.js)
   Port 5173      Port 8001        Port 8002      Port 3000
```

**Implementation Steps:**

1. **Create nginx.conf**
```nginx
server {
    listen 80;
    server_name app.performatives.com;

    # Frontend - Job Discovery Dashboard
    location /dashboard {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
    }

    # API - Job Matching
    location /api/match {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
    }

    # API - ATS
    location /api/ats {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
    }

    # API - Skill Gap Analysis
    location /api/skills {
        proxy_pass http://localhost:3000/api;
        proxy_set_header Host $host;
    }

    # Root - Landing page (new)
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

2. **Update docker-compose.yml (Root Level)**
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - prob3
      - problem1
      - prob4
      - problem5

  prob3:
    build: ./prob-3
    ports:
      - "5173:5173"

  problem1:
    build: ./problem-1
    ports:
      - "8001:8000"

  prob4:
    build: ./prob-4
    ports:
      - "8002:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/ats

  problem5:
    build: ./problem-5
    ports:
      - "3000:3000"

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ats
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Pros:**
- ✅ Zero code changes required
- ✅ Each service remains independent
- ✅ Easy to deploy
- ✅ Can add/remove services easily
- ✅ Single domain for all services

**Cons:**
- ⚠️ No shared authentication (yet)
- ⚠️ Still duplicate logic

**Effort:** 1-2 hours

---

### **OPTION 2: Shared Authentication Layer** (Medium Complexity)

**Concept:** Use prob-4's JWT auth as the central authentication service

```
┌─────────────────────────────────────────┐
│      prob-4 (Auth Service)              │
│      POST /auth/login → JWT Token       │
└─────────────────────────────────────────┘
              │ (JWT Token)
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
  prob-3  problem-1  problem-5  prob-4
  (React)  (FastAPI) (Next.js)  (ATS)
    │         │         │         │
  [Verify] [Verify]  [Verify]  [Native]
```

**Implementation Steps:**

1. **Extract Auth Service from prob-4**
   - Create `shared/auth-service/` directory
   - Copy `prob-4/app/utils/auth.py`
   - Copy `prob-4/app/api/auth.py`
   - Create standalone FastAPI app

2. **Create Shared Auth Library**
```python
# shared/auth-lib/verify_token.py
from jose import jwt, JWTError

def verify_jwt_token(token: str, secret_key: str) -> dict:
    """Verify JWT token - can be used by all services"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
```

3. **Update Each Service**
   - **problem-1**: Add JWT verification middleware
   - **problem-5**: Add JWT verification in Next.js middleware
   - **prob-3**: Store JWT in localStorage, send with API requests

**Pros:**
- ✅ Centralized authentication
- ✅ Single login for all services
- ✅ Role-based access control

**Cons:**
- ⚠️ Requires code changes in all projects
- ⚠️ Need to share SECRET_KEY securely

**Effort:** 1-2 days

---

### **OPTION 3: Unified Frontend with Backend Services** (More Complex)

**Concept:** Create a new Next.js frontend that consumes all backend APIs

```
┌────────────────────────────────────────────────┐
│     New Next.js Frontend (Unified Dashboard)   │
│                                                 │
│  /jobs → prob-3 components                     │
│  /applications → prob-4 API                    │
│  /skills → problem-5 API                       │
│  /match → problem-1 API                        │
└────────────────────────────────────────────────┘
         │           │           │           │
    problem-1    prob-4    problem-5    prob-3
    (API only)  (API only)  (API only)  (Components)
```

**Implementation Steps:**

1. **Create new Next.js app**
```bash
npx create-next-app@latest unified-app
cd unified-app
```

2. **Project Structure**
```
unified-app/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/
│   │   ├── page.tsx              # Main dashboard
│   │   ├── jobs/page.tsx         # Job discovery (prob-3 logic)
│   │   ├── applications/page.tsx # ATS (prob-4 API)
│   │   └── skills/page.tsx       # Skill gap (problem-5 API)
│   └── layout.tsx
├── components/
│   ├── prob3/                    # Import from prob-3
│   ├── shared/                   # Shared components
│   └── layout/                   # Navigation, header, etc.
├── lib/
│   ├── api/
│   │   ├── matching.ts           # problem-1 client
│   │   ├── ats.ts                # prob-4 client
│   │   └── skills.ts             # problem-5 client
│   └── auth.ts                   # Auth utilities
└── types/
    └── index.ts                  # Shared TypeScript types
```

3. **API Integration Example**
```typescript
// lib/api/matching.ts
export async function matchJobs(candidate: Candidate) {
  const response = await fetch('http://localhost:8001/match', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify({ candidate, jobs })
  });
  return response.json();
}

// lib/api/ats.ts
export async function getApplications(filters: Filters) {
  const response = await fetch('http://localhost:8002/api/v1/applications', {
    headers: { 'Authorization': `Bearer ${getToken()}` }
  });
  return response.json();
}
```

**Pros:**
- ✅ Single unified UI/UX
- ✅ Consistent design system
- ✅ Shared authentication
- ✅ Better user experience

**Cons:**
- ⚠️ Significant development effort
- ⚠️ Need to port prob-3 components to Next.js
- ⚠️ Lose some project independence

**Effort:** 1-2 weeks

---

### **OPTION 4: Microservices with API Gateway** (Most Complex)

**Concept:** Full microservices architecture with Kong/AWS API Gateway

```
┌─────────────────────────────────────────┐
│         API Gateway (Kong)              │
│                                         │
│  /api/v1/match      → problem-1         │
│  /api/v1/ats        → prob-4            │
│  /api/v1/skills     → problem-5         │
│  /api/v1/shared     → shared-service    │
└─────────────────────────────────────────┘
              │
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
problem-1  prob-4  problem-5  shared-service
(FastAPI) (FastAPI) (Next.js)  (FastAPI)
    │         │         │         │
  [Jobs]   [ATS]    [Skills]  [Auth, Utils]
```

**New Shared Service:**
```
shared-service/
├── app/
│   ├── auth/           # Centralized auth
│   ├── matching/       # Skill matching logic
│   └── utils/          # Common utilities
└── main.py
```

**Pros:**
- ✅ True microservices architecture
- ✅ Scalable independently
- ✅ Centralized shared logic
- ✅ Production-grade

**Cons:**
- ⚠️ High complexity
- ⚠️ Requires infrastructure (K8s, service mesh)
- ⚠️ Overkill for current scope

**Effort:** 2-4 weeks

---

## 🎯 RECOMMENDED APPROACH

### **Phase 1: Quick Win (Option 1)** - Week 1

1. Create root-level `docker-compose.yml`
2. Add Nginx reverse proxy
3. Create simple landing page with links to all services
4. Deploy locally and test

**Deliverable:** All services accessible from `localhost` with different paths

---

### **Phase 2: Shared Auth (Option 2)** - Week 2-3

1. Extract auth service from prob-4
2. Create shared auth library
3. Update all services to verify JWT tokens
4. Implement single sign-on

**Deliverable:** One login works across all services

---

### **Phase 3: Unified Frontend (Option 3)** - Week 4-6 (Optional)

1. Create new Next.js app
2. Port prob-3 components
3. Integrate all backend APIs
4. Create unified dashboard

**Deliverable:** Single cohesive application

---

## 📁 Proposed Directory Structure (After Integration)

```
Performatives/
├── frontend/                    # New unified frontend (Phase 3)
│   ├── app/
│   ├── components/
│   └── lib/
│
├── services/                    # Backend microservices
│   ├── auth-service/           # Extracted from prob-4 (Phase 2)
│   ├── matching-service/       # problem-1 (renamed)
│   ├── ats-service/            # prob-4 (renamed)
│   └── skills-service/         # problem-5 API routes
│
├── shared/                      # Shared libraries
│   ├── auth-lib/               # JWT verification
│   ├── types/                  # TypeScript/Pydantic types
│   └── utils/                  # Common utilities
│
├── legacy/                      # Original projects (reference)
│   ├── prob-3/
│   ├── problem-1/
│   ├── prob-4/
│   └── problem-5/
│
├── infrastructure/
│   ├── nginx/
│   │   └── nginx.conf
│   ├── docker/
│   │   └── docker-compose.yml
│   └── k8s/                    # For Phase 4 (if needed)
│
├── docs/
│   ├── INTEGRATION_GUIDE.md
│   ├── API_REFERENCE.md
│   └── DEPLOYMENT.md
│
└── README.md                    # Updated with integration info
```

---

## 🚀 Quick Start Commands (After Phase 1)

```bash
# Start all services
docker-compose up -d

# Access services
# Landing page:     http://localhost
# Job Discovery:    http://localhost/dashboard
# Job Matching API: http://localhost/api/match/docs
# ATS API:          http://localhost/api/ats/docs
# Skills API:       http://localhost/api/skills/analyze
```

---

## 🔑 Key Decision Points

| Decision | Simple Path | Advanced Path |
|----------|-------------|---------------|
| **Deployment** | Docker Compose | Kubernetes |
| **Auth** | Shared JWT Secret | OAuth2/OIDC Provider |
| **Frontend** | Keep separate | Unified Next.js |
| **API Gateway** | Nginx | Kong/AWS API Gateway |
| **Database** | Single PostgreSQL | Per-service DBs |
| **Monitoring** | Docker logs | Prometheus + Grafana |

---

## 💡 Simplest Viable Path (MVP)

**Goal:** Get all services running together in 1 day

1. ✅ Create `docker-compose.yml` at root
2. ✅ Add Nginx config for routing
3. ✅ Create simple `index.html` landing page
4. ✅ Update each service's port in docker-compose
5. ✅ Run `docker-compose up`

**Result:** All services accessible from one domain, zero code changes!

---

## 📊 Comparison Matrix

| Approach | Complexity | Time | Code Changes | Benefits |
|----------|-----------|------|--------------|----------|
| **Option 1: Reverse Proxy** | ⭐ Low | 2 hours | None | Quick, simple |
| **Option 2: Shared Auth** | ⭐⭐ Medium | 2 days | Minimal | SSO enabled |
| **Option 3: Unified Frontend** | ⭐⭐⭐ High | 2 weeks | Significant | Best UX |
| **Option 4: Microservices** | ⭐⭐⭐⭐ Very High | 4 weeks | Major | Production-grade |

---

## 🎯 FINAL RECOMMENDATION

**Start with Option 1 (Reverse Proxy)** - Get immediate value with minimal effort

**Then add Option 2 (Shared Auth)** - Enable single sign-on

**Consider Option 3 (Unified Frontend)** - Only if you want a cohesive product

**Skip Option 4** - Unless you need enterprise-scale deployment

---

**Next Steps:** Let me know which approach you'd like to pursue, and I can provide detailed implementation files (nginx config, docker-compose, etc.) without writing the actual integration code!
