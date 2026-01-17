"""
Custom Exception Hierarchy

Application-specific exceptions for better error handling.
"""

from typing import Optional, Dict, Any


class ATSException(Exception):
    """Base exception for all ATS application errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize ATS exception.
        
        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(ATSException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize validation error with 422 status code."""
        super().__init__(message, status_code=422, details=details)


class AuthenticationError(ATSException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed") -> None:
        """Initialize authentication error with 401 status code."""
        super().__init__(message, status_code=401)


class AuthorizationError(ATSException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, message: str = "Insufficient permissions") -> None:
        """Initialize authorization error with 403 status code."""
        super().__init__(message, status_code=403)


class ResourceNotFoundError(ATSException):
    """Raised when requested resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: str) -> None:
        """
        Initialize resource not found error.
        
        Args:
            resource_type: Type of resource (e.g., "Application", "Candidate")
            resource_id: ID of the resource
        """
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message, status_code=404)


class DuplicateResourceError(ATSException):
    """Raised when attempting to create a duplicate resource."""
    
    def __init__(self, resource_type: str, field: str, value: str) -> None:
        """
        Initialize duplicate resource error.
        
        Args:
            resource_type: Type of resource
            field: Field that has duplicate value
            value: The duplicate value
        """
        message = f"{resource_type} with {field}='{value}' already exists"
        super().__init__(message, status_code=400)


class InvalidStatusTransitionError(ATSException):
    """Raised when status transition is invalid."""
    
    def __init__(
        self,
        current_status: str,
        new_status: str,
        allowed_statuses: list[str]
    ) -> None:
        """
        Initialize invalid status transition error.
        
        Args:
            current_status: Current application status
            new_status: Attempted new status
            allowed_statuses: List of allowed statuses
        """
        message = (
            f"Invalid status transition: {current_status} → {new_status}. "
            f"Allowed transitions: {', '.join(allowed_statuses)}"
        )
        details = {
            "current_status": current_status,
            "requested_status": new_status,
            "allowed_statuses": allowed_statuses
        }
        super().__init__(message, status_code=400, details=details)


class DatabaseError(ATSException):
    """Raised when database operation fails."""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        """
        Initialize database error.
        
        Args:
            message: Error message
            original_error: Original exception that caused the error
        """
        details = {}
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(message, status_code=500, details=details)


class EmailServiceError(ATSException):
    """Raised when email service fails."""
    
    def __init__(self, message: str = "Failed to send email") -> None:
        """Initialize email service error with 500 status code."""
        super().__init__(message, status_code=500)
