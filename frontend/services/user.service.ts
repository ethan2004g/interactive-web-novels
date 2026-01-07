// User service

import api from '@/lib/api';
import { User, UserUpdate } from '@/types';

export const userService = {
  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me');
    return response.data;
  },

  /**
   * Update current user profile
   */
  async updateProfile(data: UserUpdate): Promise<User> {
    const response = await api.put<User>('/users/me', data);
    return response.data;
  },

  /**
   * Get user by ID
   */
  async getUserById(userId: string): Promise<User> {
    const response = await api.get<User>(`/users/${userId}`);
    return response.data;
  },
};

