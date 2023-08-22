import datetime
import uuid
from typing import Generator

from sqlalchemy import (
    create_engine,
    String,
    Boolean,
    DateTime,
)
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
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid.uuid4)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )
    updated_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    __name__: Mapped[str] = mapped_column(String)

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
