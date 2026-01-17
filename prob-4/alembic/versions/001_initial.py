"""
Initial migration: Create ATS tables

Revision ID: 001_initial
Create Date: 2026-01-17 11:00:00

Creates the initial database schema for the ATS system:
- candidates table
- jobs table
- applications table
- status_history table

Includes all indexes, foreign keys, and constraints.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables for ATS system."""
    
    # Create ENUM types
    op.execute("CREATE TYPE application_status_enum AS ENUM ('SUBMITTED', 'SCREENING', 'INTERVIEW_SCHEDULED', 'INTERVIEWED', 'OFFER_EXTENDED', 'HIRED', 'REJECTED')")
    op.execute("CREATE TYPE job_status_enum AS ENUM ('DRAFT', 'OPEN', 'CLOSED', 'CANCELLED')")
    
    # Create candidates table
    op.create_table(
        'candidates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20)),
        sa.Column('resume_url', sa.String(500)),
        sa.Column('skills', postgresql.JSON, default=list),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
    )
    
    # Create indexes for candidates
    op.create_index('idx_candidate_email', 'candidates', ['email'])
    op.create_index('idx_candidate_deleted', 'candidates', ['deleted_at'])
    
    # Create jobs table
    op.create_table(
        'jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('department', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('required_skills', postgresql.JSON, default=list),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('employment_type', sa.String(50), nullable=False),
        sa.Column('salary_min', sa.Integer),
        sa.Column('salary_max', sa.Integer),
        sa.Column('status', sa.Enum('DRAFT', 'OPEN', 'CLOSED', 'CANCELLED', name='job_status_enum'), nullable=False),
        sa.Column('posted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('closed_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
    )
    
    # Create indexes for jobs
    op.create_index('idx_job_title', 'jobs', ['title'])
    op.create_index('idx_job_department', 'jobs', ['department'])
    op.create_index('idx_job_status', 'jobs', ['status'])
    op.create_index('idx_job_deleted', 'jobs', ['deleted_at'])
    op.create_index('idx_job_posted_at', 'jobs', ['posted_at'])
    
    # Create applications table
    op.create_table(
        'applications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.Enum('SUBMITTED', 'SCREENING', 'INTERVIEW_SCHEDULED', 'INTERVIEWED', 'OFFER_EXTENDED', 'HIRED', 'REJECTED', name='application_status_enum'), nullable=False),
        sa.Column('cover_letter', sa.Text),
        sa.Column('resume_data', postgresql.JSON),
        sa.Column('score', sa.Integer),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('candidate_id', 'job_id', name='uq_candidate_job_application'),
    )
    
    # Create indexes for applications
    op.create_index('idx_application_candidate', 'applications', ['candidate_id'])
    op.create_index('idx_application_job', 'applications', ['job_id'])
    op.create_index('idx_application_status', 'applications', ['status'])
    op.create_index('idx_application_submitted_at', 'applications', ['submitted_at'])
    op.create_index('idx_application_deleted', 'applications', ['deleted_at'])
    op.create_index('idx_application_job_status', 'applications', ['job_id', 'status'])
    op.create_index('idx_application_candidate_status', 'applications', ['candidate_id', 'status'])
    
    # Create status_history table
    op.create_table(
        'status_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('application_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('from_status', sa.String(50), nullable=False),
        sa.Column('to_status', sa.String(50), nullable=False),
        sa.Column('changed_by', sa.String(255), nullable=False),
        sa.Column('notes', sa.Text),
        sa.Column('changed_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE'),
    )
    
    # Create indexes for status_history
    op.create_index('idx_status_history_application', 'status_history', ['application_id'])
    op.create_index('idx_status_history_to_status', 'status_history', ['to_status'])
    op.create_index('idx_status_history_changed_at', 'status_history', ['changed_at'])
    op.create_index('idx_status_history_app_date', 'status_history', ['application_id', 'changed_at'])
    op.create_index('idx_status_history_transition', 'status_history', ['from_status', 'to_status'])


def downgrade() -> None:
    """Drop all tables for ATS system."""
    
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_table('status_history')
    op.drop_table('applications')
    op.drop_table('jobs')
    op.drop_table('candidates')
    
    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS application_status_enum")
    op.execute("DROP TYPE IF EXISTS job_status_enum")
