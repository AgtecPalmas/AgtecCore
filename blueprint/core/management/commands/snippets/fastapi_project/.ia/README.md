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

---

## Configuração do ambiente de desenvolvimento assistido por IA

Esta seção descreve como preparar o ambiente neste projeto FastAPI. Execute os passos na ordem apresentada.

### 1. Instalar o OpenCode

OpenCode é o ambiente de terminal com IA que orquestra os agentes neste projeto.

```bash
# macOS / Linux (recomendado)
curl -fsSL https://opencode.ai/install | bash

# Homebrew
brew install anomalyco/tap/opencode

# npm
npm install -g opencode-ai
```

Após a instalação, inicialize na raiz do repositório:

```bash
cd /caminho/do/projeto
opencode
```

Dentro da sessão OpenCode, execute `/init` para que o agente analise o repositório e registre o `AGENTS.md` existente como contexto ativo.

> Documentação completa: https://opencode.ai/docs

---

### 2. Instalar o RTK

RTK (Rust Token Killer) intercepta comandos shell e os reescreve para versões filtradas, reduzindo 60–90% do consumo de tokens em operações de dev.

```bash
# Homebrew (recomendado)
brew install rtk

# Linux / macOS via script
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

Verificar instalação:

```bash
rtk --version
rtk gain
```

Integrar ao OpenCode (cria hook de interceptação):

```bash
rtk init -g --opencode
```

> Repositório: https://github.com/rtk-ai/rtk

---

### 3. Instalar o Caveman

Caveman ativa o modo de comunicação comprimido nos agentes de IA, reduzindo ~75% dos tokens de saída sem perda de precisão técnica.

```bash
# macOS / Linux / WSL
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
```

O instalador detecta automaticamente os agentes presentes (Claude Code, OpenCode, Codex) e implanta os hooks necessários em cada um.

Modos disponíveis após instalação: `/caveman lite`, `/caveman full` (padrão), `/caveman ultra`.

> Repositório: https://github.com/JuliusBrussee/caveman

---

### 4. Configurar o Obsidian Brain (memória persistente)

O Obsidian Brain integra o agente com um vault Obsidian, permitindo armazenar e consultar contexto de forma persistente entre sessões.

1. Instale o Obsidian: https://obsidian.md/download
2. Crie um vault chamado `DevBrain` (ou nome de sua preferência).
3. Configure a variável de ambiente no projeto:

```bash
OBSIDIAN_DEV_VAULT="CAMINHO_PARA_SEU_VAULT/DevBrain"
```

Após configurar, use as skills `obsidian-sync` para exportar contexto do repositório para o vault e `obsidian-query` para consultar histórico e specs.

---

### 5. Preencher os documentos de arquitetura

Após receber o projeto gerado, preencha os placeholders dos documentos de arquitetura antes de iniciar qualquer demanda assistida:

```
Leia AGENTS.md e preencha os documentos de arquitetura em .ia/docs/architecture/
com a stack confirmada do projeto. Use a skill atualizar-artefatos-ia.
```

O agente irá verificar `pyproject.toml`, `core/config.py`, `core/routers.py` e demais arquivos do projeto para preencher `overview.md`, `relatorio-arquitetural.md` e `modules.md` com os dados reais.

---

## Como escrever prompts para desenvolvimento assistido por IA

A qualidade do resultado entregue pelo agente é diretamente proporcional à qualidade do prompt. Um prompt ruim gera código genérico, ignora a arquitetura do projeto e exige retrabalho. Um prompt bem escrito ativa o contexto correto, respeita o fluxo de tasks e produz código alinhado ao padrão real do repositório.

---

### Prompt ruim — o que evitar

```
Cria um endpoint de listagem para o módulo de contratos
```

**Por que é ruim:**

| Problema | Consequência |
|---|---|
| Sem contexto de origem | Agente não sabe se é feature nova, bugfix ou refactor — não cria task |
| Sem referência à arquitetura | Agente pode criar lógica de negócio no router, ignorar o padrão `use_cases.py` |
| Sem escopo definido | Agente decide sozinho quais arquivos tocar, podendo alterar `core/` |
| Sem pedido de planejamento | Agente vai direto para código sem plano de ação ou critérios de aceite |
| Verbo imperativo direto | Induz o agente a implementar antes de entender — viola o fluxo de task |

---

### Prompt correto — o que fazer

```
O time de produto identificou que o módulo de contratos precisa expor um endpoint
de listagem paginada com filtros por status e data. Siga as regras de AGENTS.md.

Consulte .ia/docs/architecture/overview.md e .ia/docs/architecture/modules.md
para entender o padrão de router → schema → use_case. Crie o planejamento da
demanda com as camadas impactadas (router, schema, use_case, testes), os critérios
de aceite e as skills a usar. Não implemente até a aprovação.
```

**Por que é correto:**

| Elemento | Função |
|---|---|
| Origem da demanda declarada | Agente entende o contexto de negócio sem precisar inferir |
| Referência explícita aos docs de arquitetura | Agente ancora a implementação no padrão real do projeto |
| Referência a `AGENTS.md` | Agente carrega as skills corretas e respeita as restrições |
| Pedido de planejamento com task | Ativa o fluxo de `workflow-demandas` e cria rastreabilidade |
| Camadas listadas explicitamente | Agente sabe exatamente o que carregar antes de implementar |
| "Não implemente até a aprovação" | Preserva o ciclo de revisão humana — agente não avança sozinho |

---

### Anatomia de um prompt bem escrito

```
[ORIGEM]
De onde veio a demanda (produto, cliente, bug reportado, débito técnico).

[OBJETIVO]
O que precisa ser verdade ao final — em termos de comportamento, não de código.

[REFERÊNCIAS]
- Documentação externa relevante (URLs)
- Arquivos internos a consultar primeiro (.ia/docs/*, AGENTS.md)

[RESTRIÇÕES]
Camadas que não devem ser tocadas, compatibilidade necessária, prazo, LGPD.
Lembrete: core/ não deve ser alterado sem autorização explícita.

[INSTRUÇÃO DE FLUXO]
"Crie o planejamento e aguarde aprovação antes de implementar."
ou
"Task já aprovada em .ia/docs/tasks/todo/<hash>.md — execute a implementação."
```

---

### Exemplos adicionais

**Ruim:**
```
Adiciona paginação nos endpoints de listagem
```

**Correto:**
```
O time de produto identificou que endpoints de listagem do módulo `servico` estão
retornando todos os registros sem paginação, causando timeout em produção.

Consulte AGENTS.md e .ia/docs/architecture/overview.md para entender o padrão
adotado de paginação. Crie o planejamento com as camadas impactadas (router,
schema, use_case, testes) e os critérios de aceite antes de implementar.
```

---

**Ruim:**
```
Refatora o módulo de autenticação
```

**Correto:**
```
O módulo `authentication` possui acesso direto ao banco em `routers.py`,
violando a regra RULE-ARCH-002 de .ia/docs/guides/constraints.md.

Siga as regras de AGENTS.md — crie uma task com escopo (apenas os handlers
identificados), plano de ação e critérios de aceite. Não altere arquivos de
`core/` sem autorização explícita. Aguarde aprovação antes de implementar.
```

---

> **Regra geral:** o agente executa melhor quando recebe _contexto_, _restrições_ e _ordem de operações_ — não apenas _o que fazer_. Quanto mais o prompt se parece com um briefing técnico, menos retrabalho haverá.

---

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

---

## Como os agentes usam este contexto

O ponto de entrada para qualquer agente é o arquivo `AGENTS.md` na raiz do repositório. Ele define:

1. **Idioma e stack** — resposta em português, FastAPI + SQLAlchemy + Pydantic v2, PostgreSQL.
2. **Fontes de verdade** — lista explícita de quais arquivos de `.ia/docs/` prevalecem sobre qualquer outra instrução.
3. **Catálogo de skills** — quais skills existem e onde encontrá-las.
4. **Fluxo de tasks** — como criar, executar, aprovar e encerrar uma demanda rastreável.
5. **Comandos de build** — `rtk uv sync`, `rtk task run`, `rtk task lint`, `rtk task test`.
6. **Proibições de segurança** — `git commit/push/rebase/pull` nunca são executados pela IA; `core/` nunca é alterado sem autorização explícita.

**Regra de precedência:** `AGENTS.md` é o ponto de entrada; em caso de conflito, os arquivos de `.ia/docs/` prevalecem.

---

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

---

## Documentação arquitetural

| Arquivo | Conteúdo canônico |
|---|---|
| `overview.md` | Stack confirmada, organização da aplicação, padrão por módulo e regras transversais |
| `modules.md` | Estrutura interna esperada por módulo e regras de acoplamento |
| `ia_modules.md` | Módulo de IA do projeto (se existir) — runtime, agentes, embeddings, endpoints |
| `ia_embeddings.md` | Padrão e especificações para embeddings vetoriais |
| `security.md` | JWT, bcrypt, CORS, LGPD, anonimização de dados sensíveis |
| `relatorio-arquitetural.md` | Relatório factual da arquitetura atual do projeto gerado |

---

## Gestão de tarefas

- Backlog operacional em `.ia/docs/tasks/todo/`.
- Concluídas em `.ia/docs/tasks/done/` com prefixo `done-`.
- Template em `.ia/docs/templates/task-template.md`.
- Regras completas em `AGENTS.md` §5.

## Gestão de specs

- Specs ativas ficam em `.ia/docs/specs/`, usando status em inglês e data `DD-MM-YYYY`.
- Specs concluídas ficam em `.ia/docs/specs/done/` com status `done` ou `superseded`.

---

## Regras de manutenção deste diretório

1. **Não duplicar conteúdo entre arquivos.** Cada regra tem uma fonte canônica. Se uma informação já existe em outro arquivo, aponte para ele.
2. **Não fixar versão de dependências em texto corrido.** Fonte de verdade para versões: `pyproject.toml`.
3. **Manter `AGENTS.md` focado em regras operacionais.** Detalhes de arquitetura ficam em `.ia/docs/`; `AGENTS.md` é apenas o ponto de entrada.
4. **Toda mudança em `.ia/` que envolva múltiplos arquivos deve ter task rastreável** em `tasks/todo/` antes de ser executada.
5. **Scripts Python em `.ia/skills/` não devem ser alterados pela IA sem instrução explícita** do desenvolvedor.
6. **`core/` nunca deve ser alterado pela IA** sem autorização explícita documentada em task aprovada.
