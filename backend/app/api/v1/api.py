"""
API v1 router aggregation
"""
from fastapi import APIRouter

api_router = APIRouter()

# Import and include endpoint routers here as they are created
# Example:
# from app.api.v1.endpoints import auth, users, books, chapters
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(books.router, prefix="/books", tags=["books"])
# api_router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])

@api_router.get("/")
async def api_root():
    """API v1 root endpoint"""
    return {"message": "Interactive Web Novels API v1"}

