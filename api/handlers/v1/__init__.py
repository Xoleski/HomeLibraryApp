from fastapi import APIRouter

from api.handlers.v1 import categories, books_private, users, general_books, tags

__all__ = ["router", ]


router = APIRouter(prefix="/v1")
router.include_router(router=categories.router)
router.include_router(router=books_private.router)
router.include_router(router=users.router)
router.include_router(router=general_books.router)
router.include_router(router=tags.router)

