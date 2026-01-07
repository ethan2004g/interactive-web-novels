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

## Features Implemented (Phase 2.1)

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

## Next Steps (Phase 2.2)

- [ ] Create authentication UI (login/register pages)
- [ ] Implement authentication context
- [ ] Create protected route wrapper
- [ ] Add user profile page
- [ ] Implement logout functionality

## Notes

- The API client automatically handles JWT token storage and refresh
- All services use TypeScript for type safety
- Error handling is built into the API client
- The application uses Next.js App Router (not Pages Router)

## Contributing

Follow the project's coding standards and conventions when contributing.
