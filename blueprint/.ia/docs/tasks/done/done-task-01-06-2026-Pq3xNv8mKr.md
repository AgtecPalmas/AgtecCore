# Tarefa: Ajustes cirúrgicos em AGENTS.md do snippet fastapi_project

## 1. Metadados

- ID da task: `task-01-06-2026-Pq3xNv8mKr`
- Status da task: `done`
- Prioridade: `high`
- Tipo: `refactor`
- Modulo/area: `core/management/commands/snippets/fastapi_project/`
- Responsavel: `agente-ia`
- Solicitante: `guilherme`
- Data de criacao: `01-06-2026`
- Ultima atualizacao: `01-06-2026`

## 2. Referencias

- Spec/PRD: `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`
- TechSpec: `nao_se_aplica`
- Task relacionada: `task-01-06-2026-Hb7wYt2cLe` (Job 2 — overview.md)
- Board/issue externa: `nao_se_aplica`
- Fontes consultadas:
  - `core/management/commands/snippets/fastapi_project/AGENTS.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `AGENTS.md` do snippet contém dois pontos de acoplamento funcional com o projeto Argus que o CLI não substitui automaticamente: (1) os triggers das skills de IA citam `argus_ia_agent/` como entidade fixa; (2) a tabela §8.1 lista "Modificar arquivos sob `argus_ia_agent/`" como operação restrita absoluta. Projetos gerados sem módulo de IA receberão uma restrição sem sentido e skills com gatilhos incorretos.

## 4. Objetivo

Tornar os dois pontos de acoplamento condicionais e genéricos, preservando todas as demais regras operacionais intactas.

## 5. Escopo

- Inclui:
  - `AGENTS.md` §3.2: atualizar descrição das skills `adicionar-embeddings`, `nova-tool-ia`, `novo-agente-ia` — substituir `argus_ia_agent/` por "módulo de IA do projeto (se existir)"
  - `AGENTS.md` §8.1: tornar a linha de restrição do módulo de IA condicional — "Modificar arquivos sob o módulo de IA/agentes (se existir no projeto)"
- Nao inclui:
  - Qualquer outra seção do `AGENTS.md`
  - Arquivos de código do snippet

## 6. Criterios de aceite

1. §3.2: as três skills de IA não citam `argus_ia_agent/` como entidade fixa
2. §8.1: a restrição do módulo de IA usa linguagem condicional
3. Todas as demais seções (§1–§9) permanecem inalteradas

## 7. Restricoes e premissas

- Restricoes:
  - Alterar somente `AGENTS.md` — nenhum outro arquivo
  - Não reformatar seções não afetadas
- Premissas:
  - O CLI substitui o nome do projeto; esta task trata somente do conteúdo funcional

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — AGENTS.md do snippet fastapi_project`

## 9. Plano de execucao

1. Ler `AGENTS.md` do snippet
2. Localizar as três entradas de skills de IA em §3.2 e atualizar descrições
3. Localizar linha `argus_ia_agent/` na tabela §8.1 e torná-la condicional
4. Verificar que nenhuma outra linha foi alterada

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/AGENTS.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] §3.2 sem referência a `argus_ia_agent/` como entidade fixa
- [ ] §8.1 com restrição de módulo de IA condicional
- [ ] Demais seções intactas
- [ ] Aprovação obtida

## 13. Fechamento

- Riscos residuais: `nenhum identificado`
- Proximos passos: `Jobs 2–10 independentes`

## Descricao da solucao implementada

(Pendente — preencher ao concluir)

## Trade-offs

(Pendente — preencher ao concluir)

## Arquivos alterados

(Pendente — preencher ao concluir)
