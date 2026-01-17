"""
Create users table migration

Revision ID: 002_create_users
Create Date: 2026-01-17 11:40:00

Creates users table for authentication.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_create_users'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create users table."""
    
    # Create user_role_enum
    op.execute("CREATE TYPE user_role_enum AS ENUM ('ADMIN', 'RECRUITER', 'CANDIDATE')")
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(100), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'RECRUITER', 'CANDIDATE', name='user_role_enum'), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True)),
    )
    
    # Create indexes
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_username', 'users', ['username'])
    op.create_index('idx_user_role', 'users', ['role'])


def downgrade() -> None:
    """Drop users table."""
    
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS user_role_enum")
