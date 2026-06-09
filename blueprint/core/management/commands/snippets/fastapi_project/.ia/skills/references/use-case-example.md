# Referência One-Shot: Use Case

> Fonte real: `filiado/cargotrabalho/use_cases.py`
> Padrão canônico de use case FastAPI do projeto AgtecCore.

## Padrão de use case com BaseUseCases

```python
from uuid import UUID

from fastapi import Request
from sqlalchemy import select

from core.database import AsyncDBDependency
from core.schemas import PaginationBase
from core.use_cases import BaseUseCases

from .models import NomeModelo
from .schemas import NomeModelo as NomeModeloSchema
from .schemas import NomeModeloCreate, NomeModeloSearchFilter, NomeModeloUpdate


class NomeModeloUseCase(
    BaseUseCases[NomeModelo, NomeModeloCreate, NomeModeloUpdate]
):

    @staticmethod
    def _dump_model(item: NomeModelo) -> dict:
        return NomeModeloSchema.model_validate(item).model_dump()

    def _dump_model_for_response(self, item: NomeModelo) -> dict:
        return self._dump_model(item)

    @staticmethod
    def _default_query():
        return select(NomeModelo).where(NomeModelo.deleted.is_(False))

    async def fetch_by_campo(
        self,
        db: AsyncDBDependency,
        request: Request,
        campo_id: UUID,
        offset: int = 0,
        limit: int = 25,
    ) -> PaginationBase:
        query = (
            self._default_query()
            .where(NomeModelo.campo_id == campo_id)
            .order_by(NomeModelo.nome)
        )
        result = await db.execute(query.offset(offset).limit(limit))
        items = result.scalars().all()

        paginated_result = await self.get_paginated_from_query(
            db, query, request.url, offset, limit
        )
        paginated_result.results = [self._dump_model(i) for i in items]
        return paginated_result


# Instância singleton obrigatória ao final do arquivo
nome_modulo = NomeModeloUseCase(NomeModelo)
```

## Regras obrigatórias (use case)

- `RULE-ARCH-003`: use case deve herdar de `BaseUseCases[Model, CreateSchema, UpdateSchema]`
- Instância singleton **obrigatória** ao final do arquivo: `nome_modulo = NomeModeloUseCase(NomeModelo)`
- `RULE-ASYNC-001`: todos os métodos de I/O devem ser `async def`
- `_default_query()` sempre filtra `deleted.is_(False)`
- Use `model_validate()` (Pydantic v2), nunca `from_orm()`
