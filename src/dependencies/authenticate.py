from typing import Annotated

from fastapi import Depends, Header, HTTPException
from fastapi.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from src.database import User
from src.dependencies.database_session import DBAsyncSession
from src.settings import jwt_manager

__all__ = [
    "authenticate",
    "get_current_user",
    "CurrentUser",
]


async def _authenticate(
        request: Request,
        db_session: DBAsyncSession,
        autharization: str = Header(default=None)) -> User:
    if autharization is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN
        )

    payload = jwt_manager.verify_access_token(token=autharization)
    user = await db_session.get(entity=User, ident=payload.get("sub"))
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND
        )

    request.scope["state"]["user"] = user
    return user

authenticate = Depends(dependency=_authenticate)


async def get_current_user(request: Request) -> User:
    return request.scope["state"]["user"]


CurrentUser = Annotated[User, Depends(dependency=get_current_user)]
