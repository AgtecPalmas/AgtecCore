# Tarefa: Substituir project-context.md por template guiado

## 1. Metadados

- ID da task: `task-01-06-2026-Fn8cBx3wSd`
- Status da task: `done`
- Prioridade: `high`
- Tipo: `refactor`
- Modulo/area: `core/management/commands/snippets/fastapi_project/.ia/docs/guides/`
- Responsavel: `agente-ia`
- Solicitante: `guilherme`
- Data de criacao: `01-06-2026`
- Ultima atualizacao: `01-06-2026`

## 2. Referencias

- Spec/PRD: `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`
- TechSpec: `nao_se_aplica`
- Task relacionada: `nao_se_aplica`
- Board/issue externa: `nao_se_aplica`
- Fontes consultadas:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/guides/project-context.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `project-context.md` é camada R1 de restrições operacionais — lido por agentes em toda demanda. Atualmente todo o seu conteúdo é do Argus: `argus_ia_agent`, Agno Team, mem0, Redis com session naming específico (`agno_redis_db`), Elasticsearch. Qualquer projeto gerado receberá contexto operacional de um sistema completamente diferente.

## 4. Objetivo

Substituir o conteúdo por um template guiado por componente (banco, cache, busca, IA, observabilidade, git), com placeholders e instruções para o analista descrever a realidade do projeto gerado. Manter apenas as diretrizes de git que são universais.

## 5. Escopo

- Inclui:
  - Reescrita completa com seções por componente e placeholders instrucionais
  - Manter a diretriz global de git (nunca executar git commit diretamente)
  - Remover todo conteúdo específico do Argus (argus_ia_agent, Agno, mem0, Redis session naming, regra NUNCA do argus_ia_agent)
- Nao inclui:
  - Outros arquivos do guia

## 6. Criterios de aceite

1. Nenhum conteúdo do Argus (argus_ia_agent, Agno, mem0, etc.) no arquivo resultante
2. Seções por componente com placeholders e instruções de preenchimento
3. Diretriz universal de git mantida

## 7. Restricoes e premissas

- Restricoes:
  - Manter o mesmo nome de arquivo e localização
  - Manter a nota de precedência R1
- Premissas:
  - Analista preenche os placeholders ao assumir o projeto gerado

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — project-context.md do snippet`

## 9. Plano de execucao

1. Ler o arquivo atual para identificar estrutura e diretrizes universais
2. Escrever novo conteúdo: cabeçalho R1 + seções por componente com placeholders + diretriz git
3. Verificar ausência de conteúdo do Argus

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/guides/project-context.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Zero conteúdo do Argus no arquivo
- [ ] Seções por componente com placeholders instrucionais
- [ ] Diretriz universal de git mantida
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
