// Book types

export interface Book {
  id: string;
  author_id: string;
  title: string;
  description: string;
  cover_image_url?: string;
  thumbnail_url?: string;
  genre?: string;
  tags: string[];
  status: 'draft' | 'ongoing' | 'completed';
  total_views: number;
  total_likes: number;
  created_at: string;
  updated_at: string;
  author?: {
    id: string;
    username: string;
    profile_picture_url?: string;
  };
  average_rating?: number;
  total_ratings?: number;
}

export interface BookCreate {
  title: string;
  description: string;
  cover_image_url?: string;
  genre?: string;
  tags?: string[];
  status?: 'draft' | 'ongoing' | 'completed';
}

export interface BookUpdate {
  title?: string;
  description?: string;
  cover_image_url?: string;
  genre?: string;
  tags?: string[];
  status?: 'draft' | 'ongoing' | 'completed';
}

export interface BookFilters {
  search?: string;
  genre?: string;
  status?: 'draft' | 'ongoing' | 'completed';
  author_id?: string;
  tags?: string[];
  sort_by?: 'created_at' | 'updated_at' | 'title' | 'total_views' | 'total_likes';
  order?: 'asc' | 'desc';
  page?: number;
  size?: number;
}

export interface BookStats {
  total_views: number;
  total_likes: number;
  total_ratings: number;
  average_rating: number;
  total_comments: number;
  total_bookmarks: number;
}

