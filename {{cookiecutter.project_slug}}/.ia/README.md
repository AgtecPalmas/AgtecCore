# Pacote `.ia/` — AgtecCore

Diretório central de governança de IA do projeto. Contém skills, documentação arquitetural, tasks assistidas e scripts de automação. Regras operacionais estão em `AGENTS.md` (raiz) e `CLAUDE.md` (raiz).

## Estrutura

```
.ia/
├── docs/
│   ├── architecture/        # overview, system-architecture, modules, security
│   ├── guides/              # constraints, patterns, testing, commits, feature, agent-tooling
│   ├── reports/             # relatórios gerados por skills (ex.: análise arquitetural)
│   ├── specs/               # specs técnicas (raiz = em andamento; done/ = concluídas; fastapi/ = camada FastAPI)
│   ├── tasks/               # todo/ e done/
│   └── templates/           # task-template.md, spec-template.md, prd.md
└── skills/                  # skills internas (ver tabela abaixo)
```

> **Nota**: artefatos antes na raiz (`constraints.md`, `project-context.md`, `prompt-templates/`) foram consolidados em `.ia/docs/guides/` e `.ia/docs/architecture/`. Stack/contexto canônico em `.ia/docs/architecture/overview.md`.

## Workflows documentais

- **Datas de governança**: metadados documentais e nomes de novos artefatos usam `DD-MM-YYYY`.
- **Tasks** (`docs/tasks/`): unidade de execução. Ciclo `planned → approved → in_progress → in_review → blocked → done/cancelled`. Regras em `AGENTS.md` §5.
- O campo canônico de lifecycle da task é `Status da task` em `## 1. Metadados`; `Controle de implementacao` registra aprovação, branch e validações operacionais. Novas tasks usam `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`; concluídas usam `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md`; a branch usa o nome do arquivo sem `.md`.
- **Specs técnicas** (`docs/specs/`): design upfront para mudanças amplas, integrações e refatorações multi-app. Uma spec gera N tasks derivadas. Specs Django usam `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`; specs FastAPI usam `<dominio>-<descricao-curta>-fastapi-spec-DD-MM-YYYY.md`; status válidos são `draft`, `approved`, `in_progress`, `in_review`, `done`, `cancelled`, `superseded`. Regras em `AGENTS.md` §6.
- **Relatórios** (`docs/reports/`): saída de scripts de skills (análise arquitetural, conformidade etc). Novos reports usam `DD-MM-YYYY-<descricao-curta>.md` e `Status do relatorio` em `draft`, `in_review`, `done` ou `superseded`.
- **Templates** (`docs/templates/`): `task-template.md`, `spec-template.md`, `prd.md`.

### Quando usar cada artefato de planejamento

| Artefato            | Localização       | Para quê                                                                  | Quando usar                                                            |
| ------------------- | ----------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `task-template.md`  | `docs/templates/` | Unidade de execução (uma demanda concreta, escopo delimitado)             | Toda demanda assistida por IA (§5 do `AGENTS.md`)                      |
| `spec-template.md`  | `docs/templates/` | Design técnico upfront com AS-IS/TO-BE, contratos, ordem de implementação | Mudança ampla, integração externa, refatoração multi-app (§6)          |
| `prd.md`            | `docs/templates/` | PRD completo de produto (problema, escopo, métricas, release plan)        | Funcionalidade nova com discussão de produto antes da spec técnica     |
| `feature-prompt.md` | `docs/templates/` | Prompt-template curto para pedir feature Django ao agente                 | Quando o desenvolvedor quer um prompt pronto para uma feature concreta |

## Skills

### Skills disponíveis

| Skill                               | Caminho                                                 | Resumo                                                                                 |
| ----------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `branch-task-aprovada`              | `.ia/skills/branch-task-aprovada/SKILL.md`              | Cria branch de implementação a partir de task aprovada.                                |
| `django-analise-arquitetura-legado` | `.ia/skills/django-analise-arquitetura-legado/SKILL.md` | Levantamento arquitetural inicial Django + PostgreSQL.                                 |
| `django-api-serializers`            | `.ia/skills/django-api-serializers/SKILL.md`            | Serializers DRF.                                                                       |
| `django-api-views`                  | `.ia/skills/django-api-views/SKILL.md`                  | ViewSets/CBVs DRF e roteamento.                                                        |
| `django-celery-tasks`               | `.ia/skills/django-celery-tasks/SKILL.md`               | **Dormente/preparatória** — Tarefas assíncronas Celery; Celery ausente na stack atual. |
| `django-managers`                   | `.ia/skills/django-managers/SKILL.md`                   | QuerySets e managers customizados.                                                     |
| `django-migrations`                 | `.ia/skills/django-migrations/SKILL.md`                 | Planejamento e revisão de migrations.                                                  |
| `django-models`                     | `.ia/skills/django-models/SKILL.md`                     | Modelos ORM.                                                                           |
| `django-services-use-cases`         | `.ia/skills/django-services-use-cases/SKILL.md`         | Regras de negócio em `services.py`/`use_cases.py`.                                     |
| `django-tests-pytest`               | `.ia/skills/django-tests-pytest/SKILL.md`               | Testes pytest/pytest-django.                                                           |
| `fastapi-especificacao-tecnica`     | `.ia/skills/fastapi-especificacao-tecnica/SKILL.md`     | Spec técnica para a camada FastAPI.                                                    |
| `governanca-compliance`             | `.ia/skills/governanca-compliance/SKILL.md`             | Auditoria de governança documental de `AGENTS.md` + `.ia/`.                            |
| `merge-com-dev`                     | `.ia/skills/merge-com-dev/SKILL.md`                     | Merge de branch de task para `dev`.                                                    |
| `obsidian-query`                    | `.ia/skills/obsidian-query/SKILL.md`                    | Consulta ao vault DevBrain (vault → repo fallback).                                    |
| `obsidian-sync`                     | `.ia/skills/obsidian-sync/SKILL.md`                     | Sincronização do repositório com o vault DevBrain.                                     |
| `task-encerramento`                 | `.ia/skills/task-encerramento/SKILL.md`                 | Encerra task e move `todo/` → `done/`.                                                 |
| `workflow-demandas`                 | `.ia/skills/workflow-demandas/SKILL.md`                 | Orquestra ciclo de task assistida por IA.                                              |

### Scripts de automação

| Script                                                                   | Skill                               | Propósito                                                                                                                   |
| ------------------------------------------------------------------------ | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `.ia/skills/branch-task-aprovada/create_task_implementation_branch.py`   | `branch-task-aprovada`              | Cria branch a partir do nome do arquivo da task.                                                                            |
| `.ia/skills/task-encerramento/close_task_and_move_to_done.py`            | `task-encerramento`                 | Valida status final e move task para `done/`.                                                                               |
| `.ia/skills/merge-com-dev/merge_task_branch_with_dev.py`                 | `merge-com-dev`                     | Merge da branch atual para `dev` com `--dry-run` opcional; unica excecao permitida para efetivar merge via automacao da IA. |
| `.ia/skills/governanca-compliance/check_ia_governance.py`                | `governanca-compliance`             | Auditoria automatizada de `AGENTS.md` + `.ia/`.                                                                             |
| `.ia/skills/django-analise-arquitetura-legado/analyze_legacy_project.py` | `django-analise-arquitetura-legado` | Coleta factual para análise arquitetural inicial.                                                                           |
| `.ia/skills/obsidian-sync/export_devbrain.py`                            | `obsidian-sync`                     | Exporta contexto do repositório para o vault DevBrain.                                                                      |

## Documentação arquitetural

- `.ia/docs/architecture/overview.md`
- `.ia/docs/architecture/system-architecture.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/security.md`

## Gestão de tarefas

- Backlog em `.ia/docs/tasks/todo/`.
- Concluídas em `.ia/docs/tasks/done/` com prefixo `done-`.
- Template em `.ia/docs/templates/task-template.md`.
- Regras completas em `AGENTS.md` §5.
