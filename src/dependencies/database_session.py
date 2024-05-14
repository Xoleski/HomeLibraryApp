from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import async_db_sessionmaker


async def create_db_session():
    async with async_db_sessionmaker() as session:  # type: AsyncSession
        yield session

DBAsyncSession = Annotated[AsyncSession, Depends(dependency=create_db_session)]
