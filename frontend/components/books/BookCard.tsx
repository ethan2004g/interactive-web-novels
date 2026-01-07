'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Book } from '@/types';

interface BookCardProps {
  book: Book;
  showAuthor?: boolean;
}

export default function BookCard({ book, showAuthor = true }: BookCardProps) {
  const coverImage = book.cover_image_url || '/placeholder-book-cover.jpg';
  const averageRating = book.average_rating?.toFixed(1) || '0.0';

  return (
    <Link href={`/books/${book.id}`}>
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 h-full flex flex-col">
        {/* Book Cover */}
        <div className="relative h-64 w-full bg-gray-200">
          <Image
            src={coverImage}
            alt={book.title}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
          {/* Status Badge */}
          <div className="absolute top-2 right-2">
            <span
              className={`px-2 py-1 text-xs font-semibold rounded ${
                book.status === 'completed'
                  ? 'bg-green-100 text-green-800'
                  : book.status === 'ongoing'
                  ? 'bg-blue-100 text-blue-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              {book.status.charAt(0).toUpperCase() + book.status.slice(1)}
            </span>
          </div>
        </div>

        {/* Book Info */}
        <div className="p-4 flex-1 flex flex-col">
          {/* Title */}
          <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
            {book.title}
          </h3>

          {/* Author */}
          {showAuthor && book.author && (
            <p className="text-sm text-gray-600 mb-2">
              by {book.author.username}
            </p>
          )}

          {/* Description */}
          <p className="text-sm text-gray-600 mb-3 line-clamp-3 flex-1">
            {book.description}
          </p>

          {/* Genre */}
          {book.genre && (
            <div className="mb-3">
              <span className="inline-block bg-blue-50 text-blue-700 text-xs px-2 py-1 rounded">
                {book.genre}
              </span>
            </div>
          )}

          {/* Stats */}
          <div className="flex items-center justify-between text-sm text-gray-500 pt-3 border-t border-gray-100">
            <div className="flex items-center gap-3">
              {/* Rating */}
              <div className="flex items-center">
                <svg
                  className="w-4 h-4 text-yellow-400 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <span>{averageRating}</span>
              </div>

              {/* Views */}
              <div className="flex items-center">
                <svg
                  className="w-4 h-4 mr-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
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
                <span>{book.total_views || 0}</span>
              </div>
            </div>

            {/* Likes */}
            <div className="flex items-center">
              <svg
                className="w-4 h-4 mr-1 text-red-500"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                  clipRule="evenodd"
                />
              </svg>
              <span>{book.total_likes || 0}</span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}

