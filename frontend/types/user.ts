// User types

export interface User {
  id: string;
  username: string;
  email: string;
  role: 'reader' | 'author' | 'admin';
  profile_picture_url?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

export interface UserUpdate {
  email?: string;
  bio?: string;
  profile_picture_url?: string;
}

