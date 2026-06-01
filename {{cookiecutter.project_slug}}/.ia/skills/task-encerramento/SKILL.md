---
name: task-encerramento
description: Encerrar uma task implementada, validar os campos finais obrigatórios e mover o arquivo de `.ia/docs/tasks/todo/` para `.ia/docs/tasks/done/` com status final canônico. Skill agnóstica de linguagem e framework — opera apenas sobre arquivos markdown e Git. Usar quando a implementação da task estiver concluída e a demanda estiver pronta para fechamento documental.
---

# Objetivo
Garantir que o encerramento de tasks assistidas por IA ocorra de forma determinística, validada e rastreável, sem depender apenas de edição manual.

# Fluxo
1. Confirmar que a task existe em `.ia/docs/tasks/todo/`, possui um unico campo `Status da task` e que seu status atual é `in_progress`.
2. Confirmar que a task possui as seções `## Descricao da solucao implementada`, `## Trade-offs` e `## Arquivos alterados` preenchidas.
3. Executar `rtk python .ia/skills/task-encerramento/close_task_and_move_to_done.py <caminho_da_task>`.
4. Verificar que o status final foi atualizado para `done`.
5. Verificar que o arquivo foi movido para `.ia/docs/tasks/done/` com prefixo `done-` e mesmo hash original.

# Regras obrigatórias
- O status final canônico de task concluída é `done` (valor literal do campo `Status da task`).
- A task deve conter um unico campo `Status da task`; se houver duplicidade, ela deve ser reconciliada antes do encerramento.
- O script deve falhar explicitamente se a task não estiver em `in_progress`.
- O script deve falhar se `## Descricao da solucao implementada`, `## Trade-offs` ou `## Arquivos alterados` estiverem vazios ou com placeholders.
- O encerramento deve preservar o mesmo hash do nome original da task.
- Usar `--dry-run` quando a intenção for validar o fechamento sem mover o arquivo.

# Checklist de qualidade
- A task saiu de `todo/` e apareceu em `done/`.
- O nome final segue `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md` para tasks novas; tasks históricas com `DD_MM_YYYY` podem ser encerradas preservando o padrão legado do arquivo original.
- O status final está como `done`.
- A task possui um unico campo `Status da task` e os campos finais obrigatórios estão preenchidos.
- O arquivo original em `todo/` não permanece duplicado após o encerramento real.

# Referências locais
- `AGENTS.md`
- `.ia/README.md`
- `.ia/docs/templates/task-template.md`
- `.ia/skills/workflow-demandas/SKILL.md`
- `.ia/skills/task-encerramento/close_task_and_move_to_done.py`
