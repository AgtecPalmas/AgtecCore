from typing import Optional

from pydantic import BaseModel, EmailStr

"""
Arquivo com os schemas da app

- Nesse arquivo e possível configurar o schemas de entrada e saída de dados da api
"""


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    groups: Optional[list] = []


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    groups: Optional[list] = []


class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str


class UserToken(User):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


# Permisions
class PermissionBase(BaseModel):
    name: str
    content_type_id: int
    codename: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionInDBBase(PermissionBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Permission(PermissionInDBBase):
    pass


# Additional properties stored in DB
class PermissionInDB(PermissionInDBBase):
    pass


# Groups
class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    permissions: list[int] = []


class GroupUpdate(GroupBase):
    permissions: list[int] = []


class GroupInDBBase(GroupBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Group(GroupInDBBase):
    pass


# Additional properties stored in DB
class GroupInDB(GroupInDBBase):
    pass
