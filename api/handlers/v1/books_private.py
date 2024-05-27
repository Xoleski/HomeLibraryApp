from typing import Optional, List

from celery.result import AsyncResult
from sqlite3 import IntegrityError

from fastapi import APIRouter, HTTPException, Path, Query
from sqlalchemy import select, asc, desc, delete, and_
from sqlalchemy.orm import joinedload, validates
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from api.annotated_types import (
    CategoryID,
    PageQuery,
    PageNumberQuery,
    CategorySortAttrQuery,
    SortByQuery, BookPrivateSortAttrQuery
)
from src.database import (Category,
                          BookPrivate,
                          GeneralBook)
from src.dependencies.database_session import (
    DBAsyncSession
)
from src.dependencies.authenticate import authenticate
from src.types import (
    BookPrivateDTO,
    BookPrivateCreateDTO,
)

from src.tasks.tasks import foo
from sqlalchemy import event

from src.types.book_private import BookPrivateExtendedDTO

router = APIRouter(tags=["BookPrivate"])


# @router.get(
#     path="/books_private",
#     response_model=list[BookPrivateDTO],
#     status_code=HTTP_200_OK,
#     response_description="List of books_private",
#     summary="Getting a list of books_private",
#     name="book_private-list"
# )
# async def book_private_list(
#         session: DBAsyncSession,
#         page: PageQuery = 1,
#         page_number: PageNumberQuery = 25,
#         order: BookPrivateSortAttrQuery = "id",
#         order_by: SortByQuery = "asc"
# ):
#     statement = (select(BookPrivate).
#                  limit(page_number).
#                  offset(page * page_number - page_number))
#
#     if order_by == "asc":
#         statement = statement.order_by(asc(order))
#     else:
#         statement = statement.order_by(desc(order))
#
#     objs = await session.scalars(statement=statement)
#     return [BookPrivateDTO.model_validate(obj=obj) for obj in objs.all()]



@router.get(
    path="/books_private/{title}{author}",
    response_model=list[BookPrivateDTO],
    status_code=HTTP_200_OK,
    response_description="List of books_private",
    summary="Getting a list of books_private",
    name="book_private-list"
)
async def book_private_list(
        session: DBAsyncSession,
        page: int = Query(1, alias='page'),
        page_number: int = Query(25, alias='page_number'),
        order: str = Query("id", alias='order'),
        order_by: str = Query("asc", alias='order_by'),
        title: Optional[str] = Query(None, alias='title'),
        author: Optional[str] = Query(None, alias='author')
):
    result = await session.execute(
        select(BookPrivate)
        .where(BookPrivate.title == title and BookPrivate.author == author)
        .options(
            joinedload(BookPrivate.general_book).subqueryload(BookPrivate.tags)
        )
    )
    book_private = result.scalars().first()

    if book_private is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"category {title} {author} does not exist")
    return BookPrivateExtendedDTO.model_validate(obj=book_private)

    # statement = select(BookPrivate)
    #
    # filters = []
    # if title:
    #     filters.append(BookPrivate.title == title)
    # if author:
    #     filters.append(BookPrivate.author == author)
    #
    # if filters:
    #     statement = statement.where(and_(*filters))
    #
    #
    # if order_by == "asc":
    #     statement = statement.order_by(asc(order))
    # else:
    #     statement = statement.order_by(desc(order))
    #
    # statement = statement.limit(page_number).offset(page * page_number - page_number)
    #
    # objs = await session.scalars(statement=statement)
    # book_list = objs.all()
    #
    # if not book_list:
    #     raise HTTPException(status_code=404, detail="Books not found")
    #
    # return [BookPrivateDTO.model_validate(obj=obj) for obj in book_list]


# @event.listens_for(Category, 'before_insert')
# def before_insert_listener(mapper, connection, target: Category):
#     # target.to_lowercase()
#     if not target.slug:
#         target.generate_slug()
#


