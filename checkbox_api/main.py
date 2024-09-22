from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from piccolo_api.csrf.middleware import CSRFMiddleware
from sqlalchemy.ext.asyncio import (
	create_async_engine,
	AsyncSession, async_sessionmaker
)
from sqlmodel import SQLModel

from checkbox_api.config import POSTGRES_CONFIG, APP_CONFIG, RunModes
from checkbox_api.features.receipt.api.router import router as receipt_router


class CheckBoxFastAPI(FastAPI):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession] | None:
        return self._sessionmaker

    @sessionmaker.setter
    def sessionmaker(self, value: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = value


@asynccontextmanager
async def app_lifespan(
        _app: CheckBoxFastAPI
) -> AsyncGenerator[None]:
    _engine = create_async_engine(
        url=str(POSTGRES_CONFIG.db_uri),
        echo=True
    )
    _app.sessionmaker = async_sessionmaker(
        bind=_engine.engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = CheckBoxFastAPI(lifespan=app_lifespan)

app_router = APIRouter(prefix='/api/v1/')

app_router.include_router(
    router=receipt_router
)

app.include_router(
    app_router
)

if APP_CONFIG.run_mode == RunModes.PRODUCTION:
    app.add_middleware(CSRFMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=APP_CONFIG.allowed_hosts
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=APP_CONFIG.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
