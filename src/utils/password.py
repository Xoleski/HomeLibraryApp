from bcrypt import gensalt, checkpw, hashpw

__all__ = [
    "create_password_hash",
    "verify_password",
]


def create_password_hash(password: str) -> str:
    salt = gensalt(rounds=12)
    return hashpw(password=password.encode(), salt=salt).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return checkpw(password=password.encode(), hashed_password=hashed_password.encode())


