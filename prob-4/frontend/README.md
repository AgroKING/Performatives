# ATS Dashboard Frontend

## Overview

Modern, responsive dashboard for the Applicant Tracking System API with beautiful UI and demo mode support.

## Features

🎨 **Premium Design**
- Blue gradient theme with professional styling
- Responsive tabs for Applications/Candidates/Jobs
- Status badges with color coding
- Smooth animations and transitions

🔐 **Authentication**
- Login screen with credentials
- JWT token management
- Demo mode fallback

📊 **Dashboard Views**
- **Stats Cards**: Total applications, candidates, positions, hires
- **Applications Tab**: View all applications with status badges
- **Candidates Tab**: Browse candidate profiles
- **Jobs Tab**: See open positions

## Quick Start

### Option 1: Demo Mode (No API)

1. Open `frontend/index.html` in your browser
2. Click "Sign In" with demo credentials:
   - Email: demo@example.com
   - Password: demo123
3. Explore the dashboard with mock data

### Option 2: With Live API

1. **Start the API server:**
   ```bash
   cd prob-4
   uvicorn app.main:app --reload
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   python -m http.server 3001
   # Visit http://localhost:3001
   ```

3. **Register a user** (via API):
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "username": "testuser",
       "password": "Test123!@#",
       "full_name": "Test User"
     }'
   ```

4. **Login** with your credentials in the UI

## Dashboard Features

### Stats Overview
- **Total Applications**: Count of all applications
- **Active Candidates**: Number of candidates in system
- **Open Positions**: Available job listings
- **Hired This Month**: Recent hires

### Applications Tab

View all applications with:
- Candidate name
- Job title and company
- Status badge (color-coded)
- Application date

**Status Types:**
- 🔵 SUBMITTED - Just applied
- 🟡 SCREENING - Under review
- 🟣 INTERVIEW_SCHEDULED - Interview set
- 🟣 INTERVIEWED - Interview completed
- 🟢 OFFER_EXTENDED - Offer sent
- ✅ HIRED - Successfully hired
- 🔴 REJECTED - Application rejected

### Candidates Tab

Browse all candidates with:
- Full name
- Email address
- Phone number
- Quick contact info

### Jobs Tab

View open positions with:
- Job title
- Company name
- Location

## Authentication Flow

### Login
1. Enter email and password
2. Click "Sign In"
3. Token stored in localStorage
4. Redirected to dashboard

### Logout
1. Click "Logout" button in navbar
2. Token cleared
3. Redirected to login screen

### Demo Mode
If API is not reachable, the UI automatically enters demo mode with mock data.

## Configuration

### API Endpoint

Default: `http://localhost:8000/api/v1`

To change, edit in code:

```javascript
const API_BASE = 'http://your-api.com/api/v1';
```

### Mock Data

Demo mode includes:
- 3 sample applications
- 3 sample candidates
- 3 sample jobs

Edit `loadMockData()` function to customize.

## UI Components

### Navbar
- Logo
- User info with avatar
- Logout button

### Stat Cards
- Large numbers with gradient text
- Hover lift effect
- Auto-updating from API

### Tabs
- Active indicator (blue underline)
- Smooth transitions
- Clean toggle between views

### Application Items
- Left border color coding
- Hover effects
- Status badges
- Compact info display

## Styling

### Color Scheme
- **Primary**: Blue (#1e3a8a to #3b82f6)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300-800
- **Responsive sizes**

## Responsive Design

**Desktop** (>768px):
- Stats in 4-column grid
- Full sidebar layout

**Mobile** (<768px):
- Stats stacked vertically
- Compact card design
- Touch-friendly buttons

## Security

- JWT tokens stored in localStorage
- Automatic token refresh (if API supports)
- HTTPS recommended for production

## Error Handling

- **Login Failed**: Shows error message
- **API Unreachable**: Falls back to demo mode
- **Empty States**: Friendly icons and messages

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Future Enhancements

- [ ] Create new application form
- [ ] Edit application status
- [ ] Advanced filtering
- [ ] Search functionality
- [ ] Real-time notifications
- [ ] Export to CSV
- [ ] Application analytics chart

## Troubleshooting

**CORS Errors**
```bash
# API should allow frontend origin
# FastAPI CORS is already configured
```

**Login Fails**
- Check API is running: `curl http://localhost:8000/health`
- Verify credentials via API docs: http://localhost:8000/docs
- Try demo mode

**Data Not Loading**
- Open browser console (F12)
- Check for API errors
- Verify token in localStorage

---

**Built for recruiters, by developers**
