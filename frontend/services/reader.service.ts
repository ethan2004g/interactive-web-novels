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
  async getBookmarks(): Promise<Bookmark[]> {
    const response = await api.get<Bookmark[]>('/bookmarks');
    return response.data;
  },

  async getMyBookmarks(): Promise<Bookmark[]> {
    return this.getBookmarks();
  },

  async addBookmark(bookId: string): Promise<Bookmark> {
    const response = await api.post<Bookmark>('/bookmarks', { book_id: bookId });
    return response.data;
  },

  async removeBookmark(bookId: string): Promise<void> {
    // First, get all bookmarks to find the one for this book
    const bookmarks = await this.getBookmarks();
    const bookmark = bookmarks.find((b) => b.book_id === bookId);
    if (bookmark) {
      await api.delete(`/bookmarks/${bookmark.id}`);
    }
  },

  async deleteBookmark(bookmarkId: string): Promise<void> {
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

  async getUserRating(bookId: string): Promise<Rating | null> {
    try {
      const response = await api.get<Rating>(`/books/${bookId}/ratings/me`);
      return response.data;
    } catch {
      return null;
    }
  },

  async getMyRating(bookId: string): Promise<Rating | null> {
    return this.getUserRating(bookId);
  },

  async rateBook(bookId: string, rating: number): Promise<Rating> {
    const response = await api.post<Rating>(`/books/${bookId}/ratings`, { rating });
    return response.data;
  },

  async createRating(bookId: string, data: RatingCreate): Promise<Rating> {
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
  async getComments(chapterId: string): Promise<Comment[]> {
    // Note: The backend API expects /chapters/{chapterId}/comments
    const response = await api.get<Comment[]>(`/chapters/${chapterId}/comments`);
    return response.data;
  },

  async getChapterComments(bookId: string, chapterId: string): Promise<Comment[]> {
    const response = await api.get<Comment[]>(`/books/${bookId}/chapters/${chapterId}/comments`);
    return response.data;
  },

  async addComment(chapterId: string, content: string, parentCommentId?: string): Promise<Comment> {
    const data: CommentCreate = { content, parent_comment_id: parentCommentId };
    const response = await api.post<Comment>(`/chapters/${chapterId}/comments`, data);
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

  async deleteComment(commentId: string): Promise<void> {
    await api.delete(`/comments/${commentId}`);
  },

  async deleteChapterComment(bookId: string, chapterId: string, commentId: string): Promise<void> {
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

  async updateProgress(
    bookId: string,
    chapterId: string,
    progressPercentage: number
  ): Promise<ReadingProgress> {
    const data: ReadingProgressUpdate = { progress_percentage: progressPercentage };
    const response = await api.post<ReadingProgress>(
      `/books/${bookId}/chapters/${chapterId}/progress`,
      data
    );
    return response.data;
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

