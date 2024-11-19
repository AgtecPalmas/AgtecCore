"""
===================================================================================================
Atenção:
===================================================================================================

Arquivo gerado pelo Build FastAPI.

Esse arquivo de configuração de testes
utiliza o testcontainers para criar um container do Postgres e rodar os testes
"""

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from core.database import get_async_db, Base
from main import app

BASE_URL = 'https://test/api/v1/'


# Fixture para o container do Postgres
@pytest_asyncio.fixture
def postgres_container():
    with PostgresContainer('postgres:16', driver='asyncpg') as postgres:
        yield postgres


# Fixture para a sessão assíncrona do SQLAlchemy
@pytest_asyncio.fixture
async def async_session(postgres_container):
    async_db_url = postgres_container.get_connection_url().replace(
        "postgresql://", "postgresql+asyncpg://")
    async_engine = create_async_engine(
        async_db_url, pool_pre_ping=True, echo=True
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as as_session:
        yield as_session


# Fixture para o cliente de teste do FastAPI
@pytest_asyncio.fixture
async def async_client(async_session):
    app.dependency_overrides[get_async_db] = lambda: async_session  # noqa
    _transport = ASGITransport(app=app)  # noqa

    async with AsyncClient(transport=_transport, base_url=BASE_URL) as client:
        yield client

    app.dependency_overrides.clear()  # noqa
