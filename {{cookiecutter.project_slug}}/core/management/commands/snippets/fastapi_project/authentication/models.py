import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Column,
    Table,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

"""
Arquivo com os  models da app de autenticação

- É configurado o nome da tabela, colunas e relacionamentos
"""



class ContentType(Base):
    __tablename__ = "django_content_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    app_label: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)


class Permission(Base):
    __tablename__ = "auth_permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    content_type_id: Mapped[int] = mapped_column(
        ForeignKey("django_content_type.id"), nullable=False
    )
    codename: Mapped[str] = mapped_column(String, nullable=False)
    contentType = relationship("ContentType")


group_permission = Table(
    "auth_group_permissions",
    Base.metadata,
    Column("group_id", ForeignKey("auth_group.id"), primary_key=True),
    Column("permission_id", ForeignKey("auth_permission.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "auth_group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    permissions = relationship("Permission", secondary=group_permission)


user_group = Table(
    "auth_user_groups",
    Base.metadata,
    Column("group_id", ForeignKey("auth_group.id"), primary_key=True),
    Column("user_id", ForeignKey("auth_user.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    groups = relationship("Group", secondary=user_group)
    is_staff = mapped_column(Boolean, default=False)
    date_joined = mapped_column(DateTime, default=datetime.datetime.now)
