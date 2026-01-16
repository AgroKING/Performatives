# Skill Gap Analysis & Learning Roadmap System

## 📁 Project Structure

All project files are now organized in the `problem-5/` directory:

```
problem-5/
├── app/                          # Next.js app directory
│   ├── api/
│   │   ├── analyze/route.ts     # POST /api/analyze endpoint
│   │   └── taxonomy/route.ts    # GET /api/taxonomy endpoint
│   ├── dashboard/page.tsx       # Main dashboard page
│   ├── globals.css              # Global styles with Tailwind
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Landing page
├── components/                   # React components
│   ├── AnalysisForm.tsx         # Input form with presets
│   ├── FuturePaths.tsx          # Career trajectory suggestions
│   ├── ReadinessScoreCard.tsx   # Radial progress chart
│   ├── SalaryProjection.tsx     # Salary growth estimates
│   ├── SimilarTransitionsSidebar.tsx
│   ├── SkillGapList.tsx         # Two-column skill comparison
│   ├── SkillRadarChart.tsx      # Category visualization
│   └── TimelineRoadmap.tsx      # Learning path timeline
├── data/
│   └── seed-data.json           # 40 skills, 6 roles
├── examples/
│   └── example-usage.ts         # Algorithm usage examples
├── models/
│   └── pydantic-models.py       # Python data models
├── tests/
│   ├── api-tests.ts             # Automated API tests
│   └── example-requests.md      # Test examples
├── types/
│   └── skill-taxonomy.ts        # TypeScript interfaces
├── utils/
│   └── gap-analysis.ts          # Core algorithms
├── .gitignore
├── API_README.md                # API documentation
├── README.md                    # Project overview
├── next.config.js
├── package.json
├── postcss.config.js
├── tailwind.config.js
└── tsconfig.json
```

## 🚀 Quick Start

```bash
cd problem-5
npm install
npm run dev
```

Open http://localhost:3000

## ✨ Features

### Core Features
- ✅ Gap analysis with weighted readiness scoring
- ✅ Prerequisite-aware learning roadmap
- ✅ Interactive dashboard with 8 components
- ✅ Next.js API routes

### Bonus Features
- ✅ **Salary Projection**: Current vs target earnings with growth estimates
- ✅ **Future Career Paths**: 3 next steps after target role
- ✅ **Strict Type Safety**: No `any` types
- ✅ **Edge Case Handling**: Zero skills, empty arrays, division by zero

## 📊 Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React

## 🔗 Repository

**GitHub**: https://github.com/AgroKING/Performatives.git

**Commits**:
- `22b2b0d` - Initial implementation
- `48eefce` - Reorganized into problem-5 folder

## 📝 Documentation

- [API_README.md](problem-5/API_README.md) - API endpoints and usage
- [README.md](problem-5/README.md) - Detailed project documentation
- Testing walkthrough available in artifacts

## 🎯 Key Components

1. **ReadinessScoreCard** - Radial progress (0-100)
2. **SalaryProjection** - Earnings growth visualization
3. **FuturePaths** - Career trajectory suggestions
4. **SkillRadarChart** - 4-category skill comparison
5. **SkillGapList** - Matching vs missing skills
6. **TimelineRoadmap** - Phase-based learning path
7. **AnalysisForm** - Candidate and role selection
8. **SimilarTransitionsSidebar** - Success rate insights

## ✅ Verification

- [x] All files moved to problem-5/
- [x] Git history preserved
- [x] Pushed to GitHub successfully
- [x] 30 files reorganized
- [x] No breaking changes
