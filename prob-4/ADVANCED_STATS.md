# Advanced Statistics Endpoint

## 📊 GET /api/v1/applications/stats/advanced

Comprehensive analytics endpoint optimized for Chart.js visualization.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | UUID | No | Filter statistics by specific job |
| `date_from` | Date | No | Start date (YYYY-MM-DD), defaults to 30 days ago |
| `date_to` | Date | No | End date (YYYY-MM-DD), defaults to today |

### Response Structure

```json
{
  "total_applications": 150,
  "date_range": {
    "from": "2026-01-01",
    "to": "2026-01-31"
  },
  "status_breakdown": [
    {
      "status": "SUBMITTED",
      "count": 50,
      "percentage": 33.33
    },
    {
      "status": "SCREENING",
      "count": 40,
      "percentage": 26.67
    }
  ],
  "conversion_metrics": {
    "applied_to_screening": 80.0,
    "screening_to_interview": 75.0,
    "interview_to_offer": 60.0,
    "offer_to_hired": 85.0,
    "overall_conversion": 30.6
  },
  "avg_time_per_stage": [
    {
      "stage": "SUBMITTED",
      "avg_days": 2.5,
      "min_days": 1.0,
      "max_days": 5.0,
      "count": 50
    }
  ],
  "funnel_data": {
    "labels": ["Applied", "Screening", "Interview", "Offer", "Hired"],
    "values": [100, 80, 60, 40, 30],
    "colors": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
  },
  "daily_trends": {
    "labels": ["2026-01-01", "2026-01-02", "2026-01-03"],
    "values": [5, 8, 12]
  }
}
```

### Features

**1. Status Breakdown**
- Count and percentage for each status
- Total applications in date range

**2. Conversion Metrics**
- Applied → Screening conversion rate
- Screening → Interview conversion rate
- Interview → Offer conversion rate
- Offer → Hired conversion rate
- Overall conversion rate (Applied → Hired)

**3. Time Metrics**
- Average days in each stage
- Min/max days per stage
- Count of applications per stage

**4. Funnel Data (Chart.js Ready)**
- Labels for each funnel stage
- Values (counts) for visualization
- Color codes for consistent theming

**5. Daily Trends**
- Application counts per day
- Fills missing dates with 0
- Ready for line/bar charts

### Usage Examples

**Get all stats for last 30 days:**
```bash
GET /api/v1/applications/stats/advanced
Authorization: Bearer {token}
```

**Get stats for specific job:**
```bash
GET /api/v1/applications/stats/advanced?job_id=123e4567-e89b-12d3-a456-426614174001
Authorization: Bearer {token}
```

**Get stats for date range:**
```bash
GET /api/v1/applications/stats/advanced?date_from=2026-01-01&date_to=2026-01-31
Authorization: Bearer {token}
```

### Chart.js Integration

**Funnel Chart:**
```javascript
const funnelChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: response.funnel_data.labels,
    datasets: [{
      data: response.funnel_data.values,
      backgroundColor: response.funnel_data.colors
    }]
  }
});
```

**Daily Trend Chart:**
```javascript
const trendChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: response.daily_trends.labels,
    datasets: [{
      label: 'Applications',
      data: response.daily_trends.values,
      borderColor: '#3B82F6',
      fill: true
    }]
  }
});
```

**Conversion Funnel:**
```javascript
const conversionData = {
  labels: ['Applied', 'Screening', 'Interview', 'Offer', 'Hired'],
  datasets: [{
    label: 'Conversion Rate (%)',
    data: [
      100,
      response.conversion_metrics.applied_to_screening,
      response.conversion_metrics.screening_to_interview,
      response.conversion_metrics.interview_to_offer,
      response.conversion_metrics.offer_to_hired
    ]
  }]
};
```

### Optimization

**SQLAlchemy Aggregations:**
- Uses `func.count()` for efficient counting
- Single query per metric type
- `cast()` for date filtering
- Indexed columns for fast filtering

**Performance:**
- Minimized database queries
- Efficient date range handling
- Optimized with proper indexes

---

**Status**: ✅ Advanced statistics endpoint complete!
