# Spec: Genericizar conteúdo funcional dos artefatos de IA do snippet `fastapi_project`

## 1. Metadados

- **ID da spec**: `fastapi-snippet-genericizar-ia-spec-01-06-2026`
- **Status**: `done`
- **Prioridade**: `high`
- **Tipo**: `refactor`
- **Módulo/área**: `core/management/commands/snippets/fastapi_project/.ia/` + `AGENTS.md`
- **Responsável**: `agente-ia`
- **Solicitante**: `guilherme`
- **Data de criação**: `01-06-2026`
- **Última atualização**: `01-06-2026`

---

## 2. Contexto

O snippet `fastapi_project` é copiado pelo management command Django (`build_projeto.py`) quando um analista invoca o comando para gerar um projeto FastAPI. O **CLI já substitui o nome do projeto** corretamente a partir das configurações Django — portanto referências ao nome "Argus" em títulos e texto corrido não são problema: o CLI as resolve.

O problema real está no **conteúdo funcional** que o CLI não pode substituir automaticamente — informações que descrevem a realidade específica de um projeto concreto e que qualquer novo projeto FastAPI gerado herdaria erroneamente:

- **Lista de módulos de negócio** do Argus hardcoded no `overview.md` (19 módulos: agenda, atendimento, contabilidade, convenio, financeiro, ressarcimento, patrimônio, etc.) — cada projeto tem seus próprios módulos
- **Versões exatas** de stack fixadas no `overview.md` (FastAPI `0.135.0`, Python `3.12.2`, SQLAlchemy `2.*`, etc.) — podem divergir no projeto gerado
- **Referência a task real** do Argus no cabeçalho do `overview.md` (`task-30-05-2026-FpA7kLm2Qx`)
- **`relatorio-arquitetural.md`** (218 linhas): relatório completo de análise arquitetural do Argus — sem valor para um projeto novo que ainda não foi analisado
- **`ia_modules.md`** (79 linhas): estrutura interna do módulo `argus_ia_agent` (Agno Team, mem0, pgvector table names, endpoints fixos) — ausente em qualquer projeto recém-gerado
- **`project-context.md`**: contexto operacional inteiramente do Argus (argus_ia_agent, Agno, Redis session naming, Elasticsearch) — não corresponde ao projeto gerado
- **Restrição absoluta** a `argus_ia_agent/` em `AGENTS.md` §8.1 e `README.md` — esse módulo é específico do Argus; o novo projeto pode não ter módulo de IA, ou tê-lo com outro nome
- **Skills IA** (`adicionar-embeddings`, `nova-tool-ia`, `novo-agente-ia`) com triggers e restrições acopladas a `argus_ia_agent/` como entidade fixa
- **Exceção legada** em `constraints.md` ("acesso direto a `db` em `authentication/routers.py`") — dívida técnica exclusiva do Argus

---

## 3. Objetivo

Tornar o conteúdo funcional dos artefatos de IA correto para **qualquer projeto FastAPI** gerado pelo template, sem depender do contexto do Argus. Isso significa:

- Substituir listas de módulos, versões e configurações específicas por **placeholders guiados** que o analista do projeto preenche pós-geração
- Transformar documentos inteiramente derivados do Argus em **templates vazios com estrutura** para o projeto gerado documentar sua realidade
- Tornar a restrição do módulo de IA **condicional** — aplica-se somente se o projeto tiver esse módulo
- Remover dívidas técnicas e referências a artefatos do Argus que não existem no projeto gerado

As regras operacionais reutilizáveis (RTK, ciclo de task, governança, skills) permanecem intactas.

---

## 4. AS-IS / TO-BE

### 4.1 `AGENTS.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| §3.2 skills IA | triggers citam `argus_ia_agent/` como entidade fixa | genérico: "módulo de IA do projeto (se existir)" |
| §8.1 restrição módulo IA | "Modificar arquivos sob `argus_ia_agent/`" como linha fixa da tabela | linha condicional: "Modificar arquivos sob o módulo de IA/agentes (se existir no projeto)" |

### 4.2 `.ia/README.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Nota de restrição `argus_ia_agent/` | Nota global fixa no cabeçalho | Removida; a restrição condicional fica apenas em `AGENTS.md` §8.1 |
| Referências a `legacy/` em tasks e specs | Descreve diretórios `legacy/` como parte do workflow | Removidas — esses diretórios não existem no snippet |

### 4.3 `overview.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Referência a task | Nota com `task-30-05-2026-FpA7kLm2Qx` no cabeçalho | Removida |
| Stack: versões | Valores exatos (`FastAPI 0.135.0`, `Python 3.12.2`, `SQLAlchemy 2.*`, etc.) | "A confirmar no projeto — verificar `pyproject.toml`" |
| Stack: módulo IA | Linha fixa com `argus_ia_agent`, Agno, mem0, pgvector | Seção condicional: "Se o projeto tiver módulo de IA, documentar aqui" |
| Lista de módulos agregados | 19 módulos de negócio específicos do Argus | Placeholder: "A documentar conforme módulos do projeto" com exemplo de formato |
| Integrações §4 | Detalhes de integração específicos do Argus | Genérico: placeholders por tipo de integração (Django, Flutter, Redis, IA) |

### 4.4 `modules.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Regra de configuração | Cita `argus_ia_agent.config.IaSettings` como exemplo fixo | Genérico: "se o projeto tiver módulo de IA com config própria, mantê-la isolada de `core.config.Settings`" |

### 4.5 `relatorio-arquitetural.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Conteúdo (218 linhas) | Relatório arquitetural completo e específico do Argus | Template vazio com seções guiadas e instruções: "Preencher após análise inicial do projeto gerado" |

### 4.6 `ia_modules.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Conteúdo (79 linhas) | Estrutura interna do `argus_ia_agent` (Agno, mem0, pgvector tables, endpoints) | Placeholder: "Documentar módulo de IA do projeto se existir — estrutura, endpoints, restrições" |

### 4.7 `project-context.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Conteúdo | Contexto operacional inteiro do Argus: argus_ia_agent, Agno Team, mem0, Redis session naming, Elasticsearch | Template guiado: seções por componente (banco, cache, busca, IA, observabilidade) com placeholders |

### 4.8 `security.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Referência IA config | `argus_ia_agent.config.IaSettings` em regra fixa | Removida; substituída por nota genérica: "se houver módulo de IA, manter config isolada" |

### 4.9 `constraints.md`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Exceção legada | "Exceção legada documentada: acesso direto a `db` em `authentication/routers.py`" | Removida (dívida técnica exclusiva do Argus) |

### 4.10 Skills: `adicionar-embeddings`, `nova-tool-ia`, `novo-agente-ia`

| Aspecto | AS-IS | TO-BE |
|---|---|---|
| Trigger/escopo | "módulo Argus IA", `argus_ia_agent/` como entidade fixa | "módulo de IA/embeddings/agentes do projeto (se existir)" |
| Restrição | "sem alterar `argus_ia_agent/`" | "sem alterar o módulo de IA/agentes do projeto" |

---

## 5. Escopo

### Inclui

- `AGENTS.md` (raiz do snippet) — ajustes em §3.2 e §8.1
- `.ia/README.md` — remover nota de restrição e referências a `legacy/`
- `.ia/docs/architecture/overview.md` — versões, módulos, task ref, módulo IA
- `.ia/docs/architecture/modules.md` — regra de config de IA
- `.ia/docs/architecture/relatorio-arquitetural.md` — substituição completa por template
- `.ia/docs/architecture/ia_modules.md` — substituição completa por placeholder
- `.ia/docs/guides/project-context.md` — substituição por template guiado
- `.ia/docs/guides/security.md` — remover ref de config IA específica
- `.ia/docs/guides/constraints.md` — remover exceção legada
- `.ia/skills/adicionar-embeddings/SKILL.md` — genericizar trigger e restrição
- `.ia/skills/nova-tool-ia/SKILL.md` — genericizar trigger e restrição
- `.ia/skills/novo-agente-ia/SKILL.md` — genericizar trigger e restrição

### Não inclui

- Scripts Python das skills (`.py`) — automação independente de conteúdo de projeto
- Skills operacionais e técnicas FastAPI já genéricas
- Templates de tasks/specs/PRD
- Arquivos de código do snippet (`core/`, `authentication/`, `main.py`, `tests/`)
- `docs/guides/patterns.md`, `rules-catalog.md`, `rules-governance.md`, `skills-decision.md` — já genéricos

---

## 6. Critérios de aceite

1. `overview.md` não lista módulos de negócio específicos — usa placeholder com instrução de preenchimento
2. `overview.md` não contém versões hard-coded — usa instrução para verificar `pyproject.toml`
3. `overview.md` não contém referência a `task-30-05-2026-FpA7kLm2Qx`
4. `relatorio-arquitetural.md` e `ia_modules.md` são templates vazios com seções guiadas — zero conteúdo do Argus
5. `project-context.md` é template guiado — zero conteúdo do Argus
6. A restrição de módulo de IA em `AGENTS.md` §8.1 e `README.md` é condicional, não absoluta
7. Skills `adicionar-embeddings`, `nova-tool-ia`, `novo-agente-ia` usam "módulo de IA do projeto (se existir)"
8. Exceção legada removida de `constraints.md`
9. Referência a `argus_ia_agent.config.IaSettings` removida de `security.md` e `modules.md`
10. Todas as regras operacionais (RTK, governança, ciclo de task, skills) permanecem intactas

---

## 7. Restrições e premissas

### Restrições

- **Não alterar** arquivos de código do snippet (`core/`, `authentication/`, `main.py`, `tests/`)
- **Não alterar** scripts Python das skills (`.py`)
- **Não alterar** skills que já são genéricas
- Manter estrutura de diretórios `.ia/` intacta
- Preservar §3–§9 do `AGENTS.md` — apenas ajustes cirúrgicos onde indicado

### Premissas

- O CLI já substitui o nome do projeto nos arquivos copiados — não é escopo desta spec
- O analista que recebe o projeto gerado irá preencher os placeholders com os dados do projeto real usando a skill `atualizar-artefatos-ia`

---

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integrações: `não`
- Segurança/LGPD: `não`
- Testes: `não`
- Documentação: `sim — artefatos .ia/ e AGENTS.md do snippet fastapi_project`

---

## 9. Jobs de implementação

| # | Job | Arquivo(s) | Prioridade | Complexidade |
|---|---|---|---|---|
| 1 | Ajustes cirúrgicos em `AGENTS.md` | `AGENTS.md` | Alta | Baixa |
| 2 | Genericizar `overview.md` | `.ia/docs/architecture/overview.md` | Alta | Média |
| 3 | Substituir `relatorio-arquitetural.md` por template | `.ia/docs/architecture/relatorio-arquitetural.md` | Alta | Baixa |
| 4 | Substituir `ia_modules.md` por placeholder | `.ia/docs/architecture/ia_modules.md` | Alta | Baixa |
| 5 | Ajuste cirúrgico em `modules.md` | `.ia/docs/architecture/modules.md` | Média | Baixa |
| 6 | Substituir `project-context.md` por template guiado | `.ia/docs/guides/project-context.md` | Alta | Baixa |
| 7 | Ajuste cirúrgico em `security.md` | `.ia/docs/guides/security.md` | Média | Baixa |
| 8 | Remover exceção legada de `constraints.md` | `.ia/docs/guides/constraints.md` | Baixa | Baixa |
| 9 | Genericizar skills IA | 3 × `SKILL.md` | Média | Baixa |
| 10 | Ajustes em `README.md` do `.ia/` | `.ia/README.md` | Média | Baixa |

**Total: 10 jobs** — todos independentes, sem dependência de ordem obrigatória.

Ordem recomendada de leitura pelo agente no projeto gerado: Job 1 → 2 → 6 → 3+4 → 5+7+8 → 9 → 10.

---

## 10. Definition of Done

- [ ] `overview.md` sem módulos do Argus, sem versões fixas, sem task ref
- [ ] `relatorio-arquitetural.md` e `ia_modules.md` como templates vazios com seções guiadas
- [ ] `project-context.md` como template guiado
- [ ] Restrição de módulo de IA em `AGENTS.md` §8.1 é condicional
- [ ] Nota de restrição absoluta removida do `README.md` do `.ia/`
- [ ] Skills IA com triggers e restrições genéricas
- [ ] `argus_ia_agent.config.IaSettings` removido de `security.md` e `modules.md`
- [ ] Exceção legada removida de `constraints.md`
- [ ] Regras operacionais (RTK, governança, ciclo de task) intactas em `AGENTS.md`
- [ ] Aprovação do desenvolvedor obtida antes da implementação

---

## 11. Próximos passos

Após aprovação desta spec: criar tasks derivadas em `.ia/docs/tasks/todo/` do blueprint para os 10 jobs, seguindo o fluxo `workflow-demandas → branch-task-aprovada`.
