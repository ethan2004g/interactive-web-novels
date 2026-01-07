"""add_thumbnail_url_to_books

Revision ID: 730c64a8e7fe
Revises: e3c5f7ae48a9
Create Date: 2026-01-06 23:00:30.943593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '730c64a8e7fe'
down_revision = 'e3c5f7ae48a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add thumbnail_url column to books table
    op.add_column('books', sa.Column('thumbnail_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    # Remove thumbnail_url column from books table
    op.drop_column('books', 'thumbnail_url')

