from celery.result import AsyncResult
# from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError


from fastapi import APIRouter, HTTPException, Path
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
    SortByQuery, TagSortAttrQuery, TagID
)
from src.database import (Category,
                          BookPrivate,
                          GeneralBook, Tag)
from src.dependencies.database_session import (
    DBAsyncSession
)
from src.dependencies.authenticate import authenticate
from src.types import (
    CategoryDTO,
    CategoryCreateDTO,
    CategoryUpdateDTO,
    CategoryExtendedDTO
)

from src.tasks.tasks import foo
from sqlalchemy import event

from src.types.tag import TagDTO, TagCreateDTO, TagUpdateDTO

router = APIRouter(tags=["Tag"])


@router.get(
    path="/tags_all",
    response_model=list[TagDTO],
    status_code=HTTP_200_OK,
    response_description="List of tags",
    summary="Getting a list of tags",
    name="tag-list"
)
async def tag_list(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: TagSortAttrQuery = "id",
        order_by: SortByQuery = "asc"
):
    statement = (select(Tag).
                 limit(page_number).
                 offset(page * page_number - page_number))

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [TagDTO.model_validate(obj=obj) for obj in objs.all()]


@router.post(
    path="/tags",
    response_model=TagDTO,
    status_code=HTTP_201_CREATED,
    response_description="Detail of tag",
    summary="Creating a new ctag",
    dependencies=[authenticate],
    name="tag-create"
)
async def tag_create(session: DBAsyncSession, data: TagCreateDTO):
    tag = Tag(**data.model_dump())
    print(f"Creating tag with data: {data}")
    session.add(instance=tag)
    try:
        await session.commit()
    except IntegrityError as e:
        print(f"IntegrityError {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"tag {data.name} exists")
    else:
        await session.refresh(instance=tag)
        return TagDTO.model_validate(obj=tag)


@router.put(
    path="/tags/{id}",
    status_code=HTTP_201_CREATED,
    response_model=TagDTO,
    dependencies=[authenticate],
    name="tag-update"
)
async def tag_update(session: DBAsyncSession, body: TagUpdateDTO, pk: TagID):
    obj = await session.get(entity=Tag, ident=pk)
    for k, v in body:
        setattr(obj, k, v)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="tag name is not found")
    else:
        return TagDTO.model_validate(obj=obj)


@router.delete(
    path="/tags/{id}",
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[authenticate],
    name="tag-delete"
)
async def tag_delete(session: DBAsyncSession, pk: TagID):
    await session.execute(delete(Tag).filter(and_(Tag.id == pk)))
    await session.commit()
