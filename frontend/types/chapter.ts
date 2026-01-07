// Chapter types

import { Book } from './book';

export interface Chapter {
  id: string;
  book_id: string;
  chapter_number: number;
  title: string;
  content_type: 'simple' | 'interactive';
  content_data: Record<string, any>;
  word_count: number;
  is_published: boolean;
  published_at?: string;
  created_at: string;
  updated_at: string;
}

export interface ChapterCreate {
  title: string;
  content_type: 'simple' | 'interactive';
  content_data: Record<string, any>;
  chapter_number?: number;
  is_published?: boolean;
}

export interface ChapterUpdate {
  title?: string;
  content_type?: 'simple' | 'interactive';
  content_data?: Record<string, any>;
  chapter_number?: number;
  is_published?: boolean;
}

export interface ChapterFilters {
  is_published?: boolean;
  content_type?: 'simple' | 'interactive';
}

// Reading progress
export interface ReadingProgress {
  id: string;
  user_id: string;
  book_id: string;
  chapter_id: string;
  progress_percentage: number;
  last_read_at: string;
  updated_at: string;
}

export interface ReadingProgressUpdate {
  progress_percentage: number;
}

// Comments
export interface Comment {
  id: string;
  user_id: string;
  chapter_id: string;
  parent_comment_id?: string;
  content: string;
  created_at: string;
  updated_at: string;
  user?: {
    id: string;
    username: string;
    profile_picture_url?: string;
  };
  replies?: Comment[];
}

export interface CommentCreate {
  content: string;
  parent_comment_id?: string;
}

export interface CommentUpdate {
  content: string;
}

// Bookmarks
export interface Bookmark {
  id: string;
  user_id: string;
  book_id: string;
  created_at: string;
  updated_at: string;
  book?: Book;
}

// Ratings
export interface Rating {
  id: string;
  user_id: string;
  book_id: string;
  rating: number;
  created_at: string;
  updated_at: string;
}

export interface RatingCreate {
  rating: number;
}

export interface RatingUpdate {
  rating: number;
}

