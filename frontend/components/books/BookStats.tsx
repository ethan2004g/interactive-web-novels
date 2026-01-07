import { BookStats as BookStatsType } from '@/types';
import { Card } from '@/components/ui';

interface BookStatsProps {
  stats: BookStatsType;
  className?: string;
}

export function BookStats({ stats, className = '' }: BookStatsProps) {
  return (
    <Card className={className}>
      <div className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Statistics</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">👁️</span>
              <span className="text-sm font-medium text-gray-600">Total Views</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{stats.total_views.toLocaleString()}</p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">❤️</span>
              <span className="text-sm font-medium text-gray-600">Total Likes</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{stats.total_likes.toLocaleString()}</p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">⭐</span>
              <span className="text-sm font-medium text-gray-600">Average Rating</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {stats.average_rating.toFixed(1)}
              <span className="text-sm text-gray-500 ml-1">/ 5.0</span>
            </p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">📊</span>
              <span className="text-sm font-medium text-gray-600">Total Ratings</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{stats.total_ratings.toLocaleString()}</p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">💬</span>
              <span className="text-sm font-medium text-gray-600">Comments</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{stats.total_comments.toLocaleString()}</p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">🔖</span>
              <span className="text-sm font-medium text-gray-600">Bookmarks</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{stats.total_bookmarks.toLocaleString()}</p>
          </div>
        </div>
      </div>
    </Card>
  );
}

interface SimpleStatsGridProps {
  stats: Array<{
    label: string;
    value: string | number;
    icon: string;
  }>;
  columns?: 2 | 3 | 4;
  className?: string;
}

export function SimpleStatsGrid({ stats, columns = 4, className = '' }: SimpleStatsGridProps) {
  const gridCols = {
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  };

  return (
    <div className={`grid ${gridCols[columns]} gap-6 ${className}`}>
      {stats.map((stat, index) => (
        <div key={index} className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
            <div className="text-3xl">{stat.icon}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

