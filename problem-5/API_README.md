# Skill Gap Analysis API

## 🚀 Quick Start

### Installation

Due to PowerShell execution policy restrictions, you'll need to run the installation manually:

1. **Enable script execution** (run PowerShell as Administrator):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run the development server**:
```bash
npm run dev
```

4. **Open your browser**:
```
http://localhost:3000
```

## 📡 API Endpoints

### GET /api/taxonomy

Fetch the complete skill taxonomy.

**Request:**
```bash
curl http://localhost:3000/api/taxonomy
```

**Response:**
```json
{
  "success": true,
  "data": {
    "taxonomy": {
      "version": "1.0.0",
      "skills": [...],
      "categories": {...}
    },
    "target_roles": [...],
    "metadata": {
      "total_skills": 40,
      "total_roles": 6
    }
  }
}
```

---

### POST /api/analyze

Analyze skill gaps and generate a learning roadmap.

**Request:**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "id": "cand-001",
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "experience_years": 2,
      "current_skills": [
        {
          "skill_id": "fe-001",
          "proficiency_level": 8,
          "years_of_experience": 2
        },
        {
          "skill_id": "fe-002",
          "proficiency_level": 7,
          "years_of_experience": 2
        },
        {
          "skill_id": "fe-003",
          "proficiency_level": 6,
          "years_of_experience": 1.5
        }
      ],
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2026-01-17T00:00:00Z"
    },
    "target_role": "role-001"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis": {
      "candidate_id": "cand-001",
      "target_role_id": "role-001",
      "target_role_title": "Senior Full Stack Developer",
      "readiness_score": 45,
      "missing_skills_count": 8,
      "skill_gaps": [
        {
          "skill_id": "fe-004",
          "current_proficiency": 0,
          "required_proficiency": 7,
          "gap_score": 7,
          "priority": "Critical"
        }
      ]
    },
    "learning_roadmap": {
      "estimated_total_weeks": 42,
      "estimated_months": 11,
      "phases": [
        {
          "phase_number": 1,
          "phase_name": "Fundamentals",
          "estimated_weeks": 12,
          "skills": [...]
        }
      ]
    },
    "recommended_resources": [
      {
        "skill_id": "fe-004",
        "skill_name": "TypeScript",
        "resources": [
          {
            "type": "documentation",
            "title": "TypeScript Official Handbook",
            "url": "https://www.typescriptlang.org/docs/handbook/intro.html",
            "difficulty": "Beginner"
          }
        ]
      }
    ]
  }
}
```

## 🏗️ Project Structure

```
d:\cohort1\Performatives\
├── app/
│   ├── api/
│   │   ├── analyze/
│   │   │   └── route.ts          # POST /api/analyze
│   │   └── taxonomy/
│   │       └── route.ts          # GET /api/taxonomy
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Homepage with docs
├── types/
│   └── skill-taxonomy.ts         # TypeScript interfaces
├── utils/
│   └── gap-analysis.ts           # Core algorithms
├── data/
│   └── seed-data.json            # Skill taxonomy data
├── models/
│   └── pydantic-models.py        # Python models (reference)
├── examples/
│   └── example-usage.ts          # Usage examples
├── package.json
├── tsconfig.json
└── next.config.js
```

## 🧪 Testing the API

### Using curl

**Test taxonomy endpoint:**
```bash
curl http://localhost:3000/api/taxonomy | jq
```

**Test analyze endpoint:**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "candidate": {
    "id": "test-001",
    "name": "Test User",
    "email": "test@example.com",
    "experience_years": 2,
    "current_skills": [
      {"skill_id": "fe-003", "proficiency_level": 6, "years_of_experience": 1.5},
      {"skill_id": "do-001", "proficiency_level": 7, "years_of_experience": 2}
    ],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2026-01-17T00:00:00Z"
  },
  "target_role": "role-001"
}
EOF
```

### Using JavaScript/TypeScript

```typescript
// Fetch taxonomy
const taxonomy = await fetch('http://localhost:3000/api/taxonomy')
  .then(res => res.json());

// Analyze candidate
const analysis = await fetch('http://localhost:3000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    candidate: { /* ... */ },
    target_role: 'role-001'
  })
}).then(res => res.json());
```

## 🎯 Key Features

### Gap Analysis Algorithm
- ✅ **Readiness Score**: 0-100 weighted score (70% skills, 30% experience)
- ✅ **Importance Weighting**: Critical (1.5x), High (1.2x), Medium (1.0x), Low (0.8x)
- ✅ **Proficiency Matching**: Compares current vs required skill levels
- ✅ **Missing Skills Detection**: Identifies gaps with priority levels

### Roadmap Generation
- ✅ **Topological Sorting**: Respects skill prerequisites using Kahn's algorithm
- ✅ **Automatic Prerequisites**: Adds missing prerequisites to learning path
- ✅ **Phase Grouping**: Groups skills into Fundamentals/Intermediate/Advanced
- ✅ **Duration Estimation**: Calculates total learning time in weeks/months

### Learning Resources
- ✅ **Curated Resources**: Documentation, courses, tutorials, books
- ✅ **Difficulty Levels**: Beginner, Intermediate, Advanced
- ✅ **Multiple Sources**: Official docs, Udemy courses, tutorials

## 🔧 Troubleshooting

### PowerShell Execution Policy Error

If you see "running scripts is disabled on this system":

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use

If port 3000 is busy:
```bash
npm run dev -- -p 3001
```

### TypeScript Errors

Ensure all dependencies are installed:
```bash
npm install
```

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [API Routes Guide](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
