'use client';

import { Book } from '@/types';
import BookCard from './BookCard';
import { EmptyState } from '../common';

interface BookGridProps {
  books: Book[];
  emptyMessage?: string;
  showAuthor?: boolean;
}

export default function BookGrid({ 
  books, 
  emptyMessage = 'No books found', 
  showAuthor = true 
}: BookGridProps) {
  if (!books || books.length === 0) {
    return (
      <EmptyState 
        icon="📚" 
        title={emptyMessage}
        description="Check back later for new content"
      />
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {books.map((book) => (
        <BookCard key={book.id} book={book} showAuthor={showAuthor} />
      ))}
    </div>
  );
}

