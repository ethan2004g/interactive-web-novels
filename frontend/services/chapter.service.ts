// Chapter service

import api from '@/lib/api';
import { Chapter, ChapterCreate, ChapterUpdate, ChapterFilters } from '@/types';

export const chapterService = {
  /**
   * Get all chapters for a book
   */
  async getChaptersByBook(bookId: string, filters?: ChapterFilters): Promise<Chapter[]> {
    const params = new URLSearchParams();
    
    if (filters?.is_published !== undefined) {
      params.append('published_only', filters.is_published.toString());
    }
    if (filters?.content_type) {
      params.append('content_type', filters.content_type);
    }

    const response = await api.get<any>(`/books/${bookId}/chapters?${params.toString()}`);
    
    // Backend returns: {chapters: [...], total: ...}
    // Frontend expects: just the array [...]
    return response.data.chapters || [];
  },

  /**
   * Get single chapter by ID
   */
  async getChapterById(bookId: string, chapterId: string): Promise<Chapter> {
    const response = await api.get<Chapter>(`/books/${bookId}/chapters/${chapterId}`);
    return response.data;
  },

  /**
   * Create a new chapter
   */
  async createChapter(bookId: string, data: ChapterCreate): Promise<Chapter> {
    const response = await api.post<Chapter>(`/books/${bookId}/chapters`, data);
    return response.data;
  },

  /**
   * Update a chapter
   */
  async updateChapter(bookId: string, chapterId: string, data: ChapterUpdate): Promise<Chapter> {
    const response = await api.put<Chapter>(`/books/${bookId}/chapters/${chapterId}`, data);
    return response.data;
  },

  /**
   * Delete a chapter
   */
  async deleteChapter(bookId: string, chapterId: string): Promise<void> {
    await api.delete(`/books/${bookId}/chapters/${chapterId}`);
  },

  /**
   * Reorder chapters
   */
  async reorderChapters(bookId: string, chapterIds: string[]): Promise<void> {
    await api.post(`/books/${bookId}/chapters/reorder`, { chapter_ids: chapterIds });
  },
};

