from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager


from fastapi import FastAPI
from sqlmodel import SQLModel
from checkbox_api.dependencies.database import engine


@asynccontextmanager
async def app_lifespan(
    _app: FastAPI
) -> AsyncGenerator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
