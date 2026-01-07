"""
API v1 router aggregation
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, books, chapters, files
from app.api.v1.endpoints import reading_progress, bookmarks, ratings, comments

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(chapters.router, tags=["chapters"])
api_router.include_router(reading_progress.router, prefix="/reading-progress", tags=["reading-progress"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(files.router, prefix="/files", tags=["files"])

@api_router.get("/")
async def api_root():
    """API v1 root endpoint"""
    return {"message": "Interactive Web Novels API v1"}

