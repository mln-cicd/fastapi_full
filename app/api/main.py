from fastapi import APIRouter

from app.api.routes import users, posts, login

api_router = APIRouter()
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(login.router, prefix="/login", tags=["Login"])
