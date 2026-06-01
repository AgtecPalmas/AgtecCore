# Guia para atuação de agentes de IA

## RTK

- É mandatório adicionar o prefixo `rtk` em todos os comandos.
- Exceção: comandos de preparação do shell local, como ativação de ambiente virtual via `source`, não recebem o prefixo `rtk`; todos os demais comandos operacionais do projeto devem usar o prefixo.

## 1. Linguagem e contexto

- Sempre responder em **português**, a menos que o contexto da tarefa exija outro idioma (por exemplo, contrato externo em inglês).
- Este projeto é um **backend Django 4.2 com DRF**, organizado como **monólito modular por apps**, usando **PostgreSQL** como banco principal (com extensões `pgvector` e `pg_trgm`), autenticação baseada em **dj-rest-auth + SimpleJWT** e observabilidade via **Sentry + Elastic APM**. O projeto **coexiste com um serviço FastAPI externo** que compartilha o mesmo banco PostgreSQL (não há Redis, Celery ou Elasticsearch ativos hoje — versão canônica e atualizada da stack em `.ia/docs/architecture/overview.md`).

## 2. Fontes de verdade para arquitetura

Ao gerar/alterar código, priorizar `.ia/docs/architecture/` (`overview.md`, `system-architecture.md`, `modules.md`, `security.md`) e `.ia/docs/guides/` (`patterns.md`, `testing.md`). Em caso de conflito, **`.ia/docs/` prevalece sobre este arquivo**.

## 3. Skills de IA por camada (obrigatório)

### 3.1. Localização das skills

Skills em `.ia/skills/<skill-name>/SKILL.md`.

### 3.2. Catálogo de skills disponíveis

Ordem do catálogo agrupa por finalidade (governança → camadas Django → especificação/análise → Obsidian).

| Skill                               | Quando ativar (trecho curto)                                                                                                                                                                                 |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `workflow-demandas`                 | Pedido envolve tarefa, feature, bugfix, refactor ou mudanças em `.ia/`                                                                                                                                       |
| `branch-task-aprovada`              | Task aprovada — abrir branch de implementação a partir do arquivo da task                                                                                                                                    |
| `merge-com-dev`                     | Desenvolvedor pediu **merge com dev** ou merge da branch de task com dev                                                                                                                                     |
| `task-encerramento`                 | Implementação concluída — mover task de `todo/` para `done/`                                                                                                                                                 |
| `governanca-compliance`             | Auditoria de governança em `.ia/` ou validação antes de mudanças amplas                                                                                                                                      |
| `django-models`                     | Criar/alterar entidades, campos, relacionamentos ou constraints em `models.py`                                                                                                                               |
| `django-managers`                   | Criar QuerySets ou managers customizados; resolver N+1 reutilizável                                                                                                                                          |
| `django-services-use-cases`         | Implementar fluxos de domínio, integrações externas e operações multi-escrita em `services.py`/`use_cases.py`                                                                                                |
| `django-api-serializers`            | Criar/alterar serializers DRF — validação e contrato de API                                                                                                                                                  |
| `django-api-views`                  | Criar/alterar ViewSets, permissões, filtros e roteamento DRF                                                                                                                                                 |
| `django-tests-pytest`               | Adicionar/alterar testes pytest com `.venv`, mandatório usar TestContainers                                                                                                                                  |
| `django-celery-tasks` *(dormente)*  | Projetar tarefas assíncronas Celery — **preparatória/dormente**, Celery ausente na stack (ver `.ia/docs/architecture/overview.md` §2); aplicar apenas em revisão antecipada ou quando Celery for incorporado |
| `django-migrations`                 | Gerar/revisar migrations de schema, índices, constraints ou backfill                                                                                                                                         |
| `fastapi-especificacao-tecnica`     | Gerar spec/plano técnico para a camada FastAPI externa                                                                                                                                                       |
| `django-analise-arquitetura-legado` | Levantamento inicial quando `.ia/docs/architecture/` está vazio                                                                                                                                              |
| `obsidian-sync`                     | Sincronizar repositório com vault DevBrain do Obsidian                                                                                                                                                       |
| `obsidian-query`                    | Responder pergunta sobre histórico/tasks/specs consultando vault DevBrain                                                                                                                                    |

### 3.3. Regra de uso das skills

Antes de implementar: identificar camadas afetadas (model, manager, API, serviço, task, migration, testes), ler os `SKILL.md` correspondentes — cada skill declara seu gatilho na frontmatter (`description:`) — aplicar as regras e registrar na task quais skills foram usadas. Mudança multicamada → combinar skills na mesma task.

### 3.4. Precedência de aplicação

Mudança técnica em código: **primeiro** `workflow-demandas` (cria task, define escopo) → **depois** skills por camada (`django-*`, `fastapi-*`) durante execução → branch só via `branch-task-aprovada` após status `approved`. Pedidos operacionais (merge com dev, encerrar task, sincronizar Obsidian, auditoria) acionam direto a skill correspondente.

## 4. Estrutura do projeto Django

Mapa arquitetural amplo (catálogo de apps, integrações, fluxos) vive em `.ia/docs/architecture/system-architecture.md`. Fonte de verdade para apps ativos: `base/settings.py` (`INSTALLED_APPS`). Este arquivo permanece focado em regras operacionais.

**Padrão por app:** `models.py` (ORM/Regras de negócio) · `managers.py` (QuerySets) · `api/serializers/*.py` · `api/views/*.py` · `api/routers.py` (APIRest)) · `tasks.py` (assíncrono — Celery não instalado hoje).

**Regras transversais:**

- Um app **não consulta diretamente** modelos de outro app sem passar por serviços/contratos claros.
- Views/ViewSets **não carregam regras de negócio**; trabalhamos com o conceito FatModel do Django.
- Consultas devem ser otimizadas com `select_related`/`prefetch_related` e QuerySets reutilizáveis.
- Migrations devem ser **pequenas, reversíveis e documentadas**.

## 5. Gestão de tarefas assistidas por IA (obrigatório)

Gatilho: pedidos que envolvam `tarefa`, `demanda`, `feature`, `requisito`, `bugfix`, `refactor`, `refatorar`, `refatoração` ou `melhoria de testes`.

O ciclo de vida de uma task é orquestrado pelas skills dedicadas — cada `SKILL.md` é fonte de verdade para o próprio fluxo:

- Criação, acompanhamento e fechamento documental → `.ia/skills/workflow-demandas/SKILL.md`.
- Aprovação e abertura de branch de implementação → `.ia/skills/branch-task-aprovada/SKILL.md`.
- Merge local com `dev` (único fluxo em que `git commit` interno é permitido) → `.ia/skills/merge-com-dev/SKILL.md`.
- Encerramento e movimentação para `done/` → `.ia/skills/task-encerramento/SKILL.md`.

Convenção de nome obrigatória para novas tasks: `task-DD-MM-YYYY-<hash_alfanumerico_10>.md` (hash com 10 caracteres `A-Z`, `a-z`, `0-9`; nunca reutilizar fragmentos de credenciais). Tasks concluídas usam `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md`, e a branch de implementação usa exatamente o nome do arquivo da task sem `.md`. Template base: `.ia/docs/templates/task-template.md`. Aprovação humana é obrigatória antes da implementação.

**Status válidos de task:** `planned` | `approved` | `in_progress` | `in_review` | `blocked` | `done` | `cancelled`

## 6. Specs técnicos

Spec = **design upfront** (contratos, arquitetura, decisões). Task = **execução**. Uma spec ampla pode gerar várias tasks.

**Localização:** `.ia/docs/specs/` (rascunho/aprovação) · `.ia/docs/specs/done/` (concluídas) · `.ia/docs/specs/fastapi/` (geradas pela skill `fastapi-especificacao-tecnica`).

**Quando criar:** mudança que afeta múltiplos apps, integração com sistema externo, refatoração ampla com decisões arquiteturais, ou pedido explícito de "spec técnica". Para mudanças localizadas, ir direto para task (§5).

**Convenção de nome:** `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`. Specs FastAPI usam `<dominio>-<descricao-curta>-fastapi-spec-DD-MM-YYYY.md` em `.ia/docs/specs/fastapi/`.

**Status válidos de spec:** `draft` | `approved` | `in_progress` | `in_review` | `done` | `cancelled` | `superseded`

**Ciclo de vida:** criar em `.ia/docs/specs/` → aprovar com o desenvolvedor → quebrar em tasks em `.ia/docs/tasks/todo/` → mover para `done/` ao concluir todas as tasks derivadas. Specs Django são manuais — usar `.ia/docs/templates/spec-template.md` como template base; usar `.ia/docs/templates/prd-template.md` apenas quando a demanda exigir um PRD de produto antes da spec técnica.

## 7. Comandos de build em desenvolvimento

- Ativar o ambiente virtual (Obrigatório, exceção sem `rtk`) -> source .venv/bin/activate (Linux/Mac) ou .venv\Scripts\activate (Windows).
- Dependências -> `rtk uv sync`.
- Migrations -> `rtk python manage.py makemigrations` / `rtk python manage.py migrate`.
- Lint/Test -> `rtk task lint` (black/isort) · `rtk task test`.

## 8. Segurança e configuração

- Variáveis de ambiente obrigatórias para banco, secrets e integrações externas (Redis ausente na stack atual — ver `overview.md`).
- Nunca commitar credenciais reais; usar `.env.example` como referência.

### 8.1. Operações restritas para a IA

| Operação                          | IA pode executar? | Exceção controlada.            |
| --------------------------------- | ----------------- | ------------------------------ |
| Modificar arquivos da app `core/` | Não               | Nenhuma                        |
| `git commit` direto               | Não               | Apenas via skill merge-com-dev |
| `git push`                        | Não               | Nenhuma                        |
| `git rebase`                      | Não               | Nenhuma                        |
| `git pull`                        | Não               | Nenhuma                        |

## 9. Resumo operacional

1. Task em `.ia/docs/tasks` antes de implementar; aprovar e abrir branch via `branch-task-aprovada`
2. Carregar skills de `.ia/skills/` (camadas impactadas)
3. Encerrar via `task-encerramento` (status `done`, mover para `done/` e apagar do `todo/`)
4. Mudanças pequenas, rastreáveis, alinhadas à documentação em `.ia/docs/`
