"""Create summary tables.

Revision ID: 001
Revises: 
Create Date: 2024-01-02
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
    # Create document_summaries table
    op.create_table(
        'document_summaries',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('document_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('executive_summary', sa.String(), nullable=False),
        sa.Column('detailed_summary', sa.String(), nullable=False),
        sa.Column('key_points', postgresql.JSONB(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('generated_at', sa.DateTime(), nullable=True),
        sa.Column('model_version', sa.String(), nullable=True),
        sa.Column('summary_stats', postgresql.JSONB(), nullable=True),
        sa.Column('confidence_scores', postgresql.JSONB(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on document_id
    op.create_index(
        'idx_document_summaries_document_id',
        'document_summaries',
        ['document_id']
    )
    
    # Create section_summaries table
    op.create_table(
        'section_summaries',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('summary_id', sa.String(), nullable=False),
        sa.Column('section_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('key_points', postgresql.JSONB(), nullable=True),
        sa.Column('importance_score', sa.Float(), nullable=True),
        sa.Column('entities', postgresql.JSONB(), nullable=True),
        sa.Column('legal_references', postgresql.JSONB(), nullable=True),
        sa.Column('temporal_references', postgresql.JSONB(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['summary_id'], ['document_summaries.id'])
    )
    
    # Create indexes
    op.create_index(
        'idx_section_summaries_summary_id',
        'section_summaries',
        ['summary_id']
    )
    
    # Create GIN indexes for JSON fields
    op.execute(
        'CREATE INDEX idx_document_summaries_metadata ON document_summaries USING gin (metadata)'
    )
    op.execute(
        'CREATE INDEX idx_section_summaries_entities ON section_summaries USING gin (entities)'
    )

def downgrade():
    # Drop indexes
    op.drop_index('idx_section_summaries_entities')
    op.drop_index('idx_document_summaries_metadata')
    op.drop_index('idx_section_summaries_summary_id')
    op.drop_index('idx_document_summaries_document_id')
    
    # Drop tables
    op.drop_table('section_summaries')
    op.drop_table('document_summaries')