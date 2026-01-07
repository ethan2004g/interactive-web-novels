// Authentication hook

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService, userService } from '@/services';
import { User, LoginRequest, RegisterRequest } from '@/types';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Load user on mount
  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      if (authService.isAuthenticated()) {
        const userData = await userService.getCurrentUser();
        setUser(userData);
      }
    } catch (err) {
      console.error('Failed to load user:', err);
      authService.logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials: LoginRequest) => {
    try {
      setLoading(true);
      setError(null);
      await authService.login(credentials);
      await loadUser();
      router.push('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (data: RegisterRequest) => {
    try {
      setLoading(true);
      setError(null);
      await authService.register(data);
      await loadUser();
      router.push('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    router.push('/auth/login');
  };

  return {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isAuthor: user?.role === 'author',
    isReader: user?.role === 'reader',
    isAdmin: user?.role === 'admin',
  };
}

