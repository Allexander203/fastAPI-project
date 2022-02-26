"""add content to posts table

Revision ID: ed4800063427
Revises: 60e0a5f8277c
Create Date: 2022-02-23 11:30:50.448620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed4800063427'
down_revision = '60e0a5f8277c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("posts","content")
    pass
