'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthContext } from '@/contexts';

interface RoleGuardProps {
  children: React.ReactNode;
  allowedRoles: ('reader' | 'author' | 'admin')[];
  redirectTo?: string;
  fallback?: React.ReactNode;
}

/**
 * Component that restricts access based on user role
 */
export function RoleGuard({
  children,
  allowedRoles,
  redirectTo = '/',
  fallback,
}: RoleGuardProps) {
  const { user, loading, isAuthenticated } = useAuthContext();
  const router = useRouter();

  const hasRequiredRole = user && allowedRoles.includes(user.role);

  useEffect(() => {
    if (!loading && isAuthenticated && !hasRequiredRole) {
      router.push(redirectTo);
    }
  }, [hasRequiredRole, loading, isAuthenticated, redirectTo, router]);

  // Show loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // If user doesn't have required role
  if (!hasRequiredRole) {
    if (fallback) {
      return <>{fallback}</>;
    }
    return null;
  }

  return <>{children}</>;
}

