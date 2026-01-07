# Interactive Web Novels - Frontend

This is the Next.js frontend application for the Interactive Web Novels platform.

## Tech Stack

- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **State Management:** React Hooks + Context (to be implemented)

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
├── components/             # React components
│   ├── layout/            # Layout components (Header, Footer, etc.)
│   ├── ui/                # UI components (Button, Input, etc.)
│   ├── books/             # Book-related components
│   ├── chapters/          # Chapter-related components
│   ├── auth/              # Authentication components
│   └── common/            # Common/shared components
├── contexts/              # React contexts
├── hooks/                 # Custom React hooks
├── lib/                   # Utility functions and configurations
│   ├── api.ts            # API client configuration
│   └── utils.ts          # Utility functions
├── services/              # API service layer
│   ├── auth.service.ts   # Authentication services
│   ├── user.service.ts   # User services
│   ├── book.service.ts   # Book services
│   ├── chapter.service.ts # Chapter services
│   └── reader.service.ts # Reader features (bookmarks, ratings, etc.)
├── types/                 # TypeScript type definitions
│   ├── api.ts            # API response types
│   ├── auth.ts           # Authentication types
│   ├── user.ts           # User types
│   ├── book.ts           # Book types
│   └── chapter.ts        # Chapter types
└── public/                # Static assets
```

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file (copy from `.env.example`):
```bash
cp .env.example .env.local
```

3. Update environment variables in `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Interactive Web Novels
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Build for production:

```bash
npm run build
```

Start production server:

```bash
npm start
```

## Features Implemented

### Phase 2.1: Frontend Project Setup ✅
✅ Next.js project with TypeScript  
✅ Tailwind CSS configured  
✅ Project structure (components, hooks, services, types, lib)  
✅ Environment variables setup  
✅ API client with authentication and token refresh  
✅ Service layer for all backend endpoints:
  - Authentication (login, register, logout)
  - Users (profile management)
  - Books (CRUD operations)
  - Chapters (CRUD operations)
  - Reader features (bookmarks, ratings, comments, reading progress)
✅ TypeScript types for all API models  
✅ Custom hooks (useAuth)  
✅ Utility functions

### Phase 2.2: Authentication UI ✅
✅ AuthContext provider for global authentication state  
✅ Login page with form validation  
✅ Registration page with role selection (Reader/Author)  
✅ Protected route component  
✅ Role-based access control component  
✅ User profile page with edit functionality  
✅ Navigation header with auth-aware UI  
✅ Footer component  
✅ Modern home page with hero section  
✅ Placeholder pages for books and dashboard

## API Services

The application includes a complete service layer for interacting with the backend API:

### Authentication Service
- `login(credentials)` - User login
- `register(data)` - User registration
- `logout()` - User logout
- `isAuthenticated()` - Check authentication status
- `refreshToken(token)` - Refresh access token

### User Service
- `getCurrentUser()` - Get current user profile
- `updateProfile(data)` - Update user profile
- `getUserById(userId)` - Get user by ID

### Book Service
- `getBooks(filters)` - Get all books with filters
- `getBookById(bookId)` - Get single book
- `createBook(data)` - Create new book
- `updateBook(bookId, data)` - Update book
- `deleteBook(bookId)` - Delete book
- `getBookStats(bookId)` - Get book statistics
- `getMyBooks(filters)` - Get current user's books

### Chapter Service
- `getChaptersByBook(bookId, filters)` - Get chapters for a book
- `getChapterById(bookId, chapterId)` - Get single chapter
- `createChapter(bookId, data)` - Create new chapter
- `updateChapter(bookId, chapterId, data)` - Update chapter
- `deleteChapter(bookId, chapterId)` - Delete chapter
- `reorderChapters(bookId, chapterIds)` - Reorder chapters

### Reader Service
- Bookmarks: `getMyBookmarks()`, `addBookmark()`, `removeBookmark()`, `checkBookmark()`
- Ratings: `getBookRatings()`, `getMyRating()`, `rateBook()`, `updateRating()`, `deleteRating()`
- Comments: `getChapterComments()`, `createComment()`, `updateComment()`, `deleteComment()`
- Reading Progress: `getReadingProgress()`, `updateReadingProgress()`

## Available Pages

### Public Pages
- `/` - Home page with hero section
- `/auth/login` - User login
- `/auth/register` - User registration
- `/books` - Browse books (placeholder for Phase 2.4)

### Protected Pages (Authentication Required)
- `/profile` - User profile management
- `/dashboard` - Author dashboard (authors only, placeholder for Phase 2.5)

## Authentication System

### Using AuthContext
```tsx
import { useAuthContext } from '@/contexts';

function MyComponent() {
  const { user, isAuthenticated, isAuthor, logout } = useAuthContext();
  
  return (
    <div>
      {isAuthenticated && <p>Welcome, {user.username}!</p>}
      {isAuthor && <button>Create Book</button>}
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### Protected Routes
```tsx
import { ProtectedRoute } from '@/components/auth';

export default function MyPage() {
  return (
    <ProtectedRoute>
      <div>Protected content</div>
    </ProtectedRoute>
  );
}
```

### Role-Based Access
```tsx
import { RoleGuard } from '@/components/auth';

export default function AuthorPage() {
  return (
    <RoleGuard allowedRoles={['author', 'admin']}>
      <div>Author-only content</div>
    </RoleGuard>
  );
}
```

## Next Steps (Phase 2.3)

- [ ] Create main layout component variations
- [ ] Implement sidebar for user dashboard
- [ ] Add loading states and error boundaries
- [ ] Enhance responsive design
- [ ] Add breadcrumbs and page titles

## Notes

- The API client automatically handles JWT token storage and refresh
- All services use TypeScript for type safety
- Error handling is built into the API client
- The application uses Next.js App Router (not Pages Router)

## Contributing

Follow the project's coding standards and conventions when contributing.
