"""add foreign key to posts table

Revision ID: f3b665ace7a4
Revises: e9c30a33b0b6
Create Date: 2022-02-23 11:57:14.341771

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'f3b665ace7a4'
down_revision = 'e9c30a33b0b6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table="posts", referent_table='users',local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    # explanation (for foreign key) : name, table1, table2, column for table1, column for table2, what to do when deleted (CASCADE)
    pass


def downgrade():
    #undoing the changes from the upgrade function
    op.drop_constraint("posts_users_fkey", table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
