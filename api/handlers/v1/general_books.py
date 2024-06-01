from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, asc, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from starlette.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
)

from api.annotated_types import PageQuery, PageNumberQuery, BookPrivateSortAttrQuery, SortByQuery, BookPrivateID, \
    GeneralBookSortAttrQuery, GeneralBookID
from src.database import (BookPrivate,
                          GeneralBook,
                          Tag, BookPrivateTag, User)
from src.dependencies.authenticate import authenticate, get_current_user
from src.dependencies.database_session import (
    DBAsyncSession
)
from src.types import GeneralBookExtendedDTO, BookPrivateDTO, GeneralBooksDTO
from sqlalchemy import select, asc, desc, delete, and_

from sqlalchemy import event

from src.types.book_private import BookPrivateListDTO, BookPrivateCreateDTO, BookPrivateUpdateDTO
from src.types.general_books import GeneralBooksForPrivateDTO, GeneralBookCreateDTO, GeneralBookUpdateDTO

router = APIRouter(tags=["GeneralBook"])


@router.get(
    path="/general_books_all",
    response_model=list[GeneralBooksForPrivateDTO],
    status_code=HTTP_200_OK,
    response_description="List of books_private",
    summary="Getting a list of books_private",
    name="book-private-all"
)
async def book_private_all(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: GeneralBookSortAttrQuery = "id",
        order_by: SortByQuery = "asc"
):
    statement = (
        select(GeneralBook)
        .limit(page_number)
        .offset(page * page_number - page_number)
    )

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [GeneralBooksForPrivateDTO.model_validate(obj=obj) for obj in objs.all()]


@event.listens_for(GeneralBook, 'before_insert')
def before_insert_listener(mapper, connection, target: GeneralBook):
    if not target.slug:
        target.generate_slug()


@router.post(
    path="/general_books",
    response_model=GeneralBookCreateDTO,
    status_code=HTTP_201_CREATED,
    response_description="Detail of general book",
    summary="Creating a new general book",
    dependencies=[authenticate],
    name="book-private-create"
)
async def books_private_create(session: DBAsyncSession, data: GeneralBookCreateDTO):
    general_book = GeneralBook(**data.model_dump())
    print(f"Creating general book with data: {data}")
    session.add(instance=general_book)
    try:
        await session.commit()
    except IntegrityError as e:
        print(f"IntegrityError {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"book {data.title} exists")
    else:
        await session.refresh(instance=general_book)
        return GeneralBookCreateDTO.model_validate(obj=general_book)


@router.put(
    path="/general_books/{id}",
    status_code=HTTP_201_CREATED,
    response_model=GeneralBooksForPrivateDTO,
    dependencies=[authenticate],
    name="general-book-update"
)
async def general_book_update(session: DBAsyncSession, body: GeneralBookUpdateDTO, pk: GeneralBookID):
    obj = await session.get(entity=GeneralBook, ident=pk)
    for k, v in body:
        setattr(obj, k, v)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="GeneralBook name is not found")
    else:
        return GeneralBooksForPrivateDTO.model_validate(obj=obj)


@router.delete(
    path="/general_books/{id}",
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[authenticate],
    name="general-books-delete"
)
async def general_book_delete(session: DBAsyncSession, pk: GeneralBookID):
    await session.execute(delete(GeneralBook).filter(and_(GeneralBook.id == pk)))
    await session.commit()
