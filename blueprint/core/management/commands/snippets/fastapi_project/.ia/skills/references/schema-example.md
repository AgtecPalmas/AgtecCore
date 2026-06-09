# Referência One-Shot: Schema

> Fonte real: `filiado/cargotrabalho/schemas.py`
> Padrão canônico de schemas Pydantic v2 do projeto AgtecCore.

## Padrão de schemas Pydantic v2

```python
import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core.schemas import FilterPagination


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NomeModeloBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)


class NomeModeloCreate(NomeModeloBase):
    pass


class NomeModeloUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)


class NomeModeloCreateResponse(ORMBase):
    id: UUID


class NomeModeloInDBBase(ORMBase, NomeModeloBase):
    id: UUID
    deleted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class NomeModelo(NomeModeloInDBBase):
    pass


class NomeModeloInDB(NomeModeloInDBBase):
    pass


class NomeModeloSearchFilter(FilterPagination):
    search: Optional[str] = Field(
        None,
        min_length=2,
        description="Busca geral pelo nome",
    )
    nome: Optional[str] = Field(
        None,
        min_length=2,
        description="Filtra por nome específico",
    )
```

## Hierarquia obrigatória

```bash
NomeModeloBase          ← campos comuns
  ├── NomeModeloCreate  ← herda Base, campos obrigatórios
  ├── NomeModeloUpdate  ← todos os campos Optional
  └── NomeModeloInDBBase (ORMBase + Base)
        ├── NomeModelo  ← schema de resposta padrão
        └── NomeModeloInDB
```

## Regras obrigatórias (schema)

- `ORMBase` com `model_config = ConfigDict(from_attributes=True)` em todos os schemas de resposta
- `NomeModeloUpdate`: todos os campos `Optional[T] = None`
- `NomeModeloInDBBase` inclui: `id`, `deleted`, `created_at`, `updated_at` — nunca redeclarar no model SQLAlchemy
- `NomeModeloSearchFilter` herda de `FilterPagination` (paginação + filtros)
- Usar `Field(...)` para validações obrigatórias; `Field(None, ...)` para opcionais
- Pydantic v2: usar `field_validator` / `model_validator` (nunca `@validator` do v1)
