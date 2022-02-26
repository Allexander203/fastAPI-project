"""add last few colimns to posts table

Revision ID: 8fc1224e7afd
Revises: f3b665ace7a4
Create Date: 2022-02-23 12:07:52.582623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc1224e7afd'
down_revision = 'f3b665ace7a4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
