# Tarefa: Ajuste cirúrgico em security.md do snippet fastapi_project

## 1. Metadados

- ID da task: `task-01-06-2026-Qr2vJk7nMa`
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
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/security.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `security.md` é majoritariamente genérico e de alta qualidade (JWT, bcrypt, CORS, LGPD). O único ponto de acoplamento funcional é a seção "Configuração e Segredos", que cita `argus_ia_agent.config.IaSettings` como exemplo de config de IA isolada — tornando a regra atrelada a um módulo específico do Argus.

## 4. Objetivo

Remover a referência a `argus_ia_agent.config.IaSettings` substituindo-a por princípio genérico de isolamento de configuração de IA, mantendo todas as demais boas práticas de segurança intactas.

## 5. Escopo

- Inclui:
  - Seção "Configuração e Segredos": remover linha `argus_ia_agent.config.IaSettings` e substituir por nota genérica
- Nao inclui:
  - Nenhuma outra seção do arquivo (JWT, bcrypt, LGPD, CORS, boas práticas)

## 6. Criterios de aceite

1. Nenhuma referência a `argus_ia_agent.config.IaSettings` no arquivo
2. Princípio de isolamento de config de IA mantido como nota genérica
3. Todas as demais seções intactas

## 7. Restricoes e premissas

- Restricoes:
  - Alterar somente a linha afetada na seção "Configuração e Segredos"
- Premissas:
  - As variáveis de ambiente `KEY_ANONYMIZATION_CPF` e `IV_ANONYMIZATION_CPF` são mantidas como boas práticas do snippet (não são específicas do Argus)

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — security.md do snippet`

## 9. Plano de execucao

1. Ler `security.md`
2. Localizar referência a `argus_ia_agent.config.IaSettings`
3. Substituir por nota genérica sobre isolamento de config de IA
4. Verificar demais seções intactas

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/architecture/security.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Sem referência a `argus_ia_agent.config.IaSettings`
- [ ] Nota genérica de isolamento de config de IA inserida
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
