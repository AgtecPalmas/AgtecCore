# Tarefa: Substituir ia_modules.md por placeholder

## 1. Metadados

- ID da task: `task-01-06-2026-Gk1oZr4bTx`
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
- Task relacionada: `task-01-06-2026-Dj5nAu9sWf` (Job 3 — relatorio-arquitetural.md, mesma natureza)
- Board/issue externa: `nao_se_aplica`
- Fontes consultadas:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/ia_modules.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `ia_modules.md` tem 79 linhas descrevendo internos do módulo `argus_ia_agent`: Agno Team como runtime, subagentes especializados, mem0, pgvector, nomes específicos de tabelas (`iaschemaembedding`, `ia_content_embeddings`), endpoint fixo de chat. Qualquer projeto gerado sem esse módulo receberá documentação de um sistema inexistente. Projetos que criarem seu próprio módulo de IA precisarão substituir tudo de qualquer forma.

## 4. Objetivo

Substituir o conteúdo por um placeholder com instrução clara: "Se o projeto tiver módulo de IA, documentar aqui a estrutura, runtime, memória, embeddings e endpoints."

## 5. Escopo

- Inclui:
  - Reescrita completa do arquivo com placeholder instrucional e estrutura de seções sugerida
- Nao inclui:
  - Qualquer conteúdo do Argus no resultado
  - Outros arquivos

## 6. Criterios de aceite

1. Nenhum conteúdo específico do Argus/argus_ia_agent no arquivo resultante
2. Arquivo tem instrução de preenchimento e estrutura sugerida para documentar módulo de IA genérico

## 7. Restricoes e premissas

- Restricoes:
  - Manter o mesmo nome de arquivo e localização
  - Alterar somente este arquivo
- Premissas:
  - Projetos sem módulo de IA podem manter o arquivo vazio ou removê-lo manualmente

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — ia_modules.md do snippet`

## 9. Plano de execucao

1. Ler o arquivo atual
2. Escrever novo conteúdo: cabeçalho instrucional + seções sugeridas (runtime, agentes, memória, embeddings, endpoints, restrições)
3. Verificar ausência de conteúdo do Argus

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/ia_modules.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Zero conteúdo do Argus/argus_ia_agent no arquivo
- [ ] Placeholder com estrutura sugerida para módulo de IA genérico
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
