---
name: fastapi-especificacao-tecnica
description: Gerar especificação técnica para a equipe da camada FastAPI integrada ao Django. Usar sempre que o pedido envolver spec técnica, arquitetura, plano técnico ou detalhamento de implementação para FastAPI.
---

# Objetivo
Produzir especificações técnicas acionáveis, alinhadas ao padrão real da camada FastAPI gerada neste projeto, com foco em arquitetura, contratos, segurança, testes e plano incremental de execução.

# Referências locais obrigatórias
- `core/management/commands/fastapi.py`
- `core/management/commands/fastapi_managers/`
- `core/management/commands/snippets/fastapi/`
- `core/management/commands/snippets/fastapi_project/`
- `docs/fastapi/index.md`

# Padrão arquitetural a respeitar
- Projeto FastAPI base em `FastAPI/<nome_projeto>/`.
- Entrada da aplicação em `main.py` com `app.include_router(api_router)`.
- Roteamento central em `core/routers.py` com prefixo `settings.api_str` (padrão `/api/v1`).
- Organização por domínio em módulos com:
  - `<app>/<model>/models.py`
  - `<app>/<model>/schemas.py`
  - `<app>/<model>/use_cases.py` Concentra regras de negócio e acesso a dados; routers apenas orquestram.
  - `<app>/<model>/routers.py` Apenas para orquestração, sem lógica de negócio; use cases concentram regras e acesso a dados.
  - `<app>/routers.py` agregando rotas do app.
- Use cases devem concentrar regras de negócio e acesso a dados (routers apenas orquestram).
- Models em SQLAlchemy 2 (`Mapped`, `mapped_column`, `relationship`).
- Schemas em Pydantic (separação clara para create/update/read/search).
- Segurança baseada em OAuth2/JWT e checagem de permissões integradas ao domínio `authentication`.

# Regras obrigatórias
- Modularizar endpoints com `APIRouter` e `include_router`.
- Declarar dependências com `Depends` (DB, auth, autorização, filtros).
- Declarar `response_model` nos endpoints para contrato explícito.
- Preferir `async def` para operações I/O-bound.
- Separar schema de entrada e saída para estabilidade de contrato.
- Definir estratégia de erros com exceções de domínio e status code consistente.

# Como escrever a especificação técnica
Ao receber pedido de especificação para FastAPI, produzir o documento em Markdown com esta estrutura:

Metadados obrigatórios no topo do arquivo:

- Data: `DD-MM-YYYY`
- Status: `draft` | `approved` | `in_progress` | `in_review` | `done` | `cancelled` | `superseded`
- Task(s) de rastreabilidade: `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md`

## 1) Contexto e objetivo
- Problema de negócio.
- Resultado esperado.
- Escopo e fora de escopo.

## 2) Impacto arquitetural
- Apps e módulos FastAPI afetados.
- Dependências com Django (auth, permissões, modelos equivalentes).
- Mudanças em cache (Redis na camada FastAPI externa, quando aplicável — Redis não compõe a stack Django; ver `.ia/docs/architecture/overview.md` §2), observabilidade e configuração.

## 3) Contratos de API
- Endpoints propostos (método, rota, finalidade).
- Query params, payloads e `response_model`.
- Regras de paginação, busca e filtros.
- Erros esperados (4xx/5xx) por endpoint.

## 4) Modelagem de dados
- Entidades SQLAlchemy afetadas.
- Relacionamentos (`ForeignKey`, `ManyToMany`, herança `CoreBase/CoreBaseInherit`).
- Campos obrigatórios/opcionais e defaults.

## 5) Schemas e validação
- Schemas de entrada e saída (`Create`, `Update`, `InDB`, `SearchFilter`).
- Regras de validação e normalização.
- Campos sensíveis que devem ser omitidos na resposta.

## 6) Regras de negócio (use cases)
- Casos de uso novos/alterados.
- Fluxo de persistência e critérios de idempotência.
- Estratégia para evitar lógica de negócio em routers.

## 7) Segurança e autorização
- Dependências de autenticação/autorização.
- Permissões por ação (`view`, `add`, `change`, `delete`).
- Riscos e mitigação de exposição de dados.

## 8) Cache e observabilidade
- Chaves Redis afetadas na camada FastAPI externa (quando aplicável), estratégia de invalidação e refresh.
- Logs relevantes sem PII.
- Eventos/métricas úteis para operação.

## 9) Estratégia de testes
- Testes unitários de use cases.
- Testes de integração HTTP (pytest-asyncio + `httpx.AsyncClient`).
- Cenários mínimos: sucesso, validação, autorização, erro de negócio.

## 10) Plano incremental de implementação
- Fases pequenas e sequenciais.
- Arquivos por fase.
- Critérios de aceite por fase.

## 11) Riscos e pendências
- Riscos técnicos.
- Decisões pendentes.
- Premissas assumidas.

# Regras de saída
- Escrever em português técnico, direto e sem ambiguidade.
- Usar caminhos de arquivo concretos quando sugerir alterações.
- Sempre listar arquivos FastAPI esperados por módulo impactado.
- Quando houver lacuna de contexto, declarar premissas explicitamente.
- Salvar as especificações em `.ia/docs/specs/fastapi/` com nome descritivo e data no padrão `<dominio>-<descricao-curta>-fastapi-spec-DD-MM-YYYY.md` (ex.: `sso-govbr-integracao-fastapi-spec-30-05-2026.md`).
