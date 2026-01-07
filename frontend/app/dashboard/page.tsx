'use client';

import { ProtectedRoute } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { useAuthContext } from '@/contexts';

function DashboardContent() {
  const { user, isAuthor } = useAuthContext();

  return (
    <DashboardLayout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.username}!
        </h1>
        <p className="text-gray-600 mb-8">
          {isAuthor
            ? 'Manage your books and track your reader engagement'
            : 'Explore and enjoy your reading journey'}
        </p>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Total Books' : 'Books Reading'}
                </p>
                <p className="text-2xl font-bold text-gray-900">0</p>
              </div>
              <div className="text-3xl">📚</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Total Views' : 'Completed'}
                </p>
                <p className="text-2xl font-bold text-gray-900">0</p>
              </div>
              <div className="text-3xl">👁️</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Total Chapters' : 'Bookmarks'}
                </p>
                <p className="text-2xl font-bold text-gray-900">0</p>
              </div>
              <div className="text-3xl">📖</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {isAuthor ? 'Avg Rating' : 'Hours Read'}
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {isAuthor ? '0.0' : '0h'}
                </p>
              </div>
              <div className="text-3xl">⭐</div>
            </div>
          </div>
        </div>

        {/* Recent Activity Section */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              {isAuthor ? 'Recent Activity' : 'Continue Reading'}
            </h2>
          </div>
          <div className="p-6 text-center text-gray-600">
            <p className="mb-4">
              {isAuthor
                ? 'Your recent book and chapter activity will appear here'
                : 'Your reading progress will appear here'}
            </p>
            <p className="text-sm text-gray-500">
              This feature will be fully implemented in Phase 2.5
            </p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}

