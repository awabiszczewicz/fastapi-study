"""add content column to posts table

Revision ID: 11c2c88e5651
Revises: 6ab07d546144
Create Date: 2023-07-18 12:53:19.726819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11c2c88e5651'
down_revision = '6ab07d546144'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
