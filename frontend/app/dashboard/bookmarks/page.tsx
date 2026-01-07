'use client';

import { ProtectedRoute } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { EmptyState } from '@/components/common';

function BookmarksContent() {
  return (
    <DashboardLayout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Bookmarks</h1>
        <p className="text-gray-600 mb-6">Your saved books and favorite chapters</p>

        <div className="bg-white rounded-lg shadow">
          <EmptyState
            icon="🔖"
            title="No bookmarks yet"
            description="Bookmark books and chapters to quickly access them later"
          />
        </div>
      </div>
    </DashboardLayout>
  );
}

export default function BookmarksPage() {
  return (
    <ProtectedRoute>
      <BookmarksContent />
    </ProtectedRoute>
  );
}

