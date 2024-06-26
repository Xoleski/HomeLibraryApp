from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, asc, desc, delete, and_, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload
from starlette.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT
)
from typing import Optional

from api.annotated_types import (
    PageQuery,
    PageNumberQuery,
    BookPrivateSortAttrQuery,
    SortByQuery,
    BookPrivateID
)
from src.database import (
    BookPrivate,
    GeneralBook,
    Tag,
    User,
)
from src.dependencies.authenticate import authenticate, get_current_user, CurrentUser
from src.dependencies.database_session import DBAsyncSession
from src.types import GeneralBookExtendedDTO, BookPrivateDTO
from src.types.book_private import (
    BookPrivateListDTO,
    BookPrivateUpdateDTO,
    BookPrivateCreateDTO
)
from src.utils.slugify import slugify

router = APIRouter(tags=["BookPrivate"])


@router.get(
    path="/books_private/{slug}",
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
        author: Optional[str] = Query(None, alias='author'),
):
    result = await session.scalar(
        select(GeneralBook)
        .filter(
            and_(
                GeneralBook.title == title,
                GeneralBook.author == author
            )
        )
        .options(
            joinedload(GeneralBook.books_private).subqueryload(BookPrivate.tags_private)
        )
    )
    book_private = result
    print(book_private)

    if book_private is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"book {title} {author} does not exist")
    return GeneralBookExtendedDTO.model_validate(obj=book_private)


# @event.listens_for(BookPrivate, 'before_insert')
# def before_insert_listener(mapper, connection, target: BookPrivate):
#     if not target.slug:
#         target.slug = slugify(value=target.title)
#         print(f"Generated slug: {target.slug}")


@router.post(
    path="/books_private",
    response_model=BookPrivateCreateDTO,
    status_code=HTTP_201_CREATED,
    response_description="Detail of book private",
    summary="Creating a new book private",
    dependencies=[authenticate],
    name="book-private-create"
)
async def books_private_create(
        session: DBAsyncSession,
        data: BookPrivateCreateDTO,
        current_user: CurrentUser
):
    book_private = BookPrivate(**data.model_dump(exclude={"tags"}))
    book_private.user_email = current_user.email
    print(f"Creating your book with data: {data}")
    print(f"Creating your book with user: {current_user}")
    if data.tags:
        tags = await session.scalars(select(Tag).where(Tag.id.in_(data.tags)))
        if len(data.tags) != len(tags.all()):
            raise ValueError("Передан невалидный тэг")
        tags = await session.scalars(select(Tag).where(Tag.id.in_(data.tags)))
        book_private.tags_private = tags.all()

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
    path="/books_private",
    response_model=list[BookPrivateListDTO],
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
        .options(
            selectinload(BookPrivate.tags_private)
        )
        .limit(page_number)
        .offset(page * page_number - page_number)
    )

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [BookPrivateListDTO.model_validate(obj=obj) for obj in objs]


@router.put(
    path="/books_private/{id}",
    status_code=HTTP_200_OK,
    response_model=BookPrivateDTO,
    dependencies=[authenticate],
    name="book-private-update"
)
async def book_private_update(session: DBAsyncSession, body: BookPrivateUpdateDTO, pk: BookPrivateID):
    obj = await session.get(
        entity=BookPrivate,
        ident=pk,
        options=[selectinload(BookPrivate.tags_private)],
    )

    for k, v in body.model_dump(exclude={"tags"}).items():
        setattr(obj, k, v)

    if body.tags is not None:
        current_tag_ids = {tag.id for tag in obj.tags_private}
        print("current_tag_ids", current_tag_ids)
        new_tag_ids = set(body.tags)
        print("new_tag_ids", new_tag_ids)

        # Теги для добавления
        tags_to_add = new_tag_ids - current_tag_ids
        print("tags_to_add", tags_to_add)

        # Теги для удаления
        tags_to_remove = current_tag_ids - new_tag_ids
        print("tags_to_remove", tags_to_remove)

        if tags_to_add:
            print("ADD to")
            tags_result = await session.scalars(select(Tag).where(Tag.id.in_(tags_to_add)))
            tags_to_add_objs = tags_result.all()
            for tag in tags_to_add_objs:
                obj.tags_private.append(tag)

        if tags_to_remove:
            print("REMOVE to")
            tags_to_remove_objs = [tag for tag in obj.tags_private if tag.id in tags_to_remove]
            for tag in tags_to_remove_objs:
                obj.tags_private.remove(tag)
    else:
        obj.tags_private = []
        ...

    try:
        await session.commit()
        # await session.refresh(obj)
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="PrivateBook name is not found")
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


# @router.put(
#     path="/books_private/{id}",
#     status_code=HTTP_200_OK,
#     response_model=BookPrivateDTO,
#     dependencies=[authenticate],
#     name="book-private-update"
# )
# async def book_private_update(session: DBAsyncSession, body: BookPrivateUpdateDTO, pk: BookPrivateID):
#     obj = await session.get(entity=BookPrivate, ident=pk)
#     for k, v in body:
#         setattr(obj, k, v)
#     try:
#         await session.commit()
#     except IntegrityError:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="GeneralBook name is not found")
#     else:
#         return BookPrivateDTO.model_validate(obj=obj)


# @router.put(
#     path="/books_private/{id}",
#     status_code=HTTP_200_OK,
#     response_model=BookPrivateDTO,
#     dependencies=[authenticate],
#     name="book-private-update"
# )
# async def book_private_update(session: DBAsyncSession, body: BookPrivateUpdateDTO, pk: BookPrivateID):
#     obj = await session.get(
#         entity=BookPrivate,
#         ident=pk,
#         options=[selectinload(BookPrivate.tags_private)],
#         with_for_update=True
#     )
#     for k, v in body.model_dump(exclude={"tags"}).items():
#         setattr(obj, k, v)
#
#     if body.tags:
#         tags_result = await session.execute(select(Tag).where(Tag.id.in_(body.tags)))
#         tags = tags_result.scalars().all()
#         obj.tags_private = tags
#     else:
#         obj.tags_private = []
#         ...
#
#     try:
#         await session.commit()
#         # await session.refresh(obj)
#     except IntegrityError:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="GeneralBook name is not found")
#     else:
#         return BookPrivateDTO.model_validate(obj=obj)
