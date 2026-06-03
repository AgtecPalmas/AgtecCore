# Tarefa: Genericizar skills de IA do snippet fastapi_project

## 1. Metadados

- ID da task: `task-01-06-2026-Xe6uNm1jRb`
- Status da task: `done`
- Prioridade: `medium`
- Tipo: `refactor`
- Modulo/area: `core/management/commands/snippets/fastapi_project/.ia/skills/`
- Responsavel: `agente-ia`
- Solicitante: `guilherme`
- Data de criacao: `01-06-2026`
- Ultima atualizacao: `01-06-2026`

## 2. Referencias

- Spec/PRD: `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`
- TechSpec: `nao_se_aplica`
- Task relacionada: `task-01-06-2026-Pq3xNv8mKr` (Job 1 — AGENTS.md, mesma natureza)
- Board/issue externa: `nao_se_aplica`
- Fontes consultadas:
  - `core/management/commands/snippets/fastapi_project/.ia/skills/adicionar-embeddings/SKILL.md`
  - `core/management/commands/snippets/fastapi_project/.ia/skills/nova-tool-ia/SKILL.md`
  - `core/management/commands/snippets/fastapi_project/.ia/skills/novo-agente-ia/SKILL.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

As três skills de IA do snippet têm triggers e restrições que citam `argus_ia_agent/` como entidade fixa: "sem alterar `argus_ia_agent/`". Projetos sem esse módulo receberão skills com restrições sem referente. A correção é usar linguagem condicional genérica em todos os três arquivos.

## 4. Objetivo

Substituir todas as referências a `argus_ia_agent/` e "Argus IA" nos três `SKILL.md` por "módulo de IA/agentes do projeto (se existir)", mantendo a estrutura e demais conteúdos das skills.

## 5. Escopo

- Inclui:
  - `.ia/skills/adicionar-embeddings/SKILL.md`
  - `.ia/skills/nova-tool-ia/SKILL.md`
  - `.ia/skills/novo-agente-ia/SKILL.md`
  - Apenas as ocorrências de `argus_ia_agent/` e "Argus IA" em triggers e restrições
- Nao inclui:
  - Scripts Python (`.py`) das skills
  - Demais skills do snippet

## 6. Criterios de aceite

1. Nenhuma referência a `argus_ia_agent/` como entidade fixa nos três arquivos
2. Nenhuma referência a "Argus IA" como entidade fixa
3. Restrição usa linguagem condicional: "módulo de IA/agentes do projeto (se existir)"
4. Estrutura e demais conteúdos das skills intactos

## 7. Restricoes e premissas

- Restricoes:
  - Alterar somente os três `SKILL.md` listados
  - Não alterar scripts `.py`
- Premissas:
  - O CLI substitui o nome do projeto; esta task trata apenas do conteúdo funcional das restrições

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — 3 SKILL.md do snippet`

## 9. Plano de execucao

1. Ler os três SKILL.md
2. Identificar todas as ocorrências de `argus_ia_agent/` e "Argus IA"
3. Substituir por linguagem genérica condicional em cada arquivo
4. Verificar estrutura restante intacta

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/skills/adicionar-embeddings/SKILL.md`
  - `core/management/commands/snippets/fastapi_project/.ia/skills/nova-tool-ia/SKILL.md`
  - `core/management/commands/snippets/fastapi_project/.ia/skills/novo-agente-ia/SKILL.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Sem `argus_ia_agent/` fixo nos três SKILL.md
- [ ] Sem "Argus IA" fixo nos três SKILL.md
- [ ] Restrição condicional genérica inserida
- [ ] Estrutura das skills intacta
- [ ] Aprovação obtida

## 13. Fechamento

- Riscos residuais: `nenhum identificado`
- Proximos passos: `Job 10 — README .ia/`

## Descricao da solucao implementada

(Pendente — preencher ao concluir)

## Trade-offs

(Pendente — preencher ao concluir)

## Arquivos alterados

(Pendente — preencher ao concluir)
