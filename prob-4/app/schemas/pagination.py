"""
Pagination Schema

Response schema for paginated results.
"""

from pydantic import BaseModel, Field
from typing import List, Generic, TypeVar, Optional

T = TypeVar('T')


class PaginationMetadata(BaseModel):
    """Pagination metadata."""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number (1-indexed)")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T] = Field(..., description="List of items")
    metadata: PaginationMetadata = Field(..., description="Pagination metadata")
