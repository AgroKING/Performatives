# Advanced Search and Filtering

## 🔍 GET /api/v1/applications (Enhanced)

Advanced search and filtering with pagination metadata.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | int | No | Page number (1-indexed, default: 1) |
| `per_page` | int | No | Items per page (default: 50, max: 100) |
| `candidate_email` | string | No | Candidate email (partial match, case-insensitive) |
| `job_title` | string | No | Job title (partial match, case-insensitive) |
| `status` | string | No | Status filter (exact or comma-separated) |
| `applied_from` | date | No | Applied from date (YYYY-MM-DD) |
| `applied_to` | date | No | Applied to date (YYYY-MM-DD) |
| `sort_by` | string | No | Sort field (submitted_at, updated_at) |
| `order` | string | No | Sort order (asc, desc) |

### Response Format

```json
{
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "candidate_id": "...",
      "job_id": "...",
      "status": "SUBMITTED",
      "submitted_at": "2026-01-17T10:00:00Z",
      "updated_at": "2026-01-17T10:00:00Z"
    }
  ],
  "metadata": {
    "total": 150,
    "page": 1,
    "per_page": 50,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### Usage Examples

**1. Search by candidate email (partial match):**
```bash
GET /api/v1/applications?candidate_email=john
Authorization: Bearer {token}
```
Returns all applications from candidates with "john" in their email.

**2. Filter by job title:**
```bash
GET /api/v1/applications?job_title=engineer
Authorization: Bearer {token}
```
Returns applications for jobs with "engineer" in the title.

**3. Multiple status filter:**
```bash
GET /api/v1/applications?status=SUBMITTED,SCREENING
Authorization: Bearer {token}
```
Returns applications with status SUBMITTED or SCREENING.

**4. Date range filter:**
```bash
GET /api/v1/applications?applied_from=2026-01-01&applied_to=2026-01-31
Authorization: Bearer {token}
```
Returns applications submitted in January 2026.

**5. Combined filters with sorting:**
```bash
GET /api/v1/applications?status=SCREENING&sort_by=updated_at&order=asc&page=2&per_page=20
Authorization: Bearer {token}
```
Returns page 2 of screening applications, sorted by update date (oldest first).

**6. Search candidate and job:**
```bash
GET /api/v1/applications?candidate_email=doe&job_title=backend
Authorization: Bearer {token}
```
Returns applications from candidates with "doe" in email for "backend" jobs.

### Pagination Metadata

**Fields:**
- `total`: Total number of matching applications
- `page`: Current page number (1-indexed)
- `per_page`: Items per page
- `total_pages`: Total number of pages
- `has_next`: Boolean - whether there's a next page
- `has_prev`: Boolean - whether there's a previous page

**Example Navigation:**
```javascript
// Next page
if (response.metadata.has_next) {
  fetch(`/api/v1/applications?page=${response.metadata.page + 1}`);
}

// Previous page
if (response.metadata.has_prev) {
  fetch(`/api/v1/applications?page=${response.metadata.page - 1}`);
}
```

### Search Features

**1. Partial Match (Case-Insensitive):**
- `candidate_email`: Uses SQL `ILIKE` for fuzzy matching
- `job_title`: Uses SQL `ILIKE` for fuzzy matching

**2. Multiple Status Filter:**
- Single: `status=SUBMITTED`
- Multiple: `status=SUBMITTED,SCREENING,INTERVIEWED`
- Comma-separated values

**3. Date Range:**
- `applied_from`: Inclusive start date
- `applied_to`: Inclusive end date
- Format: YYYY-MM-DD

**4. Sorting:**
- `sort_by=submitted_at` (default) - Sort by application date
- `sort_by=updated_at` - Sort by last update
- `order=desc` (default) - Newest first
- `order=asc` - Oldest first

### Performance Optimization

**SQLAlchemy Features Used:**
- `joinedload()` - Eager loading for candidate and job
- `ilike()` - Case-insensitive partial matching
- `cast()` - Date filtering on timestamps
- `in_()` - Multiple status filtering
- Dynamic filter building - Only applies provided filters

**Indexes Used:**
- `idx_application_job_status` - Job + status filtering
- `idx_application_candidate` - Candidate filtering
- `idx_application_submitted_at` - Date sorting
- `idx_application_updated_at` - Update date sorting

### Frontend Integration

**React Example:**
```javascript
const [page, setPage] = useState(1);
const [filters, setFilters] = useState({
  candidate_email: '',
  status: '',
  sort_by: 'submitted_at',
  order: 'desc'
});

const fetchApplications = async () => {
  const params = new URLSearchParams({
    page,
    per_page: 20,
    ...filters
  });
  
  const response = await fetch(
    `/api/v1/applications?${params}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  
  const data = await response.json();
  return data;
};
```

**Vue Example:**
```javascript
const applications = ref([]);
const metadata = ref({});

const loadApplications = async (filters) => {
  const params = {
    page: filters.page || 1,
    per_page: 50,
    candidate_email: filters.email,
    status: filters.statuses?.join(','),
    sort_by: filters.sortBy || 'submitted_at',
    order: filters.order || 'desc'
  };
  
  const { data } = await axios.get('/api/v1/applications', { params });
  applications.value = data.items;
  metadata.value = data.metadata;
};
```

---

**Status**: ✅ Advanced search and filtering complete!
