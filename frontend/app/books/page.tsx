'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { bookService } from '@/services';
import { Book, BookFilters } from '@/types';
import { BookGrid } from '@/components/books';
import { LoadingSpinner } from '@/components/common';
import { MainLayout } from '@/components/layout';

const GENRES = [
  'Fantasy',
  'Science Fiction',
  'Romance',
  'Mystery',
  'Thriller',
  'Horror',
  'Adventure',
  'Historical',
  'Contemporary',
  'Young Adult',
];

const SORT_OPTIONS = [
  { label: 'Most Recent', value: 'created_at', order: 'desc' },
  { label: 'Most Popular', value: 'views', order: 'desc' },
  { label: 'Highest Rated', value: 'rating', order: 'desc' },
  { label: 'Most Liked', value: 'likes', order: 'desc' },
  { label: 'Title (A-Z)', value: 'title', order: 'asc' },
];

const STATUS_OPTIONS = [
  { label: 'All Status', value: '' },
  { label: 'Ongoing', value: 'ongoing' },
  { label: 'Completed', value: 'completed' },
  { label: 'Draft', value: 'draft' },
];

export default function BooksPage() {
  const searchParams = useSearchParams();
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [selectedSort, setSelectedSort] = useState(SORT_OPTIONS[0]);

  useEffect(() => {
    const filter = searchParams.get('filter');
    if (filter === 'featured') {
      setSelectedStatus('completed');
      setSelectedSort(SORT_OPTIONS[2]); // Highest Rated
    } else if (filter === 'trending') {
      setSelectedSort(SORT_OPTIONS[1]); // Most Popular
    }
  }, [searchParams]);

  useEffect(() => {
    fetchBooks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPage, selectedGenre, selectedStatus, selectedSort]);

  const fetchBooks = async () => {
    setLoading(true);
    try {
      const filters: BookFilters = {
        page: currentPage,
        size: 12,
        sort_by: selectedSort.value as any,
        order: selectedSort.order as 'asc' | 'desc',
      };

      if (searchQuery) filters.search = searchQuery;
      if (selectedGenre) filters.genre = selectedGenre;
      if (selectedStatus) filters.status = selectedStatus as any;

      const response = await bookService.getBooks(filters);
      setBooks(response.items);
      setTotalPages(response.pages);
    } catch (error) {
      console.error('Error fetching books:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchBooks();
  };

  const handleClearFilters = () => {
    setSearchQuery('');
    setSelectedGenre('');
    setSelectedStatus('');
    setSelectedSort(SORT_OPTIONS[0]);
    setCurrentPage(1);
  };

  return (
    <MainLayout>
      <div>
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Browse Books</h1>
          <p className="text-gray-600">
            Discover amazing interactive stories from our community of authors
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="mb-6">
            <div className="flex gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search books by title, author, or description..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                Search
              </button>
            </div>
          </form>

          {/* Filters */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Genre Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Genre
              </label>
              <select
                value={selectedGenre}
                onChange={(e) => {
                  setSelectedGenre(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Genres</option>
                {GENRES.map((genre) => (
                  <option key={genre} value={genre}>
                    {genre}
                  </option>
                ))}
              </select>
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={selectedStatus}
                onChange={(e) => {
                  setSelectedStatus(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {STATUS_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Sort Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sort By
              </label>
              <select
                value={SORT_OPTIONS.findIndex(
                  (opt) => opt.value === selectedSort.value && opt.order === selectedSort.order
                )}
                onChange={(e) => {
                  setSelectedSort(SORT_OPTIONS[parseInt(e.target.value)]);
                  setCurrentPage(1);
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {SORT_OPTIONS.map((option, index) => (
                  <option key={index} value={index}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Clear Filters Button */}
          {(searchQuery || selectedGenre || selectedStatus || selectedSort !== SORT_OPTIONS[0]) && (
            <div className="mt-4">
              <button
                onClick={handleClearFilters}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                Clear all filters
              </button>
            </div>
          )}
        </div>

        {/* Results */}
        {loading ? (
          <div className="flex justify-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <>
            {/* Results Count */}
            <div className="mb-6">
              <p className="text-gray-600">
                Found {books.length} book{books.length !== 1 ? 's' : ''}
              </p>
            </div>

            {/* Books Grid */}
            <BookGrid books={books} emptyMessage="No books found. Try adjusting your filters." />

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8 flex justify-center">
                <div className="flex gap-2">
                  <button
                    onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
                    disabled={currentPage === 1}
                    className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum;
                    if (totalPages <= 5) {
                      pageNum = i + 1;
                    } else if (currentPage <= 3) {
                      pageNum = i + 1;
                    } else if (currentPage >= totalPages - 2) {
                      pageNum = totalPages - 4 + i;
                    } else {
                      pageNum = currentPage - 2 + i;
                    }
                    
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setCurrentPage(pageNum)}
                        className={`px-4 py-2 border rounded-md ${
                          currentPage === pageNum
                            ? 'bg-blue-600 text-white border-blue-600'
                            : 'border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}

                  <button
                    onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </MainLayout>
  );
}
