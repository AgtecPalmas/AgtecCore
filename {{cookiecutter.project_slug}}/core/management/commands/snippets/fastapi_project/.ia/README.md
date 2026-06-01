# Pacote `.ia/` — FastAPI

Diretório central de governança de IA do projeto FastAPI. Contém skills, documentação arquitetural, specs, tasks assistidas, templates e scripts de automação. Regras operacionais estão em `AGENTS.md` (raiz).

## Estrutura

```
.ia/
├── docs/
│   ├── architecture/        # overview, modules, ia_modules, ia_embeddings, security, relatorio-arquitetural
│   ├── guides/              # constraints, patterns, project-context, rules-catalog, rules-governance, skills-decision
│   ├── prd/                 # PRDs de produto (gerados a partir de docs/templates/prd.md)
│   ├── reports/             # relatórios de auditoria/conformidade gerados por skills
│   ├── rfc/                 # RFCs técnicas
│   ├── specs/               # specs técnicas (raiz = em andamento; done/ = concluídas)
│   ├── tasks/               # todo/ e done/
│   ├── templates/           # task-template.md, spec-template.md, prd.md, feature-prompt.md, integracao-flutter.md
│   └── testing/             # estratégia de testes
└── skills/                  # skills internas (ver tabela abaixo)
```

> **Nota**: a governança recebida da camada Django é referência para contrato transversal de tasks, status, datas, branchs, merge e gate. Regras técnicas Django não são padrão ativo desta camada FastAPI.

## Workflows documentais

- **Datas de governança**: metadados documentais e nomes de novos artefatos usam `DD-MM-YYYY`.
- **Tasks** (`docs/tasks/`): unidade de execução. Ciclo `planned → approved → in_progress → in_review → blocked → done/cancelled`. Regras em `AGENTS.md` §5.
- O campo canônico de lifecycle da task é `Status da task` em `## 1. Metadados`; `Controle de implementacao` registra aprovação, branch e validações operacionais. Novas tasks usam `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`; concluídas usam `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md`; a branch usa o nome do arquivo sem `.md`.
- **Specs técnicas** (`docs/specs/`): design upfront para mudanças amplas, integrações e refatorações multi-módulo. Uma spec gera N tasks derivadas. O padrão canônico é `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`; status válidos são `draft`, `approved`, `in_progress`, `in_review`, `done`, `cancelled`, `superseded`. Regras em `AGENTS.md` §6.
- **Reports**: saídas de auditoria/conformidade devem usar `DD-MM-YYYY-<descricao-curta>.md` e `Status do relatorio` em `draft`, `in_review`, `done` ou `superseded` quando o diretório de reports existir no fluxo aprovado.
- **Templates** (`docs/templates/`): `task-template.md`, `spec-template.md`, `prd.md`, `feature-prompt.md`, `integracao-flutter.md`.

### Quando usar cada artefato de planejamento

| Artefato | Localização | Para quê | Quando usar |
|---|---|---|---|
| `task-template.md` | `docs/templates/` | Unidade de execução (uma demanda concreta, escopo delimitado) | Toda demanda assistida por IA (§5 do `AGENTS.md`) |
| `spec-template.md` | `docs/templates/` | Design técnico upfront com AS-IS/TO-BE, contratos e ordem de implementação | Mudança ampla, integração externa, refatoração multi-módulo (§6) |
| `prd.md` | `docs/templates/` | PRD completo de produto (problema, escopo, métricas, release plan) | Funcionalidade nova com discussão de produto antes da spec técnica |
| `feature-prompt.md` | `docs/templates/` | Prompt-template curto para pedir feature FastAPI ao agente | Quando o desenvolvedor quer um prompt pronto para uma feature concreta |
| `integracao-flutter.md` | `docs/templates/` | Template de contrato para consumo Flutter | Quando a mudança afetar contrato HTTP consumido pelo cliente Flutter |

## Skills

### Skills disponíveis

| Skill | Caminho | Resumo |
|---|---|---|
| `workflow-demandas` | `.ia/skills/workflow-demandas/SKILL.md` | Orquestra ciclo de task assistida por IA. |
| `branch-task-aprovada` | `.ia/skills/branch-task-aprovada/SKILL.md` | Cria branch de implementação a partir de task aprovada. |
| `merge-com-dev` | `.ia/skills/merge-com-dev/SKILL.md` | Merge local de branch de task para `dev`. |
| `task-encerramento` | `.ia/skills/task-encerramento/SKILL.md` | Encerra task e move `todo/` → `done/`. |
| `governanca-compliance` | `.ia/skills/governanca-compliance/SKILL.md` | Auditoria de governança documental de `AGENTS.md` + `.ia/`. |
| `atualizar-artefatos-ia` | `.ia/skills/atualizar-artefatos-ia/SKILL.md` | Atualiza documentação operacional de agentes e artefatos `.ia/`. |
| `adicionar-endpoint` | `.ia/skills/adicionar-endpoint/SKILL.md` | Adiciona endpoint FastAPI seguindo router → use case → contratos. |
| `refatorar-modulo` | `.ia/skills/refatorar-modulo/SKILL.md` | Refatora módulo FastAPI para padrões arquiteturais vigentes. |
| `corrigir-bug` | `.ia/skills/corrigir-bug/SKILL.md` | Diagnostica e corrige bugs seguindo protocolo anti-alucinação. |
| `escrever-testes` | `.ia/skills/escrever-testes/SKILL.md` | Escreve testes automatizados pytest/pytest-asyncio/TestContainers. |
| `fastapi-tests-pytest` | `.ia/skills/fastapi-tests-pytest/SKILL.md` | Testes para routers, use cases e models do projeto FastAPI. |
| `adicionar-embeddings` | `.ia/skills/adicionar-embeddings/SKILL.md` | Analisa ou especifica embeddings, pgvector, busca semântica e memória — não alterar módulo de IA/agentes do projeto (se existir). |
| `nova-tool-ia` | `.ia/skills/nova-tool-ia/SKILL.md` | Especifica tool assíncrona para agentes — não alterar módulo de IA/agentes do projeto (se existir). |
| `novo-agente-ia` | `.ia/skills/novo-agente-ia/SKILL.md` | Especifica agente especialista — não alterar módulo de IA/agentes do projeto (se existir). |
| `spec-integracao-flutter` | `.ia/skills/spec-integracao-flutter/SKILL.md` | Cria spec de integração entre API FastAPI e cliente Flutter. |
| `obsidian-sync` | `.ia/skills/obsidian-sync/SKILL.md` | Sincronização do repositório com o vault DevBrain. |
| `obsidian-query` | `.ia/skills/obsidian-query/SKILL.md` | Consulta ao vault DevBrain com fallback para o repositório. |

### Scripts de automação

| Script | Skill | Propósito |
|---|---|---|
| `.ia/skills/branch-task-aprovada/create_task_implementation_branch.py` | `branch-task-aprovada` | Cria branch a partir do nome do arquivo da task. |
| `.ia/skills/task-encerramento/close_task_and_move_to_done.py` | `task-encerramento` | Valida status final e move task para `done/`. |
| `.ia/skills/merge-com-dev/merge_task_branch_with_dev.py` | `merge-com-dev` | Merge da branch atual para `dev` com `--dry-run` opcional; única exceção permitida para efetivar merge via automação da IA. |
| `.ia/skills/governanca-compliance/check_ia_governance.py` | `governanca-compliance` | Auditoria automatizada de `AGENTS.md` + `.ia/`. |
| `.ia/skills/obsidian-sync/export_devbrain.py` | `obsidian-sync` | Exporta contexto do repositório para o vault DevBrain. |
| `.ia/skills/obsidian-query/query_devbrain.py` | `obsidian-query` | Consulta o vault DevBrain e retorna contexto rastreável. |

## Documentação arquitetural

- `.ia/docs/architecture/overview.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/ia_modules.md`
- `.ia/docs/architecture/ia_embeddings.md`
- `.ia/docs/architecture/security.md`
- `.ia/docs/architecture/relatorio-arquitetural.md`

## Gestão de tarefas

- Backlog operacional em `.ia/docs/tasks/todo/`.
- Concluídas em `.ia/docs/tasks/done/` com prefixo `done-`.
- Template em `.ia/docs/templates/task-template.md`.
- Regras completas em `AGENTS.md` §5.

## Gestão de specs

- Specs ativas ficam em `.ia/docs/specs/`, usando status em inglês e data `DD-MM-YYYY`.
- Specs concluídas ficam em `.ia/docs/specs/done/` com status `done` ou `superseded`.