'use client';

import { useState, useEffect } from 'react';
import { ProtectedRoute, RoleGuard } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { Button, LoadingSpinner } from '@/components/common';
import { Card, Alert } from '@/components/ui';
import { bookService, chapterService } from '@/services';
import { Book, ChapterCreate } from '@/types';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';

function CreateChapterContent() {
  const router = useRouter();
  const params = useParams();
  const bookId = params?.id as string;

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [book, setBook] = useState<Book | null>(null);
  const [existingChapters, setExistingChapters] = useState<number>(0);
  const [formData, setFormData] = useState<ChapterCreate>({
    title: '',
    content_type: 'simple',
    content_data: { text: '' },
    is_published: false,
    chapter_number: 1,
  });

  useEffect(() => {
    loadBook();
  }, [bookId]);

  const loadBook = async () => {
    try {
      setLoading(true);
      const [bookData, chapters] = await Promise.all([
        bookService.getBookById(bookId),
        chapterService.getChaptersByBook(bookId),
      ]);
      setBook(bookData);
      setExistingChapters(chapters.length);
      
      // Set next chapter number
      const nextChapterNumber = chapters.length + 1;
      setFormData(prev => ({
        ...prev,
        chapter_number: nextChapterNumber,
      }));
    } catch (err: any) {
      console.error('Error loading book:', err);
      setError('Failed to load book details');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!formData.title.trim()) {
      setError('Chapter title is required');
      return;
    }
    if (formData.content_type === 'simple' && !formData.content_data.text?.trim()) {
      setError('Chapter content is required');
      return;
    }

    try {
      setSaving(true);
      await chapterService.createChapter(bookId, formData);
      router.push(`/dashboard/books/${bookId}/chapters`);
    } catch (err: any) {
      console.error('Error creating chapter:', err);
      
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
          setError('Failed to create chapter. Please check your input.');
        }
      } else {
        setError('Failed to create chapter. Please try again.');
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

  if (!book) {
    return (
      <DashboardLayout>
        <Alert variant="error" title="Error">
          Book not found
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
            <span className="text-gray-900">New Chapter</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Create New Chapter</h1>
          <p className="text-gray-600 mt-1">Add a new chapter to "{book.title}"</p>
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

            {/* Content Type */}
            <div>
              <label htmlFor="contentType" className="block text-sm font-medium text-gray-700 mb-2">
                Content Type
              </label>
              <select
                id="contentType"
                value={formData.content_type}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    content_type: e.target.value as 'simple' | 'interactive',
                  })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="simple">Simple Text</option>
                <option value="interactive">Interactive (Coming in Phase 3)</option>
              </select>
              <p className="mt-1 text-sm text-gray-500">
                Interactive chapters with branching storylines and animations will be available in Phase 3
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
                  value={formData.content_data.text || ''}
                  onChange={(e) => updateContentText(e.target.value)}
                  rows={20}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono"
                  placeholder="Write your chapter content here..."
                  required
                />
                <p className="mt-1 text-sm text-gray-500">
                  Word count: {formData.content_data.text?.split(/\s+/).filter(Boolean).length || 0}
                </p>
              </div>
            )}

            {formData.content_type === 'interactive' && (
              <Alert variant="info" title="Interactive Chapters">
                Interactive chapter editor will be available in Phase 3. For now, you can only create simple text chapters.
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
                Publish chapter immediately
              </label>
            </div>

            {/* Form Actions */}
            <div className="flex gap-3 pt-4 border-t">
              <Button
                type="submit"
                variant="primary"
                disabled={saving || formData.content_type === 'interactive'}
              >
                {saving ? (
                  <>
                    <LoadingSpinner size="sm" className="mr-2" />
                    Creating...
                  </>
                ) : (
                  'Create Chapter'
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
            </div>
          </form>
        </Card>
      </div>
    </DashboardLayout>
  );
}

export default function CreateChapterPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <CreateChapterContent />
      </RoleGuard>
    </ProtectedRoute>
  );
}

