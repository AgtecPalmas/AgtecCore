import datetime
import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import CoreBase
from .schemas import PaginationBase

ModelType = TypeVar("ModelType", bound=CoreBase)
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
        if hasattr(self.model, "deleted"):
            query = select(self.model).where(
                self.model.id == id, self.model.deleted.is_(False)
            )

        else:
            query = select(self.model).where(self.model.id == id)

        return db.scalar(query)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 25
    ) -> List[ModelType]:
        if skip <= 0 or limit <= 0:
            raise HTTPException(
                status_code=400,
                detail="Skip and limit must be greater than 0",
            )

        if hasattr(self.model, "deleted"):
            query = select(self.model).where(self.model.deleted.is_(False))

        else:
            query = select(self.model)

        return db.scalars(query.offset(skip).limit(limit))

    def get_paginate(
        self,
        db: Session,
        *,
        request: Request,
        offset: int = 0,
        limit: int = 5,
        model_pydantic: Type[BaseModel] = None,
    ) -> PaginationBase:
        if offset < 0 or limit <= 0:
            raise HTTPException(
                status_code=400,
                detail="Offset must be greater than or equal to 0 and limit must be greater than 0",
            )

        if hasattr(self.model, "deleted"):
            query = select(self.model).where(self.model.deleted.is_(False))

        else:
            query = select(self.model)

        total = db.query(func.count()).select_from(query).scalar()
        results = db.scalars(query.offset(offset).limit(limit)).all()

        url = "https://" if request.url.is_secure else "http://"
        url = f"{url}{request.url.hostname}"

        if request.url.port != 80:
            url = f"{url}:{request.url.port}"

        url += request.url.path

        hasNextPage = int(total / limit) > offset
        hasPreviousPage = total > limit and int(total / limit) <= offset

        data = PaginationBase()
        data.count = total
        data.results = [
            json.loads(model_pydantic(**item.__dict__).model_dump_json())
            for item in results
        ]

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
        if hasattr(self.model, "deleted"):
            db_obj.deleted = True
        else:
            db.delete(db_obj)
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
