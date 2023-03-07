"""create posts table

Revision ID: 357a0c9fcaca
Revises: 
Create Date: 2023-03-07 20:31:19.119400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '357a0c9fcaca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            primary_key=True
        ),
        sa.Column(
            'title',
            sa.String(),
            nullable=False
        )
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
