# Tarefa: Ajustes em README.md do .ia/ do snippet fastapi_project

## 1. Metadados

- ID da task: `task-01-06-2026-Cs0fAp5kTv`
- Status da task: `done`
- Prioridade: `medium`
- Tipo: `refactor`
- Modulo/area: `core/management/commands/snippets/fastapi_project/.ia/`
- Responsavel: `agente-ia`
- Solicitante: `guilherme`
- Data de criacao: `01-06-2026`
- Ultima atualizacao: `01-06-2026`

## 2. Referencias

- Spec/PRD: `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`
- TechSpec: `nao_se_aplica`
- Task relacionada: `task-01-06-2026-Pq3xNv8mKr` (Job 1), `task-01-06-2026-Xe6uNm1jRb` (Job 9)
- Board/issue externa: `nao_se_aplica`
- Fontes consultadas:
  - `core/management/commands/snippets/fastapi_project/.ia/README.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `README.md` do `.ia/` é o índice do pacote de governança. Contém dois problemas: (1) nota global de restrição absoluta ao `argus_ia_agent/` no cabeçalho — tornando uma restrição condicional em regra fixa para todos os projetos; (2) descrição de diretórios `legacy/` em tasks e specs que não existem no snippet, gerando expectativa de estrutura ausente.

## 4. Objetivo

Remover a nota de restrição absoluta ao `argus_ia_agent/` do cabeçalho e as referências a diretórios `legacy/` que não existem no snippet, mantendo o índice de skills, documentação e gestão de tarefas intactos.

## 5. Escopo

- Inclui:
  - Cabeçalho: remover nota `> **Restrição global**: nenhuma skill deve criar, editar, mover ou remover arquivos sob argus_ia_agent/...`
  - Seção "Workflows documentais": remover referências a `legacy/` em tasks e specs
- Nao inclui:
  - Tabela de skills
  - Tabela de scripts de automação
  - Seções de documentação arquitetural e gestão de tarefas (exceto referências legacy)

## 6. Criterios de aceite

1. Nota de restrição absoluta `argus_ia_agent/` removida do cabeçalho
2. Referências a `legacy/` removidas da seção de workflows documentais
3. Tabela de skills e scripts intactos
4. Estrutura geral do README intacta

## 7. Restricoes e premissas

- Restricoes:
  - Alterar somente os trechos indicados
  - Não reformatar tabelas ou outras seções
- Premissas:
  - Esta task deve ser executada por último (Job 10) — depende dos demais jobs para que o README reflita o estado final correto dos artefatos

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — README.md do .ia/ do snippet`

## 9. Plano de execucao

1. Ler `README.md` completo
2. Remover nota de restrição absoluta do cabeçalho
3. Remover referências a `legacy/` nos workflows documentais
4. Verificar tabelas e demais seções intactas

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/README.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Nota de restrição absoluta `argus_ia_agent/` removida
- [ ] Referências a `legacy/` removidas
- [ ] Tabelas de skills e scripts intactas
- [ ] Aprovação obtida

## 13. Fechamento

- Riscos residuais: `nenhum identificado`
- Proximos passos: `Todos os 10 jobs concluídos — spec pode ser movida para done/`

## Descricao da solucao implementada

(Pendente — preencher ao concluir)

## Trade-offs

(Pendente — preencher ao concluir)

## Arquivos alterados

(Pendente — preencher ao concluir)
