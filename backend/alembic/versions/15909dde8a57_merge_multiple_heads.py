"""merge multiple heads

Revision ID: 15909dde8a57
Revises: 6a1e4451297d, f09ce7f45946
Create Date: 2025-12-26 14:45:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '15909dde8a57'
down_revision = ('6a1e4451297d', 'f09ce7f45946')
branch_labels = None
depends_on = None

def upgrade():
    pass  # nothing to do in merge migration

def downgrade():
    pass
