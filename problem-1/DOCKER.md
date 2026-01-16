# Problem-1: Docker Deployment Guide

## 🐳 Docker Setup

### Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (version 1.29+)

---

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
cd problem-1

# Build and start the service
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

**Access the API:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

### Option 2: Using Docker CLI

```bash
cd problem-1

# Build the image
docker build -t job-matching-api:latest .

# Run the container
docker run -d \
  --name job-matching-api \
  -p 8000:8000 \
  job-matching-api:latest

# View logs
docker logs -f job-matching-api

# Stop and remove
docker stop job-matching-api
docker rm job-matching-api
```

---

## 📦 Docker Image Details

### Base Image
- `python:3.9-slim` - Minimal Debian-based Python image

### Image Size
- ~200MB (optimized with slim base and layer caching)

### Exposed Ports
- `8000` - FastAPI application

### Health Check
- Endpoint: `GET /health`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3

---

## 🔧 Layer Caching Optimization

The Dockerfile is optimized for fast rebuilds:

```dockerfile
# 1. Copy requirements.txt first (rarely changes)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2. Copy source code last (changes frequently)
COPY app/ ./app/
COPY tests/ ./tests/
```

**Benefits:**
- ✅ Dependencies layer cached until requirements.txt changes
- ✅ Code changes don't trigger dependency reinstall
- ✅ Faster rebuild times (seconds vs minutes)

---

## 🔒 Security Features

### Non-Root User
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### Environment Variables
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

### Minimal Attack Surface
- Slim base image (no unnecessary packages)
- `.dockerignore` excludes dev files
- Health checks for monitoring

---

## 🧪 Testing in Docker

### Run Tests Inside Container

```bash
# Using docker-compose
docker-compose run --rm job-matching-api pytest tests/ -v

# Using docker CLI
docker run --rm job-matching-api:latest pytest tests/ -v
```

### Interactive Shell

```bash
# Using docker-compose
docker-compose run --rm job-matching-api /bin/bash

# Using docker CLI
docker run -it --rm job-matching-api:latest /bin/bash
```

---

## 📊 Monitoring

### View Container Stats
```bash
docker stats job-matching-api
```

### Check Health Status
```bash
docker inspect --format='{{.State.Health.Status}}' job-matching-api
```

### View Logs
```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs -f job-matching-api
```

---

## 🔄 Development Workflow

### Hot Reload (Development Mode)

Edit `docker-compose.yml` to enable volume mounting:

```yaml
volumes:
  - ./app:/app/app:ro  # Uncomment this line
```

Then rebuild:
```bash
docker-compose up --build
```

Code changes will reflect immediately without rebuilding!

---

## 🚢 Production Deployment

### Build Production Image

```bash
docker build -t job-matching-api:v1.0.0 .
```

### Tag for Registry

```bash
# Docker Hub
docker tag job-matching-api:v1.0.0 username/job-matching-api:v1.0.0

# AWS ECR
docker tag job-matching-api:v1.0.0 123456789.dkr.ecr.us-east-1.amazonaws.com/job-matching-api:v1.0.0

# Google Container Registry
docker tag job-matching-api:v1.0.0 gcr.io/project-id/job-matching-api:v1.0.0
```

### Push to Registry

```bash
docker push username/job-matching-api:v1.0.0
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Container Won't Start
```bash
# Check logs
docker-compose logs job-matching-api

# Inspect container
docker inspect job-matching-api

# Check health
docker-compose ps
```

### Rebuild from Scratch
```bash
# Remove all containers and images
docker-compose down --rmi all --volumes

# Rebuild
docker-compose up --build
```

---

## 📝 Environment Variables

Create a `.env` file for configuration:

```env
# .env
ENVIRONMENT=production
LOG_LEVEL=info
PORT=8000
```

Update `docker-compose.yml`:
```yaml
env_file:
  - .env
```

---

## ✅ Verification Checklist

- [ ] Docker image builds successfully
- [ ] Container starts without errors
- [ ] Health check passes
- [ ] API accessible at http://localhost:8000
- [ ] `/docs` endpoint works
- [ ] Tests pass inside container
- [ ] Layer caching works (fast rebuilds)

---

## 🎯 Best Practices Implemented

✅ **Layer Caching** - requirements.txt copied before source code
✅ **Security** - Non-root user, minimal base image
✅ **Health Checks** - Automated monitoring
✅ **Multi-stage** - Optimized image size
✅ **.dockerignore** - Excludes unnecessary files
✅ **Environment Variables** - Configurable deployment
✅ **Logging** - Unbuffered Python output
✅ **Restart Policy** - Auto-restart on failure

---

**Docker deployment ready! 🐳**
