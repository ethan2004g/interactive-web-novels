'use client';

import { useState, useEffect } from 'react';
import { ProtectedRoute, RoleGuard } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { Button, LoadingSpinner, EmptyState } from '@/components/common';
import { Card, Alert } from '@/components/ui';
import { bookService, chapterService } from '@/services';
import { Book, Chapter } from '@/types';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';

function ChaptersManagementContent() {
  const router = useRouter();
  const params = useParams();
  const bookId = params?.id as string;

  const [loading, setLoading] = useState(true);
  const [book, setBook] = useState<Book | null>(null);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [bookId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [bookData, chaptersData] = await Promise.all([
        bookService.getBookById(bookId),
        chapterService.getChaptersByBook(bookId),
      ]);
      setBook(bookData || null);
      const chapters = chaptersData || [];
      setChapters(chapters.sort((a, b) => a.chapter_number - b.chapter_number));
    } catch (err: any) {
      console.error('Error loading data:', err);
      setError('Failed to load book and chapters');
      setBook(null);
      setChapters([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteChapter = async (chapterId: string) => {
    if (!confirm('Are you sure you want to delete this chapter? This action cannot be undone.')) {
      return;
    }

    try {
      await chapterService.deleteChapter(bookId, chapterId);
      setChapters(chapters.filter((c) => c.id !== chapterId));
    } catch (error) {
      console.error('Error deleting chapter:', error);
      alert('Failed to delete chapter. Please try again.');
    }
  };

  const handleTogglePublish = async (chapter: Chapter) => {
    try {
      const updated = await chapterService.updateChapter(bookId, chapter.id, {
        is_published: !chapter.is_published,
      });
      setChapters(
        chapters.map((c) => (c.id === chapter.id ? updated : c))
      );
    } catch (error) {
      console.error('Error updating chapter:', error);
      alert('Failed to update chapter. Please try again.');
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

  if (error || !book) {
    return (
      <DashboardLayout>
        <Alert variant="error" title="Error">
          {error || 'Book not found'}
        </Alert>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div>
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
            <Link href="/dashboard/books" className="hover:text-indigo-600">
              My Books
            </Link>
            <span>/</span>
            <span className="text-gray-900">{book.title}</span>
          </div>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Manage Chapters</h1>
              <p className="text-gray-600 mt-1">
                {chapters.length} chapter{chapters.length !== 1 ? 's' : ''} •{' '}
                {chapters.filter((c) => c.is_published).length} published
              </p>
            </div>
            <Link href={`/dashboard/books/${bookId}/chapters/new`}>
              <Button variant="primary">Add Chapter</Button>
            </Link>
          </div>
        </div>

        {/* Chapters List */}
        {chapters.length === 0 ? (
          <div className="bg-white rounded-lg shadow">
            <EmptyState
              icon="📖"
              title="No chapters yet"
              description="Start writing by creating your first chapter"
              action={
                <Link href={`/dashboard/books/${bookId}/chapters/new`}>
                  <Button variant="primary">Create First Chapter</Button>
                </Link>
              }
            />
          </div>
        ) : (
          <div className="space-y-4">
            {chapters.map((chapter) => (
              <Card key={chapter.id}>
                <div className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-sm font-medium text-gray-500">
                          Chapter {chapter.chapter_number}
                        </span>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {chapter.title}
                        </h3>
                      </div>

                      <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                        <div className="flex items-center gap-1">
                          <span>
                            {chapter.is_published ? (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                Published
                              </span>
                            ) : (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                                Draft
                              </span>
                            )}
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <span>
                            {chapter.content_type === 'interactive' ? (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                                Interactive
                              </span>
                            ) : (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                Simple
                              </span>
                            )}
                          </span>
                        </div>
                        <span>{chapter.word_count || 0} words</span>
                        {chapter.published_at && (
                          <span>
                            Published {new Date(chapter.published_at).toLocaleDateString()}
                          </span>
                        )}
                      </div>

                      {/* Actions */}
                      <div className="flex gap-3">
                        {chapter.is_published && (
                          <Link href={`/books/${bookId}/chapters/${chapter.id}`}>
                            <Button variant="outline" size="sm">
                              View
                            </Button>
                          </Link>
                        )}
                        <Link href={`/dashboard/books/${bookId}/chapters/${chapter.id}/edit`}>
                          <Button variant="outline" size="sm">
                            Edit
                          </Button>
                        </Link>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleTogglePublish(chapter)}
                        >
                          {chapter.is_published ? 'Unpublish' : 'Publish'}
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDeleteChapter(chapter.id)}
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

        {/* Quick Stats Card */}
        <Card className="mt-6">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-600">Total Chapters</p>
                <p className="text-2xl font-bold text-gray-900">{chapters.length}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Published</p>
                <p className="text-2xl font-bold text-gray-900">
                  {chapters.filter((c) => c.is_published).length}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Words</p>
                <p className="text-2xl font-bold text-gray-900">
                  {chapters.reduce((sum, c) => sum + (c.word_count || 0), 0).toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Interactive</p>
                <p className="text-2xl font-bold text-gray-900">
                  {chapters.filter((c) => c.content_type === 'interactive').length}
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
}

export default function ChaptersManagementPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <ChaptersManagementContent />
      </RoleGuard>
    </ProtectedRoute>
  );
}

