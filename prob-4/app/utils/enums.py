"""
Enums for ATS System

Provides type-safe enum values for application and job statuses.
"""

from enum import Enum


class ApplicationStatus(str, Enum):
    """
    Application status enum.
    
    Flow: SUBMITTED → SCREENING → INTERVIEW_SCHEDULED → INTERVIEWED → OFFER_EXTENDED → HIRED
    Can transition to REJECTED from any non-terminal state.
    """
    SUBMITTED = "SUBMITTED"
    SCREENING = "SCREENING"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    INTERVIEWED = "INTERVIEWED"
    OFFER_EXTENDED = "OFFER_EXTENDED"
    HIRED = "HIRED"
    REJECTED = "REJECTED"


class JobStatus(str, Enum):
    """Job posting status enum."""
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


# Valid status transitions for state machine
STATUS_TRANSITIONS = {
    ApplicationStatus.SUBMITTED: [
        ApplicationStatus.SCREENING,
        ApplicationStatus.REJECTED
    ],
    ApplicationStatus.SCREENING: [
        ApplicationStatus.INTERVIEW_SCHEDULED,
        ApplicationStatus.REJECTED
    ],
    ApplicationStatus.INTERVIEW_SCHEDULED: [
        ApplicationStatus.INTERVIEWED,
        ApplicationStatus.REJECTED
    ],
    ApplicationStatus.INTERVIEWED: [
        ApplicationStatus.OFFER_EXTENDED,
        ApplicationStatus.REJECTED
    ],
    ApplicationStatus.OFFER_EXTENDED: [
        ApplicationStatus.HIRED,
        ApplicationStatus.REJECTED
    ],
    ApplicationStatus.HIRED: [],  # Terminal state
    ApplicationStatus.REJECTED: []  # Terminal state
}
