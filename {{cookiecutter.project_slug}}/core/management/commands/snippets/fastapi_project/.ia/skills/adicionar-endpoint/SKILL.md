---
name: adicionar-endpoint
description: Adiciona um novo endpoint FastAPI ao projeto Argus seguindo a arquitetura em camadas (router → use_case → crud). Use quando o usuário pedir para criar um endpoint, adicionar uma rota, implementar um CRUD, ou estender um módulo existente. Também ativa automaticamente quando o contexto menciona "novo endpoint", "nova rota", "criar endpoint" ou arquivos em módulos com routers.py.
---

# Adicionar Endpoint — FastAPI Argus

# Objetivo
Criar ou evoluir endpoints FastAPI seguindo o padrão modular do projeto, mantendo routers finos, contratos Pydantic claros e regras em use cases.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- Criar ou reutilizar task aprovada antes de implementar.
- Preservar a arquitetura router → use case → ORM.
- Não aceitar `filiado_id` em endpoints self-service de filiado autenticado.
- Registrar testes e impactos no artefato da task.

## Pré-requisitos

Antes de começar:
1. Ler `.ia/docs/guides/rules-catalog.md` (rules canônicas e `rule_id`)
2. Ler `.ia/docs/guides/patterns.md` (padrões obrigatórios do projeto)
3. Ler `.ia/docs/architecture/relatorio-arquitetural.md` (fonte de verdade)
4. Ler `.ia/docs/guides/regra-endpoint-filiado-autenticado.md` quando o endpoint envolver contexto de filiado logado
5. Identificar o módulo alvo e sua estrutura existente
6. Criar spec em `.ia/docs/specs/<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md` quando a mudança exigir design upfront
7. Criar task em `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md` referenciando a spec
8. **Aguardar aprovação antes de implementar**

## Arquitetura em camadas (obrigatória)

```
Router       → só orquestração, sem lógica de negócio
  ↓
Use Case     → toda a lógica de negócio (herda BaseUseCases)
  ↓
CRUD / ORM   → acesso ao banco via SQLAlchemy 2.x async
```

## Checklist de implementação

- [ ] Criar/atualizar schema em `<modulo>/schemas.py` (padrão Pydantic v2)
- [ ] Criar/atualizar model em `<modulo>/models.py` (herdar de `CoreBase`)
- [ ] Criar/atualizar use case em `<modulo>/use_cases.py` (herdar de `BaseUseCases`)
- [ ] Criar/atualizar router em `<modulo>/routers.py`
- [ ] Registrar router no agregador do módulo se necessário
- [ ] Criar testes em `tests/tests_<modulo>/test_<feature>.py`
- [ ] Seguir convenção de path: `/api/v1/<modulo>/<acao>/` (kebab-case, barra final)
- [ ] Se for endpoint self-service de filiado: nao aceitar `filiado_id` na assinatura HTTP
- [ ] Se for endpoint self-service de filiado: resolver `filiado` no use case via `get_filiado_by_auth_user`
- [ ] Atualizar spec Flutter com secao de/para quando houver remocao/ajuste de `filiado_id`

## Padrão de schemas (Pydantic v2)

```python
from pydantic import BaseModel
from typing import Optional
import uuid

class NomeModuloBase(BaseModel):
    campo: str

class NomeModuloCreate(NomeModuloBase):
    pass

class NomeModuloUpdate(NomeModuloBase):
    campo: Optional[str] = None

class NomeModuloInDBBase(NomeModuloBase):
    id: uuid.UUID
    deleted: bool
    created_at: datetime
    updated_at: datetime
    enabled: bool

    model_config = ConfigDict(from_attributes=True)
```

## Padrão de model (herdar CoreBase)

```python
from core.database import CoreBase
from sqlalchemy.orm import Mapped, mapped_column

class NomeModelo(CoreBase):
    __tablename__ = "nome_tabela"
    campo: Mapped[str] = mapped_column(nullable=False)
    # NÃO redeclarar: id, deleted, created_at, updated_at, enabled
```

## Padrão de use case (herdar BaseUseCases)

```python
from core.use_cases import BaseUseCases
from .models import NomeModelo
from .schemas import NomeModeloCreate, NomeModeloUpdate

class NomeModeloUseCase(BaseUseCases[NomeModelo, NomeModeloCreate, NomeModeloUpdate]):
    pass

# Singleton obrigatório ao fim do arquivo:
nome_modulo = NomeModeloUseCase(NomeModelo)
```

## Padrão de router com permissões

```python
from fastapi import APIRouter, Depends
from core import security
from core.schemas import AsyncDBDependency
from . import use_cases, schemas

router = APIRouter(prefix="/nome-modulo", tags=["NomeModulo"])

GET_DEPENDENCY = Depends(security.has_permission("modulo.view_modelo"))
CREATE_DEPENDENCY = Depends(security.has_permission("modulo.add_modelo"))
UPDATE_DEPENDENCY = Depends(security.has_permission("modulo.change_modelo"))
DELETE_DEPENDENCY = Depends(security.has_permission("modulo.delete_modelo"))

@router.get("/fetch-paginated/", dependencies=[GET_DEPENDENCY])
async def fetch_paginated(
    db: AsyncDBDependency,
    usuario: security.CurrentUserByTokenDependency,
    filters: schemas.NomeModeloSearchFilter = Depends(),
):
    return await use_cases.nome_modulo.get_paginated_from_query(db, filters)
```

## Convenções de rotas

- Prefixo global: `/api/v1/`
- Paths: kebab-case (ex.: `/fetch-paginated/`, `/fetch-by-id/`)
- Barra final (`/`): sempre presente no final do path
- Verbos: `fetch-paginated`, `fetch-by-*`, `search`, `create`, `update`, `delete`, `restore`

## Regra especifica para filiado autenticado

Para endpoints do proprio filiado logado:

- Router: `usuario: security.CurrentUserByTokenDependency`
- Nao receber `filiado_id` em query/body/path
- Use case resolve filiado internamente via `authentication.security.get_filiado_by_auth_user(...)`
- Se filiado nao existir, retornar erro de dominio apropriado

## Referências de código

- Padrões completos: `.ia/docs/guides/patterns.md`
- CoreBase: `core/database.py`
- BaseUseCases: `core/use_cases.py`
- Segurança/DI: `core/security.py`
- Módulo de referência: `usuario/`, `filiado/`
