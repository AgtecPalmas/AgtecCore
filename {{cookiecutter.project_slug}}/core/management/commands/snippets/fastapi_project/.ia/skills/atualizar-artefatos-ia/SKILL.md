---
name: atualizar-artefatos-ia
description: Atualiza os artefatos de desenvolvimento assistido por IA do projeto Argus (`.ia/` e `AGENTS.md`) quando há mudanças arquiteturais, novos módulos, novas restrições ou inconsistências detectadas. Use quando o usuário pedir para atualizar documentação IA, corrigir artefatos, ou após uma mudança arquitetural significativa. Também ativa automaticamente quando o contexto menciona "atualizar artefatos", "documentação IA", "artefatos desatualizados" ou arquivos em `.ia/`.
---

# Atualizar Artefatos IA — Argus

# Objetivo
Manter `AGENTS.md`, `.ia/README.md` e artefatos `.ia/` alinhados ao código real, às decisões arquiteturais vigentes e ao contrato de governança do projeto.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- Atualizar apenas artefatos diretamente relacionados à mudança aprovada.
- Documentar somente fatos confirmados por arquivos reais do repositório.
- Preservar o contrato `DD-MM-YYYY`, status canônicos e comandos com prefixo `rtk`.
- Não registrar credenciais, caminhos pessoais ou valores reais de ambiente.

## Inventário de artefatos

| Arquivo | Propósito | Quem usa |
|---|---|---|
| `.ia/README.md` | **Entry point para LLMs** — estrutura, routing (intenção → skill), guia de carregamento | Todo agente no cold start |
| `.ia/docs/architecture/relatorio-arquitetural.md` | **Fonte de verdade principal** — estado atual completo | Todos os agentes |
| `.ia/docs/architecture/overview.md` | Índice de navegação dos artefatos | Orientação rápida |
| `.ia/docs/architecture/modules.md` | Módulos ativos e responsabilidades | Novos módulos |
| `.ia/docs/architecture/ia_modules.md` | Arquitetura do módulo `argus_ia_agent` | Demandas IA |
| `.ia/docs/architecture/security.md` | JWT, LGPD, CORS, middlewares | Segurança |
| `.ia/docs/guides/patterns.md` | Padrões obrigatórios de implementação | Toda implementação |
| `.ia/docs/guides/rules-catalog.md` | Catálogo canônico de rules (`rule_id`) | Governança de instruções |
| `.ia/docs/guides/rules-governance.md` | Protocolo de precedência, conflito e quality gate | Governança de instruções |
| `.ia/docs/guides/skills-decision.md` | Matriz canônica de decisão e desempate de skills | Execução de agentes |
| `.ia/docs/testing/strategy.md` | Estratégia de testes (pytest + TestContainers) | Testes |
| `.ia/docs/guides/project-context.md` | Contexto operacional para agentes | Orientação de agentes |
| `.ia/docs/guides/constraints.md` | Restrições técnicas obrigatórias | Toda implementação |
| `AGENTS.md` | Guia geral para todos os agentes | Todos os agentes |
| `.ia/docs/specs/` | Especificações técnicas em andamento | Planejamento e execução |
| `.ia/docs/tasks/todo/` | Registro operacional das demandas ativas | Rastreabilidade |

## Quando atualizar cada artefato

| Evento | Artefatos a atualizar |
|---|---|
| Novo módulo FastAPI criado | `modules.md`, `relatorio-arquitetural.md` |
| Nova versão do Python/lib | `relatorio-arquitetural.md`, `docs/guides/project-context.md` |
| Novo agente/tool IA | `ia_modules.md`, `relatorio-arquitetural.md` |
| Nova restrição técnica | `docs/guides/constraints.md`, `AGENTS.md` |
| Novo conflito de rules | `rules-catalog.md`, `rules-governance.md`, artefato afetado |
| Mudança em decisão de skills | `AGENTS.md`, `README.md`, `skills-decision.md`, `rules-catalog.md` (se impactar `rule_id`) |
| Mudança arquitetural | `relatorio-arquitetural.md`, `overview.md` |
| Novo padrão de implementação | `patterns.md` |
| Mudança na estratégia de testes | `strategy.md` |
| Mudança de segurança | `security.md`, `relatorio-arquitetural.md` |

## Checklist de atualização

- [ ] Ler o artefato atual antes de modificar
- [ ] Identificar qual informação está desatualizada ou ausente
- [ ] Verificar se a mudança está refletida no `relatorio-arquitetural.md` (fonte de verdade)
- [ ] Atualizar o(s) artefato(s) afetado(s) de forma consistente
- [ ] Não duplicar informação entre artefatos — manter `relatorio-arquitetural.md` como referência
- [ ] Atualizar `rule_id` no catálogo canônico quando houver criação/remoção/ajuste de rule
- [ ] Garantir consistência entre `AGENTS.md` e `.ia/docs/guides/skills-decision.md` para matriz de skills
- [ ] Em refatoração de skills, preservar seções `## Padrão ...` e exemplos de código
- [ ] Criar task em `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md` se for mudança relevante
- [ ] Ao concluir: mover task para `done/` com prefixo `done-`

## Regras de qualidade dos artefatos

- **Anti-alucinação**: só documentar o que está implementado no código real
- **Rastreabilidade**: citar paths de arquivos reais como fonte
- **Brevidade**: artefatos de contexto devem ser concisos, não enciclopédicos
- **Hierarquia clara**: `relatorio-arquitetural.md` é a fonte; os demais são complementos
- **Sem duplicidade**: se dois artefatos dizem a mesma coisa, um deles é redundante

## Restrições de segurança (nunca violar)

- Nunca registrar API keys, senhas, secrets ou credenciais em artefatos
- Nunca registrar conexões reais de banco ou URIs de produção
- Referenciar variáveis de ambiente por nome, não por valor

## Após atualizar

1. Listar todos os arquivos modificados
2. Descrever o que mudou e por quê
3. Aguardar revisão do desenvolvedor antes de qualquer commit
4. Renomear task para `done-task-*` ao concluir
