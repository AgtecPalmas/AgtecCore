# Referência One-Shot: Router

> Fonte real: `filiado/cargotrabalho/routers.py`
> Padrão canônico de router FastAPI do projeto AgtecCore.

## Padrão de router com permissões

```python
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status

from authentication import security
from core.database import AsyncDBDependency
from core.schemas import PaginationBase

from . import schemas
from .use_cases import nome_modulo as use_cases

router = APIRouter()

# Constantes de permissão (topo do arquivo, antes dos endpoints)
GET_DEPENDENCY    = Depends(security.has_permission("modulo.view_modelo"))
CREATE_DEPENDENCY = Depends(security.has_permission("modulo.add_modelo"))
UPDATE_DEPENDENCY = Depends(security.has_permission("modulo.change_modelo"))
DELETE_DEPENDENCY = Depends(security.has_permission("modulo.delete_modelo"))

MODEL_NAME   = "nome_do_model"
ROUTE_PREFIX = "/nome-do-modulo"

model_router = APIRouter(
    prefix=ROUTE_PREFIX,
    tags=["nome-do-modulo"],
)


@model_router.get(
    "/fetch-paginated/",
    response_model=PaginationBase,
    summary="Lista registros paginados",
)
async def fetch_paginated(
    request: Request,
    db: AsyncDBDependency,
    usuario: security.CurrentUserByTokenDependency,
    offset: int = 0,
    limit: int = 25,
    _: Any = GET_DEPENDENCY,
) -> Any:
    return await use_cases.get_paginate(
        db,
        request=request,
        offset=offset,
        limit=limit,
        model_pydantic=schemas.NomeModelo,
    )


@model_router.post(
    "/create/",
    response_model=schemas.NomeModeloCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo registro",
)
async def create(
    db: AsyncDBDependency,
    usuario: security.CurrentUserByTokenDependency,
    payload: schemas.NomeModeloCreate,
    _: Any = CREATE_DEPENDENCY,
) -> Any:
    return await use_cases.create(db, obj_in=payload)


@model_router.put(
    "/update/{item_id}/",
    response_model=schemas.NomeModeloCreateResponse,
    summary="Atualiza um registro existente",
)
async def update(
    db: AsyncDBDependency,
    usuario: security.CurrentUserByTokenDependency,
    item_id: UUID,
    payload: schemas.NomeModeloUpdate,
    _: Any = UPDATE_DEPENDENCY,
) -> Any:
    return await use_cases.update(db, item_id=item_id, obj_in=payload)


@model_router.delete(
    "/delete/{item_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove (soft delete) um registro",
)
async def delete(
    db: AsyncDBDependency,
    usuario: security.CurrentUserByTokenDependency,
    item_id: UUID,
    _: Any = DELETE_DEPENDENCY,
) -> None:
    await use_cases.delete(db, item_id=item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

## Regras obrigatórias (router)

- `RULE-ARCH-001`: sem lógica de negócio no router — delegar tudo para `use_cases`
- `RULE-ARCH-002`: sem acesso direto ao DB — usar `AsyncDBDependency` via use_case
- `RULE-ROUTE-001`: prefixo `/api/v1/` + kebab-case
- Constantes de permissão sempre no topo do arquivo
- `usuario: security.CurrentUserByTokenDependency` obrigatório em todos os endpoints autenticados
