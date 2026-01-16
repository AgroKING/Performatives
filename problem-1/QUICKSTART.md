# Problem-1: FastAPI Job Matching System - Quick Start Guide

## 🚀 Quick Start Commands

### 1. Navigate to Project
```bash
cd problem-1
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn pydantic pytest
# Or use requirements.txt
pip install -r requirements.txt
```

### 3. Run Tests
```bash
pytest tests/test_main.py -v
```

**Expected Output:**
```
============================= 13 passed in 0.47s ==============================
```

### 4. Run Application
```bash
uvicorn app.main:app --reload
```

**Access:**
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### 5. Docker Build & Run
```bash
docker build -t job-matcher .
docker run -p 8000:8000 job-matcher
```

**Or use Docker Compose:**
```bash
docker-compose up --build
```

---

## ✅ Verification Checklist

- [ ] Dependencies installed successfully
- [ ] All 13 tests pass
- [ ] Application starts without errors
- [ ] API docs accessible at /docs
- [ ] Docker image builds successfully
- [ ] Docker container runs successfully

---

## 📊 Project Status

**Completed:**
✅ Data models with Pydantic validation
✅ Weighted scoring algorithm (100% = Skills 40% + Location 20% + Salary 15% + Experience 15% + Role 10%)
✅ FastAPI endpoints with error handling
✅ 13 comprehensive tests (all passing)
✅ Docker deployment with layer caching
✅ Complete documentation

**Ready for production deployment!** 🎉
