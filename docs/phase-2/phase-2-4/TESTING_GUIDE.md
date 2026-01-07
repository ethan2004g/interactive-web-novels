# Phase 2.4 Testing Guide

This guide will help you test all the features implemented in Phase 2.4.

---

## Prerequisites

1. **Backend Running:** Make sure the FastAPI backend is running
   ```bash
   cd backend
   # Activate venv
   python main.py
   ```

2. **Frontend Running:** Make sure the Next.js frontend is running
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Data:** Have at least:
   - 2-3 user accounts (reader and author roles)
   - 5+ books with different genres and statuses
   - Multiple chapters for at least 2 books
   - Some existing ratings and comments

---

## Test Scenarios

### 1. Home Page

**URL:** `http://localhost:3000/`

**Test:**
- [ ] Page loads without errors
- [ ] Featured books section appears (if books exist)
- [ ] Trending books section appears (if books exist)
- [ ] Book cards display correctly with images
- [ ] "View All" links work
- [ ] "Browse Books" button works
- [ ] Navigation works

**Expected:**
- Featured section shows highest-rated completed books
- Trending section shows most-viewed books
- All images load or show placeholder
- Stats (rating, views, likes) display correctly

---

### 2. Book Listing Page

**URL:** `http://localhost:3000/books`

#### 2.1 Basic Display
**Test:**
- [ ] Page loads with all books
- [ ] Books display in grid (1/2/3/4 columns based on screen size)
- [ ] Each book card shows all info (title, author, description, stats)
- [ ] Status badges show correct colors
- [ ] Results count displays

#### 2.2 Search
**Test:**
- [ ] Type book title in search box
- [ ] Click "Search"
- [ ] Results filter to matching books
- [ ] Try searching for author name
- [ ] Try searching for keywords in description

**Expected:**
- Search works for title, author, and description
- Results update after search
- Results count updates

#### 2.3 Filters
**Test Genre Filter:**
- [ ] Select a genre from dropdown
- [ ] Books filter to that genre
- [ ] Select "All Genres"
- [ ] All books show again

**Test Status Filter:**
- [ ] Select "Ongoing"
- [ ] Only ongoing books show
- [ ] Select "Completed"
- [ ] Only completed books show

**Test Sort:**
- [ ] Select "Most Popular" - books sorted by views
- [ ] Select "Highest Rated" - books sorted by rating
- [ ] Select "Title (A-Z)" - books alphabetically sorted

#### 2.4 Pagination
**Test (if you have 12+ books):**
- [ ] Page 1 shows first 12 books
- [ ] Click "Next"
- [ ] Page 2 shows next books
- [ ] Page numbers display correctly
- [ ] Click page number to jump
- [ ] "Previous" button works

#### 2.5 Combined Filters
**Test:**
- [ ] Apply search + genre filter
- [ ] Results show books matching both
- [ ] Add status filter
- [ ] Results update correctly
- [ ] Click "Clear all filters"
- [ ] All filters reset

---

### 3. Book Detail Page

**URL:** `http://localhost:3000/books/[book-id]`

**Navigate:** Click any book card from listing

#### 3.1 Information Display
**Test:**
- [ ] Cover image displays large
- [ ] Title and author name show
- [ ] Author name is clickable link
- [ ] Status badge shows correct status
- [ ] Genre badge displays (if book has genre)
- [ ] Full description displays
- [ ] Tags display (if book has tags)

#### 3.2 Statistics
**Test:**
- [ ] Average rating displays (0.0-5.0)
- [ ] Rating count shows
- [ ] View count shows
- [ ] Like count shows
- [ ] Chapter count shows correctly

#### 3.3 Bookmarks (Requires Login)
**Test as Guest:**
- [ ] Click bookmark button
- [ ] Redirects to login page

**Test as Logged-in User:**
- [ ] Click bookmark button (☆)
- [ ] Button changes to filled (★)
- [ ] Text changes to "Bookmarked"
- [ ] Click again to remove
- [ ] Button changes back to outline
- [ ] Go to dashboard → Bookmarks
- [ ] Bookmarked book appears in list

#### 3.4 Rating System (Requires Login)
**Test as Guest:**
- Rating section doesn't show

**Test as Logged-in User:**
- [ ] "Rate this book:" text shows
- [ ] 5 empty stars display
- [ ] Hover over stars - they fill on hover
- [ ] Click 4th star
- [ ] Rating saves
- [ ] Text changes to "Your Rating:"
- [ ] 4 stars remain filled
- [ ] Refresh page
- [ ] Your rating still shows
- [ ] Click different star to change rating

#### 3.5 Chapter List
**Test:**
- [ ] All published chapters display
- [ ] Chapter numbers show correctly
- [ ] Chapter titles display
- [ ] Word count shows for each chapter
- [ ] Interactive badge shows for interactive chapters
- [ ] Click a chapter - navigates to reading page

**Test Empty State:**
- [ ] If no chapters, shows "No chapters published yet"

#### 3.6 Start Reading
**Test:**
- [ ] Click "Start Reading" button
- [ ] Navigates to first chapter
- [ ] If no chapters, button is disabled

---

### 4. Chapter Reading Page

**URL:** `http://localhost:3000/books/[book-id]/chapters/[chapter-id]`

**Navigate:** Click "Start Reading" or click a chapter

#### 4.1 Chapter Display
**Test:**
- [ ] "Back to Book" link works
- [ ] Chapter number and title display
- [ ] Word count shows
- [ ] Interactive badge shows (if interactive)
- [ ] Chapter content renders properly
- [ ] Text is readable with good spacing

#### 4.2 Font Controls
**Test:**
- [ ] Click "A-" button
- [ ] Font size decreases
- [ ] Click "A+" button
- [ ] Font size increases
- [ ] Try clicking A- multiple times
- [ ] Font stops at minimum (12px)
- [ ] Try clicking A+ multiple times
- [ ] Font stops at maximum (24px)

#### 4.3 Chapter Navigation (Top Controls)
**Test on First Chapter:**
- [ ] "Previous" button is disabled
- [ ] "Next" button is enabled (if next chapter exists)
- [ ] Click "Next"
- [ ] Navigates to next chapter

**Test on Middle Chapter:**
- [ ] Both buttons are enabled
- [ ] "Previous" goes to previous chapter
- [ ] "Next" goes to next chapter

**Test on Last Chapter:**
- [ ] "Previous" button is enabled
- [ ] "Next" button is disabled

#### 4.4 Bottom Navigation
**Test:**
- [ ] Same as top navigation
- [ ] Shows chapter titles
- [ ] Works correctly

#### 4.5 Reading Progress (Requires Login)
**Test:**
- [ ] View a chapter
- [ ] Go to dashboard → Library
- [ ] Book shows in "Continue Reading" or progress list
- [ ] Progress is tracked

---

### 5. Comment Section

**Location:** Bottom of chapter reading page

#### 5.1 Display (As Guest)
**Test:**
- [ ] Comment count shows in header
- [ ] Existing comments display
- [ ] Username shows for each comment
- [ ] Timestamps display
- [ ] Comment content displays
- [ ] "You must be logged in" message shows
- [ ] "Log In" button displays

#### 5.2 Adding Comments (Requires Login)
**Test:**
- [ ] Log in as a user
- [ ] Comment form appears
- [ ] Type a comment
- [ ] Click "Post Comment"
- [ ] Comment appears in list
- [ ] Comment shows your username
- [ ] Comment count increases

**Test Empty Comment:**
- [ ] Try to post empty comment
- [ ] Button is disabled

#### 5.3 Replying to Comments
**Test:**
- [ ] Click "Reply" on a comment
- [ ] Form shows "Replying to comment..." indicator
- [ ] "Cancel" button appears
- [ ] Type a reply
- [ ] Click "Post Reply"
- [ ] Reply appears under original comment
- [ ] Reply is indented
- [ ] Click "Cancel"
- [ ] Reply indicator disappears

#### 5.4 Nested Replies
**Test:**
- [ ] Reply to a reply
- [ ] Second-level reply appears
- [ ] Indentation increases
- [ ] Try replying multiple levels deep
- [ ] All replies nest correctly

#### 5.5 Show/Hide Replies
**Test:**
- [ ] Comment with replies shows "Show X replies" button
- [ ] Click "Show X replies"
- [ ] Replies appear
- [ ] Button changes to "Hide X replies"
- [ ] Click again
- [ ] Replies hide

#### 5.6 Deleting Comments
**Test Own Comment:**
- [ ] Your comments show "Delete" button
- [ ] Click "Delete"
- [ ] Confirmation dialog appears
- [ ] Click "OK"
- [ ] Comment disappears
- [ ] Comment count decreases

**Test Others' Comments:**
- [ ] Other users' comments don't show "Delete" button
- [ ] Can't delete others' comments

---

### 6. Responsive Design

#### 6.1 Mobile (< 768px)
**Test:**
- [ ] Home page: Grid shows 1 column
- [ ] Book listing: Grid shows 1-2 columns
- [ ] Book detail: Cover and info stack vertically
- [ ] Chapter reading: Content is readable
- [ ] Comment section: Form is usable
- [ ] Navigation menu works (hamburger)
- [ ] All buttons are tap-friendly

#### 6.2 Tablet (768px - 1024px)
**Test:**
- [ ] Book grid shows 2 columns
- [ ] Book detail page looks good
- [ ] Chapter reading is comfortable
- [ ] All interactive elements work

#### 6.3 Desktop (> 1024px)
**Test:**
- [ ] Book grid shows 3-4 columns
- [ ] All spacing looks good
- [ ] Max-width containers work
- [ ] No horizontal scrolling

---

## Common Issues to Check

### Images
- [ ] Book covers load (or show placeholder)
- [ ] No broken image icons
- [ ] Images are responsive

### Authentication
- [ ] Login redirects work correctly
- [ ] Logged-in features show/hide properly
- [ ] Logout works everywhere

### Data Loading
- [ ] Loading spinners show during fetch
- [ ] Error messages show if fetch fails
- [ ] Empty states display when appropriate

### Navigation
- [ ] All links work
- [ ] Back button works
- [ ] Page transitions are smooth
- [ ] No console errors

---

## Browser Testing

Test in multiple browsers:
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari (if on Mac)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

---

## Performance

- [ ] Pages load in under 2 seconds
- [ ] Images lazy load
- [ ] No memory leaks (watch console)
- [ ] Pagination doesn't load all books at once
- [ ] Navigation is responsive

---

## Accessibility

- [ ] All buttons have hover states
- [ ] Form inputs have labels
- [ ] Error messages are visible
- [ ] Keyboard navigation works
- [ ] Tab order is logical
- [ ] Focus states are visible

---

## Final Checks

Before moving to Phase 2.5:
- [ ] All 8 Phase 2.4 features work
- [ ] No console errors on any page
- [ ] Mobile experience is good
- [ ] Authentication flows work
- [ ] Data persists after refresh
- [ ] Backend API calls succeed

---

## Bug Reporting

If you find issues:
1. Note the URL where issue occurs
2. Note what you were doing
3. Check browser console for errors
4. Note your user role (guest/reader/author)
5. Try to reproduce the issue
6. Document steps to reproduce

---

**Happy Testing!** 🧪

If all tests pass, Phase 2.4 is working correctly and you're ready for Phase 2.5!

