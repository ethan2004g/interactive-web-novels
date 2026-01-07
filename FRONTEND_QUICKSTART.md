# Frontend Quick Start Guide

This guide will help you get the frontend running quickly.

## Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

## Quick Setup

### 1. Navigate to Frontend Directory

```bash
cd "C:\Users\ethan\Cursor Projects\interactive-web-novels\frontend"
```

### 2. Install Dependencies (if not already done)

```bash
npm install
```

### 3. Environment Variables

The `.env.local` file should already be configured with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Interactive Web Novels
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

If you need to change the backend URL, edit `.env.local`.

### 4. Start Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure Overview

```
frontend/
├── app/                    # Next.js pages (App Router)
├── components/             # React components
├── contexts/              # React contexts
├── hooks/                 # Custom hooks (useAuth, etc.)
├── lib/                   # Utilities (API client, utils)
├── services/              # API services (auth, books, etc.)
├── types/                 # TypeScript types
└── public/                # Static assets
```

## API Services Available

All services are located in `services/` directory:

- **authService** - Login, register, logout, token refresh
- **userService** - User profile management
- **bookService** - Book CRUD operations
- **chapterService** - Chapter CRUD operations
- **readerService** - Bookmarks, ratings, comments, reading progress

## Using API Services

Example usage:

```typescript
import { authService, bookService } from '@/services';

// Login
const tokens = await authService.login({ username, password });

// Get books
const books = await bookService.getBooks({ page: 1, size: 10 });

// Create book (requires authentication)
const newBook = await bookService.createBook({
  title: 'My Novel',
  description: 'A great story',
  status: 'draft'
});
```

## Using Custom Hooks

### useAuth Hook

```typescript
import { useAuth } from '@/hooks';

function MyComponent() {
  const { user, login, logout, isAuthenticated, isAuthor } = useAuth();

  // Check if user is authenticated
  if (!isAuthenticated) {
    return <div>Please login</div>;
  }

  // Check if user is an author
  if (isAuthor) {
    return <div>Author Dashboard</div>;
  }

  return <div>Welcome, {user?.username}!</div>;
}
```

## Connecting to Backend

Make sure the backend is running before starting the frontend:

1. Navigate to backend directory:
   ```bash
   cd "C:\Users\ethan\Cursor Projects\interactive-web-novels\backend"
   ```

2. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Start backend server:
   ```bash
   uvicorn main:app --reload
   ```

4. Backend should be running at: **http://localhost:8000**

5. API documentation available at: **http://localhost:8000/docs**

## Next Steps

Phase 2.1 (Project Setup) is complete! Next tasks in Phase 2.2:

- [ ] Create login page UI
- [ ] Create registration page UI
- [ ] Implement authentication context
- [ ] Create protected route wrapper
- [ ] Build user profile page

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, you can use a different port:

```bash
npm run dev -- -p 3001
```

### API Connection Issues

- Verify backend is running on port 8000
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Check browser console for CORS errors

### Module Not Found Errors

Run:

```bash
npm install
```

## Documentation

- Frontend README: `frontend/README.md`
- Phase 2.1 Completion: `PHASE_2_1_COMPLETE.md`
- Project Scope: `PROJECT_SCOPE.md`

## Support

For issues or questions, refer to the comprehensive documentation in the project files.

