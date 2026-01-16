# Problem-1: FastAPI Job Matching System - Testing Guide

## Running Tests

### Install Dependencies
```bash
cd problem-1
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest tests/test_main.py -v
```

### Run with Coverage Report
```bash
pytest tests/test_main.py -v --cov=app --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_main.py::test_perfect_match -v
```

### Run Tests with Detailed Output
```bash
pytest tests/test_main.py -v --tb=short
```

## Test Coverage

### Unit Tests (15 total)

#### Algorithm Tests (6 tests)
1. **test_perfect_match** - All criteria match (score = 100)
2. **test_partial_match_location_only** - Only location matches (score = 60)
3. **test_partial_match_skills_only** - 50% skills match (score = 20)
4. **test_empty_required_skills** - Edge case: no required skills
5. **test_no_expected_salary** - Edge case: flexible salary
6. **test_no_preferred_locations** - Edge case: flexible location

#### API Endpoint Tests (9 tests)
7. **test_match_endpoint_success** - Valid request returns 200
8. **test_match_endpoint_missing_name** - Missing name returns 422
9. **test_match_endpoint_invalid_salary_range** - Invalid range returns 422
10. **test_match_endpoint_no_jobs** - Empty jobs returns 400
11. **test_health_endpoint** - Health check returns 200
12. **test_root_endpoint** - Root endpoint returns API info
13. **test_example_endpoint** - Example endpoint returns sample data

## Expected Test Results

```
tests/test_main.py::test_perfect_match PASSED
tests/test_main.py::test_partial_match_location_only PASSED
tests/test_main.py::test_partial_match_skills_only PASSED
tests/test_main.py::test_empty_required_skills PASSED
tests/test_main.py::test_no_expected_salary PASSED
tests/test_main.py::test_no_preferred_locations PASSED
tests/test_main.py::test_match_endpoint_success PASSED
tests/test_main.py::test_match_endpoint_missing_name PASSED
tests/test_main.py::test_match_endpoint_invalid_salary_range PASSED
tests/test_main.py::test_match_endpoint_no_jobs PASSED
tests/test_main.py::test_health_endpoint PASSED
tests/test_main.py::test_root_endpoint PASSED
tests/test_main.py::test_example_endpoint PASSED

=============== 15 passed in X.XXs ===============
```

## Test Scenarios Explained

### Test 1: Perfect Match
- **Candidate**: Python, FastAPI, Docker, PostgreSQL | 5 years | SF | $120k
- **Job**: Same skills | 3-5 years | SF | $100k-150k
- **Expected Score**: 100 (all weights satisfied)

### Test 2: Partial Match (Location Only)
- **Candidate**: Java, Spring, MySQL | 4 years | Remote | $110k
- **Job**: Python, FastAPI, Docker, PostgreSQL | 3-5 years | Remote | $100k-130k
- **Expected Score**: 60 (0 skills + 20 location + 15 salary + 15 exp + 10 role)

### Test 3: Edge Cases
- **Empty Skills**: Job has no required skills → Full 40 points (no crash)
- **No Salary**: Candidate flexible → Full 15 points
- **No Location**: Candidate flexible → Full 20 points
- **Missing Name**: API returns 422 Validation Error

## Continuous Integration

Add to `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=app
```

## Troubleshooting

### Import Errors
If you get `ModuleNotFoundError: No module named 'app'`:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/test_main.py -v
```

### Port Already in Use
If FastAPI test client fails:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

---

**All tests verify the system works as required for Evaluation Criteria (10%).**
