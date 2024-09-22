import multiprocessing
from asyncio import shield
from collections.abc import AsyncGenerator
from typing import Annotated

import fastapi
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import (
	AsyncSession
)
from starlette.requests import Request


async def _get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async_sessionmaker = request.app.state.sessionmaker
    async with async_sessionmaker() as session:
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
    'DBSession'
]
