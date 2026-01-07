# Author Dashboard - Quick Start Guide

**Phase 2.5 Feature Guide**  
**Last Updated:** January 7, 2026

---

## 🎯 Overview

The Author Dashboard is a comprehensive content management system for authors to create, edit, and manage their books and chapters. This guide walks you through all the features.

---

## 🚀 Getting Started

### Prerequisites

1. **Backend server running:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **Frontend server running:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Registered author account:**
   - Go to `/auth/register`
   - Select "Author" role during registration

---

## 📚 Feature Walkthrough

### 1. Dashboard Home (`/dashboard`)

**What you'll see:**
- Welcome message with your username
- Four statistics cards showing:
  - Total Books
  - Total Views
  - Total Chapters
  - Average Rating
- Recent Books section with up to 4 books

**Try this:**
1. Log in as an author
2. Notice the stats update based on your books
3. Click on a book card to view it
4. Click "View All" to see all your books

---

### 2. My Books Page (`/dashboard/books`)

**What you'll see:**
- Filter tabs: All, Drafts, Ongoing, Completed
- List of your books with:
  - Cover image (or gradient fallback)
  - Title and status badge
  - Genre and description
  - Chapter count, views, and rating
  - Action buttons

**Try this:**
1. Navigate to "My Books" from sidebar
2. Try filtering by status (Drafts, Ongoing, Completed)
3. Click "View" to see public view of a book
4. Click "Edit" to modify book details
5. Click "Chapters" to manage chapters
6. Click "Delete" to remove a book (confirms first)

---

### 3. Create New Book (`/dashboard/books/new`)

**What you'll see:**
- Form with fields for:
  - Title (required)
  - Description (required)
  - Genre (dropdown)
  - Tags (add/remove)
  - Status (draft/ongoing/completed)
  - Cover Image URL

**Try this:**
1. Click "Create New Book" button
2. Enter a title: "My First Novel"
3. Write a description
4. Select a genre from dropdown
5. Add tags by typing and pressing Enter or clicking "Add"
6. Remove tags by clicking the × button
7. Optionally add a cover image URL
8. Click "Create Book"
9. You'll be redirected to the edit page

**Sample Data:**
```
Title: The Dragon's Journey
Description: An epic fantasy about a young dragon discovering their destiny in a world of magic and adventure.
Genre: Fantasy
Tags: dragon, magic, adventure, coming-of-age
Status: Ongoing
```

---

### 4. Edit Book (`/dashboard/books/[id]/edit`)

**What you'll see:**
- Pre-filled form with current book data
- All editable fields from creation
- Live cover image preview
- Statistics panel at bottom showing:
  - Total Views
  - Total Likes
  - Average Rating
  - Total Ratings

**Try this:**
1. Click "Edit" on any book
2. Modify the title or description
3. Add or remove tags
4. Change the status
5. Update cover image URL and see preview
6. Click "Save Changes"
7. Or click "Cancel" to discard changes

---

### 5. Manage Chapters (`/dashboard/books/[id]/chapters`)

**What you'll see:**
- List of all chapters with:
  - Chapter number and title
  - Published/Draft badge
  - Simple/Interactive badge
  - Word count
  - Publication date
  - Action buttons
- Quick Stats panel showing:
  - Total Chapters
  - Published count
  - Total words
  - Interactive count

**Try this:**
1. Click "Chapters" on any book
2. Click "Add Chapter" to create new
3. Click "View" on published chapter to see reader view
4. Click "Edit" to modify chapter
5. Click "Publish" to make draft visible
6. Click "Unpublish" to revert to draft
7. Click "Delete" to remove chapter (confirms first)

---

### 6. Create Chapter (`/dashboard/books/[id]/chapters/new`)

**What you'll see:**
- Breadcrumb navigation
- Form with:
  - Chapter title
  - Content type selector
  - Large text area for content
  - Real-time word count
  - Publish checkbox

**Try this:**
1. Click "Add Chapter" from chapter management
2. Enter chapter title: "Chapter 1: The Beginning"
3. Keep content type as "Simple Text"
4. Write your chapter content in the text area
5. Watch the word count update as you type
6. Check "Publish chapter immediately" if ready
7. Click "Create Chapter"
8. You'll return to chapter list

**Sample Content:**
```
Title: Chapter 1: The Beginning

Content:
The morning sun cast long shadows across the ancient forest as Aria stepped through the massive oak trees. She had been walking for hours, following the mysterious map her grandmother had left her.

"This can't be right," she muttered, studying the worn parchment. According to the map, the ruins should be right here, but all she could see were trees.

Then she noticed it—a faint shimmer in the air, like heat waves rising from summer pavement. She reached out cautiously...
```

---

### 7. Edit Chapter (`/dashboard/books/[id]/chapters/[chapterId]/edit`)

**What you'll see:**
- Pre-filled form with chapter data
- Content type (read-only)
- Large text area with current content
- Real-time word count
- Publish checkbox
- Preview button (if published)
- Chapter Information panel showing:
  - Chapter number
  - Word count
  - Created date
  - Last updated
  - Published date

**Try this:**
1. Click "Edit" on any chapter
2. Modify the title or content
3. Watch word count update
4. Toggle published status
5. Click "Preview" to see reader view (new tab)
6. Click "Save Changes" to update
7. View updated info in information panel

---

## 🎨 UI Features

### Status Badges

- **Draft** (Gray): Book/chapter not visible to readers
- **Ongoing** (Blue): Book actively being written
- **Completed** (Green): Book finished
- **Published** (Green): Chapter visible to readers
- **Simple** (Blue): Simple text chapter
- **Interactive** (Purple): Interactive chapter (Phase 3)

### Empty States

When you have no content, you'll see friendly messages with:
- Emoji icon
- Helpful title
- Descriptive text
- Action button to create content

### Loading States

While data loads, you'll see:
- Spinners on buttons during saves
- Full-page spinner for initial loads
- "Loading..." text on buttons

### Error Handling

If something goes wrong:
- Red alert boxes appear with error message
- Form validation messages show inline
- Delete actions require confirmation

---

## 🔐 Access Control

All author features are protected:
- Must be logged in
- Must have "author" or "admin" role
- Readers cannot access these pages
- Authors can only edit their own books

**Role-based redirects:**
- Readers trying to access author pages → redirected
- Non-authors trying to create books → blocked
- Authors can view but not edit others' books

---

## 📱 Responsive Design

All pages work on:
- Desktop (optimal experience)
- Tablet (adjusted layouts)
- Mobile (single column, touch-friendly)

**Mobile tips:**
- Swipe to see all stats cards
- Filter tabs scroll horizontally
- Forms stack vertically
- Action buttons wrap to new lines

---

## ⚡ Quick Tips

### Creating Books
1. Start with "Draft" status while writing
2. Add a cover image URL for better visibility
3. Use tags to help readers find your book
4. Keep descriptions concise but engaging

### Managing Chapters
1. Write chapters in order for best reader experience
2. Use "Draft" to hide work-in-progress chapters
3. Publish when ready—you can unpublish anytime
4. Check word count to maintain consistent chapter lengths

### Performance
1. Dashboard loads all your books at once
2. Stats are calculated in real-time
3. Large chapter lists may take a moment to load
4. Use filters to find books quickly

### Best Practices
1. Save work frequently (no auto-save yet)
2. Use descriptive chapter titles
3. Preview chapters before publishing
4. Check statistics to see reader engagement

---

## 🐛 Troubleshooting

### "Failed to load books"
- Check backend server is running
- Verify you're logged in
- Check browser console for errors

### "Failed to create book"
- Ensure title and description are filled
- Check all required fields have values
- Verify backend connection

### Stats showing 0
- Stats update when books are created
- Views/ratings from readers take time
- New accounts start with empty stats

### Can't see published chapter
- Verify chapter is marked as published
- Check book status is not "Draft"
- Try refreshing the page

### Cover image not showing
- Verify URL is correct and accessible
- Check image format (jpg, png, webp)
- Try a different image URL

---

## 🎯 Next Steps

After familiarizing yourself with the dashboard:

1. **Create your first book** with all details
2. **Add several chapters** to build your story
3. **Publish chapters** when ready for readers
4. **Check statistics** to see engagement
5. **Edit and refine** based on feedback

**Coming in Phase 3:**
- Rich text editor with formatting
- Code editor for interactive chapters
- Auto-save functionality
- Template system
- Advanced preview modes

---

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Review error messages carefully
3. Check browser console (F12)
4. Verify backend logs
5. Review Phase 2.5 completion document

---

**Happy Writing! 📖✨**

