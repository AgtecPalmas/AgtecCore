import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

"""
Arquivo com os  models da app de autenticação

- É configurado o nome da tabela, colunas e relacionamentos
"""


class Base(DeclarativeBase):
    __abstract__ = True


class ContentType(Base):
    __tablename__ = "django_content_type"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    app_label: Mapped[str] = mapped_column(sa.String, nullable=False)
    model: Mapped[str] = mapped_column(sa.String, nullable=False)


class Permission(Base):
    __tablename__ = "auth_permission"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    content_type_id: Mapped[int] = mapped_column(
        sa.ForeignKey("django_content_type.id"), nullable=False
    )
    codename: Mapped[str] = mapped_column(sa.String, nullable=False)
    contentType = relationship("ContentType")


group_permission = sa.Table(
    "auth_group_permissions",
    Base.metadata,
    sa.Column("group_id", sa.ForeignKey("auth_group.id"), primary_key=True),
    sa.Column("permission_id", sa.ForeignKey("auth_permission.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "auth_group"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    permissions = relationship("Permission", secondary=group_permission)


user_group = sa.Table(
    "auth_user_groups",
    Base.metadata,
    sa.Column("group_id", sa.ForeignKey("auth_group.id"), primary_key=True),
    sa.Column("user_id", sa.ForeignKey("auth_user.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(sa.String)
    last_name: Mapped[str] = mapped_column(sa.String)
    username: Mapped[str] = mapped_column(sa.String, nullable=False)
    email: Mapped[str] = mapped_column(sa.String, unique=True, index=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    groups = relationship("Group", secondary=user_group)
    is_staff = mapped_column(sa.Boolean, default=False)
    date_joined = mapped_column(sa.DateTime, default=datetime.datetime.now)
