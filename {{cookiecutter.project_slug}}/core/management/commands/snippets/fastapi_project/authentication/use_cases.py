from typing import Any, Dict, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from authentication.models import ContentType, Group, Permission, User
from authentication.schemas import (
    GroupCreate,
    GroupUpdate,
    PermissionCreate,
    PermissionUpdate,
    UserCreate,
    UserUpdate,
)
from core.database import AsyncDBDependency
from core.exceptions import GenericException
from core.security import get_password_hash, verify_password
from core.use_cases import BaseUseCases

from core.redis import redis_service



class UserAuthUseCases(BaseUseCases[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncDBDependency, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar()

    async def get_by_username(
        self, db: AsyncDBDependency, username: str
    ) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar()

    async def get_by_id(self, db: AsyncDBDependency, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = await db.execute(query)
        return result.scalar()

    async def create(self, db: AsyncDBDependency, data: UserCreate) -> User:
        _query = select(Group).where(Group.id.in_(data.groups))
        _result = await db.execute(_query)
        _result = _result.scalars().all()

        if len(_result) != len(data.groups):
            raise GenericException(
                error="One or more groups does not exist in the system.",
            )
        
        data.groups = _result

        return await super().create(db, data)

    async def update(
        self,
        db: AsyncDBDependency,
        objeto: User,
        data: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        _query = select(Group).where(Group.id.in_(data.groups))
        _result = await db.execute(_query)
        _result = _result.scalars().all()

        if len(_result) != len(data.groups):
            raise GenericException(
                error="One or more groups does not exist in the system.",
            )
        
        data.groups = _result

        if data.password:
            data.password = get_password_hash(data.password)

        return await super().update(db, objeto, data)

    async def authenticate(
        self, db: Session, username: str, password: str
    ) -> Optional[User]:
        current_user = await self.get_by_username(db, username)

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
    async def check_permission_db(
        self, db: AsyncDBDependency, content_type_id: int, codename: str
    ) -> bool:
        content_type = select(ContentType).where(ContentType.id == content_type_id)
        result = await db.execute(content_type)
        result = result.scalar()

        if not result:
            raise GenericException(
                error=f"Content type with id {content_type_id} does not exist in the system.",
            )

        query = select(Permission).where(
            Permission.content_type_id == content_type_id,
            Permission.codename == codename,
        )
        result = await db.execute(query)
        result = result.scalar()

        if result:
            raise GenericException(
                error=f"Permission with codename {codename} and content_type_id {content_type_id} already exists in the system.",
            )

    async def create(self, db: AsyncDBDependency, data: PermissionCreate) -> Permission:
        await self.check_permission_db(
            db, content_type_id=data.content_type_id, codename=data.codename
        )

        return await super().create(db, data)

    async def update(
        self,
        db: AsyncDBDependency,
        objeto: Permission,
        data: Union[PermissionUpdate, Dict[str, Any]],
    ) -> Permission:
        await self.check_permission_db(db, data.content_type_id, data.codename)

        return await super().update(db, objeto, data)


permission = PermissionAuthUseCases(Permission)


class GroupAuthUseCases(BaseUseCases[Group, GroupCreate, GroupUpdate]):
    async def get_by_name(self, db: AsyncDBDependency, name: str) -> Optional[Group]:
        query = select(Group).where(Group.name == name)
        result = await db.execute(query)
        return result.scalar()

    async def create(self, db: AsyncDBDependency, data: GroupCreate) -> Group:
        if await self.get_by_name(db, data.name):
            raise GenericException(
                error=f"Group with name {data.name} already exists in the system.",
            )

        _query = select(Permission).where(Permission.id.in_(data.permissions))
        _result = await db.execute(_query)
        _result = _result.scalars().all()

        if len(_result) != len(data.permissions):
            raise GenericException(
                error="One or more permissions does not exist in the system.",
            )
        
        data.permissions = _result

        return await super().create(db, data)

    async def update(
        self, db: AsyncDBDependency, objeto: Group, data: GroupUpdate
    ) -> Group:
        if await self.get_by_name(db, data.name):
            raise GenericException(
                error=f"Group with name {data.name} already exists in the system.",
            )
        _query = select(Permission).where(Permission.id.in_(data.permissions))
        _result = await db.execute(_query)
        _result = _result.scalars().all()

        if len(_result) != len(data.permissions):
            raise GenericException(
                error="One or more permissions does not exist in the system.",
            )
        
        data.permissions = _result

        return await super().update(db, objeto, data)


group = GroupAuthUseCases(Group)
