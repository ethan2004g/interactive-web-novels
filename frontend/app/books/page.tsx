import { MainLayout } from '@/components/layout';
import { Alert } from '@/components/ui';

export default function BooksPage() {
  return (
    <MainLayout>
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-6">Browse Books</h1>
        
        <Alert variant="info" title="Coming Soon">
          Book browsing functionality with search, filters, and pagination will be implemented in Phase 2.4
        </Alert>

        {/* Placeholder for book grid */}
        <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {/* Book cards will be rendered here */}
        </div>
      </div>
    </MainLayout>
  );
}

