"""
Schemas package initialization.

Imports all schemas for easy access.
"""

from app.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse
)
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse
)
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithHistory,
    StatusChangeRequest,
    ApplicationStatsResponse
)
from app.schemas.status_history import StatusHistoryResponse
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
    TokenData
)

__all__ = [
    # Candidate schemas
    "CandidateCreate",
    "CandidateUpdate",
    "CandidateResponse",
    # Job schemas
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    # Application schemas
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "ApplicationWithHistory",
    "StatusChangeRequest",
    "ApplicationStatsResponse",
    # Status history schemas
    "StatusHistoryResponse",
    # User schemas
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
]
