"""add_document_request_tables

Revision ID: 001
Revises: 
Create Date: 2025-01-02 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_type', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('storage_path', sa.String(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('integrity_verified', sa.Boolean(), nullable=True),
        sa.Column('deepfake_detection_result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('compliance_status', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('request_id', sa.String(), nullable=True),
        sa.Column('requested_by', sa.Integer(), nullable=True),
        sa.Column('requested_at', sa.DateTime(), nullable=True),
        sa.Column('submitted_by', sa.Integer(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('ai_summary', sa.String(), nullable=True),
        sa.Column('ai_processed', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.ForeignKeyConstraint(['requested_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['submitted_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_documents_request_id',
        'documents',
        ['request_id'],
        unique=False
    )

def downgrade():
    op.drop_index('ix_documents_request_id', table_name='documents')
    op.drop_table('documents')