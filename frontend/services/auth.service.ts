// Authentication service

import api, { apiClient } from '@/lib/api';
import { LoginRequest, RegisterRequest, AuthTokens } from '@/types';

export const authService = {
  /**
   * Login user
   */
  async login(credentials: LoginRequest): Promise<AuthTokens> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await api.post<AuthTokens>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // Save tokens
    apiClient.saveTokens(response.data.access_token, response.data.refresh_token);

    return response.data;
  },

  /**
   * Register new user
   */
  async register(data: RegisterRequest): Promise<AuthTokens> {
    const response = await api.post<AuthTokens>('/auth/register', data);

    // Save tokens
    apiClient.saveTokens(response.data.access_token, response.data.refresh_token);

    return response.data;
  },

  /**
   * Logout user
   */
  logout(): void {
    apiClient.removeTokens();
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return apiClient.isAuthenticated();
  },

  /**
   * Refresh access token
   */
  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    const response = await api.post<AuthTokens>('/auth/refresh', {
      refresh_token: refreshToken,
    });

    // Save new tokens
    apiClient.saveTokens(response.data.access_token, response.data.refresh_token);

    return response.data;
  },
};

