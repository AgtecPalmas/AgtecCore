import datetime
from typing import Optional
from uuid import UUID

from authentication.schemas import User
from pydantic import BaseModel

# Usuario


class UsuarioBase(BaseModel):
    django_user_id: Optional[int]
    django_user: Optional[User]
    cpf: Optional[str]
    nome: str
    email: str
    telefone: Optional[str]
    token: Optional[str]
    firebase: Optional[str]
    access_token: Optional[str]
    id_token: Optional[str]
    latitude: float = 0.0
    longitude: float = 0.0
    endereco: Optional[str]


class UsuarioCreate(BaseModel):
    cpf: Optional[str]
    nome: str
    email: str
    telefone: Optional[str]
    token: Optional[str]
    firebase: Optional[str]
    access_token: Optional[str]
    id_token: Optional[str]
    latitude: float = 0.0
    longitude: float = 0.0
    endereco: Optional[str]


class UsuarioUpdate(UsuarioBase):
    pass


class UsuarioInDBBase(UsuarioBase):
    id: UUID
    deleted: bool
    created_on: datetime.datetime
    updated_on: datetime.datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Usuario(UsuarioInDBBase):
    pass


# Additional properties stored in DB
class UsuarioInDB(UsuarioInDBBase):
    pass
