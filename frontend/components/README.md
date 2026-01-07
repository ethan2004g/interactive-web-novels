# Components Directory

This directory contains all React components organized by feature and purpose.

## Directory Structure

```
components/
├── layout/          # Layout components
│   └── (Header, Footer, Navbar, Sidebar, etc.)
├── ui/              # Reusable UI components
│   └── (Button, Input, Card, Modal, etc.)
├── books/           # Book-related components
│   └── (BookCard, BookList, BookForm, etc.)
├── chapters/        # Chapter-related components
│   └── (ChapterCard, ChapterEditor, ChapterReader, etc.)
├── auth/            # Authentication components
│   └── (LoginForm, RegisterForm, AuthGuard, etc.)
└── common/          # Common/shared components
    └── (Loading, ErrorBoundary, EmptyState, etc.)
```

## Component Guidelines

### File Naming
- Use PascalCase for component files: `BookCard.tsx`
- One component per file
- Index files for barrel exports when needed

### Component Structure

```typescript
'use client'; // Add if component uses client-side features

import { FC } from 'react';
import { cn } from '@/lib/utils';

interface ComponentProps {
  // Props definition
}

export const ComponentName: FC<ComponentProps> = ({ ...props }) => {
  // Component logic
  
  return (
    // JSX
  );
};
```

### Best Practices

1. **Use TypeScript** - Define proper types for all props
2. **Client/Server** - Mark client components with `'use client'`
3. **Reusability** - Keep components focused and reusable
4. **Styling** - Use Tailwind CSS with `cn()` utility
5. **Accessibility** - Follow WCAG guidelines
6. **Documentation** - Add JSDoc comments for complex components

## Component Categories

### Layout Components (`layout/`)
Components that define the structure of pages:
- Header with navigation
- Footer
- Sidebar for dashboards
- Page layouts

### UI Components (`ui/`)
Basic, reusable UI elements:
- Buttons
- Input fields
- Cards
- Modals/Dialogs
- Dropdowns
- Tooltips
- Loading spinners
- Alerts/Toasts

Consider using a UI library like:
- shadcn/ui
- Radix UI
- Headless UI

### Book Components (`books/`)
Components for book features:
- BookCard - Display book preview
- BookList - List of books with pagination
- BookForm - Create/edit book form
- BookDetail - Full book details
- BookStats - Display book statistics
- BookFilters - Filter books by genre, status, etc.

### Chapter Components (`chapters/`)
Components for chapter features:
- ChapterCard - Chapter preview
- ChapterList - List chapters in a book
- ChapterReader - Read chapter content
- ChapterEditor - Write/edit chapters
- ChapterNav - Navigate between chapters

### Auth Components (`auth/`)
Components for authentication:
- LoginForm - User login form
- RegisterForm - User registration form
- AuthGuard - Protect routes (HOC or wrapper)
- ProfileForm - Edit user profile
- PasswordReset - Reset password form

### Common Components (`common/`)
Shared utility components:
- Loading - Loading indicators
- ErrorBoundary - Error handling
- EmptyState - Empty state placeholders
- Pagination - Page navigation
- SearchBar - Search input
- NotFound - 404 page content

## Example Component

```typescript
'use client';

import { FC } from 'react';
import { Book } from '@/types';
import { cn, formatDate } from '@/lib/utils';

interface BookCardProps {
  book: Book;
  onClick?: () => void;
  className?: string;
}

/**
 * BookCard component displays a book preview card
 */
export const BookCard: FC<BookCardProps> = ({ 
  book, 
  onClick, 
  className 
}) => {
  return (
    <div
      onClick={onClick}
      className={cn(
        'rounded-lg border bg-card p-4 shadow-sm transition-shadow hover:shadow-md cursor-pointer',
        className
      )}
    >
      {book.cover_image_url && (
        <img
          src={book.cover_image_url}
          alt={book.title}
          className="w-full h-48 object-cover rounded-md mb-4"
        />
      )}
      
      <h3 className="text-lg font-semibold mb-2">{book.title}</h3>
      
      <p className="text-sm text-muted-foreground mb-2 line-clamp-2">
        {book.description}
      </p>
      
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <span>{book.genre}</span>
        <span>{formatDate(book.created_at)}</span>
      </div>
      
      <div className="flex items-center gap-4 mt-2 text-xs">
        <span>👁️ {book.total_views}</span>
        <span>❤️ {book.total_likes}</span>
        <span className="capitalize">{book.status}</span>
      </div>
    </div>
  );
};
```

## Usage Example

```typescript
import { BookCard } from '@/components/books/BookCard';

function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {books.map((book) => (
        <BookCard
          key={book.id}
          book={book}
          onClick={() => router.push(`/books/${book.id}`)}
        />
      ))}
    </div>
  );
}
```

## Next Steps (Phase 2.2+)

Components to be created:
- [ ] Layout: Header, Footer, Sidebar
- [ ] Auth: LoginForm, RegisterForm
- [ ] UI: Button, Input, Card, Modal
- [ ] Common: Loading, ErrorBoundary, EmptyState
- [ ] Books: BookCard, BookList, BookForm
- [ ] Chapters: ChapterReader

## Resources

- [Next.js Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/) - Recommended UI component library

