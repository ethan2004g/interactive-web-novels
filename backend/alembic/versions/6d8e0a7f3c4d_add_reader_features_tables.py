"""Add reader features tables

Revision ID: 6d8e0a7f3c4d
Revises: 5c7e9f8d2a3b
Create Date: 2026-01-06 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d8e0a7f3c4d'
down_revision = '5c7e9f8d2a3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create reading_progress table
    op.create_table('reading_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('progress_percentage', sa.Float(), nullable=False),
        sa.Column('last_read_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reading_progress_id'), 'reading_progress', ['id'], unique=False)
    op.create_index(op.f('ix_reading_progress_user_id'), 'reading_progress', ['user_id'], unique=False)
    op.create_index(op.f('ix_reading_progress_book_id'), 'reading_progress', ['book_id'], unique=False)
    op.create_index(op.f('ix_reading_progress_chapter_id'), 'reading_progress', ['chapter_id'], unique=False)
    
    # Create unique constraint for user_id + book_id (one progress per user per book)
    op.create_unique_constraint('uq_reading_progress_user_book', 'reading_progress', ['user_id', 'book_id'])
    
    # Create bookmarks table
    op.create_table('bookmarks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookmarks_id'), 'bookmarks', ['id'], unique=False)
    op.create_index(op.f('ix_bookmarks_user_id'), 'bookmarks', ['user_id'], unique=False)
    op.create_index(op.f('ix_bookmarks_book_id'), 'bookmarks', ['book_id'], unique=False)
    
    # Create unique constraint for user_id + book_id (one bookmark per user per book)
    op.create_unique_constraint('uq_bookmarks_user_book', 'bookmarks', ['user_id', 'book_id'])
    
    # Create ratings table
    op.create_table('ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ratings_id'), 'ratings', ['id'], unique=False)
    op.create_index(op.f('ix_ratings_user_id'), 'ratings', ['user_id'], unique=False)
    op.create_index(op.f('ix_ratings_book_id'), 'ratings', ['book_id'], unique=False)
    
    # Create unique constraint for user_id + book_id (one rating per user per book)
    op.create_unique_constraint('uq_ratings_user_book', 'ratings', ['user_id', 'book_id'])
    
    # Create comments table
    op.create_table('comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('parent_comment_id', sa.Integer(), nullable=True),
        sa.Column('content', sa.String(length=2000), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_comment_id'], ['comments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_comments_user_id'), 'comments', ['user_id'], unique=False)
    op.create_index(op.f('ix_comments_chapter_id'), 'comments', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_comments_parent_comment_id'), 'comments', ['parent_comment_id'], unique=False)


def downgrade() -> None:
    # Drop comments table
    op.drop_index(op.f('ix_comments_parent_comment_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_chapter_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_user_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    
    # Drop ratings table
    op.drop_constraint('uq_ratings_user_book', 'ratings', type_='unique')
    op.drop_index(op.f('ix_ratings_book_id'), table_name='ratings')
    op.drop_index(op.f('ix_ratings_user_id'), table_name='ratings')
    op.drop_index(op.f('ix_ratings_id'), table_name='ratings')
    op.drop_table('ratings')
    
    # Drop bookmarks table
    op.drop_constraint('uq_bookmarks_user_book', 'bookmarks', type_='unique')
    op.drop_index(op.f('ix_bookmarks_book_id'), table_name='bookmarks')
    op.drop_index(op.f('ix_bookmarks_user_id'), table_name='bookmarks')
    op.drop_index(op.f('ix_bookmarks_id'), table_name='bookmarks')
    op.drop_table('bookmarks')
    
    # Drop reading_progress table
    op.drop_constraint('uq_reading_progress_user_book', 'reading_progress', type_='unique')
    op.drop_index(op.f('ix_reading_progress_chapter_id'), table_name='reading_progress')
    op.drop_index(op.f('ix_reading_progress_book_id'), table_name='reading_progress')
    op.drop_index(op.f('ix_reading_progress_user_id'), table_name='reading_progress')
    op.drop_index(op.f('ix_reading_progress_id'), table_name='reading_progress')
    op.drop_table('reading_progress')


