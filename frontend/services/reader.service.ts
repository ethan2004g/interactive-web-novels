// Reader features service (bookmarks, ratings, comments, reading progress)

import api from '@/lib/api';
import {
  Bookmark,
  Rating,
  RatingCreate,
  RatingUpdate,
  Comment,
  CommentCreate,
  CommentUpdate,
  ReadingProgress,
  ReadingProgressUpdate,
} from '@/types';

export const readerService = {
  // Bookmarks
  async getMyBookmarks(): Promise<Bookmark[]> {
    const response = await api.get<Bookmark[]>('/bookmarks');
    return response.data;
  },

  async addBookmark(bookId: string): Promise<Bookmark> {
    const response = await api.post<Bookmark>('/bookmarks', { book_id: bookId });
    return response.data;
  },

  async removeBookmark(bookmarkId: string): Promise<void> {
    await api.delete(`/bookmarks/${bookmarkId}`);
  },

  async checkBookmark(bookId: string): Promise<boolean> {
    try {
      const response = await api.get<{ bookmarked: boolean }>(`/bookmarks/check/${bookId}`);
      return response.data.bookmarked;
    } catch {
      return false;
    }
  },

  // Ratings
  async getBookRatings(bookId: string): Promise<Rating[]> {
    const response = await api.get<Rating[]>(`/books/${bookId}/ratings`);
    return response.data;
  },

  async getMyRating(bookId: string): Promise<Rating | null> {
    try {
      const response = await api.get<Rating>(`/books/${bookId}/ratings/me`);
      return response.data;
    } catch {
      return null;
    }
  },

  async rateBook(bookId: string, data: RatingCreate): Promise<Rating> {
    const response = await api.post<Rating>(`/books/${bookId}/ratings`, data);
    return response.data;
  },

  async updateRating(bookId: string, ratingId: string, data: RatingUpdate): Promise<Rating> {
    const response = await api.put<Rating>(`/books/${bookId}/ratings/${ratingId}`, data);
    return response.data;
  },

  async deleteRating(bookId: string, ratingId: string): Promise<void> {
    await api.delete(`/books/${bookId}/ratings/${ratingId}`);
  },

  // Comments
  async getChapterComments(bookId: string, chapterId: string): Promise<Comment[]> {
    const response = await api.get<Comment[]>(`/books/${bookId}/chapters/${chapterId}/comments`);
    return response.data;
  },

  async createComment(bookId: string, chapterId: string, data: CommentCreate): Promise<Comment> {
    const response = await api.post<Comment>(
      `/books/${bookId}/chapters/${chapterId}/comments`,
      data
    );
    return response.data;
  },

  async updateComment(
    bookId: string,
    chapterId: string,
    commentId: string,
    data: CommentUpdate
  ): Promise<Comment> {
    const response = await api.put<Comment>(
      `/books/${bookId}/chapters/${chapterId}/comments/${commentId}`,
      data
    );
    return response.data;
  },

  async deleteComment(bookId: string, chapterId: string, commentId: string): Promise<void> {
    await api.delete(`/books/${bookId}/chapters/${chapterId}/comments/${commentId}`);
  },

  // Reading Progress
  async getReadingProgress(bookId: string): Promise<ReadingProgress | null> {
    try {
      const response = await api.get<ReadingProgress>(`/books/${bookId}/progress`);
      return response.data;
    } catch {
      return null;
    }
  },

  async updateReadingProgress(
    bookId: string,
    chapterId: string,
    data: ReadingProgressUpdate
  ): Promise<ReadingProgress> {
    const response = await api.post<ReadingProgress>(
      `/books/${bookId}/chapters/${chapterId}/progress`,
      data
    );
    return response.data;
  },
};

