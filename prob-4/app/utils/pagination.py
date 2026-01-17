"""
Pagination Utilities

Helper functions for consistent pagination across API endpoints.
"""

from typing import TypeVar, Generic, List, Any
from sqlalchemy.orm import Query
from app.schemas.pagination import PaginationMetadata


T = TypeVar('T')


def paginate(
    query: Query,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[Any], PaginationMetadata]:
    """
    Apply pagination to a SQLAlchemy query and generate metadata.
    
    Args:
        query: SQLAlchemy query object
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return
        
    Returns:
        Tuple of (paginated_results, pagination_metadata)
        
    Example:
        ```python
        query = db.query(Application).filter(...)
        results, metadata = paginate(query, skip=0, limit=20)
        ```
    """
    # Get total count before pagination
    total_count = query.count()
    
    # Apply pagination
    results = query.offset(skip).limit(limit).all()
    
    # Calculate pagination metadata
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 1
    current_page = (skip // limit) + 1 if limit > 0 else 1
    
    metadata = PaginationMetadata(
        total=total_count,
        page=current_page,
        per_page=limit,
        total_pages=total_pages,
        has_next=(skip + limit) < total_count,
        has_prev=skip > 0
    )
    
    return results, metadata


def calculate_skip(page: int, per_page: int) -> int:
    """
    Calculate skip/offset from page number.
    
    Args:
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        Skip/offset value for query
        
    Example:
        ```python
        skip = calculate_skip(page=2, per_page=20)  # Returns 20
        ```
    """
    return (page - 1) * per_page if page > 0 else 0
