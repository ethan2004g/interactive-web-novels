# Components Guide

This document provides an overview of all available components in the Interactive Web Novels platform.

---

## 📁 Component Structure

```
components/
├── layout/          # Layout components for page structure
├── common/          # Reusable common components
├── ui/              # UI primitives and building blocks
├── auth/            # Authentication-related components
├── books/           # Book-related components (future)
└── chapters/        # Chapter-related components (future)
```

---

## 🎨 Layout Components

### DashboardLayout
Container layout for dashboard pages with integrated sidebar navigation.

```tsx
import { DashboardLayout } from '@/components/layout';

<DashboardLayout>
  {/* Your dashboard content */}
</DashboardLayout>
```

**Features:**
- Integrated responsive sidebar
- Mobile menu toggle
- Optimal spacing and constraints

### MainLayout
General purpose layout for content pages.

```tsx
import { MainLayout } from '@/components/layout';

<MainLayout maxWidth="7xl">
  {/* Your content */}
</MainLayout>
```

**Props:**
- `maxWidth`: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '7xl' | 'full'
- `className`: Additional CSS classes

### Sidebar
Navigation sidebar for dashboard with role-based menu items.

```tsx
import { Sidebar } from '@/components/layout';

<Sidebar isOpen={true} onClose={() => {}} />
```

**Props:**
- `isOpen`: Boolean to control visibility (mobile)
- `onClose`: Callback when sidebar should close

**Features:**
- Role-based navigation items
- Active route highlighting
- User info display
- Mobile responsive

### Header
Main navigation header with authentication and mobile menu.

```tsx
import { Header } from '@/components/layout';

<Header />
```

**Features:**
- Sticky positioning
- Mobile hamburger menu
- User dropdown menu
- Auth-aware navigation

### Footer
Site footer with links and info.

```tsx
import { Footer } from '@/components/layout';

<Footer />
```

---

## 🔧 Common Components

### Button
Flexible button component with variants and loading states.

```tsx
import { Button } from '@/components/common';

<Button 
  variant="primary" 
  size="md" 
  isLoading={false}
  onClick={handleClick}
>
  Click Me
</Button>
```

**Props:**
- `variant`: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
- `size`: 'sm' | 'md' | 'lg'
- `isLoading`: Shows spinner when true
- Standard button HTML attributes

### LoadingSpinner
Animated loading spinner.

```tsx
import { LoadingSpinner } from '@/components/common';

<LoadingSpinner size="md" />
```

**Props:**
- `size`: 'sm' | 'md' | 'lg' | 'xl'
- `className`: Additional CSS classes

### LoadingScreen
Full-screen loading state with message.

```tsx
import { LoadingScreen } from '@/components/common';

<LoadingScreen message="Loading your content..." />
```

**Props:**
- `message`: Loading message to display

### ErrorBoundary
React error boundary for catching and displaying errors.

```tsx
import { ErrorBoundary } from '@/components/common';

<ErrorBoundary 
  fallback={<CustomErrorUI />}
  onError={(error, errorInfo) => console.error(error)}
>
  {children}
</ErrorBoundary>
```

**Props:**
- `fallback`: Custom error UI (optional)
- `onError`: Error callback (optional)

### SkeletonLoader
Loading placeholder with animation.

```tsx
import { SkeletonLoader, BookCardSkeleton } from '@/components/common';

<SkeletonLoader variant="text" />
<BookCardSkeleton />
```

**Variants:**
- `text`: Text line placeholder
- `card`: Card-shaped placeholder
- `avatar`: Circular avatar placeholder
- `rectangle`: Generic rectangle

**Pre-built Skeletons:**
- `BookCardSkeleton`: For book cards
- `ChapterListSkeleton`: For chapter lists

### EmptyState
Display when no content is available.

```tsx
import { EmptyState } from '@/components/common';

<EmptyState
  icon="📚"
  title="No books yet"
  description="Start by creating your first book"
  action={<Button>Create Book</Button>}
/>
```

**Props:**
- `icon`: ReactNode (emoji or icon component)
- `title`: String
- `description`: String (optional)
- `action`: ReactNode (optional)

---

## 🎯 UI Components

### Card
Container card with header, content, and footer sections.

```tsx
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui';

<Card>
  <CardHeader>
    <h2>Title</h2>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

**Components:**
- `Card`: Base card container
- `CardHeader`: Header with border
- `CardContent`: Main content area
- `CardFooter`: Footer with background

### Alert
Notification/status messages with variants.

```tsx
import { Alert } from '@/components/ui';

<Alert variant="info" title="Information">
  This is an informational message.
</Alert>
```

**Props:**
- `variant`: 'info' | 'success' | 'warning' | 'error'
- `title`: Alert title (optional)
- `children`: Alert content

---

## 🔐 Auth Components

### ProtectedRoute
Wrapper for routes that require authentication.

```tsx
import { ProtectedRoute } from '@/components/auth';

<ProtectedRoute>
  {/* Protected content */}
</ProtectedRoute>
```

### RoleGuard
Wrapper for routes that require specific roles.

```tsx
import { RoleGuard } from '@/components/auth';

<RoleGuard allowedRoles={['author', 'admin']}>
  {/* Role-protected content */}
</RoleGuard>
```

**Props:**
- `allowedRoles`: Array of allowed role strings

---

## 📱 Responsive Design

All components are built mobile-first with these breakpoints:

- **sm**: 640px
- **md**: 768px  
- **lg**: 1024px
- **xl**: 1280px
- **2xl**: 1536px

### Mobile Patterns

#### Sidebar Navigation
- Desktop: Always visible
- Mobile: Hidden, slides in with overlay

#### Header Menu
- Desktop: Horizontal navigation with dropdown
- Mobile: Hamburger menu with full-screen overlay

#### Layouts
- Use responsive grid classes: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Stack vertically on mobile, expand on larger screens

---

## 🎨 Design System

### Colors

**Primary (Blue):**
- 50: `bg-blue-50`
- 600: `bg-blue-600` (primary)
- 700: `bg-blue-700` (hover)

**Neutral (Gray):**
- 50: `bg-gray-50`
- 100: `bg-gray-100`
- 200: `bg-gray-200`
- 600: `text-gray-600`
- 900: `text-gray-900`

**Semantic:**
- Success: `green-*`
- Warning: `yellow-*`
- Error: `red-*`
- Info: `blue-*`

### Typography

- **Headings**: `font-bold`
  - H1: `text-3xl`
  - H2: `text-2xl`
  - H3: `text-xl`
  
- **Body**: `text-base`
- **Small**: `text-sm`
- **Tiny**: `text-xs`

### Spacing

- Padding: `p-4`, `p-6`, `p-8`
- Margin: `m-4`, `m-6`, `m-8`
- Gap: `gap-4`, `gap-6`, `gap-8`

### Shadows

- Card: `shadow-md`
- Hover: `shadow-lg`
- Small: `shadow-sm`

---

## 🔄 Common Patterns

### Loading States

```tsx
// Inline loading
{isLoading ? <LoadingSpinner /> : <Content />}

// Full screen loading
{isLoading ? <LoadingScreen message="Loading..." /> : <Content />}

// Button loading
<Button isLoading={isSubmitting}>Submit</Button>

// Skeleton placeholder
{isLoading ? <BookCardSkeleton /> : <BookCard />}
```

### Empty States

```tsx
{items.length === 0 ? (
  <EmptyState
    icon="📚"
    title="No items"
    description="Add your first item"
    action={<Button>Add Item</Button>}
  />
) : (
  <ItemList items={items} />
)}
```

### Error Handling

```tsx
// Component level
<ErrorBoundary>
  <Component />
</ErrorBoundary>

// Alert messages
{error && (
  <Alert variant="error" title="Error">
    {error.message}
  </Alert>
)}
```

### Layout Pattern

```tsx
// Dashboard pages
<ProtectedRoute>
  <DashboardLayout>
    <h1>Page Title</h1>
    {/* Content */}
  </DashboardLayout>
</ProtectedRoute>

// Content pages
<MainLayout maxWidth="2xl">
  <h1>Page Title</h1>
  {/* Content */}
</MainLayout>
```

---

## 📝 Best Practices

1. **Always use semantic HTML** - Use proper heading hierarchy, buttons for actions, links for navigation

2. **Maintain accessibility** - Include aria-labels, focus states, keyboard navigation

3. **Keep components small** - Single responsibility principle

4. **Use TypeScript** - Define proper prop types with interfaces

5. **Mobile-first** - Design for mobile, enhance for desktop

6. **Consistent spacing** - Use Tailwind's spacing scale

7. **Error boundaries** - Wrap major features in ErrorBoundary

8. **Loading states** - Always show loading UI for async operations

9. **Empty states** - Provide guidance when no content exists

10. **Reusability** - Extract common patterns into components

---

## 🚀 Creating New Components

### Component Template

```tsx
// components/common/NewComponent.tsx
import { ReactNode } from 'react';

interface NewComponentProps {
  children: ReactNode;
  variant?: 'default' | 'special';
  className?: string;
}

export function NewComponent({ 
  children, 
  variant = 'default',
  className = '' 
}: NewComponentProps) {
  return (
    <div className={`base-classes ${variant} ${className}`}>
      {children}
    </div>
  );
}
```

### Steps

1. Create component file in appropriate directory
2. Define TypeScript interface for props
3. Implement component with proper types
4. Add to `index.ts` export file
5. Document usage in this guide
6. Test responsive behavior
7. Check accessibility

---

**Last Updated:** January 7, 2026  
**Phase:** 2.3 Complete

