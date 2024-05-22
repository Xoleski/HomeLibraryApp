from celery.result import AsyncResult
from sqlite3 import IntegrityError

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
    SortByQuery
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


router = APIRouter(tags=["BookPrivate"])