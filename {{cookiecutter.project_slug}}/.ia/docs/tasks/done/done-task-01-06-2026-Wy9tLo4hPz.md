# Tarefa: Remover exceção legada de constraints.md do snippet fastapi_project

## 1. Metadados

- ID da task: `task-01-06-2026-Wy9tLo4hPz`
- Status da task: `done`
- Prioridade: `low`
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
  - `core/management/commands/snippets/fastapi_project/.ia/docs/guides/constraints.md`
  - `.ia/docs/specs/fastapi-snippet-genericizar-ia-spec-01-06-2026.md`

## 3. Contexto

O `constraints.md` é genérico e correto, exceto por uma entrada no final que documenta uma exceção legada específica do Argus: "há acesso direto a `db` em `authentication/routers.py`; este padrão não deve ser replicado em novos módulos." Embora o código do snippet de fato contenha esse acesso, documentar a dívida técnica do Argus como restrição do template induz o analista a tratar um problema de um projeto específico como regra operacional do projeto gerado.

## 4. Objetivo

Remover apenas a linha de exceção legada, mantendo todas as demais regras e o protocolo anti-alucinação intactos.

## 5. Escopo

- Inclui:
  - Remover a nota de exceção legada sobre `authentication/routers.py`
- Nao inclui:
  - Qualquer outra regra do arquivo

## 6. Criterios de aceite

1. Nenhuma referência a exceção legada de `authentication/routers.py` no arquivo
2. Todas as demais regras (`RULE-ARCH-002`, `RULE-ASYNC-001`, `RULE-DEP-001`, `RULE-TEST-001`, `RULE-LANG-001`, `RULE-GIT-001`) intactas
3. Protocolo anti-alucinação intacto

## 7. Restricoes e premissas

- Restricoes:
  - Alterar somente a linha/bloco da exceção legada
- Premissas:
  - A remoção da nota não altera o comportamento do código do snippet; apenas remove a documentação da dívida

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `não`
- Documentacao: `sim — constraints.md do snippet`

## 9. Plano de execucao

1. Ler `constraints.md`
2. Localizar a linha de exceção legada (`RULE-EXC-001` ou equivalente)
3. Remover a entrada
4. Verificar demais regras intactas

## 10. Controle de implementacao

- Branch base da implementacao: `nao_iniciada`
- Branch de implementacao: `nao_iniciada`
- Skills usadas: `atualizar-artefatos-ia`
- Arquivos previstos:
  - `core/management/commands/snippets/fastapi_project/.ia/docs/guides/constraints.md`
- Status de aprovacao: `done`
- Execucao de testes: `nao_executada`
- Comandos executados: `nenhum`

## 11. Evidencias

- Resultado de testes: `nenhum`
- Logs, screenshots ou observacoes: `nenhum`

## 12. Definition of Done

- [ ] Exceção legada de `authentication/routers.py` removida
- [ ] Demais regras e protocolo anti-alucinação intactos
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
