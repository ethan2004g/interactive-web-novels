'use client';

import { ProtectedRoute } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { EmptyState } from '@/components/common';
import { Button } from '@/components/common';
import Link from 'next/link';

function LibraryContent() {
  return (
    <DashboardLayout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">My Library</h1>
        <p className="text-gray-600 mb-6">Books you're currently reading or have saved</p>

        <div className="bg-white rounded-lg shadow">
          <EmptyState
            icon="📖"
            title="Your library is empty"
            description="Start exploring books to build your personal library"
            action={
              <Link href="/books">
                <Button variant="primary">Browse Books</Button>
              </Link>
            }
          />
        </div>
      </div>
    </DashboardLayout>
  );
}

export default function LibraryPage() {
  return (
    <ProtectedRoute>
      <LibraryContent />
    </ProtectedRoute>
  );
}

