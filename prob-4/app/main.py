"""
FastAPI Main Application

ATS (Applicant Tracking System) API with JWT Authentication
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api import applications_router, candidates_router, jobs_router
from app.api.auth import router as auth_router
from app.utils.dependencies import get_current_user

# OpenAPI Tags for grouping endpoints
tags_metadata = [
    {
        "name": "Authentication",
        "description": "User authentication and authorization endpoints. Register new users, login to get JWT tokens, and manage user sessions.",
    },
    {
        "name": "Applications",
        "description": "Manage job applications with status tracking, search, filtering, and analytics. Includes advanced statistics and status flow validation.",
    },
    {
        "name": "Candidates",
        "description": "Candidate management endpoints. Create, update, and retrieve candidate profiles with their application history.",
    },
    {
        "name": "Jobs",
        "description": "Job posting management. Create job openings, update details, and view applications for each position.",
    },
    {
        "name": "Root",
        "description": "Root and health check endpoints.",
    },
    {
        "name": "Health",
        "description": "System health and status monitoring.",
    },
]

# Create FastAPI application with enhanced metadata
app = FastAPI(
    title="ATS API",
    description="""
## 🎯 Applicant Tracking System API

A production-ready RESTful API for managing job applications with advanced features.

### Key Features

* **JWT Authentication** - Secure user authentication with role-based access control
* **Status Flow Management** - State machine validation for application status transitions
* **Email Notifications** - Automated email notifications for status changes
* **Advanced Analytics** - Comprehensive statistics with Chart.js-ready data
* **Search & Filtering** - Powerful search with partial matching and multiple filters
* **Audit Trail** - Complete history of all status changes

### Status Flow

```
SUBMITTED → SCREENING → INTERVIEW_SCHEDULED → INTERVIEWED → OFFER_EXTENDED → HIRED
    ↓           ↓              ↓                  ↓               ↓
REJECTED    REJECTED       REJECTED          REJECTED        REJECTED
```

### Authentication

All endpoints (except `/auth/register` and `/auth/login`) require JWT authentication.

Use the **Authorize** button below to add your JWT token.

### Tech Stack

- **Framework**: FastAPI 0.115.12
- **Database**: PostgreSQL / SQLite
- **ORM**: SQLAlchemy 2.0.36
- **Authentication**: JWT (python-jose, bcrypt)
- **Validation**: Pydantic 2.10.6
    """,
    version="1.0.0",
    contact={
        "name": "ATS API Support",
        "email": "support@ats-api.example.com",
        "url": "https://github.com/AgroKING/Performatives",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide schemas section by default
        "docExpansion": "list",  # Expand tags but not operations
        "filter": True,  # Enable search filter
        "showCommonExtensions": True,
        "syntaxHighlight.theme": "monokai",  # Code syntax highlighting theme
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api/v1 prefix
API_V1_PREFIX = "/api/v1"

# Auth router (public - no authentication required)
app.include_router(auth_router, prefix=API_V1_PREFIX)

# Protected routers (require authentication)
app.include_router(
    applications_router,
    prefix=API_V1_PREFIX,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    candidates_router,
    prefix=API_V1_PREFIX,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    jobs_router,
    prefix=API_V1_PREFIX,
    dependencies=[Depends(get_current_user)]
)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "ATS API",
        "version": "1.0.0",
        "description": "Applicant Tracking System",
        "docs": "/api/v1/docs",
        "endpoints": {
            "applications": f"{API_V1_PREFIX}/applications",
            "candidates": f"{API_V1_PREFIX}/candidates",
            "jobs": f"{API_V1_PREFIX}/jobs"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "ATS API"
    }

# Custom OpenAPI schema with security
def custom_openapi():
    """Custom OpenAPI schema with JWT security."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=tags_metadata,
    )
    
    # Add JWT security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format: **Bearer &lt;token&gt;**"
        }
    }
    
    # Add security to protected endpoints
    for path in openapi_schema["paths"]:
        if not path.startswith("/api/v1/auth"):  # Skip auth endpoints
            for method in openapi_schema["paths"][path]:
                if method in ["get", "post", "put", "patch", "delete"]:
                    openapi_schema["paths"][path][method]["security"] = [
                        {"BearerAuth": []}
                    ]
    
    # Add common error responses to all endpoints
    common_responses = {
        "401": {
            "description": "Unauthorized - Invalid or missing authentication token",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        },
        "403": {
            "description": "Forbidden - Insufficient permissions",
            "content": {
                "application/json": {
                    "example": {"detail": "Access denied. Required role: ['ADMIN']"}
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            }
        }
    }
    
    # Add common responses to all endpoints
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "patch", "delete"]:
                if "responses" not in openapi_schema["paths"][path][method]:
                    openapi_schema["paths"][path][method]["responses"] = {}
                openapi_schema["paths"][path][method]["responses"].update(common_responses)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
