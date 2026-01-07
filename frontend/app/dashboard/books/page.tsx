'use client';

import { ProtectedRoute, RoleGuard } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { Button } from '@/components/common';
import { EmptyState } from '@/components/common';
import Link from 'next/link';

function MyBooksContent() {
  return (
    <DashboardLayout>
      <div>
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Books</h1>
            <p className="text-gray-600 mt-1">Manage your published and draft books</p>
          </div>
          <Link href="/dashboard/books/new">
            <Button variant="primary">Create New Book</Button>
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow">
          <EmptyState
            icon="📚"
            title="No books yet"
            description="Start your writing journey by creating your first book"
            action={
              <Link href="/dashboard/books/new">
                <Button variant="primary">Create Your First Book</Button>
              </Link>
            }
          />
        </div>
      </div>
    </DashboardLayout>
  );
}

export default function MyBooksPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <MyBooksContent />
      </RoleGuard>
    </ProtectedRoute>
  );
}

