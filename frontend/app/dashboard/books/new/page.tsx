'use client';

import { ProtectedRoute, RoleGuard } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { Alert } from '@/components/ui';

function CreateBookContent() {
  return (
    <DashboardLayout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Create New Book</h1>
        
        <Alert variant="info" title="Coming Soon">
          Book creation interface will be implemented in Phase 2.5
        </Alert>
      </div>
    </DashboardLayout>
  );
}

export default function CreateBookPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <CreateBookContent />
      </RoleGuard>
    </ProtectedRoute>
  );
}

