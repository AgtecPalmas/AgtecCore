import datetime
import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, Request
from fastapi.datastructures import URL
from pydantic import BaseModel
from sqlalchemy import func, select

from core.database import AsyncDBDependency, CoreBase
from core.exceptions import InternalServerException, NotFoundException
from core.schemas import PaginationBase

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

    async def get(
        self, db: AsyncDBDependency, id: Any, deleted: bool = False
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)

        if hasattr(self.model, "deleted") and not deleted:
            query = query.where(self.model.deleted.is_(False))

        result = await db.execute(query)
        item = result.scalar()

        if not item:
            raise NotFoundException()

        return item

    async def get_multi(
        self, db: AsyncDBDependency, *, offset: int = 0, limit: int = 25
    ) -> List[ModelType]:
        self.__validate_limit_offset(limit, offset)

        if hasattr(self.model, "deleted"):
            query = select(self.model).where(self.model.deleted.is_(False))

        else:
            query = select(self.model)

        result = await db.execute(query.offset(offset).limit(limit))
        return result.scalars().all()

    @staticmethod
    def __get_pages(url: URL, total: int, limit: int, offset: int) -> tuple:
        url = url._url.split("?")[0]
        _next = limit + offset < total
        _previous = offset > 0

        next_page, previous_page = None, None
        max_offset_previous = total - (total % limit)

        if _next:
            next_page = f"{url}?offset={offset + limit}&limit={limit}"

        if _previous and offset != 0:
            if offset <= max_offset_previous:
                previous_page = f"{url}?offset={offset - limit}&limit={limit}"

            else:
                previous_page = f"{url}?offset={max_offset_previous}&limit={limit}"

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
                detail="Offset must be greater than 0 and limit must be greater than or equal to 0",
            )
        return

    async def get_paginate(
        self,
        db: AsyncDBDependency,
        *,
        query: select = None,
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

        results = await db.execute(query.offset(offset).limit(limit))
        results = results.scalars().all()
        results = self.__load_results(
            results,
            model_pydantic,
        )

        total = select(func.count()).select_from(query)
        total = await db.execute(total)
        total = total.scalar()

        next_page, previous_page = self.__get_pages(request.url, total, limit, offset)

        return PaginationBase(
            count=total, next=next_page, previous=previous_page, results=results
        )

    async def create(self, db: AsyncDBDependency, data: CreateSchemaType) -> ModelType:
        data = self.model(**data.model_dump())
        return await self._add_commit_and_refresh(db, data)

    async def update(
        self,
        db: AsyncDBDependency,
        objeto: ModelType,
        data: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        data = data.model_dump(exclude_unset=True)

        if hasattr(self.model, "updated_on"):
            data["updated_on"] = datetime.datetime.now()

        for field in data:
            setattr(objeto, field, data[field])

        return await self._add_commit_and_refresh(db, objeto)

    async def delete(self, db: AsyncDBDependency, id: int) -> ModelType:
        db_obj = await self.get(db, id=id)

        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Item {self.model.__name__} inexistente no sistema",
            )

        if not hasattr(self.model, "deleted"):
            return await self.hard_remove(db, id=id)

        db_obj.deleted = True
        db_obj.enabled = False
        return await self._add_commit_and_refresh(db, db_obj)

    async def restore(self, db: AsyncDBDependency, model: ModelType) -> ModelType:
        if not hasattr(self.model, "deleted"):
            raise HTTPException(
                status_code=400,
                detail=f"Item {self.model.__name__} não possui soft delete",
            )

        model.deleted = False
        model.enabled = True
        model.updated_on = datetime.datetime.now()
        return await self._add_commit_and_refresh(db, model)

    async def _add_commit_and_refresh(self, db, db_obj):
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

        except Exception as e:
            await db.rollback()
            raise InternalServerException() from e

    async def hard_remove(self, db: AsyncDBDependency, *, id: int) -> ModelType:
        item = await self.get(db, id=id)
        try:
            await db.delete(item)
            await db.commit()

        except Exception as e:
            await db.rollback()
            raise InternalServerException(
                error=f"Erro ao deletar permanentemente {self.model.__name__}"
            ) from e

        return item
