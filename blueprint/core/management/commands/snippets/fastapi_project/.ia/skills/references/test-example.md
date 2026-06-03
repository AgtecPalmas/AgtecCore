# Referência One-Shot: Teste

> Fonte real: `tests/tests_usuario/test_usuario.py` + `tests/conftest.py`
> Padrão canônico de testes do projeto AgtecCore com pytest + TestContainers.

## Padrão de teste com TestContainers

```python
"""
Testes para os endpoints do módulo <NomeModulo>.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from <modulo>.<submodulo>.models import NomeModelo
from <modulo>.<submodulo>.use_cases import nome_modulo as use_cases


@pytest.mark.asyncio
async def test_fetch_paginated_empty(async_client: AsyncClient):
    response = await async_client.get("/api/v1/<modulo>/fetch-paginated/")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data and "results" in data
    assert data["count"] == 0


@pytest.mark.asyncio
async def test_create_nome_modulo(async_client: AsyncClient, async_session: AsyncSession):
    payload = {
        "nome": "Registro Teste",
        "descricao": "Descrição de teste",
    }
    response = await async_client.post("/api/v1/<modulo>/create/", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert "id" in created

    # Verificar no banco via session direta
    result = await async_session.execute(
        select(NomeModelo).where(NomeModelo.id == created["id"])
    )
    db_item = result.scalar_one_or_none()
    assert db_item is not None
    assert db_item.nome == "Registro Teste"


@pytest.mark.asyncio
async def test_update_nome_modulo(async_client: AsyncClient, async_session: AsyncSession):
    # Arrange: criar diretamente no banco
    item = NomeModelo(nome="Original")
    async_session.add(item)
    await async_session.commit()
    await async_session.refresh(item)

    # Act
    payload = {"nome": "Atualizado"}
    response = await async_client.put(f"/api/v1/<modulo>/update/{item.id}/", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(item.id)


@pytest.mark.asyncio
async def test_delete_nome_modulo(async_client: AsyncClient, async_session: AsyncSession):
    item = NomeModelo(nome="Para deletar")
    async_session.add(item)
    await async_session.commit()
    await async_session.refresh(item)

    response = await async_client.delete(f"/api/v1/<modulo>/delete/{item.id}/")
    assert response.status_code == 204

    # Verificar soft delete
    await async_session.refresh(item)
    assert item.deleted is True


@pytest.mark.asyncio
async def test_create_invalid_payload(async_client: AsyncClient):
    # Payload inválido — nome muito curto
    payload = {"nome": "A"}
    response = await async_client.post("/api/v1/<modulo>/create/", json=payload)
    assert response.status_code == 422
```

## Fixtures disponíveis em `tests/conftest.py`

| Fixture | Escopo | Descrição |
| --------- | -------- | ----------- |
| `postgres_container` | session | Container PostgreSQL (pgvector) |
| `db_url` | session | URL de conexão assíncrona |
| `create_tables` | session | Cria tabelas via `Base.metadata.create_all` |
| `async_session` | function | Sessão com SAVEPOINT (rollback automático) |
| `async_client` | function | `AsyncClient` com `ASGITransport` e `BASE_URL` |

## Regras obrigatórias (testes)

- `RULE-TEST-001`: testes assíncronos com `@pytest.mark.asyncio` + TestContainers
- `RULE-TEST-002`: arquivos em `tests/tests_<modulo>/test_<feature>.py`
- Docker deve estar rodando antes de executar: `docker info`
- Ativar venv: `source .venv/bin/activate`
- Sincronizar dependências: `uv sync`
- Executar: `task test`

## Cenários obrigatórios por endpoint CRUD

- [ ] Listagem paginada vazia
- [ ] Criação com payload válido + verificação no banco
- [ ] Atualização
- [ ] Deleção (soft delete) + verificação de `deleted=True`
- [ ] Payload inválido (422)
- [ ] Não autorizado (401/403) — quando aplicável
