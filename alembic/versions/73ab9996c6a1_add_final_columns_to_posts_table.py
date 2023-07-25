"""add final columns to posts table

Revision ID: 73ab9996c6a1
Revises: d4055f7dc1f4
Create Date: 2023-07-24 13:46:59.466137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73ab9996c6a1'
down_revision = 'd4055f7dc1f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
