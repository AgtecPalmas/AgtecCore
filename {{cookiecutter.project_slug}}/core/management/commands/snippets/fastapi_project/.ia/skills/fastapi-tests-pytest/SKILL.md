---
name: fastapi-tests-pytest
description: Escrever e revisar testes automatizados com `pytest`, `pytest-asyncio` e `TestContainers` para routers, use cases e models do projeto FastAPI Argus. Usar quando adicionar feature, bugfix, refactor ou alterar contrato de endpoint.
---

# Testes para FastAPI com pytest

# Objetivo
Garantir cobertura de regressão com testes assíncronos e determinísticos por módulo e por camada.

# Fluxo
1. Consultar `.ia/docs/testing/strategy.md` e `.ia/skills/references/test-example.md` antes de escrever qualquer teste.
2. Criar ou atualizar testes em `tests/tests_<modulo>/` seguindo `test_*.py`.
3. Cobrir pelo menos: cenário feliz, payload inválido (422) e falha relevante (404/403).
4. Usar `AsyncClient` (fixture `async_client`) para chamadas HTTP e `async_session` para verificação direta no banco.
5. Pré-condições obrigatórias antes de executar: Docker rodando e dependências sincronizadas (`rtk uv sync`).
6. Executar a suíte segmentada do módulo antes da finalização: `rtk task test`.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- Todos os testes **devem** ser assíncronos: `@pytest.mark.asyncio` + `async def test_*`.
- Usar **TestContainers** para PostgreSQL e Redis — nunca banco real.
- Manter testes determinísticos e sem dependência de ordem.
- Evitar dados sensíveis reais em massa de teste.
- URLs: strings literais com prefixo `/api/v1/<modulo>/` — nunca inventar rotas não documentadas.
- Não introduzir novas dependências de teste sem aprovação (`RULE-DEP-001`).
- Garantir que novas regras de negócio tenham cobertura automatizada.

# Checklist de qualidade
- [ ] Revisar se o teste falha quando a regra quebra.
- [ ] Confirmar autenticação e permissões em testes de API.
- [ ] Validar status code e payload de resposta.
- [ ] Verificar soft delete (`deleted is True`) quando aplicável.
- [ ] Em endpoints self-service de filiado: não enviar `filiado_id` na chamada.
- [ ] Registrar no artefato da task os comandos executados e seus resultados.

# Comandos úteis
```bash
# Pré-condições
docker info
rtk uv sync

# Execução
rtk task test
rtk pytest tests/tests_<modulo>/
```

# Fixtures disponíveis (`tests/conftest.py`)

| Fixture | Escopo | Descrição |
|---|---|---|
| `postgres_container` | session | Container PostgreSQL (pgvector) |
| `db_url` | session | URL de conexão assíncrona |
| `create_tables` | session | Cria tabelas via `Base.metadata.create_all` |
| `async_session` | function | Sessão com SAVEPOINT (rollback automático) |
| `async_client` | function | `AsyncClient` com `ASGITransport` |

# Referências locais
- `.ia/docs/testing/strategy.md`
- `.ia/skills/references/test-example.md`
- `.ia/docs/guides/patterns.md`
- `pyproject.toml`
