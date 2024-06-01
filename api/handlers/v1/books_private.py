from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, asc, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from starlette.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
)

from api.annotated_types import PageQuery, PageNumberQuery, BookPrivateSortAttrQuery, SortByQuery, BookPrivateID
from src.database import (BookPrivate,
                          GeneralBook,
                          Tag, BookPrivateTag, User)
from src.dependencies.authenticate import authenticate, get_current_user
from src.dependencies.database_session import (
    DBAsyncSession
)
from src.types import GeneralBookExtendedDTO, BookPrivateDTO
from sqlalchemy import select, asc, desc, delete, and_

from sqlalchemy import event

from src.types.book_private import BookPrivateListDTO, BookPrivateCreateDTO, BookPrivateUpdateDTO

router = APIRouter(tags=["BookPrivate"])


@router.get(
    path="/books_private_list",
    response_model=GeneralBookExtendedDTO,
    status_code=HTTP_200_OK,
    response_description="List of books_private",
    summary="Getting a list of books_private",
    name="book_private-list"
)
async def book_private_list(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: BookPrivateSortAttrQuery = "id",
        order_by: SortByQuery = "asc",
        # page: int = Query(1, alias='page'),
        # page_number: int = Query(25, alias='page_number'),
        # order: str = Query("id", alias='order'),
        # order_by: str = Query("asc", alias='order_by'),
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


@event.listens_for(BookPrivate, 'before_insert')
def before_insert_listener(mapper, connection, target: BookPrivate):
    if not target.slug:
        target.generate_slug()


@router.post(
    path="/books_private",
    response_model=BookPrivateCreateDTO,
    status_code=HTTP_201_CREATED,
    response_description="Detail of book private",
    summary="Creating a new book private",
    dependencies=[authenticate],
    name="book-private-create"
)
async def books_private_create(session: DBAsyncSession, data: BookPrivateCreateDTO, current_user: User = Depends(get_current_user)):
    book_private = BookPrivate(**data.model_dump())
    book_private.user_email = current_user.email
    print(f"Creating your book with data: {data}")
    print(f"Creating your book with user: {current_user}")
    session.add(instance=book_private)
    try:
        await session.commit()
    except IntegrityError as e:
        print(f"IntegrityError {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"book {data.title} exists")
    else:
        await session.refresh(instance=book_private)
        return BookPrivateCreateDTO.model_validate(obj=book_private)


@router.get(
    path="/books_private_all",
    response_model=list[BookPrivateDTO],
    status_code=HTTP_200_OK,
    response_description="List of books_private",
    summary="Getting a list of books_private",
    name="book-private-all"
)
async def book_private_all(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: BookPrivateSortAttrQuery = "id",
        order_by: SortByQuery = "asc"
):
    statement = (
        select(BookPrivate)
        .limit(page_number)
        .offset(page * page_number - page_number)
    )

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [BookPrivateDTO.model_validate(obj=obj) for obj in objs.all()]


@router.put(
    path="/books_private/{id}",
    status_code=HTTP_201_CREATED,
    response_model=BookPrivateDTO,
    dependencies=[authenticate],
    name="book-private-update"
)
async def book_private_update(session: DBAsyncSession, body: BookPrivateUpdateDTO, pk: BookPrivateID):
    obj = await session.get(entity=BookPrivate, ident=pk)
    for k, v in body:
        setattr(obj, k, v)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="BookPrivate name is not found")
    else:
        return BookPrivateDTO.model_validate(obj=obj)


@router.delete(
    path="/books_private/{id}",
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[authenticate],
    name="books-private-delete"
)
async def book_private_delete(session: DBAsyncSession, pk: BookPrivateID):
    await session.execute(delete(BookPrivate).filter(and_(BookPrivate.id == pk)))
    await session.commit()
