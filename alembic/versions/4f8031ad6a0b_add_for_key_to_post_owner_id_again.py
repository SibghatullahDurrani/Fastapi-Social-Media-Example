"""add for-key to post owner_id AGAIN

Revision ID: 4f8031ad6a0b
Revises: bbac131b2950
Create Date: 2023-03-07 21:03:55.634686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f8031ad6a0b'
down_revision = 'bbac131b2950'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        'posts_users_fk',
        source_table="posts",
        referent_table="users",
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint(
        'post_user_fk',
        table_name="posts"
    )
    pass
