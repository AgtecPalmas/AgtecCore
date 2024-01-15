from typing import Any, Dict, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from authentication.models import Group, Permission, User
from authentication.schemas import (
    GroupCreate,
    GroupUpdate,
    PermissionCreate,
    PermissionUpdate,
    UserCreate,
    UserUpdate,
)
from core.security import get_password_hash, verify_password
from core.use_cases import BaseUseCases


class UserAuthUseCases(BaseUseCases[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar()

    async def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar()

    async def get_by_id(self, db: Session, *, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = await db.execute(query)
        return result.scalar()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            username=obj_in.username,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
        )
        if hasattr(obj_in, "groups"):
            groups = db.query(Group).filter(Group.id.in_(obj_in.groups)).all()
            db_obj.groups = groups
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = password
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if "groups" in update_data:
            db_obj.groups.clear()
            groups = db.query(Group).filter(Group.id.in_(obj_in.groups)).all()
            db_obj.groups = groups
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        current_user = await self.get_by_username(db, username=username)
        if not current_user:
            return None
        if not verify_password(password, current_user.password):
            return None
        return current_user

    def is_active(self, current_user: User) -> bool:
        return current_user.is_active

    def is_superuser(self, current_user: User) -> bool:
        return current_user.is_superuser


user = UserAuthUseCases(User)


class PermissionAuthUseCases(
    BaseUseCases[Permission, PermissionCreate, PermissionUpdate]
):
    pass


permission = PermissionAuthUseCases(Permission)


class GroupAuthUseCases(BaseUseCases[Group, GroupCreate, GroupUpdate]):
    def create(self, db: Session, *, obj_in: GroupCreate) -> Group:
        db_obj = Group(name=obj_in.name)
        permissions = (
            db.query(Permission).filter(Permission.id.in_(obj_in.permissions)).all()
        )
        db_obj.permissions = permissions
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Group, obj_in: GroupUpdate) -> Group:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.permissions.clear()
        permissions = (
            db.query(Permission).filter(Permission.id.in_(obj_in.permissions)).all()
        )
        db_obj.permissions = permissions
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


group = GroupAuthUseCases(Group)
