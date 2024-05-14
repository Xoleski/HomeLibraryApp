from datetime import timedelta
from pathlib import Path

from pydantic import PostgresDsn, SecretStr, HttpUrl, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.utils.jwt import JWTManager


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        frozen=True,
        # env_file=".env"
    )

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    HOST: str = "0.0.0.0"
    PORT: int = 80

    POSTGRES_URL: PostgresDsn
    JWT_ACCESS_SECRET_KEY: SecretStr
    JWT_REFRESH_SECRET_KEY: SecretStr
    JWT_ACCESS_ALGORITHM: str
    JWT_REFRESH_ALGORITHM: str
    JWT_ACCESS_EXP: timedelta
    JWT_REFRESH_EXP: timedelta
    JWT_TOKEN_TYPE: str
    JWT_AUTH_HEADER: str

    GOOGLE_CLIENT_ID: SecretStr
    GOOGLE_CLIENT_SECRET: SecretStr
    GOOGLE_REDIRECT_URI: HttpUrl

    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn
    CELERY_RESULT_EXTENDED: bool


settings = Settings()

async_db_engine = create_async_engine(url=settings.POSTGRES_URL.unicode_string())
async_db_sessionmaker = async_sessionmaker(bind=async_db_engine, expire_on_commit=False)
jwt_manager = JWTManager(
    jwt_access_secret_key=settings.JWT_ACCESS_SECRET_KEY.get_secret_value(),
    jwt_refresh_secret_key=settings.JWT_REFRESH_SECRET_KEY.get_secret_value(),
    jwt_access_exp=settings.JWT_ACCESS_EXP,
    jwt_refresh_exp=settings.JWT_REFRESH_EXP,
    jwt_access_algorithm=settings.JWT_ACCESS_ALGORITHM,
    jwt_refresh_algorithm=settings.JWT_REFRESH_ALGORITHM,
    token_type=settings.JWT_TOKEN_TYPE,
)
