from typing import Self

from pydantic import EmailStr, PositiveInt, model_validator

from .book_private import BookPrivateListDTO
from .annotated_types import PasswordStr

from .base import DTO

__all__ = [
    "UserRegisterDTO",
    "UserLoginDTO",
    "UserDTO",
    "UserBooksExtendedDTO",
]


class UserLoginDTO(DTO):
    email: EmailStr
    password: PasswordStr


class UserRegisterDTO(UserLoginDTO):
    confirm_password: PasswordStr

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("passwords dose not match")
        return self


class UserDTO(DTO):
    id: PositiveInt
    email: EmailStr


class UserBooksExtendedDTO(UserDTO):
    books_private: list[BookPrivateListDTO]
