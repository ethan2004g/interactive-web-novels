'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { chapterService, readerService } from '@/services';
import { Chapter } from '@/types';
import { LoadingScreen } from '@/components/common';
import { MainLayout } from '@/components/layout';
import { CommentSection } from '@/components/chapters';
import { useAuth } from '@/hooks';

export default function ChapterReadingPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const bookId = params.id as string;
  const chapterId = params.chapterId as string;

  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [allChapters, setAllChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(true);
  const [fontSize, setFontSize] = useState(16);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchChapterData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chapterId]);

  useEffect(() => {
    // Track reading progress
    if (user && chapter) {
      const updateProgress = async () => {
        try {
          await readerService.updateProgress(bookId, chapterId, 100);
        } catch (error) {
          console.error('Error updating progress:', error);
        }
      };
      updateProgress();
    }
  }, [user, chapter, bookId, chapterId]);

  const fetchChapterData = async () => {
    try {
      const [chapterData, chaptersData] = await Promise.all([
        chapterService.getChapterById(bookId, chapterId),
        chapterService.getChaptersByBook(bookId),
      ]);
      setChapter(chapterData);
      setAllChapters(chaptersData.filter((ch) => ch.is_published));
    } catch (error) {
      console.error('Error fetching chapter data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCurrentChapterIndex = () => {
    return allChapters.findIndex((ch) => ch.id === chapterId);
  };

  const getPreviousChapter = () => {
    const currentIndex = getCurrentChapterIndex();
    if (currentIndex > 0) {
      return allChapters[currentIndex - 1];
    }
    return null;
  };

  const getNextChapter = () => {
    const currentIndex = getCurrentChapterIndex();
    if (currentIndex >= 0 && currentIndex < allChapters.length - 1) {
      return allChapters[currentIndex + 1];
    }
    return null;
  };

  const handleFontSizeChange = (delta: number) => {
    setFontSize((prev) => Math.max(12, Math.min(24, prev + delta)));
  };

  if (loading) {
    return <LoadingScreen />;
  }

  if (!chapter) {
    return (
      <MainLayout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Chapter not found</h2>
          <Link href={`/books/${bookId}`} className="text-blue-600 hover:text-blue-700">
            Back to book
          </Link>
        </div>
      </MainLayout>
    );
  }

  const previousChapter = getPreviousChapter();
  const nextChapter = getNextChapter();

  // Render chapter content based on type
  const renderContent = () => {
    if (chapter.content_type === 'simple') {
      // Simple text content
      return (
        <div
          ref={contentRef}
          className="prose prose-lg max-w-none"
          style={{ fontSize: `${fontSize}px` }}
          dangerouslySetInnerHTML={{ __html: chapter.content_data || '' }}
        />
      );
    } else {
      // Interactive content (to be implemented in Phase 4)
      return (
        <div
          ref={contentRef}
          className="prose prose-lg max-w-none"
          style={{ fontSize: `${fontSize}px` }}
        >
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              Interactive Chapter
            </h3>
            <p className="text-blue-800">
              This chapter contains interactive elements. Full interactive support will be
              available in Phase 4. For now, displaying as simple text.
            </p>
          </div>
          <div dangerouslySetInnerHTML={{ __html: chapter.content_data || '' }} />
        </div>
      );
    }
  };

  return (
    <MainLayout>
      <div className="max-w-4xl mx-auto">
        {/* Chapter Header */}
        <div className="mb-8">
          <Link
            href={`/books/${bookId}`}
            className="text-blue-600 hover:text-blue-700 mb-4 inline-flex items-center"
          >
            <svg
              className="w-5 h-5 mr-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Back to Book
          </Link>
          
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Chapter {chapter.chapter_number}: {chapter.title}
          </h1>
          
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span>{chapter.word_count || 0} words</span>
            {chapter.content_type === 'interactive' && (
              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                Interactive
              </span>
            )}
          </div>
        </div>

        {/* Reading Controls */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">Font Size:</span>
              <button
                onClick={() => handleFontSizeChange(-2)}
                className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                aria-label="Decrease font size"
              >
                A-
              </button>
              <button
                onClick={() => handleFontSizeChange(2)}
                className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                aria-label="Increase font size"
              >
                A+
              </button>
            </div>

            {/* Chapter Navigation */}
            <div className="flex gap-2">
              {previousChapter ? (
                <Link
                  href={`/books/${bookId}/chapters/${previousChapter.id}`}
                  className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded transition-colors text-sm"
                >
                  ← Previous
                </Link>
              ) : (
                <button
                  disabled
                  className="px-4 py-2 bg-gray-100 text-gray-400 rounded cursor-not-allowed text-sm"
                >
                  ← Previous
                </button>
              )}
              
              {nextChapter ? (
                <Link
                  href={`/books/${bookId}/chapters/${nextChapter.id}`}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors text-sm"
                >
                  Next →
                </Link>
              ) : (
                <button
                  disabled
                  className="px-4 py-2 bg-gray-100 text-gray-400 rounded cursor-not-allowed text-sm"
                >
                  Next →
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Chapter Content */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          {renderContent()}
        </div>

        {/* Bottom Navigation */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center justify-between">
            {previousChapter ? (
              <Link
                href={`/books/${bookId}/chapters/${previousChapter.id}`}
                className="flex items-center text-blue-600 hover:text-blue-700"
              >
                <svg
                  className="w-5 h-5 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
                <div className="text-left">
                  <div className="text-sm text-gray-600">Previous Chapter</div>
                  <div className="font-semibold">
                    Chapter {previousChapter.chapter_number}: {previousChapter.title}
                  </div>
                </div>
              </Link>
            ) : (
              <div></div>
            )}

            {nextChapter ? (
              <Link
                href={`/books/${bookId}/chapters/${nextChapter.id}`}
                className="flex items-center text-blue-600 hover:text-blue-700"
              >
                <div className="text-right">
                  <div className="text-sm text-gray-600">Next Chapter</div>
                  <div className="font-semibold">
                    Chapter {nextChapter.chapter_number}: {nextChapter.title}
                  </div>
                </div>
                <svg
                  className="w-5 h-5 ml-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </Link>
            ) : (
              <div></div>
            )}
          </div>
        </div>

        {/* Comment Section */}
        <CommentSection chapterId={chapterId} />
      </div>
    </MainLayout>
  );
}

