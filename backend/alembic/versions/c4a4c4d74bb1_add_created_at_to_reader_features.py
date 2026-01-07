"""add_created_at_to_reader_features

Revision ID: c4a4c4d74bb1
Revises: 6d8e0a7f3c4d
Create Date: 2026-01-06 21:54:22.946407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4a4c4d74bb1'
down_revision = '6d8e0a7f3c4d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add created_at column to reading_progress table
    # (bookmarks, ratings, and comments already have created_at from initial migration)
    op.add_column('reading_progress', 
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )


def downgrade() -> None:
    # Remove created_at column from reading_progress table
    op.drop_column('reading_progress', 'created_at')

