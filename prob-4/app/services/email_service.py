"""
Email Service Interface and Mock Implementation

Provides email notification functionality with Jinja2 templates.
Easily swappable with real SMTP implementation.
"""

from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime, timezone
import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailServiceInterface(ABC):
    """
    Abstract base class for email services.
    
    Allows easy swapping between mock and real SMTP implementations.
    """
    
    @abstractmethod
    async def send_status_change_email(
        self,
        candidate_email: str,
        candidate_name: str,
        old_status: str,
        new_status: str,
        job_title: str,
        company_name: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Send status change notification email.
        
        Args:
            candidate_email: Recipient email address
            candidate_name: Candidate's full name
            old_status: Previous application status
            new_status: New application status
            job_title: Job title
            company_name: Company name
            notes: Optional notes from recruiter
            
        Returns:
            True if email sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    async def send_welcome_email(
        self,
        candidate_email: str,
        candidate_name: str
    ) -> bool:
        """Send welcome email to new candidate."""
        pass


class MockEmailService(EmailServiceInterface):
    """
    Mock email service that logs to console.
    
    For development and testing. Easily swappable with real SMTP.
    """
    
    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize mock email service.
        
        Args:
            template_dir: Path to Jinja2 templates directory
        """
        if template_dir is None:
            # Default to app/templates/emails
            template_dir = Path(__file__).parent.parent / "templates" / "emails"
        
        self.template_dir = template_dir
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        logger.info(f"MockEmailService initialized with templates from: {template_dir}")
    
    async def send_status_change_email(
        self,
        candidate_email: str,
        candidate_name: str,
        old_status: str,
        new_status: str,
        job_title: str,
        company_name: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Send status change notification (mock - logs to console).
        
        Args:
            candidate_email: Recipient email
            candidate_name: Candidate's name
            old_status: Previous status
            new_status: New status
            job_title: Job title
            company_name: Company name
            notes: Optional notes
            
        Returns:
            True (always succeeds in mock)
        """
        try:
            # Get appropriate template based on new status
            template_name = self._get_template_name(new_status)
            template = self.jinja_env.get_template(template_name)
            
            # Render email body
            email_body = template.render(
                candidate_name=candidate_name,
                old_status=old_status,
                new_status=new_status,
                job_title=job_title,
                company_name=company_name,
                notes=notes,
                timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            )
            
            # Log email to console
            self._log_email(
                to=candidate_email,
                subject=f"Application Status Update: {new_status}",
                body=email_body
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send status change email: {e}")
            return False
    
    async def send_welcome_email(
        self,
        candidate_email: str,
        candidate_name: str
    ) -> bool:
        """
        Send welcome email (mock - logs to console).
        
        Args:
            candidate_email: Recipient email
            candidate_name: Candidate's name
            
        Returns:
            True (always succeeds in mock)
        """
        try:
            template = self.jinja_env.get_template("welcome.html")
            
            email_body = template.render(
                candidate_name=candidate_name,
                timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            )
            
            self._log_email(
                to=candidate_email,
                subject="Welcome to Our ATS System",
                body=email_body
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
            return False
    
    def _get_template_name(self, status: str) -> str:
        """
        Get template filename based on status.
        
        Args:
            status: Application status
            
        Returns:
            Template filename
        """
        status_templates = {
            "SCREENING": "status_screening.html",
            "INTERVIEW_SCHEDULED": "status_interview_scheduled.html",
            "INTERVIEWED": "status_interviewed.html",
            "OFFER_EXTENDED": "status_offer_extended.html",
            "HIRED": "status_hired.html",
            "REJECTED": "status_rejected.html",
        }
        
        return status_templates.get(status, "status_generic.html")
    
    def _log_email(self, to: str, subject: str, body: str) -> None:
        """
        Log email to console with formatting.
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body (HTML)
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        separator = "=" * 80
        
        log_message = f"""
{separator}
📧 MOCK EMAIL SENT
{separator}
Timestamp:  {timestamp}
To:         {to}
Subject:    {subject}
{separator}
Body:
{body}
{separator}
"""
        
        logger.info(log_message)
        print(log_message)  # Also print to console for visibility


class SMTPEmailService(EmailServiceInterface):
    """
    Real SMTP email service implementation.
    
    TODO: Implement when ready for production.
    """
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        template_dir: Optional[Path] = None
    ):
        """
        Initialize SMTP email service.
        
        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
            template_dir: Path to templates
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates" / "emails"
        
        self.template_dir = template_dir
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    async def send_status_change_email(
        self,
        candidate_email: str,
        candidate_name: str,
        old_status: str,
        new_status: str,
        job_title: str,
        company_name: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Send status change email via SMTP.
        
        TODO: Implement SMTP sending logic.
        """
        # TODO: Implement with aiosmtplib or similar
        raise NotImplementedError("SMTP email service not yet implemented")
    
    async def send_welcome_email(
        self,
        candidate_email: str,
        candidate_name: str
    ) -> bool:
        """
        Send welcome email via SMTP.
        
        TODO: Implement SMTP sending logic.
        """
        raise NotImplementedError("SMTP email service not yet implemented")


# Factory function for easy service creation
def get_email_service(use_mock: bool = True) -> EmailServiceInterface:
    """
    Get email service instance.
    
    Args:
        use_mock: If True, return MockEmailService. If False, return SMTPEmailService.
        
    Returns:
        EmailServiceInterface implementation
    """
    if use_mock:
        return MockEmailService()
    else:
        # TODO: Load SMTP config from environment variables
        raise NotImplementedError("SMTP service not configured yet")
