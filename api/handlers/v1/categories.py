from celery.result import AsyncResult
from sqlalchemy.exc import IntegrityError


from fastapi import APIRouter, HTTPException, Path
from sqlalchemy import select, asc, desc, delete, and_
from sqlalchemy import event
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
    SortByQuery
)
from src.database import (Category,
                          GeneralBook)
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

from src.utils.slugify import slugify
from src.tasks.tasks import foo

router = APIRouter(tags=["Category"])


@router.get(
    path="/categories",
    response_model=list[CategoryDTO],
    status_code=HTTP_200_OK,
    response_description="List of categories",
    summary="Getting a list of categories",
    name="category-list"
)
async def category_list(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: CategorySortAttrQuery = "id",
        order_by: SortByQuery = "asc"
):
    statement = (select(Category).
                 limit(page_number).
                 offset(page * page_number - page_number))

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [CategoryDTO.model_validate(obj=obj) for obj in objs.all()]


# @router.get(path="/job")
# async def start_job():
#     task = foo.delay(6, 6)
#     return {"job_id": task.id}
#
#
# @router.get(path="/job/status/{job_id}")
# async def get_job(job_id: str = Path()):
#     task = AsyncResult(id=job_id)
#     return {"status": task.status}


# Event listener for automatically generating slug
# @event.listens_for(Category, 'before_insert')
# def before_insert_listener(mapper, connection, target: Category):
#     # target.to_lowercase()
#     if not target.slug:
#         target.slug = slugify(value=target.name)
#         print(f"Generated slug: {target.slug}")


@router.post(
    path="/categories",
    response_model=CategoryDTO,
    status_code=HTTP_201_CREATED,
    response_description="Detail of category",
    summary="Creating a new category",
    dependencies=[authenticate],
    name="category-create"
)
async def category_create(session: DBAsyncSession, data: CategoryCreateDTO):
    category = Category(**data.model_dump())
    print(f"Creating category with data: {data}")
    session.add(instance=category)
    try:
        await session.commit()
    except IntegrityError as e:
        print(f"IntegrityError {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"category {data.name} exists")
    else:
        await session.refresh(instance=category)
        return CategoryDTO.model_validate(obj=category)


@router.get(
    path="/categories/{slug}",
    response_model=CategoryExtendedDTO,
    status_code=HTTP_200_OK,
    name="category-detail"
)
async def category_detail(session: DBAsyncSession, slug: str):
    result = await session.execute(
        select(Category)
        .where(Category.slug == slug)
        .options(
            joinedload(Category.general_books).subqueryload(GeneralBook.tags_general)
        )
    )
    category = result.scalars().first()
    print(category)

    if category is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"category {slug} does not exist")
    return CategoryExtendedDTO.model_validate(obj=category)


@router.put(
    path="/categories/{id}",
    status_code=HTTP_201_CREATED,
    response_model=CategoryDTO,
    dependencies=[authenticate],
    name="category-update"
)
async def category_update(session: DBAsyncSession, body: CategoryUpdateDTO, pk: CategoryID):
    obj = await session.get(entity=Category, ident=pk)
    for k, v in body:
        setattr(obj, k, v)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="category name is not found")
    else:
        return CategoryDTO.model_validate(obj=obj)


@router.delete(
    path="/categories/{id}",
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[authenticate],
    name="category-delete"
)
async def category_delete(session: DBAsyncSession, pk: CategoryID):
    await session.execute(delete(Category).filter(and_(Category.id == pk)))
    await session.commit()
