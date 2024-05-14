from typing import Annotated

from pydantic import Field

__all__ = [
    "PasswordStr",
]

PasswordStr = Annotated[
    str,
    Field(
        pattern=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,72}$",
        min_length=8,
        max_length=72,
        title="User Password",
        examples=["VeryStrongPassword1!"]
    )
]
