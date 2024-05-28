from fastapi import APIRouter

from api.handlers.v1 import categories, books_private

__all__ = ["router", ]


router = APIRouter(prefix="/v1")
router.include_router(router=categories.router)
router.include_router(router=books_private.router)