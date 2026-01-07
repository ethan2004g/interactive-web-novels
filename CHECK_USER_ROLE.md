# Quick Fix: Check User Role & Restart Frontend

## Issue
- Can't see "Create New Book" button
- Getting 404 errors on chapter management pages

## Solutions

### 1. Restart Next.js Dev Server (IMPORTANT!)

**The dynamic routes we created in Phase 2.5 need the dev server to restart to be recognized.**

**Steps:**
1. Find your terminal running `npm run dev` (Terminal 10 in your case)
2. Press `Ctrl + C` to stop the server
3. Run: `npm run dev` again
4. Wait for "Ready in..." message

**After restart, these routes will work:**
- ✅ `/dashboard/books` - My Books page with "Create New Book" button
- ✅ `/dashboard/books/new` - Create new book form
- ✅ `/dashboard/books/[id]/edit` - Edit book details
- ✅ `/dashboard/books/[id]/chapters` - Manage chapters
- ✅ `/dashboard/books/[id]/chapters/new` - Create new chapter
- ✅ `/dashboard/books/[id]/chapters/[chapterId]/edit` - Edit chapter

### 2. Verify Your User Role

**Check in browser console (F12):**

```javascript
// Check your role
fetch('http://localhost:8000/api/v1/auth/me', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
.then(r => r.json())
.then(user => {
  console.log('Your role:', user.role);
  console.log('User info:', user);
  if (user.role === 'author') {
    console.log('✅ You ARE an author - can create books');
  } else {
    console.log('❌ You are a ' + user.role + ' - cannot create books');
  }
})
.catch(e => console.error('Error:', e));
```

### 3. What You Should See After Restart

**On `/dashboard/books` page:**

At the top right, you should see:
```
[Create New Book]  <-- This button should be visible
```

**For each book, you should see buttons:**
- [View] - See public book page
- [Edit] - Edit book details
- [Chapters] - Manage chapters (ADD CHAPTERS HERE!)
- [Delete] - Remove book

### 4. Test Navigation

After restarting, test this flow:

1. Go to `/dashboard/books`
2. Click "Create New Book" → Should load form
3. Fill in details, click "Create Book" → Should save and redirect
4. Go back to `/dashboard/books`
5. Find your book, click "Chapters" → Should show chapter management
6. Click "Add Chapter" → Should load chapter form
7. Fill in chapter content, click "Create Chapter" → Should save

### 5. Common Issues

**Still getting 404 after restart?**
- Hard refresh the page: `Ctrl + Shift + R`
- Clear browser cache
- Check browser console for errors

**"Create New Book" button still not visible?**
- Verify you're on `/dashboard/books` (not `/books`)
- Check if you're logged in (token should exist)
- Check your user role (should be "author")

**Chapters button not working?**
- Make sure you clicked "Chapters" not "View"
- URL should be `/dashboard/books/[number]/chapters`
- Check if the book ID is valid

## Quick Diagnostic

Run this in your browser console to test all routes:

```javascript
// Test if routes are accessible
const bookId = 1; // Replace with your book ID
const chapterId = 1; // Replace with your chapter ID

const routes = [
  '/dashboard/books',
  '/dashboard/books/new',
  `/dashboard/books/${bookId}/edit`,
  `/dashboard/books/${bookId}/chapters`,
  `/dashboard/books/${bookId}/chapters/new`,
  `/dashboard/books/${bookId}/chapters/${chapterId}/edit`
];

routes.forEach(route => {
  fetch(`http://localhost:3000${route}`)
    .then(r => console.log(`${route}: ${r.status === 200 ? '✅ OK' : '❌ ' + r.status}`))
    .catch(e => console.log(`${route}: ❌ Error`));
});
```

## Expected Result

After restarting and verifying:
- ✅ "Create New Book" button visible
- ✅ Can create books
- ✅ Can edit books
- ✅ Can manage chapters
- ✅ Can create/edit chapters
- ✅ No 404 errors

---

**TL;DR:** 
1. Restart Next.js dev server (Ctrl+C, then `npm run dev`)
2. Hard refresh browser (Ctrl+Shift+R)
3. Navigate to `/dashboard/books`
4. Everything should work!

