"""Add chapters table

Revision ID: 5c7e9f8d2a3b
Revises: 3fd1f6253b18
Create Date: 2026-01-06 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '5c7e9f8d2a3b'
down_revision = '3fd1f6253b18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ContentType enum (skip if already exists)
    op.execute("DO $$ BEGIN CREATE TYPE contenttype AS ENUM ('SIMPLE', 'INTERACTIVE'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    
    # Create chapters table
    op.create_table('chapters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content_type', postgresql.ENUM('SIMPLE', 'INTERACTIVE', name='contenttype', create_type=False), nullable=False),
        sa.Column('content_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False),
        sa.Column('is_published', sa.Boolean(), nullable=False),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_chapters_id'), 'chapters', ['id'], unique=False)
    op.create_index(op.f('ix_chapters_book_id'), 'chapters', ['book_id'], unique=False)
    op.create_index(op.f('ix_chapters_chapter_number'), 'chapters', ['chapter_number'], unique=False)
    op.create_index(op.f('ix_chapters_is_published'), 'chapters', ['is_published'], unique=False)
    
    # Create unique constraint for book_id + chapter_number combination
    op.create_unique_constraint('uq_chapters_book_chapter_number', 'chapters', ['book_id', 'chapter_number'])


def downgrade() -> None:
    # Drop unique constraint
    op.drop_constraint('uq_chapters_book_chapter_number', 'chapters', type_='unique')
    
    # Drop indexes
    op.drop_index(op.f('ix_chapters_is_published'), table_name='chapters')
    op.drop_index(op.f('ix_chapters_chapter_number'), table_name='chapters')
    op.drop_index(op.f('ix_chapters_book_id'), table_name='chapters')
    op.drop_index(op.f('ix_chapters_id'), table_name='chapters')
    
    # Drop table
    op.drop_table('chapters')
    
    # Drop ContentType enum
    sa.Enum(name='contenttype').drop(op.get_bind(), checkfirst=True)

