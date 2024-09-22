import logging
from collections.abc import Sequence, AsyncGenerator
from contextlib import asynccontextmanager
from typing import (
    Generic
)

from sqlalchemy import ColumnExpressionArgument
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from checkbox_api.generics.pagination import PageParams, paginate_query
from checkbox_api.generics.type_vars import ModelTypeT


class LoggedSessionInstanceController(Generic[ModelTypeT]):
    __cls__: type[ModelTypeT]

    def __init__(
            self,
            *,
            session: AsyncSession,
            logger: logging.Logger
    ):
        self._db_session = session
        self._logger = logger

    @asynccontextmanager
    async def _transaction(self) -> AsyncGenerator[AsyncSessionTransaction]:
        async with self._db_session.begin() as transaction:
            try:
                yield transaction
            except SQLAlchemyError as error:
                await transaction.rollback()
                self._logger.exception(error)
            finally:
                await self._db_session.close()


class ReadInstanceController(
    LoggedSessionInstanceController[ModelTypeT]
):
    __cls__: type[ModelTypeT]

    async def read_one(
            self,
            *,
            filter_chain: tuple[ColumnExpressionArgument]
    ) -> ModelTypeT:
        async with self._transaction():
            results = await self._db_session.exec(
                select(self.__cls__).where(*filter_chain).limit(1)
            )
            return results.one()

    async def read_many(
            self,
            *,
            filter_chain: tuple[ColumnExpressionArgument],
            order_by_chain: tuple[ColumnExpressionArgument | str],
            page_params: PageParams
    ) -> Sequence[SQLModel]:
        async with self._transaction():
            paginated_query = await paginate_query(
                page_params=page_params,
                query=(
                    select(self.__cls__)
                    .where(*filter_chain)
                    .order_by(*order_by_chain)
                )
            )
            results = await self._db_session.exec(
                statement=paginated_query
            )
            return results.all()


class CreateInstanceController(
    LoggedSessionInstanceController[ModelTypeT]
):
    __cls__: type[ModelTypeT]

    async def upsert_one(
            self,
            *,
            instance: ModelTypeT
    ) -> ModelTypeT:
        async with self._transaction():
            self._db_session.add(instance)
            await self._db_session.flush()
            await self._db_session.refresh(instance)
            return instance

    async def insert_many(
            self,
            *,
            instances: Sequence[ModelTypeT]
    ) -> Sequence[ModelTypeT]:
        async with self._transaction():
            results = await self._db_session.scalars(
                insert(self.__cls__).returning(self.__cls__).values(instances)
            )
            await self._db_session.flush()
            return results.all()
