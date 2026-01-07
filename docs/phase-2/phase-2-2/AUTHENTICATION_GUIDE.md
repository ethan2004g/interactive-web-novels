# Authentication System Guide

**Last Updated:** January 6, 2026  
**Phase:** 2.2 - Authentication UI

---

## 🚀 Quick Start

### Prerequisites
1. Backend server running on `http://localhost:8000`
2. Frontend server running on `http://localhost:3000`

### Starting the Servers

#### Backend (Terminal 1)
```bash
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
python main.py
```

#### Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

---

## 📱 User Flows

### 1. Registration Flow

**Steps:**
1. Navigate to `http://localhost:3000`
2. Click "Sign up" button in header or hero section
3. Fill out the registration form:
   - **Username:** 3+ characters, unique
   - **Email:** Valid email format, unique
   - **Password:** 6+ characters
   - **Confirm Password:** Must match password
   - **Role:** Choose "Reader" or "Author"
4. Click "Create account"
5. On success, you'll be automatically logged in and redirected to home

**Example Credentials:**
```
Username: johndoe
Email: john@example.com
Password: password123
Role: Author
```

### 2. Login Flow

**Steps:**
1. Navigate to `http://localhost:3000`
2. Click "Sign in" button in header
3. Enter your credentials:
   - **Username:** Your registered username
   - **Password:** Your password
4. Click "Sign in"
5. On success, redirected to home page

**Test Credentials:**
If you created a user during backend testing:
```
Username: testauthor
Password: testpass123
```

### 3. Profile Management

**Steps:**
1. Log in to your account
2. Click on your avatar/username in the header
3. Select "Profile" from dropdown
4. View your profile information
5. Click "Edit Profile" to modify:
   - Email address
   - Bio
6. Click "Save Changes" or "Cancel"

### 4. Logout Flow

**Steps:**
1. Click on your avatar/username in header
2. Select "Sign out" from dropdown
3. You'll be redirected to login page
4. Session cleared

---

## 🔐 Authentication Features

### Public Pages (No Login Required)
- `/` - Home page
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/books` - Browse books (placeholder)

### Protected Pages (Login Required)
- `/profile` - User profile page
- `/dashboard` - Author dashboard (authors only)

### Role-Based Access
- **Reader:** Can read books, comment, bookmark, rate
- **Author:** Can do everything readers can + create/edit books
- **Admin:** Full access (for future implementation)

---

## 🎨 UI Components

### Header Navigation
- **Not Logged In:**
  - Logo (links to home)
  - "Browse Books" link
  - "Sign in" button
  - "Sign up" button

- **Logged In:**
  - Logo (links to home)
  - "Browse Books" link
  - "My Dashboard" link (authors only)
  - User avatar with dropdown:
    - Profile
    - Dashboard (authors only)
    - Sign out

### Authentication Context
Available throughout the app via `useAuthContext()`:
```tsx
const {
  user,           // Current user object or null
  loading,        // Loading state
  error,          // Error message
  login,          // Login function
  register,       // Register function
  logout,         // Logout function
  updateUser,     // Update user state
  isAuthenticated, // Boolean
  isAuthor,       // Boolean
  isReader,       // Boolean
  isAdmin,        // Boolean
} = useAuthContext();
```

---

## 🧪 Testing Scenarios

### Test Case 1: New User Registration
1. ✅ Register with valid credentials
2. ✅ Verify automatic login after registration
3. ✅ Check user appears in header
4. ✅ Verify role-specific features (dashboard for authors)

### Test Case 2: Login/Logout
1. ✅ Login with valid credentials
2. ✅ Verify redirect to home
3. ✅ Refresh page - should stay logged in
4. ✅ Logout - should redirect to login page
5. ✅ Try accessing protected page - should redirect to login

### Test Case 3: Form Validation
1. ✅ Try registering with short username (< 3 chars)
2. ✅ Try registering with invalid email
3. ✅ Try registering with short password (< 6 chars)
4. ✅ Try registering with non-matching passwords
5. ✅ Verify error messages display correctly

### Test Case 4: Protected Routes
1. ✅ Try accessing `/profile` without login
2. ✅ Try accessing `/dashboard` as a reader
3. ✅ Verify redirects work correctly
4. ✅ Login and access should work

### Test Case 5: Profile Management
1. ✅ View profile information
2. ✅ Edit email and bio
3. ✅ Save changes
4. ✅ Verify changes persist after page refresh
5. ✅ Try editing with invalid email

---

## 🐛 Common Issues & Solutions

### Issue: "Network Error" on login/register
**Solution:** Ensure backend server is running on `http://localhost:8000`

### Issue: "CORS Error"
**Solution:** Backend should have CORS configured for `http://localhost:3000`

### Issue: User not staying logged in after refresh
**Solution:** Check browser localStorage for `access_token` and `refresh_token`

### Issue: Protected routes not redirecting
**Solution:** Clear localStorage and try logging in again

### Issue: "Token expired" error
**Solution:** Logout and login again (token refresh will be enhanced in future)

---

## 🔧 Configuration

### Environment Variables
Create `.env.local` in frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### API Endpoints Used
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update user profile

---

## 📊 User Roles Explained

### Reader Role
- **Purpose:** For users who want to read stories
- **Access:**
  - Browse and read books
  - Track reading progress
  - Bookmark favorite books
  - Rate and comment on books
  - Manage profile

### Author Role
- **Purpose:** For users who want to write stories
- **Access:**
  - Everything readers can do
  - Create and publish books
  - Write chapters (simple and interactive)
  - View book statistics
  - Manage their books
  - Access author dashboard

### Admin Role (Future)
- **Purpose:** Platform administration
- **Access:**
  - Everything authors can do
  - Moderate content
  - Manage users
  - View platform analytics

---

## 💡 Developer Notes

### Adding New Protected Routes
```tsx
import { ProtectedRoute } from '@/components/auth';

export default function MyProtectedPage() {
  return (
    <ProtectedRoute>
      <div>Protected content</div>
    </ProtectedRoute>
  );
}
```

### Adding Role-Based Routes
```tsx
import { ProtectedRoute, RoleGuard } from '@/components/auth';

export default function AuthorOnlyPage() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author', 'admin']}>
        <div>Author-only content</div>
      </RoleGuard>
    </ProtectedRoute>
  );
}
```

### Using Auth Context in Components
```tsx
'use client';

import { useAuthContext } from '@/contexts';

export function MyComponent() {
  const { user, isAuthor } = useAuthContext();
  
  return (
    <div>
      <p>Welcome, {user?.username}!</p>
      {isAuthor && <button>Create Book</button>}
    </div>
  );
}
```

---

## 🎯 Next Steps

After Phase 2.2, the following features will be added:

### Phase 2.3: Core Layout & Navigation
- Enhanced layout components
- Sidebar for dashboards
- Breadcrumbs
- Error boundaries

### Phase 2.4: Book Discovery & Reading
- Book listing with filters
- Book detail pages
- Chapter reading interface
- Reading progress tracking

### Phase 2.5: Author Dashboard
- Book management interface
- Statistics and analytics
- Chapter creation/editing

---

## 📚 Related Documentation

- [Phase 2.2 Complete](./PHASE_2_2_COMPLETE.md) - Full phase documentation
- [Frontend README](./frontend/README.md) - Frontend setup guide
- [Project Scope](./PROJECT_SCOPE.md) - Overall project plan
- [Backend README](./backend/README.md) - Backend API documentation

---

**Happy Testing! 🎉**

If you encounter any issues, please check the common issues section or refer to the phase documentation.

