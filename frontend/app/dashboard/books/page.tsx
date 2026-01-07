'use client';

import { useState, useEffect } from 'react';
import { ProtectedRoute, RoleGuard } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { Button, LoadingSpinner, EmptyState } from '@/components/common';
import { Card } from '@/components/ui';
import Link from 'next/link';
import { bookService, chapterService } from '@/services';
import { Book, Chapter } from '@/types';
import { useRouter } from 'next/navigation';

interface BookWithChapterCount extends Book {
  chapterCount?: number;
}

function MyBooksContent() {
  const router = useRouter();
  const [books, setBooks] = useState<BookWithChapterCount[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'draft' | 'ongoing' | 'completed'>('all');

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    try {
      setLoading(true);
      const response = await bookService.getMyBooks({ size: 100 });
      const items = response?.items || [];
      
      // Get chapter counts for each book
      const booksWithCounts = await Promise.all(
        items.map(async (book) => {
          try {
            const chapters = await chapterService.getChaptersByBook(book.id);
            return { ...book, chapterCount: chapters.length };
          } catch (error) {
            return { ...book, chapterCount: 0 };
          }
        })
      );
      
      setBooks(booksWithCounts);
    } catch (error) {
      console.error('Error loading books:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteBook = async (bookId: string) => {
    if (!confirm('Are you sure you want to delete this book? This action cannot be undone.')) {
      return;
    }

    try {
      await bookService.deleteBook(bookId);
      setBooks(books.filter(b => b.id !== bookId));
    } catch (error) {
      console.error('Error deleting book:', error);
      alert('Failed to delete book. Please try again.');
    }
  };

  const filteredBooks = books.filter(book => {
    if (filter === 'all') return true;
    return book.status === filter;
  });

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'draft':
        return 'bg-gray-100 text-gray-800';
      case 'ongoing':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <DashboardLayout>
      <div>
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Books</h1>
            <p className="text-gray-600 mt-1">Manage your published and draft books</p>
          </div>
          <Link href="/dashboard/books/new">
            <Button variant="primary">Create New Book</Button>
          </Link>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All ({books.length})
          </button>
          <button
            onClick={() => setFilter('draft')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === 'draft'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Drafts ({books.filter(b => b.status === 'draft').length})
          </button>
          <button
            onClick={() => setFilter('ongoing')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === 'ongoing'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Ongoing ({books.filter(b => b.status === 'ongoing').length})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === 'completed'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Completed ({books.filter(b => b.status === 'completed').length})
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <LoadingSpinner size="lg" />
          </div>
        ) : filteredBooks.length === 0 ? (
          <div className="bg-white rounded-lg shadow">
            <EmptyState
              icon="📚"
              title={filter === 'all' ? 'No books yet' : `No ${filter} books`}
              description={
                filter === 'all'
                  ? 'Start your writing journey by creating your first book'
                  : `You don't have any ${filter} books yet`
              }
              action={
                filter === 'all' ? (
                  <Link href="/dashboard/books/new">
                    <Button variant="primary">Create Your First Book</Button>
                  </Link>
                ) : null
              }
            />
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {filteredBooks.map((book) => (
              <Card key={book.id}>
                <div className="p-6">
                  <div className="flex gap-6">
                    {/* Book Cover */}
                    <div className="flex-shrink-0">
                      {book.cover_image_url ? (
                        <img
                          src={book.cover_image_url}
                          alt={book.title}
                          className="w-32 h-48 object-cover rounded-lg"
                        />
                      ) : (
                        <div className="w-32 h-48 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg flex items-center justify-center">
                          <span className="text-4xl">📖</span>
                        </div>
                      )}
                    </div>

                    {/* Book Details */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h3 className="text-xl font-bold text-gray-900 mb-1">
                            {book.title}
                          </h3>
                          <div className="flex items-center gap-2 mb-2">
                            <span
                              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeClass(
                                book.status
                              )}`}
                            >
                              {book.status.charAt(0).toUpperCase() + book.status.slice(1)}
                            </span>
                            {book.genre && (
                              <span className="text-sm text-gray-500">• {book.genre}</span>
                            )}
                          </div>
                        </div>
                      </div>

                      <p className="text-gray-600 mb-4 line-clamp-2">
                        {book.description}
                      </p>

                      {/* Stats */}
                      <div className="flex items-center gap-6 text-sm text-gray-600 mb-4">
                        <div className="flex items-center gap-1">
                          <span>📖</span>
                          <span>{book.chapterCount || 0} chapters</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span>👁️</span>
                          <span>{book.total_views || 0} views</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span>⭐</span>
                          <span>{book.average_rating?.toFixed(1) || '0.0'} rating</span>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex gap-3">
                        <Link href={`/books/${book.id}`}>
                          <Button variant="outline" size="sm">View</Button>
                        </Link>
                        <Link href={`/dashboard/books/${book.id}/edit`}>
                          <Button variant="outline" size="sm">Edit</Button>
                        </Link>
                        <Link href={`/dashboard/books/${book.id}/chapters`}>
                          <Button variant="outline" size="sm">Chapters</Button>
                        </Link>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDeleteBook(book.id)}
                          className="text-red-600 hover:bg-red-50"
                        >
                          Delete
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default function MyBooksPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <MyBooksContent />
      </RoleGuard>
    </ProtectedRoute>
  );
}

