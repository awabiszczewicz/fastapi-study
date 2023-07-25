"""add user table

Revision ID: d48ea058f2ab
Revises: 11c2c88e5651
Create Date: 2023-07-24 13:08:28.451073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd48ea058f2ab'
down_revision = '11c2c88e5651'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
