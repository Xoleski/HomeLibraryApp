from typing import Optional
from fastapi import HTTPException, Query
from fastapi import APIRouter
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import joinedload
from starlette.status import (HTTP_200_OK, HTTP_404_NOT_FOUND)

from api.annotated_types import PageQuery, PageNumberQuery, SortByQuery, UsersSortAttrQuery, BookPrivateSortAttrQuery
from src.database import (User, BookPrivate)
from src.dependencies.database_session import (DBAsyncSession)
from src.types import UserDTO
from src.types.user import UserBooksExtendedDTO

router = APIRouter(tags=["User"])


@router.get(
    path="/users_all",
    response_model=list[UserDTO],
    status_code=HTTP_200_OK,
    response_description="List of users",
    summary="Getting a list of users",
    name="users-all"
)
async def users_all(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: UsersSortAttrQuery = "id",
        order_by: SortByQuery = "asc"
):
    statement = (
        select(User)
        .limit(page_number)
        .offset(page * page_number - page_number)
    )

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [UserDTO.model_validate(obj=obj) for obj in objs.all()]


@router.get(
    path="/user_books_private",
    response_model=UserBooksExtendedDTO,
    status_code=HTTP_200_OK,
    response_description="List of user's books",
    summary="Getting a list of user's books",
    name="user-book-list"
)
async def user_book_list(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: BookPrivateSortAttrQuery = "id",
        order_by: SortByQuery = "asc",
        email: Optional[str] = Query(None, alias='email'),
):
    result = await session.execute(
        select(User)
        .where(User.email == email)
        .options(
            joinedload(User.books_private).subqueryload(BookPrivate.tags_private)
        )
    )
    book_private = result.scalars().first()
    print(book_private)

    if book_private is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"user {email} does not exist")
    return UserBooksExtendedDTO.model_validate(obj=book_private)
