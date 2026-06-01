---
name: escrever-testes
description: Escreve testes automatizados para o projeto Argus usando pytest, pytest-asyncio e TestContainers. Use quando o usuário pedir para criar testes, aumentar cobertura, escrever test cases, ou validar uma implementação. Também ativa automaticamente quando o contexto menciona "escrever testes", "criar testes", "test coverage" ou arquivos em tests/.
---

# Escrever Testes — Argus

# Objetivo
Criar e manter testes automatizados assíncronos para a camada FastAPI, cobrindo contratos HTTP, regras de domínio e regressões relevantes.

## Pré-requisitos

Antes de começar:
1. Ler `.ia/docs/testing/strategy.md` (estratégia e regras de teste do projeto)
2. Identificar o módulo a ser testado e seu prefixo de rota (`/api/v1/<modulo>/`)
3. Verificar se já existe pasta `tests/tests_<modulo>/`

## Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.

- Testes **sempre** assíncronos (`async def test_*`)
- Usar **TestContainers** para dependências (PostgreSQL, Redis) — nunca banco real
- Usar **fixtures** para setup/teardown
- Arquivos criados em `tests/tests_<modulo>/test_*.py`
- Sincronizar dependências com `rtk uv sync` antes de executar
- Docker **deve** estar rodando antes de executar qualquer teste
- Prefixo global de rotas: `/api/v1/`

## Estrutura de arquivo de teste

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_nomear_cenario(async_client: AsyncClient):
    # Arrange
    payload = {...}

    # Act
    response = await async_client.post("/api/v1/<modulo>/endpoint/", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["campo"] == valor_esperado
```

## Checklist de criação de testes

- [ ] Criar pasta `tests/tests_<modulo>/` se não existir
- [ ] Criar `tests/tests_<modulo>/test_<feature>.py`
- [ ] Cobrir: criação, leitura, atualização, exclusão (soft delete)
- [ ] Cobrir: validações de entrada inválida (400/422)
- [ ] Cobrir: acesso não autorizado (401/403) se aplicável
- [ ] Cobrir: paginação se o endpoint for paginado
- [ ] Verificar fixtures de autenticação disponíveis em `tests/conftest.py`
- [ ] Rodar `rtk task test` e confirmar que passam
- [ ] Em endpoints self-service de filiado, validar que a chamada nao envia `filiado_id`
- [ ] Se houver `dependency_overrides` de autenticacao, retornar `Usuario` real (nao objeto dummy)

## Fixtures comuns (verificar em tests/conftest.py)

```python
# Sessão de banco via TestContainer
@pytest.fixture
async def db_session(): ...

# Cliente HTTP autenticado
@pytest.fixture
async def async_client(): ...

# Usuário autenticado para testes
@pytest.fixture
async def authenticated_user(): ...
```

## Como executar antes de qualquer teste

```bash
# 1. Verificar se Docker está rodando
docker info

# 2. Sincronizar dependências
rtk uv sync

# 3. Executar testes
rtk task test
# ou para verbose:
rtk task test-verbose
```

## Para testes do módulo IA (argus_ia_agent)

- Arquivo em: `tests/tests_argus_ia_agent/test_<nome_modulo>_tool.py`
- Criar também: `argus_ia_agent/tests/<nome_modulo>_chat.http` para validação manual
- Referências: `argus_ia_agent/tests/chat_dev_filiado.http`

## Referências de código

- Estratégia: `.ia/docs/testing/strategy.md`
- Tests existentes: `tests/` (qualquer pasta `tests_*/`)
- Padrões de rotas: `.ia/docs/guides/patterns.md`
