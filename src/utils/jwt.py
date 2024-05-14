from datetime import timedelta, datetime, UTC

from typing import Any

from fastapi import HTTPException
from jwt import (
    encode,
    decode,
    ExpiredSignatureError,
    InvalidTokenError,
    PyJWTError,
    InvalidAlgorithmError
)
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

__all__ =[
    "JWTManager",
]


class JWTManager(object):

    def __init__(
            self,
            jwt_access_secret_key: str,
            jwt_refresh_secret_key: str,
            jwt_access_exp: timedelta,
            jwt_refresh_exp: timedelta,
            jwt_access_algorithm: str,
            jwt_refresh_algorithm: str,
            token_type: str,
    ) -> None:
        self.__jwt_access_secret_key = jwt_access_secret_key
        self.__jwt_refresh_secret_key = jwt_refresh_secret_key
        self.jwt_access_exp = jwt_access_exp
        self.jwt_refresh_exp = jwt_refresh_exp
        self.jwt_access_algorithm = jwt_access_algorithm
        self.jwt_refresh_algorithm = jwt_refresh_algorithm
        self.token_type = token_type

    @staticmethod
    def create_token(
            payload: dict[str, Any],
            secret_key: str,
            algorithm: str,
            expire: timedelta = None
    ) -> str:
        if expire is not None:
            payload["exp"] = datetime.now(tz=UTC) + expire

        return encode(
            payload=payload,
            key=secret_key,
            algorithm=algorithm
        )

    def create_access_token(self, payload: dict[str, Any]) -> str:
        return self.create_token(
            payload=payload,
            secret_key=self.__jwt_access_secret_key,
            algorithm=self.jwt_access_algorithm,
            expire=self.jwt_access_exp
        )

    def create_refresh_token(self, payload: dict[str, Any]) -> str:
        return self.create_token(
            payload=payload,
            secret_key=self.__jwt_refresh_secret_key,
            algorithm=self.jwt_refresh_algorithm,
            expire=self.jwt_refresh_exp
        )

    def create_pair_token(self, payload: dict[str, Any]) -> dict[str, str]:
        return {
            "access_token": self.create_access_token(payload=payload),
            "refresh_token": self.create_refresh_token(payload=payload),
            "token_type": self.token_type
        }

    @staticmethod
    def verify_token(token: str, secret_key: str, algorithm: str) -> dict:
        try:
            return decode(
                jwt=token,
                key=secret_key,
                algorithms=[algorithm]
            )
        # except InvalidAlgorithmError:
        #     raise HTTPException(
        #         status_code=HTTP_400_BAD_REQUEST,
        #         detail="invalid token type",
        #         headers={
        #             "WWW-Authenticate": "invalid token type"
        #         }
        #     )

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="token has expired",
                headers={
                    "WWW-Authenticate": "token has expired"
                }
            )

        except PyJWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="token invalid",
                headers={
                    "WWW-Authenticate": "token invalid"
                }
            )

    def verify_access_token(self, token: str) -> dict:
        if not token.startswith(f"{self.token_type} "):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid token type",
                headers={
                    "WWW-Authenticate": "invalid token type"
                }
            )

        token = token.removeprefix(f"{self.token_type} ")
        return self.verify_token(
            token=token,
            secret_key=self.__jwt_access_secret_key,
            algorithm=self.jwt_access_algorithm
        )

    def verify_refresh_token(self, token: str) -> dict:
        return self.verify_token(
            token=token,
            secret_key=self.__jwt_refresh_secret_key,
            algorithm=self.jwt_refresh_algorithm
        )



