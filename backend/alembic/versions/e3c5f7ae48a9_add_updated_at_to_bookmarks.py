"""add_updated_at_to_bookmarks

Revision ID: e3c5f7ae48a9
Revises: c4a4c4d74bb1
Create Date: 2026-01-06 21:57:55.712179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3c5f7ae48a9'
down_revision = 'c4a4c4d74bb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add updated_at column to bookmarks table
    # (The Base class adds both created_at and updated_at, but bookmarks only had created_at)
    op.add_column('bookmarks', 
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )


def downgrade() -> None:
    # Remove updated_at column from bookmarks table
    op.drop_column('bookmarks', 'updated_at')

