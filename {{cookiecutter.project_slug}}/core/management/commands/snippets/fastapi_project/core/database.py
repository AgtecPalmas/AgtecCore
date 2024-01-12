import datetime
import uuid
from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import UUID, Boolean, DateTime, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    sessionmaker,
)

from .config import settings

"""
Arquivo responsável pelo banco de dados

- Model principal que será herdado pelos outros models de outras app
- Cria uma instância do banco e finaliza ao finalizar a transação
"""


class Base(DeclarativeBase):
    __abstract__ = True


class CoreBase(Base):
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )
    updated_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    __name__: Mapped[str] = mapped_column(String)
    __abstract__ = True

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


DB_ENGINE = settings.db_engine
DB_USER = settings.db_user
DB_PASSWORD = settings.db_password
DB_NAME = settings.db_name
DB_PORT = settings.db_port
DB_HOST = settings.db_host

# Default DB
SQLALCHEMY_DATABASE_URI: str = (
    f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Async DB
ASYNC_SQLALCHEMY_DATABASE_URI: str = (
    f"{DB_ENGINE}+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)


async def get_async_db() -> Generator:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()


ActiveAsyncSession = Depends(get_async_db)

AsyncDBDependency = Annotated[AsyncSession, ActiveAsyncSession]
