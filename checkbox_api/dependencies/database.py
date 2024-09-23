import multiprocessing
from asyncio import shield
from collections.abc import AsyncGenerator
from typing import Annotated

import fastapi
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import (
    AsyncSession
)

from checkbox_api.config import POSTGRES_CONFIG

engine = create_async_engine(
    url=str(POSTGRES_CONFIG.db_uri),
    echo=True
)


async def _get_session_maker() -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )


async def _get_db_session(
        *,
        sessionmaker: Annotated[async_sessionmaker, fastapi.Depends(_get_session_maker)]
) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await shield(session.rollback())
            logger = multiprocessing.get_logger()
            logger.exception(e)


DBSession = Annotated[
    AsyncSession,
    fastapi.Depends(_get_db_session)
]

__all__ = [
    'DBSession',
    'engine'
]
