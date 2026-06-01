# Padrões FastAPI do Projeto

## Etapas do desenvolvimento

- O fluxo de abertura/execução/encerramento de demandas deve seguir `AGENTS.md` (fonte normativa).
- Catálogo canônico de rules: `.ia/docs/guides/rules-catalog.md`.
- Protocolo de governança e qualidade: `.ia/docs/guides/rules-governance.md`.
- Matriz canônica de seleção de skills: `.ia/docs/guides/skills-decision.md`.
- Padrão canônico de naming para novos artefatos:
  - `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`
  - `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`
  - `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md`
- Padrões com `DD_MM_YYYY` são legado histórico apenas para leitura e não devem ser replicados.
- Tasks legadas com `DD_MM_YYYY` ficam em `.ia/docs/tasks/legacy/` e não representam backlog operacional. Se uma demanda desse conjunto voltar a ser necessária, criar nova task em `.ia/docs/tasks/todo/` usando o contrato atual.
- Specs legadas fora do contrato atual ficam em `.ia/docs/specs/legacy/` e não representam planejamento ativo. Se uma spec desse conjunto voltar a ser necessária, criar ou atualizar uma spec em `.ia/docs/specs/` usando status canonico e data `DD-MM-YYYY`.
- Este guia foca nos padrões técnicos de implementação (routers, use cases, schemas, testes).

## Fonte de verdade (anti-desvio)

- Antes de propor uma abordagem, encontre e cite 1–2 referências reais no repositório (código ou docs) e replique o padrão.
- Se houver conflito entre artefatos, trate a divergência como bloqueio e peça decisão (não “escolha no chute”).

## Routers

- Apenas orquestração
- Sem regras de negócio
- Sem acesso direto ao DB em novos fluxos (`RULE-ARCH-002`)
- Exceção legada documentada: `RULE-EXC-001`

## Use Cases

- Contêm toda lógica de negócio
- Recebem dependências explicitamente

## Dependency Injection

- Sempre usar Depends
- Evitar singletons implícitos
- Utilizar o Annotation-based Injection quando possível

## Rotas e endpoints (HTTP)

- Prefixo global: `/api/v1/`
- Paths: kebab-case (ex.: `/fetch-paginated/`, `/fetch-by-filiado/`)
- Barra final (`/`):
  - Em endpoints novos, preferir manter barra final para consistência de contratos (`RULE-ROUTE-002`).
  - Em módulos legados, respeitar o padrão já existente no arquivo antes de propor migração (`RULE-ROUTE-002`).
  - Migração de rotas legadas deve ser planejada em spec/task própria para evitar quebra de clientes (`RULE-ROUTE-002`).
- Routers não fazem I/O nem query direta: delegar sempre para `use_cases`

## Schemas

- Usar Pydantic para validação e serialização
- Separar schemas em:
  - class NOME_MODULOBase(BaseModel): para representar o schema base trazendo todos os atributos em comum do módulo.
  - class NOME_MODULOCreate(NOME_MODULOBase): para representar o schema de criação.
  - class NOME_MODULOUpdate(NOME_MODULOBase): para representar o schema de atualização.
  - class NOME_MODULOInDBBase(NOME_MODULOBase): para representar o schema que reflete a tabela do banco de dados, incluindo os atributos id; deleted; created_at e updated_at.
  - class NOME_MODULOInDB(NOME_MODULOInDBBase): para representar o schema quando necessário que inclua atributos adicionais do banco de dados.
  - class NOME_MODULOSearchFilter(FilterPagination): para representar o schema de filtro de busca, herdando de FilterPagination para incluir paginação
- Usar typing.Optional para campos opcionais seguindo o padrão do Pydantic `Optional[T] = None`
- Usar Field(...) para validação adicional e metadados, quando necessário, ou informado explicitamente pelo prompt

## Nomenclatura (código)

- Python:
  - Funções/métodos/variáveis: `snake_case`
  - Classes/Exceptions/Schemas: `PascalCase`
  - Constantes: `SCREAMING_SNAKE_CASE`
  - Módulos/pacotes: nomes curtos e descritivos do domínio (ex.: `patrimonioitem`, `historicoatendimento`)
- FastAPI:
  - Routers: handlers com nomes verbais e claros (ex.: `fetch-paginated`, `fetch-by-*`, `search`, `create`, `update`, `delete`, `restore`)
  - Use cases: métodos com o mesmo vocabulário do router, sem “sinônimos” inventados

## Padrões que devem ser reutilizados (não inventar outro jeito)

- Paginação/filtros: `PaginationBase` + `FilterPagination` e endpoints `fetch-paginated/` e `search/` seguindo as referências do projeto
- DI e sessão: usar `Depends` e `AsyncDBDependency` (ou o padrão vigente no módulo); não criar novas formas de obter sessão
- Exceções: usar `core.exceptions` (quando aplicável) e manter respostas consistentes

## Padrões de models, use cases e autenticação

### CoreBase (models)

Todo model **deve** herdar de `CoreBase` (`core/database.py`). Ela provê automaticamente:

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `id` | `UUID` | PK auto-gerada com `uuid4` |
| `deleted` | `bool` | Soft delete (default `False`) |
| `created_at` | `datetime` | Preenchido automaticamente |
| `updated_at` | `datetime` | Atualizado com `onupdate` |
| `enabled` | `bool` | Ativo/inativo (default `True`) |

**Nunca** redeclarar esses campos no model filho.

### BaseUseCases (use cases)

Todo use case **deve** herdar de `BaseUseCases[Model, CreateSchema, UpdateSchema]` (`core/use_cases.py`). Ele provê operações comuns de CRUD e paginação via `get_paginated_from_query()`.

Instância singleton obrigatória ao final do arquivo:

```python
nome_modulo = NomeModeloUseCase(NomeModelo)
```

### Autenticação em routers

- Usuário autenticado: `usuario: security.CurrentUserByTokenDependency`
- Permissão por operação: `Depends(security.has_permission("modulo.acao_modelo"))`
- Pattern de constantes no topo do router:

```python
GET_DEPENDENCY = Depends(security.has_permission("modulo.view_modelo"))
CREATE_DEPENDENCY = Depends(security.has_permission("modulo.add_modelo"))
UPDATE_DEPENDENCY = Depends(security.has_permission("modulo.change_modelo"))
DELETE_DEPENDENCY = Depends(security.has_permission("modulo.delete_modelo"))
```

### Endpoints self-service do filiado autenticado

- Para endpoints do proprio filiado logado, **nao** receber `filiado_id` em query/body/path
- O router recebe `usuario` via token e delega ao use case
- O use case resolve o filiado por `authentication.security.get_filiado_by_auth_user(...)`
- Caso nao exista filiado para o usuario autenticado, retornar erro de dominio coerente
- Regra detalhada: `.ia/docs/guides/regra-endpoint-filiado-autenticado.md`

## Flutter (integração) — Dio e design system

- Dio:
  - Não criar um novo client/abstração se já houver padrão no app; seguir a implementação de referência indicada nas tasks Flutter.
  - Manter padrão de tratamento de erro, paginação e retorno (ex.: `Either`) já adotado pelo projeto.
- Design system:
  - Seguir componentes/tokens existentes (fonte deve estar documentada no projeto).
  - Se a fonte do design system não estiver clara (Figma/docs/lib), tratar como bloqueio e pedir o link antes de propor UI.
