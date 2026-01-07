// Book service

import api from '@/lib/api';
import { Book, BookCreate, BookUpdate, BookFilters, BookStats, PaginatedResponse } from '@/types';

export const bookService = {
  /**
   * Get all books with filters and pagination
   */
  async getBooks(filters?: BookFilters): Promise<PaginatedResponse<Book>> {
    const params = new URLSearchParams();
    
    if (filters?.search) params.append('search', filters.search);
    if (filters?.genre) params.append('genre', filters.genre);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.author_id) params.append('author_id', filters.author_id);
    if (filters?.tags) filters.tags.forEach(tag => params.append('tags', tag.trim()));
    if (filters?.sort_by) params.append('sort_by', filters.sort_by);
    if (filters?.order) params.append('order', filters.order);
    if (filters?.page) params.append('page', filters.page.toString());
    if (filters?.size) params.append('page_size', filters.size.toString());

    const response = await api.get<any>(`/books?${params.toString()}`);
    
    // Transform backend response to match frontend expectations
    // Backend returns: {books, total, page, page_size, total_pages}
    // Frontend expects: {items, total, page, size, pages}
    return {
      items: response.data.books || [],
      total: response.data.total || 0,
      page: response.data.page || 1,
      size: response.data.page_size || 20,
      pages: response.data.total_pages || 0,
    };
  },

  /**
   * Get single book by ID
   */
  async getBookById(bookId: string): Promise<Book> {
    const response = await api.get<Book>(`/books/${bookId}`);
    return response.data;
  },

  /**
   * Create a new book
   */
  async createBook(data: BookCreate): Promise<Book> {
    const response = await api.post<Book>('/books', data);
    return response.data;
  },

  /**
   * Update a book
   */
  async updateBook(bookId: string, data: BookUpdate): Promise<Book> {
    const response = await api.put<Book>(`/books/${bookId}`, data);
    return response.data;
  },

  /**
   * Delete a book
   */
  async deleteBook(bookId: string): Promise<void> {
    await api.delete(`/books/${bookId}`);
  },

  /**
   * Get book statistics
   */
  async getBookStats(bookId: string): Promise<BookStats> {
    const response = await api.get<BookStats>(`/books/${bookId}/stats`);
    return response.data;
  },

  /**
   * Get books by current user (author)
   */
  async getMyBooks(filters?: Omit<BookFilters, 'author_id'>): Promise<PaginatedResponse<Book>> {
    const response = await api.get<Book[]>(`/books/my-books`);
    
    // Backend returns just an array, transform to paginated response
    const books = response.data || [];
    
    // Apply client-side filtering if needed
    let filteredBooks = books;
    
    if (filters?.status) {
      filteredBooks = filteredBooks.filter(book => book.status === filters.status);
    }
    if (filters?.genre) {
      filteredBooks = filteredBooks.filter(book => book.genre === filters.genre);
    }
    if (filters?.search) {
      const search = filters.search.toLowerCase();
      filteredBooks = filteredBooks.filter(book => 
        book.title.toLowerCase().includes(search) ||
        book.description.toLowerCase().includes(search)
      );
    }
    
    return {
      items: filteredBooks,
      total: filteredBooks.length,
      page: 1,
      size: filteredBooks.length,
      pages: 1,
    };
  },
};

