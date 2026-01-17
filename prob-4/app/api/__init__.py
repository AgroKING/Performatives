"""
API package initialization.
"""

from app.api.applications import router as applications_router
from app.api.candidates import router as candidates_router
from app.api.jobs import router as jobs_router

__all__ = [
    "applications_router",
    "candidates_router",
    "jobs_router",
]
