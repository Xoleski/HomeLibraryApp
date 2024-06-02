from fastapi import APIRouter, HTTPException
from sqlalchemy import select, asc, desc, delete, and_
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)

from api.annotated_types import PageQuery, PageNumberQuery, SortByQuery, \
    GeneralBookSortAttrQuery, GeneralBookID
from src.database import (
    GeneralBook,
    Tag,
)
from src.dependencies.authenticate import authenticate
from src.dependencies.database_session import (DBAsyncSession)
from src.types import GeneralBooksDTO
from src.types.general_books import GeneralBooksForPrivateDTO, GeneralBookCreateDTO, GeneralBookUpdateDTO

router = APIRouter(tags=["GeneralBook"])


@router.get(
    path="/general_books_all",
    response_model=list[GeneralBooksDTO],
    status_code=HTTP_200_OK,
    response_description="List of general books",
    summary="Getting a list of general books",
    name="general-books-all"
)
async def general_books_all(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: GeneralBookSortAttrQuery = "id",
        order_by: SortByQuery = "asc"
):
    statement = (
        select(GeneralBook)
        .options(
            selectinload(GeneralBook.tags_general)
        )
        .limit(page_number)
        .offset(page * page_number - page_number)
    )

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [GeneralBooksDTO.model_validate(obj=obj) for obj in objs.all()]


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
    name="general-book-create"
)
async def general_book_create(session: DBAsyncSession, data: GeneralBookCreateDTO):
    general_book = GeneralBook(**data.model_dump(exclude={"tags"}))
    print(f"Creating general book with data: {data}")
    if data.tags:
        tags = await session.execute(select(Tag).where(Tag.id.in_(data.tags)))
        general_book.tags_general = tags.scalars().all()
        print(tags, "tags")

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
    status_code=HTTP_200_OK,
    response_model=GeneralBooksForPrivateDTO,
    dependencies=[authenticate],
    name="general-book-update"
)
async def general_book_update(session: DBAsyncSession, body: GeneralBookUpdateDTO, pk: GeneralBookID):
    obj = await session.get(
        entity=GeneralBook,
        ident=pk,
        options=[selectinload(GeneralBook.tags_general)],
        with_for_update=True
    )

    for k, v in body.model_dump(exclude={"tags"}).items():
        setattr(obj, k, v)

    if body.tags is not None:
        current_tag_ids = {tag.id for tag in obj.tags_general}
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
            tags_result = await session.execute(select(Tag).where(Tag.id.in_(tags_to_add)))
            tags_to_add_objs = tags_result.scalars().all()
            for tag in tags_to_add_objs:
                obj.tags_general.append(tag)

        if tags_to_remove:
            print("REMOVE to")
            tags_to_remove_objs = [tag for tag in obj.tags_general if tag.id in tags_to_remove]
            for tag in tags_to_remove_objs:
                obj.tags_general.remove(tag)
    else:
        obj.tags_general = []
        ...

    try:
        await session.commit()
        # await session.refresh(obj)
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


# @router.put(
#     path="/general_books/{id}",
#     status_code=HTTP_201_CREATED,
#     response_model=GeneralBooksForPrivateDTO,
#     dependencies=[authenticate],
#     name="general-book-update"
# )
# async def general_book_update(session: DBAsyncSession, body: GeneralBookUpdateDTO, pk: GeneralBookID):
#     obj = await session.get(entity=GeneralBook, ident=pk)
#     for k, v in body:
#         setattr(obj, k, v)
#     try:
#         await session.commit()
#     except IntegrityError:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="GeneralBook name is not found")
#     else:
#         return GeneralBooksForPrivateDTO.model_validate(obj=obj)
