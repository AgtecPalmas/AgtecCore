# Estratégia de Testes

## Ferramentas

- Pytest
- pytest-asyncio
- TestContainers

## Regras

| rule_id | Statement | Detalhamento |
| --------- | ----------- | -------------- |
| `RULE-TEST-001` | Testes devem ser assíncronos, usar TestContainers e fixtures de setup/teardown. | `@pytest.mark.asyncio` obrigatório; containers efêmeros para PostgreSQL e Redis; nunca banco real. Ativar venv (`source .venv/bin/activate`) antes de executar. |
| `RULE-TEST-002` | Arquivos de teste devem ser criados em `tests/tests_<modulo>/test_*.py`. | Ex.: `tests/tests_usuario/test_usuarios.py`. |
| `RULE-ROUTE-001` | Path base dos endpoints: prefixo `/api/v1/`. | Atentar ao path de cada módulo, ex.: `/api/v1/usuarios/estadocivil`. |

## Pré-condições obrigatórias antes de executar qualquer teste

1. Docker rodando: `docker info`
2. Venv ativo: `source .venv/bin/activate`
3. Dependências sincronizadas: `uv sync`
4. Executar: `task test`

## Estrutura

```bash
tests/tests_<modulo>/test_*.py
```

## Fixtures padrão (ver `tests/conftest.py`)

- `postgres_container` — escopo `session`: container PostgreSQL (pgvector/pgvector:pg17)
- `db_url` — escopo `session`: URL de conexão assíncrona
- `create_tables` — escopo `session`: cria tabelas via `Base.metadata.create_all`
- `async_session` — escopo `function`: sessão com SAVEPOINT (rollback automático)
- `async_client` — escopo `function`: `AsyncClient` com `ASGITransport`

## Referência One-Shot

Exemplo canônico de teste: `.ia/skills/references/test-example.md`
