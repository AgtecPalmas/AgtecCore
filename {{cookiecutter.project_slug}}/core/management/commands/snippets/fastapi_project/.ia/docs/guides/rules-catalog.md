# Catálogo Canônico de Rules (IA Multi-LLM)

## Objetivo

Consolidar as rules ativas do projeto em formato único, com identificador (`rule_id`), precedência e fonte canônica.

## Precedência (camadas)

- `R0`: `AGENTS.md`
- `R1`: `.ia/docs/guides/constraints.md` + `.ia/docs/guides/project-context.md`
- `R2`: `.ia/docs/guides/*`
- `R3`: `.ia/docs/architecture/*` + `.ia/docs/testing/*`
- `R4`: `.ia/docs/templates/*`
- `R5`: `.ia/skills/*/SKILL.md`

Em conflito, vence a camada superior.

## Regras Canônicas

| rule_id | Regra objetiva | Camada canônica | Fonte canônica | Status |
| --- | --- | --- | --- | --- |
| `RULE-GOV-001` | A governança de instruções segue precedência `R0..R5`. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-GOV-002` | Conflitos devem ser resolvidos no artefato de menor precedência, sem duplicação ad hoc. | `R2` | `.ia/docs/guides/rules-governance.md` | `ativo` |
| `RULE-LANG-001` | Respostas padrão em português pt-BR, salvo necessidade explícita de outro idioma. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-WFLOW-001` | Toda demanda assistida por IA deve começar com planejamento explícito em spec ou task, conforme escopo. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-WFLOW-002` | Implementação nunca começa só com spec; qualquer execução exige task em `.ia/docs/tasks/todo/` com aprovação explícita. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-WFLOW-003` | Ao concluir, task deve conter fechamento obrigatório e ser renomeada para `done-task-...` em `done/`. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-GIT-001` | IA não pode executar `git commit`. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-MULTILLM-001` | Artefatos de instrução devem permanecer vendor-neutral, sem lock-in em um único fornecedor de LLM. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-SKILL-001` | Toda demanda deve declarar skill principal de acordo com a matriz canônica de decisão. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-SKILL-002` | Em sobreposição de skills, o desempate deve seguir protocolo canônico (artefato final, especialização, precedência `R0..R5`). | `R0` | `AGENTS.md` | `ativo` |
| `RULE-ONESHOT-001` | Em refatoração de skills, preservar padrões One-Shot por camada e exemplos em seções `## Padrão ...`. | `R0` | `AGENTS.md` | `ativo` |
| `RULE-ARCH-001` | Router deve apenas orquestrar; regra de negócio fica em `use_cases`. | `R2` | `.ia/docs/guides/patterns.md` | `ativo` |
| `RULE-ARCH-002` | Router não deve acessar DB diretamente; acesso a dados deve passar por `use_cases`. | `R1` | `.ia/docs/guides/constraints.md` | `ativo` |
| `RULE-ARCH-003` | Use cases devem herdar de `BaseUseCases` no padrão do projeto. | `R2` | `.ia/docs/guides/patterns.md` | `ativo` |
| `RULE-MODEL-001` | Models devem herdar de `CoreBase` e não redeclarar campos base. | `R2` | `.ia/docs/guides/patterns.md` | `ativo` |
| `RULE-ASYNC-001` | Operações I/O síncronas são proibidas. | `R1` | `.ia/docs/guides/constraints.md` | `ativo` |
| `RULE-DEP-001` | Novas dependências exigem aprovação arquitetural prévia. | `R1` | `.ia/docs/guides/constraints.md` | `ativo` |
| `RULE-ROUTE-001` | Rotas devem usar prefixo `/api/v1/` e `kebab-case`. | `R2` | `.ia/docs/guides/patterns.md` | `ativo` |
| `RULE-ROUTE-002` | Endpoints novos devem preferir barra final (`/`); legado mantém padrão atual até migração planejada. | `R2` | `.ia/docs/guides/patterns.md` | `ativo` |
| `RULE-FILIADO-001` | Endpoint self-service de filiado não recebe `filiado_id`; resolução ocorre no `use_case`. | `R2` | `.ia/docs/guides/regra-endpoint-filiado-autenticado.md` | `ativo` |
| `RULE-TEST-001` | Testes devem usar TestContainers e execução com ambiente preparado (docker/venv/deps). | `R0` | `AGENTS.md` | `ativo` |
| `RULE-TEST-002` | Arquivos de teste devem seguir `tests/tests_<modulo>/test_*.py`. | `R3` | `.ia/docs/testing/strategy.md` | `ativo` |
| `RULE-ANTIHAL-001` | Sem evidência no repositório: declarar “não encontrei” e pedir mínimo contexto. | `R1` | `.ia/docs/guides/constraints.md` | `ativo` |
| `RULE-ANTIHAL-002` | Não inventar módulos, rotas, contratos ou comportamentos não documentados. | `R1` | `.ia/docs/guides/constraints.md` | `ativo` |
| `RULE-EXC-001` | Exceção legada: há acesso direto a `db` no router de autenticação; não replicar esse padrão em novos módulos. | `R2` | `.ia/docs/guides/rules-governance.md` | `legado-controlado` |

## Evidências e rastreabilidade

- `RULE-EXC-001` evidência:
  - `authentication/routers.py` (`await db.commit()`, `await db.refresh(current_user)`).
- `RULE-ROUTE-002` evidência:
  - estado misto de rotas no projeto (com e sem barra final).
- `RULE-SKILL-001` e `RULE-SKILL-002` evidência:
  - `AGENTS.md` (seções de seleção, matriz e desempate de skills).
  - `.ia/docs/guides/skills-decision.md`.
- `RULE-ONESHOT-001` evidência:
  - seções `## Padrão ...` existentes em `.ia/skills/*/SKILL.md`.

## Uso obrigatório em specs/tasks/templates

- Sempre que possível, referenciar `rule_id` aplicadas na decisão técnica.
- Em conflito entre regras, registrar explicitamente os `rule_id` envolvidos e a resolução adotada.
