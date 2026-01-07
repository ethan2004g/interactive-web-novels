# Authentication Quick Reference Card

**Phase 2.2 - Interactive Web Novels**

---

## 🚀 Quick Start

### Start Both Servers
```bash
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Access the App
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🔑 Test Credentials

### Create New User
1. Go to http://localhost:3000/auth/register
2. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
   - Role: Choose Reader or Author

### Or Use Existing (if created during backend testing)
- Username: `testauthor`
- Password: `testpass123`

---

## 📍 Available Routes

### Public (No Login Required)
| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/auth/login` | Login page |
| `/auth/register` | Registration page |
| `/books` | Browse books (placeholder) |

### Protected (Login Required)
| Route | Description | Access |
|-------|-------------|--------|
| `/profile` | User profile | All users |
| `/dashboard` | Author dashboard | Authors only |

---

## 💻 Code Snippets

### Use Authentication in Component
```tsx
'use client';
import { useAuthContext } from '@/contexts';

export function MyComponent() {
  const { 
    user,           // Current user or null
    isAuthenticated, // Boolean
    isAuthor,       // Boolean
    isReader,       // Boolean
    login,          // Function
    logout          // Function
  } = useAuthContext();

  if (!isAuthenticated) {
    return <div>Please login</div>;
  }

  return <div>Welcome, {user.username}!</div>;
}
```

### Protect a Route
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

### Restrict by Role
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

### Combine Both
```tsx
import { ProtectedRoute, RoleGuard } from '@/components/auth';

export default function AuthorDashboard() {
  return (
    <ProtectedRoute>
      <RoleGuard allowedRoles={['author']}>
        <div>Author dashboard</div>
      </RoleGuard>
    </ProtectedRoute>
  );
}
```

---

## 🎨 Component Imports

### Authentication
```tsx
import { useAuthContext } from '@/contexts';
import { ProtectedRoute, RoleGuard } from '@/components/auth';
```

### Layout
```tsx
import { Header, Footer } from '@/components/layout';
```

### Services
```tsx
import { authService, userService, bookService } from '@/services';
```

### Types
```tsx
import { User, LoginRequest, RegisterRequest } from '@/types';
```

---

## 🔧 Common Tasks

### Check if User is Logged In
```tsx
const { isAuthenticated } = useAuthContext();
if (isAuthenticated) {
  // User is logged in
}
```

### Get Current User Info
```tsx
const { user } = useAuthContext();
console.log(user?.username);
console.log(user?.email);
console.log(user?.role);
```

### Check User Role
```tsx
const { isAuthor, isReader, isAdmin } = useAuthContext();

if (isAuthor) {
  // Show author features
}
```

### Logout User
```tsx
const { logout } = useAuthContext();

<button onClick={logout}>Logout</button>
```

### Conditional Rendering
```tsx
const { isAuthenticated, isAuthor } = useAuthContext();

return (
  <div>
    {isAuthenticated ? (
      <p>Logged in</p>
    ) : (
      <Link href="/auth/login">Login</Link>
    )}
    
    {isAuthor && <button>Create Book</button>}
  </div>
);
```

---

## 🐛 Troubleshooting

### Issue: Can't login
**Check:**
- Backend is running on port 8000
- Database is set up
- User exists in database
- Credentials are correct

### Issue: Token expired
**Solution:**
```tsx
const { logout } = useAuthContext();
logout(); // Clear tokens and login again
```

### Issue: Protected route not working
**Check:**
- Page is wrapped in `<ProtectedRoute>`
- AuthProvider is in root layout
- Token exists in localStorage

### Issue: CORS error
**Solution:**
- Backend CORS should allow `http://localhost:3000`
- Check backend `main.py` CORS configuration

---

## 📦 Project Structure

```
frontend/
├── app/
│   ├── auth/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── profile/page.tsx
│   ├── dashboard/page.tsx
│   ├── books/page.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── auth/
│   │   ├── ProtectedRoute.tsx
│   │   └── RoleGuard.tsx
│   └── layout/
│       ├── Header.tsx
│       └── Footer.tsx
├── contexts/
│   └── AuthContext.tsx
├── services/
│   ├── auth.service.ts
│   └── user.service.ts
└── types/
    ├── auth.ts
    └── user.ts
```

---

## 🎯 Validation Rules

### Registration
- Username: 3+ chars, unique
- Email: Valid format, unique
- Password: 6+ chars
- Confirm Password: Must match

### Login
- Username: Required
- Password: Required

### Profile Update
- Email: Valid format
- Bio: Optional

---

## 🔐 Security Notes

1. **Tokens stored in localStorage**
   - Access token
   - Refresh token

2. **Automatic token refresh**
   - Handled by API client

3. **Protected routes**
   - Redirect to `/auth/login` if not authenticated

4. **Role-based access**
   - Redirect to `/` if insufficient permissions

---

## 📚 Full Documentation

- [Phase 2.2 Complete](./PHASE_2_2_COMPLETE.md) - Full documentation
- [Authentication Guide](./AUTHENTICATION_GUIDE.md) - Detailed guide
- [Project Scope](./PROJECT_SCOPE.md) - Overall project
- [Frontend README](./frontend/README.md) - Frontend docs

---

## 🎉 Quick Test Checklist

- [ ] Register new user
- [ ] Login with credentials
- [ ] View profile
- [ ] Edit profile
- [ ] Logout
- [ ] Try accessing `/profile` without login (should redirect)
- [ ] Try accessing `/dashboard` as reader (should redirect)

---

**Need Help?** Check the full documentation files listed above!

