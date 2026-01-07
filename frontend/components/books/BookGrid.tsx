'use client';

import { Book } from '@/types';
import BookCard from './BookCard';
import { EmptyState } from '../ui';

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
  if (books.length === 0) {
    return <EmptyState message={emptyMessage} />;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {books.map((book) => (
        <BookCard key={book.id} book={book} showAuthor={showAuthor} />
      ))}
    </div>
  );
}

