"""add content col to posts tab

Revision ID: 6ffd9835983e
Revises: 357a0c9fcaca
Create Date: 2023-03-07 20:42:27.349324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ffd9835983e'
down_revision = '357a0c9fcaca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column(
            'content',
            sa.String(),
            nullable=False
        )
    )
    pass


def downgrade() -> None:
    op.drop_column(
        'posts',
        'content'
    )
    pass
