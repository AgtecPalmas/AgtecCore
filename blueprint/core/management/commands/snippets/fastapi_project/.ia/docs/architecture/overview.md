# Visão Geral da Arquitetura

Camada **FastAPI** do projeto, organizada como API modular por domínios. O serviço expõe endpoints sob o prefixo configurado em `settings.api_str`, centraliza a aplicação em `main.py` e agrega routers de domínio em `core/routers.py`.

---

## 1. Stack inicial

> Preencher após confirmar as dependências em `pyproject.toml` do projeto gerado.

| Camada | Tecnologia | Versão / origem |
|---|---|---|
| Framework web | FastAPI | A confirmar — verificar `pyproject.toml` |
| Servidor ASGI/dev | Uvicorn | A confirmar — verificar `pyproject.toml` |
| Servidor produção | Gunicorn | A confirmar — verificar `pyproject.toml` |
| ORM | SQLAlchemy | A confirmar — verificar `pyproject.toml` |
| Banco principal | PostgreSQL | Configurado via `core/config.py` e `core/database.py` |
| Sessão async | SQLAlchemy AsyncSession + asyncpg | A confirmar — verificar `pyproject.toml` |
| Sessão sync | SQLAlchemy Session | `create_engine` + `SessionLocal` |
| Schemas/validação | Pydantic v2 | A confirmar — verificar `pyproject.toml` |
| Configuração | pydantic-settings + `.env` | `BaseSettings`, `ConfigDict(env_file=".env")` |
| Auth | OAuth2 Bearer + JWT | `authentication/security.py`, `core/security.py` |
| Cache | Redis | A confirmar — verificar `pyproject.toml` e `core/redis.py` |
| Observabilidade | A confirmar | Verificar `main.py` e `pyproject.toml` |
| Testes | pytest, pytest-asyncio, TestContainers | A confirmar — verificar `pyproject.toml` |

Python: A confirmar — verificar `pyproject.toml`.

### Módulo de IA (se existir no projeto)

> Se o projeto tiver módulo de IA (embeddings, agentes, RAG), documentar aqui a linha de stack correspondente e preencher `.ia/docs/architecture/ia_modules.md`.

---

## 2. Organização da aplicação

Entrada principal:

- `main.py` cria a instância `FastAPI`, configura lifespan, CORS, observabilidade e inclui `api_router`.
- `core/routers.py` cria o `APIRouter` principal com prefixo `settings.api_str` e agrega módulos de domínio.
- `core/config.py` centraliza settings lidos do ambiente.
- `core/database.py` configura engine SQLAlchemy sync/async e dependências de sessão.

### Módulos agregados no router principal

> Documentar os módulos de domínio do projeto após a geração. Exemplo de formato:

```
- authentication
- <modulo_dominio_1>
- <modulo_dominio_2>
- <modulo_dominio_3>
```

---

## 3. Padrão por módulo

O padrão dominante por módulo/submódulo é:

- `routers.py`: rotas FastAPI, dependências, response models e registro de endpoints.
- `schemas.py`: contratos Pydantic de entrada/saída.
- `models.py`: modelos SQLAlchemy e mapeamentos para tabelas existentes.
- `use_cases.py`: orquestração de regra de aplicação e persistência.

Arquivos auxiliares aparecem quando o domínio exige integrações, uploads, background tasks ou serviços externos.

---

## 4. Integrações e dependências externas

> Documentar as integrações confirmadas do projeto após a geração.

- **Ecossistema Django**: o projeto FastAPI integra-se ao sistema Django compartilhado via autenticação JWT e modelos de negócio comuns. Documentar aqui os contratos específicos após análise.
- **Flutter** (se existir): clientes Flutter consomem contratos HTTP da API; specs de integração devem focar o contrato de API sem expor detalhe interno desnecessário.
- **Redis** (se existir): `core/redis.py` implementa serviço de cache — documentar uso após confirmar na configuração.
- **Módulo de IA** (se existir): documentar estrutura e endpoints em `.ia/docs/architecture/ia_modules.md`.
- **Observabilidade**: verificar `main.py` e variáveis de ambiente — documentar ferramentas ativas.
- **Outras integrações**: documentar aqui conforme o projeto gerado.

---

## 5. Regras transversais

- Routers devem ser finos e delegar regra de aplicação para use cases/services.
- Schemas Pydantic são o contrato público da API e devem ser mantidos consistentes com os endpoints.
- Modelos SQLAlchemy que herdam de bases comuns usam campos como `id`, `deleted`, `created_at`, `updated_at` e `enabled`.
- Consultas devem preservar filtros de `deleted`/`enabled` quando aplicável ao domínio.
- Dependências de autenticação devem reutilizar helpers existentes de `authentication/security.py` quando possível.
- Alterações que afetem integrações externas (Django, Flutter, Redis, IA, observabilidade) devem ser explicitadas em spec/task.

---

## 6. Pontos de atenção imediatos

1. O fluxo Alembic/migrations pode não estar versionado como estrutura ativa no checkout inicial — criar spec/task antes de introduzir comandos operacionais de migração.
2. O módulo `core/` é sensível e não deve ser alterado por agentes sem autorização explícita documentada.
3. Integrações com o ecossistema Django e clientes externos devem ser documentadas como contratos externos, não como motivo para reintroduzir padrões Django nesta camada FastAPI.
