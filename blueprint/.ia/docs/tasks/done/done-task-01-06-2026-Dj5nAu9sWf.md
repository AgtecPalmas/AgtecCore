# Tarefa: Substituir relatorio-arquitetural.md por template vazio

## 1. Metadados

- ID da task: `task-01-06-2026-Dj5nAu9sWf`
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
- Task relacionada: `task-01-06-2026-Gk1oZr4bTx` (Job 4 — ia_modules.md, mesma natureza)
- Board/issue externa: `nao_se_aplica`
- Fontes consultadas:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/relatorio-arquitetural.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `relatorio-arquitetural.md` tem 218 linhas descrevendo em detalhes a arquitetura do projeto Argus: módulos, stack, pontos críticos, restrições específicas. Um projeto recém-gerado não tem arquitetura a relatar — o arquivo entregaria ao analista um relatório falso de um projeto que não é o dele.

## 4. Objetivo

Substituir o conteúdo completo por um template vazio com as seções estruturadas e instruções de preenchimento, para que o analista documente a arquitetura real do projeto gerado.

## 5. Escopo

- Inclui:
  - Reescrita completa do arquivo mantendo o mesmo nome e localização
  - Estrutura com seções: contexto do projeto, stack confirmada, organização da aplicação, módulos, integrações, pontos de atenção, restrições operacionais
  - Cada seção com instrução clara de preenchimento e exemplo mínimo de formato
- Nao inclui:
  - Qualquer conteúdo específico do Argus no template resultante
  - Outros arquivos

## 6. Criterios de aceite

1. Nenhum conteúdo específico do Argus no arquivo resultante
2. Arquivo tem estrutura com seções guiadas úteis para qualquer projeto FastAPI
3. Cada seção tem instrução de preenchimento legível por um analista

## 7. Restricoes e premissas

- Restricoes:
  - Manter o mesmo nome de arquivo (`relatorio-arquitetural.md`) e localização
  - Alterar somente este arquivo
- Premissas:
  - Analista preenche as seções após análise do projeto gerado

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — relatorio-arquitetural.md do snippet`

## 9. Plano de execucao

1. Ler o arquivo atual para mapear as seções existentes
2. Escrever novo conteúdo: cabeçalho instrucional + seções genéricas com placeholders
3. Verificar que nenhum conteúdo do Argus permanece

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/relatorio-arquitetural.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Zero conteúdo do Argus no arquivo
- [ ] Seções guiadas com instruções de preenchimento
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
