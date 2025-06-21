"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('roles', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create grants table
    op.create_table(
        'grants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('funder', sa.String(length=255), nullable=False),
        sa.Column('source_url', sa.String(length=1024), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('amount_string', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('eligibility_analysis', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create organisation_profiles table
    op.create_table(
        'organisation_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('mission', sa.Text(), nullable=True),
        sa.Column('vision', sa.Text(), nullable=True),
        sa.Column('registration_number', sa.String(length=100), nullable=True),
        sa.Column('registration_date', sa.Date(), nullable=True),
        sa.Column('annual_income', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('staff_count', sa.Integer(), nullable=True),
        sa.Column('volunteer_count', sa.Integer(), nullable=True),
        sa.Column('focus_areas', sa.JSON(), nullable=True),
        sa.Column('target_beneficiaries', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indices
    op.create_index(op.f('ix_grants_funder'), 'grants', ['funder'], unique=False)
    op.create_index(op.f('ix_grants_status'), 'grants', ['status'], unique=False)
    op.create_index(op.f('ix_organisation_profiles_name'), 'organisation_profiles', ['name'], unique=True)

def downgrade():
    # Drop indices
    op.drop_index(op.f('ix_organisation_profiles_name'), table_name='organisation_profiles')
    op.drop_index(op.f('ix_grants_status'), table_name='grants')
    op.drop_index(op.f('ix_grants_funder'), table_name='grants')

    # Drop tables
    op.drop_table('organisation_profiles')
    op.drop_table('grants')
    op.drop_table('users') 