'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { bookService, chapterService, readerService } from '@/services';
import { Book, Chapter } from '@/types';
import { LoadingScreen } from '@/components/common';
import { MainLayout } from '@/components/layout';
import { useAuth } from '@/hooks';

export default function BookDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const bookId = params.id as string;

  const [book, setBook] = useState<Book | null>(null);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(true);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [userRating, setUserRating] = useState<number | null>(null);
  const [ratingHover, setRatingHover] = useState<number | null>(null);

  useEffect(() => {
    fetchBookData();
    if (user) {
      checkBookmark();
      fetchUserRating();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bookId, user]);

  const fetchBookData = async () => {
    try {
      const [bookData, chaptersData] = await Promise.all([
        bookService.getBookById(bookId),
        chapterService.getChaptersByBook(bookId),
      ]);
      setBook(bookData || null);
      setChapters(chaptersData || []);
    } catch (error) {
      console.error('Error fetching book data:', error);
      setBook(null);
      setChapters([]);
    } finally {
      setLoading(false);
    }
  };

  const checkBookmark = async () => {
    try {
      const bookmarks = await readerService.getBookmarks();
      setIsBookmarked((bookmarks || []).some((b) => b.book_id === bookId));
    } catch (error) {
      console.error('Error checking bookmark:', error);
      setIsBookmarked(false);
    }
  };

  const fetchUserRating = async () => {
    try {
      const rating = await readerService.getUserRating(bookId);
      setUserRating(rating?.rating || null);
    } catch (error) {
      console.error('Error fetching user rating:', error);
    }
  };

  const handleBookmark = async () => {
    if (!user) {
      router.push('/auth/login');
      return;
    }

    try {
      if (isBookmarked) {
        await readerService.removeBookmark(bookId);
        setIsBookmarked(false);
      } else {
        await readerService.addBookmark(bookId);
        setIsBookmarked(true);
      }
    } catch (error) {
      console.error('Error toggling bookmark:', error);
    }
  };

  const handleRate = async (rating: number) => {
    if (!user) {
      router.push('/auth/login');
      return;
    }

    try {
      await readerService.rateBook(bookId, rating);
      setUserRating(rating);
      // Refresh book data to get updated average rating
      const updatedBook = await bookService.getBookById(bookId);
      setBook(updatedBook);
    } catch (error) {
      console.error('Error rating book:', error);
    }
  };

  const handleStartReading = () => {
    if (chapters.length > 0) {
      router.push(`/books/${bookId}/chapters/${chapters[0].id}`);
    }
  };

  if (loading) {
    return <LoadingScreen />;
  }

  if (!book) {
    return (
      <MainLayout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Book not found</h2>
          <Link href="/books" className="text-blue-600 hover:text-blue-700">
            Browse all books
          </Link>
        </div>
      </MainLayout>
    );
  }

  const coverImage = book.cover_image_url || '/placeholder-book-cover.jpg';
  const averageRating = book.average_rating?.toFixed(1) || '0.0';
  const publishedChapters = chapters.filter((ch) => ch.is_published);

  return (
    <MainLayout>
      <div className="max-w-6xl mx-auto">
        {/* Book Header */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 p-8">
            {/* Book Cover */}
            <div className="md:col-span-1">
              <div className="relative aspect-[2/3] w-full">
                <Image
                  src={coverImage}
                  alt={book.title}
                  fill
                  className="object-cover rounded-lg"
                  priority
                />
              </div>
            </div>

            {/* Book Info */}
            <div className="md:col-span-2">
              {/* Title and Author */}
              <div className="mb-4">
                <h1 className="text-4xl font-bold text-gray-900 mb-2">{book.title}</h1>
                {book.author && (
                  <p className="text-lg text-gray-600">
                    by{' '}
                    <Link
                      href={`/authors/${book.author.id}`}
                      className="text-blue-600 hover:text-blue-700"
                    >
                      {book.author.username}
                    </Link>
                  </p>
                )}
              </div>

              {/* Status and Genre */}
              <div className="flex flex-wrap gap-2 mb-4">
                <span
                  className={`px-3 py-1 text-sm font-semibold rounded ${
                    book.status === 'completed'
                      ? 'bg-green-100 text-green-800'
                      : book.status === 'ongoing'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {book.status.charAt(0).toUpperCase() + book.status.slice(1)}
                </span>
                {book.genre && (
                  <span className="px-3 py-1 text-sm font-semibold bg-purple-100 text-purple-800 rounded">
                    {book.genre}
                  </span>
                )}
              </div>

              {/* Stats */}
              <div className="flex flex-wrap gap-6 mb-6 text-sm text-gray-600">
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 text-yellow-400 mr-1"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span className="font-semibold">{averageRating}</span>
                  <span className="ml-1">({book.rating_count || 0} ratings)</span>
                </div>
                <div className="flex items-center">
                  <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                  </svg>
                  <span>{book.total_views || 0} views</span>
                </div>
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-red-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <span>{book.total_likes || 0} likes</span>
                </div>
                <div className="flex items-center">
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
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                    />
                  </svg>
                  <span>{publishedChapters.length} chapters</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-4 mb-6">
                <button
                  onClick={handleStartReading}
                  disabled={publishedChapters.length === 0}
                  className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                  Start Reading
                </button>
                <button
                  onClick={handleBookmark}
                  className={`px-6 py-3 rounded-md transition-colors font-medium ${
                    isBookmarked
                      ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {isBookmarked ? '★ Bookmarked' : '☆ Bookmark'}
                </button>
              </div>

              {/* Rating */}
              {user && (
                <div className="mb-6">
                  <p className="text-sm font-medium text-gray-700 mb-2">
                    {userRating ? 'Your Rating:' : 'Rate this book:'}
                  </p>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        onClick={() => handleRate(star)}
                        onMouseEnter={() => setRatingHover(star)}
                        onMouseLeave={() => setRatingHover(null)}
                        className="text-3xl transition-colors"
                      >
                        <span
                          className={
                            (ratingHover !== null ? star <= ratingHover : star <= (userRating || 0))
                              ? 'text-yellow-400'
                              : 'text-gray-300'
                          }
                        >
                          ★
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Description */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
                <p className="text-gray-700 whitespace-pre-wrap">{book.description}</p>
              </div>

              {/* Tags */}
              {book.tags && book.tags.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Tags</h3>
                  <div className="flex flex-wrap gap-2">
                    {book.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-gray-100 text-gray-700 text-sm rounded"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Chapters List */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Chapters</h2>
          
          {publishedChapters.length === 0 ? (
            <p className="text-gray-600 text-center py-8">
              No chapters published yet. Check back later!
            </p>
          ) : (
            <div className="space-y-2">
              {publishedChapters.map((chapter) => (
                <Link
                  key={chapter.id}
                  href={`/books/${bookId}/chapters/${chapter.id}`}
                  className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        Chapter {chapter.chapter_number}: {chapter.title}
                      </h3>
                      <p className="text-sm text-gray-600 mt-1">
                        {chapter.word_count || 0} words
                        {chapter.content_type === 'interactive' && (
                          <span className="ml-2 px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded">
                            Interactive
                          </span>
                        )}
                      </p>
                    </div>
                    <svg
                      className="w-5 h-5 text-gray-400"
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
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
}

