# Frontend UI for Job Matching Engine

## Overview

Beautiful, modern web interface for the Job Matching API built with vanilla HTML/CSS/JavaScript.

## Features

✨ **Premium Design**
- Gradient purple theme with smooth animations
- Responsive mobile-first layout
- Tag-based input for skills and locations
- Interactive match result cards

🎯 **Functionality**
- Input candidate profile (name, skills, experience, locations, salary)
- Add job listings via JSON
- Connect to live API or use demo mode
- View detailed match breakdowns with scores
- See missing skills highlighted

## Quick Start

### Option 1: Static File (No Server)

1. Open `index.html` directly in your browser
2. Click "Load Example" to populate with sample data
3. Update the API endpoint if needed (default: http://localhost:8000/match)
4. Click "Find Matching Jobs"

### Option 2: With Live API

1. **Start the API server:**
   ```bash
   cd ..
   uvicorn app.main:app --reload
   ```

2. **Open the UI:**
   - Simply open `index.html` in your browser
   - Or serve with Python:
     ```bash
     python -m http.server 3000
     # Visit http://localhost:3000
     ```

## Using the UI

### 1. Candidate Profile

**Name**: Enter full name

**Skills**: Type skill and press Enter to add as tag
- Example: Python, FastAPI, Docker, React

**Experience**: Years of professional experience

**Locations**: Type location and press Enter
- Example: San Francisco, Remote, New York

**Salary**: Expected annual salary (optional)

### 2. Job Listings

Paste job data as JSON array:

```json
[
  {
    "job_id": "J001",
    "title": "Senior Backend Engineer",
    "company": "TechCorp",
    "required_skills": ["Python", "FastAPI", "Docker"],
    "experience_required": "3-5 years",
    "location": "San Francisco",
    "salary_range": [100000, 150000],
    "education_required": "Bachelor's"
  }
]
```

Use "Load Example Jobs" button for sample data.

### 3. API Endpoint

Default: `http://localhost:8000/match`

Change if your API runs on a different port or host.

### 4. View Results

Results show:
- **Match score** (0-100%)
- **Breakdown** by category (Skills, Location, Salary, Experience, Role)
- **Missing skills** to learn

## Features Demo

### Tag Input
- Type and press Enter to add
- Click × to remove
- Visual tags with gradient styling

### Match Results
- Sorted by match score (highest first)
- Color-coded breakdown scores
- Missing skills highlighted in yellow

### Responsive Design
- Works on desktop, tablet, and mobile
- Smooth card hover effects
- Touch-friendly interactions

## Customization

### Colors

Edit the gradient in `<style>`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### API Endpoint

Change default API URL:

```javascript
<input type="text" id="apiUrl" value="http://your-api.com/match">
```

## Troubleshooting

**CORS Errors**
- Make sure the API has CORS enabled
- The FastAPI app already includes CORS middleware

**API Connection Failed**
- Verify API is running: `curl http://localhost:8000/health`
- Check the API URL in the UI
- Look for errors in browser console (F12)

**Invalid JSON**
- Use "Load Example Jobs" for correct format
- Validate JSON: https://jsonlint.com/

## Technologies

- **Pure Vanilla JS** - No frameworks needed
- **Modern CSS** - Gradients, animations, flexbox/grid
- **Fetch API** - For HTTP requests
- **Responsive Design** - Mobile-first approach

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Screenshots

The UI includes:
- Clean header with title and subtitle
- Two-column grid (Candidate | Jobs)
- Beautiful gradient cards
- Tag input for skills/locations
- Match results with breakdown visualization
- Empty states and loading indicators

---

**Created with ❤️ for exceptional user experience**
