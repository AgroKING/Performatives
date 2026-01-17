"""
Models package initialization.

Imports all models for easy access and Alembic auto-generation.
"""

from app.database import Base
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.models.status_history import StatusHistory
from app.models.user import User

# Export all models
__all__ = [
    "Base",
    "Candidate",
    "Job",
    "Application",
    "StatusHistory",
    "User",
]
