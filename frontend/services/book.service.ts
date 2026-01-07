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
    if (filters?.tags) filters.tags.forEach(tag => params.append('tags', tag));
    if (filters?.sort_by) params.append('sort_by', filters.sort_by);
    if (filters?.order) params.append('order', filters.order);
    if (filters?.page) params.append('page', filters.page.toString());
    if (filters?.size) params.append('size', filters.size.toString());

    const response = await api.get<PaginatedResponse<Book>>(`/books?${params.toString()}`);
    return response.data;
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
    const params = new URLSearchParams();
    
    if (filters?.search) params.append('search', filters.search);
    if (filters?.genre) params.append('genre', filters.genre);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.tags) filters.tags.forEach(tag => params.append('tags', tag));
    if (filters?.sort_by) params.append('sort_by', filters.sort_by);
    if (filters?.order) params.append('order', filters.order);
    if (filters?.page) params.append('page', filters.page.toString());
    if (filters?.size) params.append('size', filters.size.toString());

    const response = await api.get<PaginatedResponse<Book>>(`/books/my-books?${params.toString()}`);
    return response.data;
  },
};

