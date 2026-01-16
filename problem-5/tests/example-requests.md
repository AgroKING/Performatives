# Example API Requests

## Using curl

### 1. Get Taxonomy
```bash
curl http://localhost:3000/api/taxonomy | jq
```

### 2. Analyze Junior Developer → Senior Full Stack
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "id": "cand-001",
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com",
      "experience_years": 2,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2026-01-17T00:00:00Z",
      "current_skills": [
        {"skill_id": "fe-001", "proficiency_level": 8, "years_of_experience": 2},
        {"skill_id": "fe-002", "proficiency_level": 7, "years_of_experience": 2},
        {"skill_id": "fe-003", "proficiency_level": 6, "years_of_experience": 1.5},
        {"skill_id": "fe-005", "proficiency_level": 5, "years_of_experience": 1},
        {"skill_id": "do-001", "proficiency_level": 6, "years_of_experience": 2},
        {"skill_id": "db-001", "proficiency_level": 5, "years_of_experience": 1}
      ]
    },
    "target_role": "role-001"
  }' | jq
```

### 3. Analyze Backend Developer → DevOps Engineer
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "id": "cand-002",
      "name": "Bob Smith",
      "email": "bob.smith@example.com",
      "experience_years": 4,
      "created_at": "2023-06-10T10:00:00Z",
      "updated_at": "2026-01-17T00:00:00Z",
      "current_skills": [
        {"skill_id": "be-003", "proficiency_level": 8, "years_of_experience": 4},
        {"skill_id": "be-004", "proficiency_level": 7, "years_of_experience": 3},
        {"skill_id": "be-006", "proficiency_level": 7, "years_of_experience": 3},
        {"skill_id": "db-001", "proficiency_level": 7, "years_of_experience": 3},
        {"skill_id": "db-002", "proficiency_level": 6, "years_of_experience": 2},
        {"skill_id": "do-001", "proficiency_level": 7, "years_of_experience": 4},
        {"skill_id": "do-002", "proficiency_level": 6, "years_of_experience": 2}
      ]
    },
    "target_role": "role-002"
  }' | jq
```

## Using PowerShell

### 1. Get Taxonomy
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/taxonomy" -Method Get | ConvertTo-Json -Depth 10
```

### 2. Analyze Candidate
```powershell
$body = @{
  candidate = @{
    id = "cand-001"
    name = "Alice Johnson"
    email = "alice@example.com"
    experience_years = 2
    created_at = "2024-01-15T10:00:00Z"
    updated_at = "2026-01-17T00:00:00Z"
    current_skills = @(
      @{skill_id = "fe-003"; proficiency_level = 6; years_of_experience = 1.5}
    )
  }
  target_role = "role-001"
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:3000/api/analyze" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 10
```

## Using JavaScript/Fetch

```javascript
// Get taxonomy
const taxonomy = await fetch('http://localhost:3000/api/taxonomy')
  .then(res => res.json());
console.log(taxonomy);

// Analyze candidate
const analysis = await fetch('http://localhost:3000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    candidate: {
      id: 'cand-001',
      name: 'Alice Johnson',
      email: 'alice@example.com',
      experience_years: 2,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2026-01-17T00:00:00Z',
      current_skills: [
        { skill_id: 'fe-003', proficiency_level: 6, years_of_experience: 1.5 }
      ]
    },
    target_role: 'role-001'
  })
}).then(res => res.json());

console.log('Readiness Score:', analysis.data.analysis.readiness_score);
console.log('Learning Roadmap:', analysis.data.learning_roadmap);
```
