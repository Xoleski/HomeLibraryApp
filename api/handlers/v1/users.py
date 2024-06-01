from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, asc, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from starlette.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
)

from api.annotated_types import PageQuery, PageNumberQuery, BookPrivateSortAttrQuery, SortByQuery, UsersSortAttrQuery
from src.database import (BookPrivate,
                          GeneralBook,
                          Tag,
                          BookPrivateTag,
                          User)
from src.dependencies.authenticate import authenticate
from src.dependencies.database_session import (
    DBAsyncSession
)
from src.types import GeneralBookExtendedDTO, BookPrivateDTO, UserDTO

from sqlalchemy import event

from src.types.book_private import BookPrivateListDTO, BookPrivateCreateDTO

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