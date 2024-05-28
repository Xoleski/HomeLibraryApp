from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND
)

from src.database import (BookPrivate,
                          GeneralBook)
from src.dependencies.database_session import (
    DBAsyncSession
)
from src.types import GeneralBookExtendedDTO

# from src.types.general_books import GeneralBookExtendedDTO

# from src.types.book_private import BookPrivateExtendedDTO

router = APIRouter(tags=["GeneralBook"])


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
    path="/books_private",
    response_model=GeneralBookExtendedDTO,
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
        select(GeneralBook)
        .where(GeneralBook.title == title and GeneralBook.author == author)
        .options(
            joinedload(GeneralBook.books_private).subqueryload(BookPrivate.tags_private)
        )
    )
    book_private = result.scalars().first()
    print(book_private)

    if book_private is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"book {title} {author} does not exist")
    return GeneralBookExtendedDTO.model_validate(obj=book_private)

    # query = select(BookPrivate).options(
    #     joinedload(BookPrivate.general_book).subqueryload(GeneralBook.tags)
    # )
    # if title:
    #     query = query.where(BookPrivate.title == title)
    # if author:
    #     query = query.where(BookPrivate.author == author)
    #
    # result = await session.execute(query)
    # books_private = result.scalars().all()
    #
    # if not books_private:
    #     raise HTTPException(status_code=HTTP_404_NOT_FOUND,
    #                         detail=f"Books with title '{title}' and author '{author}' do not exist")
    #
    # books_private_dto = [BookPrivateCreateDTO.from_orm(book) for book in books_private]
    #
    # return BookPrivateExtendedDTO(id=books_private[0].id, books_private=books_private_dto)


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


