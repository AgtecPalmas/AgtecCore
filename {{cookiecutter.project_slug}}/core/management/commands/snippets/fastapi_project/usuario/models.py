import sqlalchemy as sa
from authentication.models import User
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Usuario(Base):
    __tablename__ = "usuario_usuario"

    django_user_id: Mapped[int] = mapped_column(sa.ForeignKey(User.id), nullable=False)
    cpf: Mapped[str] = mapped_column(sa.String(11), nullable=True)
    nome: Mapped[str] = mapped_column(sa.String(300), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(254), nullable=False)
    telefone: Mapped[str] = mapped_column(sa.String(100), nullable=True)
    token: Mapped[str] = mapped_column(sa.String, nullable=True)
    firebase: Mapped[str] = mapped_column(sa.String, nullable=True)
    access_token: Mapped[str] = mapped_column(sa.String, nullable=True)
    id_token: Mapped[str] = mapped_column(sa.String, nullable=True)
    latitude: Mapped[float] = mapped_column(sa.Float, nullable=False, default=0.0)
    longitude: Mapped[float] = mapped_column(sa.Float, nullable=False, default=0.0)
    endereco: Mapped[str] = mapped_column(sa.String, nullable=True)
