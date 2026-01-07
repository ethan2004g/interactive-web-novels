'use client';

import { useState, useEffect } from 'react';
import { ProtectedRoute } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { useAuthContext } from '@/contexts';
import { bookService, chapterService, readerService } from '@/services';
import { Book, Bookmark } from '@/types';
import { LoadingSpinner, EmptyState, Button } from '@/components/common';
import { BookCard, BookGrid } from '@/components/books';
import Link from 'next/link';

interface DashboardStats {
  totalBooks: number;
  totalViews: number;
  totalChapters: number;
  averageRating: number;
  totalBookmarks?: number;
}

function DashboardContent() {
  const { user, isAuthor } = useAuthContext();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats>({
    totalBooks: 0,
    totalViews: 0,
    totalChapters: 0,
    averageRating: 0,
    totalBookmarks: 0,
  });
  const [recentBooks, setRecentBooks] = useState<Book[]>([]);
  const [recentBookmarks, setRecentBookmarks] = useState<Bookmark[]>([]);

  useEffect(() => {
    loadDashboardData();
  }, [isAuthor]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);

      if (isAuthor) {
        // Load author stats
        const booksResponse = await bookService.getMyBooks({ size: 100 });
        const books = booksResponse?.items || [];

        // Calculate total chapters
        let totalChapters = 0;
        let totalViews = 0;
        let totalRatings = 0;
        let totalRatingSum = 0;

        for (const book of books) {
          totalViews += book.total_views || 0;
          
          // Get chapters for this book
          try {
            const chapters = await chapterService.getChaptersByBook(book.id);
            totalChapters += chapters.length;
          } catch (error) {
            // Skip if can't fetch chapters
          }

          if (book.average_rating && book.rating_count) {
            totalRatings += book.rating_count;
            totalRatingSum += book.average_rating * book.rating_count;
          }
        }

        const averageRating = totalRatings > 0 ? totalRatingSum / totalRatings : 0;

        setStats({
          totalBooks: books.length,
          totalViews,
          totalChapters,
          averageRating,
        });

        // Set recent books (up to 4)
        setRecentBooks(books.slice(0, 4));
      } else {
        // Load reader stats
        const bookmarksResponse = await readerService.getBookmarks();
        const bookmarks = bookmarksResponse || [];
        setRecentBookmarks(bookmarks.slice(0, 4));
        
        setStats({
          totalBooks: 0,
          totalViews: 0,
          totalChapters: 0,
          averageRating: 0,
          totalBookmarks: bookmarks.length,
        });
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <LoadingSpinner size="lg" />
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.username}!
        </h1>
        <p className="text-gray-600 mb-8">
          {isAuthor
            ? 'Manage your books and track your reader engagement'
            : 'Explore and enjoy your reading journey'}
        </p>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Total Books' : 'Bookmarks'}
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {isAuthor ? stats.totalBooks : stats.totalBookmarks}
                </p>
              </div>
              <div className="text-3xl">📚</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Total Views' : 'Books Read'}
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {isAuthor ? stats.totalViews.toLocaleString() : '0'}
                </p>
              </div>
              <div className="text-3xl">👁️</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Total Chapters' : 'Reading Time'}
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {isAuthor ? stats.totalChapters : '0h'}
                </p>
              </div>
              <div className="text-3xl">📖</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Avg Rating' : 'Ratings Given'}
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {isAuthor ? stats.averageRating.toFixed(1) : '0'}
                </p>
              </div>
              <div className="text-3xl">⭐</div>
            </div>
          </div>
        </div>

        {/* Recent Activity Section */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900">
              {isAuthor ? 'Recent Books' : 'Your Bookmarks'}
            </h2>
            {isAuthor && stats.totalBooks > 0 && (
              <Link href="/dashboard/books">
                <Button variant="outline" size="sm">View All</Button>
              </Link>
            )}
          </div>
          <div className="p-6">
            {isAuthor ? (
              recentBooks.length > 0 ? (
                <BookGrid books={recentBooks} />
              ) : (
                <EmptyState
                  icon="📚"
                  title="No books yet"
                  description="Start your writing journey by creating your first book"
                  action={
                    <Link href="/dashboard/books/new">
                      <Button variant="primary">Create Your First Book</Button>
                    </Link>
                  }
                />
              )
            ) : (
              recentBookmarks.length > 0 ? (
                <BookGrid books={recentBookmarks.map(b => b.book!)} />
              ) : (
                <EmptyState
                  icon="🔖"
                  title="No bookmarks yet"
                  description="Explore books and bookmark your favorites"
                  action={
                    <Link href="/books">
                      <Button variant="primary">Explore Books</Button>
                    </Link>
                  }
                />
              )
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}

