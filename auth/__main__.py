from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY
    )
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from src.dependencies.authenticate import authenticate
from src.dependencies.database_session import DBAsyncSession
from src.database import User
from src.exception_handlers import request_validation_exception_handler
from src.types import UserRegisterDTO, UserLoginDTO, TokenPairDTO, RefreshTokenDTO, UserDTO
from src.utils.password import create_password_hash, verify_password

from src.settings import jwt_manager, settings
from auth.google import fetch_google_user_info

app = FastAPI()
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=("*",),
    allow_methods=("*",),
    allow_headers=("*",),
    allow_credentials=True
)
app.add_middleware(
    middleware_class=ProxyHeadersMiddleware,
    trusted_hosts=("*", )
)
app.add_exception_handler(
    exc_class_or_status_code=RequestValidationError,
    handler=request_validation_exception_handler  # noqa
)


GOOGLE_LOGIN_URL = (
    f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID.get_secret_value()}"
    f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
)


@app.post(
    path="/api/auth/register",
    status_code=HTTP_201_CREATED,
    name="auth-register"
)
async def register(db_session: DBAsyncSession, data: UserRegisterDTO):
    user = await db_session.scalar(
        select(User).filter(User.email == data.email)
    )
    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"user with email={data.email} exists"
        )

    user = User(
        email=data.email,
        password=create_password_hash(password=data.password)
    )
    db_session.add(instance=user)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="invalid data"
        )
    else:
        return {"status": "success"}


@app.post(
    path="/api/auth/login",
    response_model=TokenPairDTO,
)
async def login(db_session: DBAsyncSession, data: UserLoginDTO):
    user = await db_session.scalar(
        statement=select(User)
        .filter(and_(User.email == data.email))
    )
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"user with email={data.email} not found"
    )
    if not verify_password(password=data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="invalid password"
        )

# можно еще проверить, например, не забанен ли пользователь

    return jwt_manager.create_pair_token(
        payload={
            "sub": user.id
        }
    )


@app.post(
    path="/api/auth/refresh",
    response_model=TokenPairDTO
)
async def refresh(db_session: DBAsyncSession, data: RefreshTokenDTO):
    payload = jwt_manager.verify_refresh_token(token=data.refresh_token)
    user = await db_session.get(entity=User, ident=payload.get("sub"))
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    return jwt_manager.create_pair_token(
        payload=payload
    )


# @app.get(
#     path="/api/me",
#     dependencies=[authenticate]
# )
# async def me(request: Request):
#     user = request.scope["state"].get("user")
#     return UserDTO.model_validate(obj=user)


@app.get(
    path="/api/auth/login/google",
    response_class=RedirectResponse
)
async def login_google():
    return RedirectResponse(url=GOOGLE_LOGIN_URL)


@app.get(
    path="/api/auth/google",
    response_model=TokenPairDTO,
)
async def auth_google(db_session: DBAsyncSession, code: str = Query()):
    try:
        user_info = await fetch_google_user_info(code=code)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"{e}")
    else:
        user = await db_session.scalar(
            statement=select(User).filter(and_(User.email == user_info.get("email")))
        )
        if user is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND
            )
        return jwt_manager.create_pair_token(payload={"sub": user.id})


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host=settings.HOST,
        port=settings.PORT
    )
