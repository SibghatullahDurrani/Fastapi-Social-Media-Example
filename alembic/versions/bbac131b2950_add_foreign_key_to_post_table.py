"""add foreign key to post table

Revision ID: bbac131b2950
Revises: 54c3a1b8765b
Create Date: 2023-03-07 20:56:49.126533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbac131b2950'
down_revision = '54c3a1b8765b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False),
        # op.create_foreign_key(
        #     'posts_users_fk',
        #     source_table="posts",
        #     referent_table="users",
        #     local_cols=['owner-id'],
        #     remote_cols=['id'],
        #     ondelete="CASCADE"
        # )
    )
    pass


def downgrade() -> None:
    # op.drop_constraint(
    #     'post_user_fk',
    #     table_name="posts"
    # )
    op.drop_column(
        'posts',
        'owner_id'
    )
    pass
