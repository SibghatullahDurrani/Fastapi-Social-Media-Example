"""add last few columns to post

Revision ID: a75bb319fbe4
Revises: 4f8031ad6a0b
Create Date: 2023-03-07 21:06:39.645930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a75bb319fbe4'
down_revision = '4f8031ad6a0b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.BOOLEAN(),
            nullable=False,
            server_default='TRUE'
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('now()')
        )
    )
    pass


def downgrade() -> None:
    op.drop_column(
        'posts',
        'published'
    )
    op.drop_column(
        'posts',
        'created_at'
    )
    pass
