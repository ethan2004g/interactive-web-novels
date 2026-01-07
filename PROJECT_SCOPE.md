# Interactive Web Novels Platform - Project Scope

**Project Start Date:** January 6, 2026  
**Last Updated:** January 6, 2026

---

## 📋 Project Overview

An interactive web novel platform where authors can write and publish books with both traditional text and coded interactive elements. Readers can enjoy stories with branching storylines, animations, custom styling, and visual novel-style features.

### Key Differentiator
Authors can not only write chapters but also **code** them with:
- Branching storylines with reader choices
- Animations and visual effects
- Custom styling and templates
- Embedded images and code snippets
- Visual novel elements (dialogue boxes, character sprites, backgrounds)

### Reader Experience
- Toggle visual effects on/off (preserving story-critical elements)
- Render chapters like normal webpages
- Track reading progress, bookmark, comment, and rate

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python) - Fast, modern, async API
- **Database:** PostgreSQL - Relational database
- **ORM:** SQLAlchemy - Database management
- **Authentication:** JWT tokens
- **File Storage:** Local storage initially (cloud storage for production)
- **API Documentation:** Automatic with FastAPI (Swagger/OpenAPI)

### Frontend (Web)
- **Framework:** Next.js 14+ (React, App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** React Context + Zustand
- **Code Editor:** Monaco Editor (VS Code editor for authors)
- **Rich Text Editor:** Tiptap or Lexical
- **HTTP Client:** Axios or Fetch API
- **Form Handling:** React Hook Form

### Chapter Rendering Engine
- **Format:** Custom JSON-based structure
- **Execution:** Sandboxed JavaScript execution (iframe or VM)
- **Templates:** Pre-built chapter templates
- **Animations:** Framer Motion or CSS animations

### Development Tools
- **Package Manager:** npm or pnpm
- **Version Control:** Git
- **Code Quality:** ESLint, Prettier
- **Testing:** Jest, React Testing Library, Pytest

---

## 📊 Database Schema (Planned)

### Tables

#### users
- id (PK)
- username (unique)
- email (unique)
- password_hash
- role (author/reader/admin)
- profile_picture_url
- bio
- created_at
- updated_at

#### books
- id (PK)
- author_id (FK -> users.id)
- title
- description
- cover_image_url
- genre
- tags (array)
- status (draft/ongoing/completed)
- total_views
- total_likes
- created_at
- updated_at

#### chapters
- id (PK)
- book_id (FK -> books.id)
- chapter_number
- title
- content_type (simple/interactive)
- content_data (JSON)
- word_count
- is_published
- published_at
- created_at
- updated_at

#### reading_progress
- id (PK)
- user_id (FK -> users.id)
- book_id (FK -> books.id)
- chapter_id (FK -> chapters.id)
- progress_percentage
- last_read_at
- updated_at

#### comments
- id (PK)
- user_id (FK -> users.id)
- chapter_id (FK -> chapters.id)
- parent_comment_id (FK -> comments.id, nullable)
- content
- created_at
- updated_at

#### bookmarks
- id (PK)
- user_id (FK -> users.id)
- book_id (FK -> books.id)
- created_at

#### ratings
- id (PK)
- user_id (FK -> users.id)
- book_id (FK -> books.id)
- rating (1-5)
- created_at
- updated_at

#### chapter_templates
- id (PK)
- name
- description
- preview_image_url
- template_data (JSON)
- created_by (FK -> users.id)
- is_public
- created_at

---

## 🚀 Development Phases

### ✅ Phase 0: Project Setup & Planning
- [x] Create project folder structure
- [x] Initialize Git repository
- [x] Create PROJECT_SCOPE.md document
- [x] Define database schema
- [ ] Create technical architecture diagrams (optional)

### 📦 Phase 1: Backend Foundation (FastAPI)
- [x] **1.1 Project Setup**
  - [x] Initialize FastAPI project
  - [x] Set up virtual environment
  - [x] Create requirements.txt
  - [x] Configure project structure (routers, models, schemas, services)
  - [x] Set up PostgreSQL database
  - [x] Configure SQLAlchemy ORM

- [x] **1.2 User Authentication System**
  - [x] Create User model and database table
  - [x] Implement user registration endpoint
  - [x] Implement user login endpoint (JWT)
  - [x] Implement password hashing (bcrypt)
  - [x] Create authentication middleware
  - [x] Implement token refresh endpoint
  - [x] Create user profile endpoints (GET, PUT)

- [x] **1.3 Books Management API**
  - [x] Create Book model and database table
  - [x] Implement create book endpoint (authors only)
  - [x] Implement get all books endpoint (with pagination, filters)
  - [x] Implement get single book endpoint
  - [x] Implement update book endpoint (author only)
  - [x] Implement delete book endpoint (author only)
  - [x] Implement book search functionality
  - [x] Add genre and tag filtering

- [x] **1.4 Chapters Management API**
  - [x] Create Chapter model and database table
  - [x] Implement create chapter endpoint
  - [x] Implement get chapters by book endpoint
  - [x] Implement get single chapter endpoint
  - [x] Implement update chapter endpoint
  - [x] Implement delete chapter endpoint
  - [x] Implement chapter ordering/reordering
  - [x] Store both simple text and interactive JSON content

- [x] **1.5 Reader Features API**
  - [x] Create ReadingProgress model and endpoints
  - [x] Create Bookmark model and endpoints
  - [x] Create Rating model and endpoints
  - [x] Create Comment model and endpoints (with nested replies)
  - [x] Implement book statistics (views, likes, ratings)

- [x] **1.6 File Upload & Storage**
  - [x] Implement image upload endpoint (cover images, chapter images)
  - [x] Set up local file storage
  - [x] Add file validation (type, size)
  - [x] Generate thumbnails for images

- [x] **1.7 Chapter Templates API**
  - [x] Create ChapterTemplate model
  - [x] Implement CRUD endpoints for templates
  - [x] Create default template library
  - [x] Implement template sharing (public/private)

### 🎨 Phase 2: Frontend Foundation (Next.js)
- [x] **2.1 Project Setup**
  - [x] Initialize Next.js project with TypeScript
  - [x] Set up Tailwind CSS
  - [x] Configure project structure (components, pages, hooks, utils)
  - [x] Set up environment variables
  - [x] Create API client/service layer

- [x] **2.2 Authentication UI**
  - [x] Create login page
  - [x] Create registration page
  - [x] Implement authentication context
  - [x] Create protected route wrapper
  - [x] Add JWT token storage and refresh logic
  - [x] Create user profile page
  - [x] Implement logout functionality

- [x] **2.3 Core Layout & Navigation**
  - [x] Create main layout component
  - [x] Create navigation bar
  - [x] Create footer
  - [x] Create sidebar (for user dashboard)
  - [x] Implement responsive design
  - [x] Add loading states and error boundaries

- [x] **2.4 Book Discovery & Reading**
  - [x] Create home page (featured/trending books)
  - [x] Create book listing page (with filters, search, pagination)
  - [x] Create book detail page
  - [x] Create chapter reading page (simple text view)
  - [x] Implement reading progress tracking
  - [x] Add bookmark functionality
  - [x] Add rating and review UI
  - [x] Create comment section

- [x] **2.5 Author Dashboard**
  - [x] Create author dashboard page
  - [x] Create "My Books" management page
  - [x] Create book creation form
  - [x] Create book editing form
  - [x] Display book statistics (views, ratings, comments)

### ✍️ Phase 3: Chapter Writing Experience
- [ ] **3.1 Simple Text Editor**
  - [ ] Integrate rich text editor (Tiptap/Lexical)
  - [ ] Add formatting toolbar (bold, italic, headings, lists)
  - [ ] Add image insertion
  - [ ] Implement auto-save
  - [ ] Add word count display
  - [ ] Create chapter creation/editing UI

- [ ] **3.2 Advanced Code Editor**
  - [ ] Integrate Monaco Editor
  - [ ] Create code editor tab/view
  - [ ] Add syntax highlighting for custom chapter DSL
  - [ ] Implement live preview pane
  - [ ] Add code snippets and autocomplete
  - [ ] Create documentation/help panel

- [ ] **3.3 Template System**
  - [ ] Create template selection UI
  - [ ] Display template previews
  - [ ] Implement template application to chapters
  - [ ] Create template editor
  - [ ] Allow custom template creation
  - [ ] Add template gallery

### 🎮 Phase 4: Interactive Chapter Features
- [ ] **4.1 Chapter Format Definition**
  - [ ] Design JSON structure for interactive chapters
  - [ ] Define node types (text, choice, image, animation, etc.)
  - [ ] Create chapter parser/validator
  - [ ] Document chapter format specification

- [ ] **4.2 Interactive Renderer**
  - [ ] Create chapter rendering engine
  - [ ] Implement text nodes
  - [ ] Implement choice/branching nodes
  - [ ] Implement image nodes
  - [ ] Implement custom styling support
  - [ ] Add state management for reader choices
  - [ ] Track reader path through branches

- [ ] **4.3 Visual Effects & Animations**
  - [ ] Integrate animation library (Framer Motion)
  - [ ] Create fade/slide transitions
  - [ ] Add text animations (typing effect, etc.)
  - [ ] Implement background effects
  - [ ] Add sound effect support (optional)

- [ ] **4.4 Visual Novel Elements**
  - [ ] Create dialogue box component
  - [ ] Create character sprite display
  - [ ] Implement background image system
  - [ ] Add character name tags
  - [ ] Create scene transition effects

- [ ] **4.5 Reader Settings**
  - [ ] Create settings panel
  - [ ] Implement "disable visual effects" toggle
  - [ ] Preserve story-critical elements when effects disabled
  - [ ] Add font size/style customization
  - [ ] Add theme toggle (light/dark mode)

### 🎨 Phase 5: Polish & Enhancement
- [ ] **5.1 UI/UX Improvements**
  - [ ] Refine design system
  - [ ] Add animations and transitions
  - [ ] Improve mobile responsiveness
  - [ ] Add loading skeletons
  - [ ] Implement toast notifications
  - [ ] Add confirmation modals

- [ ] **5.2 Performance Optimization**
  - [ ] Implement image lazy loading
  - [ ] Add caching strategies
  - [ ] Optimize database queries
  - [ ] Implement pagination everywhere
  - [ ] Add backend rate limiting

- [ ] **5.3 Additional Features**
  - [ ] Author following system
  - [ ] Reading lists/collections
  - [ ] Book recommendations
  - [ ] Notification system
  - [ ] Search with advanced filters
  - [ ] Activity feed

### 🧪 Phase 6: Testing & Deployment
- [ ] **6.1 Testing**
  - [ ] Write backend unit tests
  - [ ] Write frontend component tests
  - [ ] Write integration tests
  - [ ] Perform manual testing
  - [ ] Test interactive chapters thoroughly
  - [ ] Cross-browser testing

- [ ] **6.2 Deployment Preparation**
  - [ ] Set up production database
  - [ ] Configure cloud file storage (S3/R2)
  - [ ] Set up environment variables
  - [ ] Create deployment scripts
  - [ ] Set up CI/CD pipeline (optional)

- [ ] **6.3 Deployment**
  - [ ] Deploy backend (Railway, Render, or DigitalOcean)
  - [ ] Deploy frontend (Vercel, Netlify, or similar)
  - [ ] Configure domain and SSL
  - [ ] Set up monitoring and logging
  - [ ] Create backup strategy

### 📱 Phase 7: Mobile Development (Future)
- [ ] Initialize React Native project
- [ ] Port core UI components
- [ ] Implement mobile-specific navigation
- [ ] Test interactive chapters on mobile
- [ ] Deploy to app stores

---

## 📝 Current Status

**Current Phase:** Phase 2 - Frontend Foundation  
**Progress:** Phase 2.5 COMPLETE! (100% of Phase 2) 🎉

### Recently Completed
- ✅ Phase 2.5: Author Dashboard (JUST COMPLETED!)
  - ✅ Enhanced dashboard with real-time stats and data loading
  - ✅ Built "My Books" management page with filtering and actions
  - ✅ Created comprehensive book creation form
  - ✅ Built book editing form with statistics display
  - ✅ Implemented chapter management interface
  - ✅ Created chapter creation page with simple text editor
  - ✅ Built chapter editing page with info panel
  - ✅ Added reusable BookStats and SimpleStatsGrid components
  - ✅ Full CRUD operations for books and chapters
  - ✅ Role-based access control throughout

- ✅ Phase 2.4: Book Discovery & Reading
  - ✅ Enhanced home page with featured and trending books
  - ✅ Created comprehensive book listing page with search, filters, and pagination
  - ✅ Built book detail page with statistics, bookmarks, and rating system
  - ✅ Implemented chapter reading page with font controls and navigation
  - ✅ Added reading progress tracking
  - ✅ Implemented bookmark functionality
  - ✅ Created interactive rating system (1-5 stars)
  - ✅ Built full comment section with nested replies
  - ✅ Created reusable BookCard and BookGrid components
  - ✅ Enhanced reader service with convenience methods

### Previously Completed
- ✅ Phase 2.3: Core Layout & Navigation
  - ✅ Created DashboardLayout with integrated sidebar
  - ✅ Created MainLayout for content pages
  - ✅ Built responsive Sidebar with role-based navigation
  - ✅ Enhanced Header with mobile menu
  - ✅ Created loading components (LoadingSpinner, LoadingScreen, SkeletonLoader)
  - ✅ Implemented ErrorBoundary for error handling
  - ✅ Built reusable UI components (Button, Card, Alert, EmptyState)
  - ✅ Updated dashboard pages with new layouts
  - ✅ Created dashboard sub-pages (My Books, Library, Bookmarks, Settings)
  - ✅ Implemented full mobile responsiveness

- ✅ Phase 2.2: Authentication UI
  - ✅ Created AuthContext provider with global state
  - ✅ Built login page with validation
  - ✅ Built registration page with role selection
  - ✅ Implemented ProtectedRoute and RoleGuard components
  - ✅ Created user profile page with edit functionality
  - ✅ Built Header with auth-aware navigation
  - ✅ Built Footer component
  - ✅ Updated root layout with AuthProvider
  - ✅ Created modern home page
  - ✅ Added placeholder pages for books and dashboard

- ✅ Phase 2.1: Frontend Project Setup
  - ✅ Initialized Next.js 14+ with TypeScript
  - ✅ Configured Tailwind CSS
  - ✅ Created comprehensive project structure
  - ✅ Set up environment variables
  - ✅ Built complete API client with token management
  - ✅ Created service layer for all backend endpoints
  - ✅ Defined TypeScript types for all models
  - ✅ Created custom hooks (useAuth)
  - ✅ Built utility functions library
  - ✅ Comprehensive documentation

### Next Up
- 📝 Phase 3: Chapter Writing Experience
  - Phase 3.1: Simple Text Editor (rich text editing)
  - Phase 3.2: Advanced Code Editor (Monaco integration)
  - Phase 3.3: Template System (chapter templates)

---

## 🎯 Success Metrics

- [ ] Users can register and authenticate
- [ ] Authors can create and publish books with multiple chapters
- [ ] Authors can write chapters in both simple and advanced mode
- [ ] Authors can create interactive chapters with branching storylines
- [ ] Readers can read and navigate through books
- [ ] Readers can make choices that affect story flow
- [ ] Readers can toggle visual effects on/off
- [ ] Platform is responsive and works on mobile browsers
- [ ] Interactive features render smoothly without security issues

---

## 📚 Resources & Documentation

### Learning Resources
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Next.js Documentation: https://nextjs.org/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Tailwind CSS: https://tailwindcss.com/docs
- Monaco Editor: https://microsoft.github.io/monaco-editor/

### Similar Platforms for Reference
- Wattpad
- Webnovel
- Royal Road
- Archive of Our Own (AO3)

---

## 🔄 Change Log

**January 7, 2026**
- ✅ Completed Phase 2.5: Author Dashboard (PHASE 2 COMPLETE! 🎉)
  - Enhanced dashboard with real-time statistics
  - "My Books" management page with filtering
  - Book creation and editing forms
  - Chapter management interface
  - Chapter creation and editing pages
  - BookStats and SimpleStatsGrid components
  - Full CRUD operations for books and chapters
  - Role-based access control
  - All 7 pages + components working perfectly
- ✅ Completed Phase 2.4: Book Discovery & Reading
  - Enhanced home page with featured/trending books
  - Comprehensive book listing with search, filters, pagination
  - Book detail page with bookmarks and ratings
  - Chapter reading page with progress tracking
  - Full comment section with nested replies
  - BookCard and BookGrid components
  - Enhanced reader service
- ✅ Completed Phase 2.3: Core Layout & Navigation
  - DashboardLayout and MainLayout components
  - Responsive Sidebar with role-based navigation
  - Enhanced Header with mobile menu
  - Loading states (LoadingSpinner, LoadingScreen, SkeletonLoader)
  - ErrorBoundary for error handling
  - UI components (Button, Card, Alert, EmptyState)
  - Dashboard sub-pages created
  - Full mobile responsiveness implemented

**January 6, 2026**
- Initial project scope created
- Defined tech stack
- Outlined development phases
- Created database schema
- ✅ Completed Phase 1: Backend Foundation (all 7 sub-phases)
- ✅ Completed Phase 2.1: Frontend Project Setup
  - Next.js 14+ with TypeScript initialized
  - Complete API client and service layer created
  - TypeScript types for all models defined
  - Custom hooks and utilities implemented
- ✅ Completed Phase 2.2: Authentication UI
  - AuthContext provider for global authentication state
  - Login and registration pages with validation
  - Protected routes and role-based access control
  - User profile page with edit functionality
  - Header and Footer components
  - Modern home page with hero section

---

## 💡 Future Enhancements (Post-MVP)

- Monetization (paid chapters, subscriptions, tips)
- Advanced analytics for authors
- Collaborative writing features
- Translation support
- Content moderation tools
- Advanced security/sandboxing for code execution
- AI writing assistance
- Audio narration
- Community features (forums, writing contests)
- Publishing/exporting books to ebook formats

---

**Note:** This is a living document and will be updated as the project progresses. Tasks will be marked as complete with ✅ once finished.

