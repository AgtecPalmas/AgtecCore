# Tarefa: Ajuste cirúrgico em modules.md do snippet fastapi_project

## 1. Metadados

- ID da task: `task-01-06-2026-Vm4pEi0qCy`
- Status da task: `done`
- Prioridade: `medium`
- Tipo: `refactor`
- Modulo/area: `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/`
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
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/modules.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `modules.md` é majoritariamente genérico (padrão por módulo, regras de acoplamento), mas a seção "Regra de Configuração por Módulo" cita explicitamente `argus_ia_agent.config.IaSettings` como o exemplo canônico de settings isolados para módulo de IA. Isso amarra a regra a um módulo específico do Argus.

## 4. Objetivo

Generalizar a regra de configuração de módulo de IA, removendo a referência explícita ao `argus_ia_agent.config.IaSettings` e mantendo apenas o princípio genérico.

## 5. Escopo

- Inclui:
  - Seção "Regra de Configuração por Módulo" — substituir o "Estado atual aprovado" específico por princípio genérico
- Nao inclui:
  - Demais seções do `modules.md` (já genéricas)
  - Outros arquivos

## 6. Criterios de aceite

1. Nenhuma referência a `argus_ia_agent.config.IaSettings` no arquivo
2. A regra de isolamento de settings de IA permanece como princípio genérico
3. Demais seções intactas

## 7. Restricoes e premissas

- Restricoes:
  - Alterar somente a seção afetada
- Premissas:
  - O princípio de isolamento de settings é válido para qualquer projeto com módulo de IA

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — modules.md do snippet`

## 9. Plano de execucao

1. Ler `modules.md`
2. Localizar seção "Regra de Configuração por Módulo"
3. Substituir "Estado atual aprovado" específico por princípio genérico
4. Verificar demais seções intactas

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/modules.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Sem referência a `argus_ia_agent.config.IaSettings`
- [ ] Princípio genérico de isolamento de settings mantido
- [ ] Demais seções intactas
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
