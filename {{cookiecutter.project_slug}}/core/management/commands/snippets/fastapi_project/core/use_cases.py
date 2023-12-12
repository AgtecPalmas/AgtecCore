import datetime
import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, Request
from fastapi.datastructures import URL
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

    @staticmethod
    def __get_pages(url: URL, total: int, limit: int, offset: int) -> tuple:
        hasNextPage = total // limit > offset
        hasPreviousPage = total > limit and total // limit <= offset

        url = url._url.split("?")[0]
        next_page = (
            f"{url}?offset={offset + limit}&limit={limit}" if hasNextPage else None
        )
        previous_page = (
            f"{url}?offset={offset - limit}&limit={limit}" if hasPreviousPage else None
        )
        return (next_page, previous_page)

    @staticmethod
    def __load_results(results: list, model_pydantic: Type[BaseModel]) -> list:
        return [
            json.loads(model_pydantic(**item.__dict__).model_dump_json())
            for item in results
        ]

    @staticmethod
    def __validate_limit_offset(limit: int, offset: int) -> None:
        if offset < 0 or limit <= 0:
            raise HTTPException(
                status_code=400,
                detail="Offset must be greater than or equal to 0 and limit must be greater than 0",
            )
        return

    def get_paginate(
        self,
        db: Session,
        query: select = None,
        *,
        request: Request,
        offset: int = 0,
        limit: int = 5,
        model_pydantic: Type[BaseModel] = None,
    ) -> PaginationBase:
        self.__validate_limit_offset(limit, offset)

        if query is None:
            query = select(self.model)
            if hasattr(self.model, "deleted"):
                query = select(self.model).where(self.model.deleted.is_(False))

        results = self.__load_results(
            db.scalars(query.offset(offset).limit(limit)).all(),
            model_pydantic,
        )
        total = db.query(func.count()).select_from(query).scalar()
        next_page, previous_page = self.__get_pages(request.url, total, limit, offset)

        return PaginationBase(
            count=total, next=next_page, previous=previous_page, results=results
        )

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
