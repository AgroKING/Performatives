# 🚀 Performatives - Integrated Platform

## Quick Start

### Start All Services

```bash
docker-compose build
docker-compose up -d
```

Visit **http://localhost** to access the unified platform!

## Services Available

| Service | URL | Description |
|---------|-----|-------------|
| **Landing Page** | http://localhost | Unified entry point |
| **Job Discovery** | http://localhost/jobs | React job search dashboard |
| **Job Matching UI** | http://localhost/problem-1/index.html | Match candidates to jobs |
| **Job Matching API** | http://localhost/api/match | RESTful matching API |
| **ATS Dashboard** | http://localhost/prob-4/frontend/index.html | Applicant tracking system |
| **ATS API** | http://localhost/api/ats | ATS REST API |
| **Skill Analyzer** | http://localhost/skills | Skill gap analysis tool |
| **Skill Analyzer API** | http://localhost/api/skills | Analysis API |

## API Documentation

- **Job Matching**: http://localhost/api/match/docs
- **ATS System**: http://localhost/api/ats/docs

## Architecture

```
                    Nginx Reverse Proxy
                    (Port 80)
                          │
        ┌─────────────────┼─────────────────┬──────────────┐
        │                 │                 │              │
    /jobs           /api/match          /api/ats     /api/skills
        │                 │                 │              │
    prob-3          problem-1           prob-4        problem-5
   (React)         (FastAPI)          (FastAPI)      (Next.js)
   Port 5173       Port 8001          Port 8002      Port 3000
                                          │
                                      PostgreSQL
                                      Port 5432
```

## Individual Services

### Start Specific Service

```bash
# Job Discovery Dashboard
docker-compose up prob3

# Job Matching API
docker-compose up problem1

# ATS System
docker-compose up prob4 postgres

# Skill Gap Analyzer
docker-compose up problem5
```

### Stop All Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f prob4
```

## Development

### Without Docker

Each project can run independently:

**prob-3:**
```bash
cd prob-3
npm install && npm run dev
# http://localhost:5173
```

**problem-1:**
```bash
cd problem-1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
# http://localhost:8001
```

**prob-4:**
```bash
cd prob-4
pip install -r requirements.txt
# Set up database first
uvicorn app.main:app --reload --port 8002
# http://localhost:8002
```

**problem-5:**
```bash
cd problem-5
npm install && npm run dev
# http://localhost:3000
```

## Configuration

### Environment Variables

Create `.env` file in root:

```env
# PostgreSQL
POSTGRES_DB=ats_db
POSTGRES_USER=ats_user
POSTGRES_PASSWORD=change_me_in_production

# ATS API
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Nginx Configuration

Edit `nginx/nginx.conf` to customize routing.

## Ports

| Service | Internal Port | External Port |
|---------|--------------|---------------|
| Nginx | 80 | 80 |
| prob-3 | 5173 | 5173 |
| problem-1 | 8000 | 8001 |
| prob-4 | 8000 | 8002 |
| problem-5 | 3000 | 3000 |
| PostgreSQL | 5432 | 5432 |

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 80
netstat -ano | findstr :80

# Or change port in docker-compose.yml:
ports:
  - "8080:80"  # Use port 8080 instead
```

### CORS Issues

Nginx config includes CORS headers. If issues persist, check browser console.

### Database Connection

```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs postgres
```

## Health Checks

```bash
# Platform health
curl http://localhost/health

# Individual services
curl http://localhost:8001/health  # problem-1
curl http://localhost:8002/health  # prob-4
```

## Production Deployment

1. Update environment variables
2. Use production-ready SECRET_KEY
3. Enable HTTPS (add SSL certificates)
4. Use managed PostgreSQL database
5. Set up monitoring (Prometheus/Grafana)

---

**All services now accessible through one unified platform!** 🎉
