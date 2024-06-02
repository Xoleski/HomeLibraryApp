
from fastapi import APIRouter
from sqlalchemy import select, asc, desc
from starlette.status import (HTTP_200_OK)

from api.annotated_types import PageQuery, PageNumberQuery, SortByQuery, UsersSortAttrQuery
from src.database import (User)
from src.dependencies.database_session import (DBAsyncSession)
from src.types import UserDTO

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
