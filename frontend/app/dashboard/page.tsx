'use client';

import { ProtectedRoute, RoleGuard } from '@/components/auth';

function DashboardContent() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Author Dashboard</h1>
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-600 text-lg">
          Author dashboard functionality will be implemented in Phase 2.5
        </p>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <DashboardContent />
      </RoleGuard>
    </ProtectedRoute>
  );
}

