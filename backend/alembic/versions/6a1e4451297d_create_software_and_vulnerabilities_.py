"""create software and vulnerabilities tables

Revision ID: 6a1e4451297d
Revises: 
Create Date: 2025-12-26 14:15:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '6a1e4451297d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'software',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('published_date', sa.Date(), nullable=True)
    )
    op.create_table(
        'vulnerabilities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('cve_id', sa.String(), nullable=False),
        sa.Column('software_name', sa.String(), nullable=False),
        sa.Column('affected_version', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('patch_command', sa.String(), nullable=True),
        sa.Column('published_date', sa.Date(), nullable=True)
    )

def downgrade():
    op.drop_table('vulnerabilities')
    op.drop_table('software')
