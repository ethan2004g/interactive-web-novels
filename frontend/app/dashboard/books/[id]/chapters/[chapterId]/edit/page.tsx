'use client';

import { useState, useEffect } from 'react';
import { ProtectedRoute, RoleGuard } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { Button, LoadingSpinner } from '@/components/common';
import { Card, Alert } from '@/components/ui';
import { bookService, chapterService } from '@/services';
import { Book, Chapter, ChapterUpdate } from '@/types';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';

function EditChapterContent() {
  const router = useRouter();
  const params = useParams();
  const bookId = params?.id as string;
  const chapterId = params?.chapterId as string;

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [book, setBook] = useState<Book | null>(null);
  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [formData, setFormData] = useState<ChapterUpdate>({
    title: '',
    content_type: 'simple',
    content_data: { text: '' },
    is_published: false,
  });

  useEffect(() => {
    loadData();
  }, [bookId, chapterId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [bookData, chapterData] = await Promise.all([
        bookService.getBookById(bookId),
        chapterService.getChapterById(bookId, chapterId),
      ]);
      setBook(bookData);
      setChapter(chapterData);
      setFormData({
        title: chapterData.title,
        content_type: chapterData.content_type,
        content_data: chapterData.content_data,
        is_published: chapterData.is_published,
      });
    } catch (err: any) {
      console.error('Error loading data:', err);
      setError('Failed to load chapter details');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!formData.title?.trim()) {
      setError('Chapter title is required');
      return;
    }
    if (formData.content_type === 'simple' && !formData.content_data?.text?.trim()) {
      setError('Chapter content is required');
      return;
    }

    try {
      setSaving(true);
      await chapterService.updateChapter(bookId, chapterId, formData);
      router.push(`/dashboard/books/${bookId}/chapters`);
    } catch (err: any) {
      console.error('Error updating chapter:', err);
      
      // Handle FastAPI validation errors
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (Array.isArray(detail)) {
          // Format validation errors
          const errors = detail.map((e: any) => `${e.loc.join('.')}: ${e.msg}`).join(', ');
          setError(`Validation error: ${errors}`);
        } else if (typeof detail === 'string') {
          setError(detail);
        } else {
          setError('Failed to update chapter. Please check your input.');
        }
      } else {
        setError('Failed to update chapter. Please try again.');
      }
    } finally {
      setSaving(false);
    }
  };

  const updateContentText = (text: string) => {
    setFormData({
      ...formData,
      content_data: { ...formData.content_data, text },
    });
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

  if (!book || !chapter) {
    return (
      <DashboardLayout>
        <Alert variant="error" title="Error">
          {error || 'Chapter not found'}
        </Alert>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
            <Link href="/dashboard/books" className="hover:text-indigo-600">
              My Books
            </Link>
            <span>/</span>
            <Link href={`/dashboard/books/${bookId}/chapters`} className="hover:text-indigo-600">
              {book.title}
            </Link>
            <span>/</span>
            <span className="text-gray-900">Edit Chapter</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Edit Chapter</h1>
          <p className="text-gray-600 mt-1">
            Chapter {chapter.chapter_number} of "{book.title}"
          </p>
        </div>

        {error && (
          <Alert variant="error" title="Error" className="mb-6">
            {error}
          </Alert>
        )}

        <Card>
          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            {/* Chapter Title */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Chapter Title *
              </label>
              <input
                type="text"
                id="title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Enter chapter title"
                required
              />
            </div>

            {/* Content Type (Read-only for now) */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content Type
              </label>
              <div className="px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg text-gray-700">
                {formData.content_type === 'simple' ? 'Simple Text' : 'Interactive'}
              </div>
              <p className="mt-1 text-sm text-gray-500">
                Content type cannot be changed after creation
              </p>
            </div>

            {/* Content */}
            {formData.content_type === 'simple' && (
              <div>
                <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
                  Chapter Content *
                </label>
                <textarea
                  id="content"
                  value={formData.content_data?.text || ''}
                  onChange={(e) => updateContentText(e.target.value)}
                  rows={20}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono"
                  placeholder="Write your chapter content here..."
                  required
                />
                <p className="mt-1 text-sm text-gray-500">
                  Word count: {formData.content_data?.text?.split(/\s+/).filter(Boolean).length || 0}
                </p>
              </div>
            )}

            {formData.content_type === 'interactive' && (
              <Alert variant="info" title="Interactive Chapters">
                Interactive chapter editor will be available in Phase 3.
              </Alert>
            )}

            {/* Publish Status */}
            <div className="flex items-center">
              <input
                type="checkbox"
                id="published"
                checked={formData.is_published}
                onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="published" className="ml-2 block text-sm text-gray-700">
                Published
              </label>
            </div>

            {/* Form Actions */}
            <div className="flex gap-3 pt-4 border-t">
              <Button type="submit" variant="primary" disabled={saving}>
                {saving ? (
                  <>
                    <LoadingSpinner size="sm" className="mr-2" />
                    Saving...
                  </>
                ) : (
                  'Save Changes'
                )}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => router.back()}
                disabled={saving}
              >
                Cancel
              </Button>
              {chapter.is_published && (
                <Link href={`/books/${bookId}/chapters/${chapterId}`} target="_blank">
                  <Button variant="outline">Preview</Button>
                </Link>
              )}
            </div>
          </form>
        </Card>

        {/* Chapter Info */}
        <Card className="mt-6">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Chapter Information</h2>
            <dl className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <dt className="text-gray-600">Chapter Number</dt>
                <dd className="font-medium text-gray-900">{chapter.chapter_number}</dd>
              </div>
              <div>
                <dt className="text-gray-600">Word Count</dt>
                <dd className="font-medium text-gray-900">{chapter.word_count || 0}</dd>
              </div>
              <div>
                <dt className="text-gray-600">Created</dt>
                <dd className="font-medium text-gray-900">
                  {new Date(chapter.created_at).toLocaleDateString()}
                </dd>
              </div>
              <div>
                <dt className="text-gray-600">Last Updated</dt>
                <dd className="font-medium text-gray-900">
                  {new Date(chapter.updated_at).toLocaleDateString()}
                </dd>
              </div>
              {chapter.published_at && (
                <div>
                  <dt className="text-gray-600">Published</dt>
                  <dd className="font-medium text-gray-900">
                    {new Date(chapter.published_at).toLocaleDateString()}
                  </dd>
                </div>
              )}
            </dl>
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
}

export default function EditChapterPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <EditChapterContent />
      </RoleGuard>
    </ProtectedRoute>
  );
}

