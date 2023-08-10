import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from .database import Base
from .schemas import PaginationBase

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseUseCases(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        query = db.query(self.model).filter(self.model.id == id)
        if hasattr(self.model, "deleted"):
            query = query.filter(self.model.deleted == False)
        return query.first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 25
    ) -> List[ModelType]:
        query = db.query(self.model)
        if hasattr(self.model, "deleted"):
            query = query.filter(self.model.deleted == False)
        return query.offset(skip).limit(limit).all()

    def get_paginate(
        self, db: Session, *, request: Request, offset: int = 0, limit: int = 25
    ) -> PaginationBase:
        query = db.query(self.model)
        if hasattr(self.model, "deleted"):
            query = query.filter(self.model.deleted == False)
        url = "https://" if request.url.is_secure else "http://"
        url = f"{url}{request.url.hostname}"
        if request.url.port != 80:
            url = f"{url}:{request.url.port}"
        url += request.url.path
        total = query.count()

        hasNextPage = int(total / limit) > offset
        hasPreviousPage = total > limit and int(total / limit) <= offset

        data = PaginationBase()
        data.count = total
        data.results = query.offset(offset).limit(limit).all()
        data.next = (
            f"{url}?offset={offset + limit}&limit={limit}" if hasNextPage else None
        )
        data.previous = (
            f"{url}?offset={offset - limit}&limit={limit}" if hasPreviousPage else None
        )

        return data

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        return self._add_commit_and_refresh(db, db_obj)

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["updated_on"] = datetime.datetime.now()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return self._add_commit_and_refresh(db, db_obj)

    def remove(self, db: Session, *, id: int) -> ModelType:
        db_obj = db.query(self.model).get(id)
        db_obj.deleted = True
        return self._add_commit_and_refresh(db, db_obj)

    def _add_commit_and_refresh(self, db, db_obj):
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def hard_remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_paginate_django_user(
        self, db: Session, request: Request, id: Any
    ) -> ModelType:
        try:
            query = db.query(self.model).filter(self.model.id == id)
            if hasattr(self.model, "deleted"):
                query = query.filter(self.model.deleted == False)
            query = query.first()

            url = "https://" if request.url.is_secure else "http://"
            url = f"{url}{request.url.hostname}"
            if request.url.port != 80:
                url = f"{url}:{request.url.port}"
            query.django_user = (
                f"{url}/api/v1/authentication/users/{query.django_user_id}"
            )
            return query
        except DataError:
            raise HTTPException(
                status_code=404, detail="Item usuario inexistente no sistema"
            )
        except Exception as exception:
            raise exception

    def get_multi_paginate_django_user(
        self, db: Session, *, request: Request, offset: int = 0, limit: int = 25
    ) -> ModelType:
        usuarios = db.query(self.model)
        if hasattr(self.model, "deleted"):
            usuarios = usuarios.filter(self.model.deleted == False)
        usuarios = usuarios.offset(offset).limit(limit).all()

        url = "https://" if request.url.is_secure else "http://"
        url = f"{url}{request.url.hostname}"
        if request.url.port != 80:
            url = f"{url}:{request.url.port}"

        for usuario in usuarios:
            usuario.django_user = (
                f"{url}/api/v1/authentication/users/{usuario.django_user_id}"
            )

        return usuarios
