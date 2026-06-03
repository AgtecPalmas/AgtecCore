# Tarefa: Genericizar overview.md do snippet fastapi_project

## 1. Metadados

- ID da task: `task-01-06-2026-Hb7wYt2cLe`
- Status da task: `done`
- Prioridade: `high`
- Tipo: `refactor`
- Modulo/area: `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/`
- Responsavel: `agente-ia`
- Solicitante: `guilherme`
- Data de criacao: `01-06-2026`
- Ultima atualizacao: `01-06-2026`

## 2. Referencias

- Spec/PRD: `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`
- TechSpec: `nao_se_aplica`
- Task relacionada: `task-01-06-2026-Pq3xNv8mKr` (Job 1 — AGENTS.md)
- Board/issue externa: `nao_se_aplica`
- Fontes consultadas:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/overview.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `overview.md` é a fonte de verdade canônica de arquitetura referenciada em `AGENTS.md` §2. Atualmente contém: (a) nota com referência a uma task específica do Argus (`task-30-05-2026-FpA7kLm2Qx`); (b) versões exatas de stack hard-coded (FastAPI `0.135.0`, Python `3.12.2`, etc.); (c) módulo de IA do Argus como linha fixa da stack; (d) lista de 19 módulos de negócio do Argus; (e) integrações com detalhes específicos do Argus. Qualquer projeto gerado herdaria um panorama arquitetural falso.

## 4. Objetivo

Reescrever o `overview.md` para descrever a arquitetura genérica do snippet (main.py, core/routers.py, padrão por módulo) usando placeholders instrucionais onde o projeto gerado precisa preencher sua realidade.

## 5. Escopo

- Inclui:
  - Remover nota com `task-30-05-2026-FpA7kLm2Qx` do cabeçalho
  - Substituir versões exatas da stack por "A confirmar no projeto — verificar `pyproject.toml`"
  - Substituir linha do módulo de IA por seção condicional com placeholder
  - Substituir lista de 19 módulos por placeholder com instrução e exemplo de formato
  - Genericizar §4 (integrações) com placeholders por tipo
  - Manter seções §3 (padrão por módulo), §5 (regras transversais) e §6 (pontos de atenção) — já são genéricos
- Nao inclui:
  - Outros arquivos de arquitetura
  - Código do snippet

## 6. Criterios de aceite

1. Nenhuma referência a `task-30-05-2026-FpA7kLm2Qx`
2. Versões da stack são placeholders, não valores exatos
3. Lista de módulos é instrução de preenchimento, não os 19 módulos do Argus
4. Módulo de IA é seção condicional, não linha fixa
5. §3, §5 e §6 intactos

## 7. Restricoes e premissas

- Restricoes:
  - Alterar somente `overview.md`
  - Manter a estrutura de seções numeradas (§1–§6)
- Premissas:
  - Analista preenche placeholders após receber o projeto gerado usando `atualizar-artefatos-ia`

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — overview.md do snippet fastapi_project`

## 9. Plano de execucao

1. Ler `overview.md` completo
2. Remover nota de task do cabeçalho
3. Substituir §1 (stack) — versões e módulo de IA
4. Substituir §2 (organização) — lista de módulos
5. Substituir §4 (integrações) — genericizar com placeholders
6. Verificar §3, §5, §6 intactos

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/overview.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Sem referência a task específica do Argus
- [ ] Sem versões hard-coded na stack
- [ ] Lista de módulos substituída por placeholder instrucional
- [ ] Módulo de IA condicional
- [ ] §3, §5, §6 intactos
- [ ] Aprovação obtida

## 13. Fechamento

- Riscos residuais: `nenhum identificado`
- Proximos passos: `Jobs restantes independentes`

## Descricao da solucao implementada

(Pendente — preencher ao concluir)

## Trade-offs

(Pendente — preencher ao concluir)

## Arquivos alterados

(Pendente — preencher ao concluir)
