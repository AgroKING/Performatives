# Problem-1: FastAPI Job Matching System

## 📋 Overview

A high-performance job matching API built with FastAPI and Pydantic that intelligently matches candidates to job postings based on skills, experience, education, location, and salary expectations.

## 🏗️ Project Structure

```
problem-1/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic data models
│   └── algorithm.py     # Matching algorithm logic
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
cd problem-1
pip install -r requirements.txt
```

### Run Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

### API Documentation

Interactive API docs: http://localhost:8000/docs

## 📊 Data Models

### Input Models

#### Candidate
```python
{
  "name": "John Doe",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "experience_years": 5.0,
  "education": [
    {
      "degree": "Bachelor's",
      "field": "Computer Science",
      "institution": "MIT",
      "graduation_year": 2018
    }
  ],
  "preferred_locations": ["San Francisco", "Remote"],
  "expected_salary": 120000
}
```

#### Job
```python
{
  "job_id": "job-001",
  "title": "Senior Backend Engineer",
  "company": "TechCorp",
  "required_skills": ["Python", "FastAPI", "Docker"],
  "experience_required": 3.0,
  "location": "San Francisco",
  "salary_range": [100000, 150000],
  "education_required": "Bachelor's"
}
```

### Output Models

#### MatchResponse
```python
{
  "candidate_name": "John Doe",
  "matches": [
    {
      "job_id": "job-001",
      "title": "Senior Backend Engineer",
      "company": "TechCorp",
      "match_percentage": 85.5,
      "breakdown": {
        "skill_match_percentage": 66.67,
        "experience_match": true,
        "education_match": true,
        "location_match": true,
        "salary_match": true
      }
    }
  ],
  "total_jobs_analyzed": 10
}
```

## 🧮 Matching Algorithm

The algorithm uses **weighted scoring**:

- **Skills**: 50% - Percentage of required skills matched
- **Experience**: 20% - Boolean (meets requirement or not)
- **Education**: 15% - Boolean (meets requirement or not)
- **Location**: 10% - Boolean (matches preference)
- **Salary**: 5% - Boolean (within range with 10% flexibility)

### Validation Rules

1. **Salary Range**: Must have exactly 2 values [min, max] where min < max
2. **Skills**: At least 1 skill required for both candidate and job
3. **Experience**: Non-negative values only
4. **Graduation Year**: Between 1950 and 2030

## 🔌 API Endpoints

### POST /match

Match a candidate to multiple job postings.

**Request:**
```json
{
  "candidate": { ... },
  "jobs": [ ... ]
}
```

**Response:**
```json
{
  "candidate_name": "John Doe",
  "matches": [ ... ],
  "total_jobs_analyzed": 10
}
```

### GET /

Health check and API information.

### GET /health

Service health status.

## ✅ Features

- ✅ Pydantic models with strict validation
- ✅ Salary range validator (min < max)
- ✅ Weighted matching algorithm
- ✅ Case-insensitive skill matching
- ✅ Education hierarchy support
- ✅ Location flexibility (Remote, Anywhere)
- ✅ Salary flexibility (±10%)
- ✅ CORS enabled
- ✅ Auto-generated API docs

## 🧪 Testing

```bash
# Run tests (to be implemented)
pytest tests/
```

## 📝 Field Name Verification

All field names match the Input Specifications exactly:

**Candidate:**
- ✅ `name`
- ✅ `skills`
- ✅ `experience_years` (not `years_of_experience`)
- ✅ `education`
- ✅ `preferred_locations`
- ✅ `expected_salary`

**Job:**
- ✅ `job_id`
- ✅ `title`
- ✅ `company`
- ✅ `required_skills`
- ✅ `experience_required`
- ✅ `location`
- ✅ `salary_range`
- ✅ `education_required`

**Education:**
- ✅ `degree`
- ✅ `field`
- ✅ `institution`
- ✅ `graduation_year`

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.115.0
- **Validation**: Pydantic 2.10.0
- **Server**: Uvicorn 0.34.0
- **Language**: Python 3.9+

## 📄 License

MIT

---

**Built by Senior Backend Architect (FastAPI Specialist)**
