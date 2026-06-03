---
name: branch-task-aprovada
description: Criar uma branch de implementação a partir de uma task aprovada, usando o nome do arquivo da task como nome da branch e a branch atual como base. Opera apenas em Git e no arquivo da task. Usar quando a task estiver aprovada para implementação, quando for necessário abrir a branch da task ou quando a execução for sair da fase de análise para implementação.
---

# Objetivo
Garantir que a abertura da branch de implementação ocorra de forma determinística, rastreável e reutilizável a partir de uma task aprovada.

# Fluxo
1. Verificar se o arquivo da task existe, se possui um unico campo `Status da task` e se `Controle de implementação` está presente.
2. Confirmar que a task está com `Status da task: approved`. Caso não esteja, perguntar ao usuário se deseja atualizar o status para `approved` e só prosseguir se a resposta for afirmativa.
3. Executar `rtk python .ia/skills/branch-task-aprovada/create_task_implementation_branch.py <caminho_da_task>`.
4. Conferir se a branch base corresponde à branch atual da análise e se a branch de implementação corresponde ao nome do arquivo da task sem `.md`.
5. Prosseguir para a implementação somente depois que o script atualizar a task para `in_progress`.

# Regras obrigatórias
- A branch de implementação deve usar exatamente o nome do arquivo da task sem a extensão `.md`.
- Para novas tasks, o nome da branch deve seguir `task-DD-MM-YYYY-<hash_alfanumerico_10>`; branches antigas com `DD_MM_YYYY` são legado apenas quando derivadas de tasks históricas.
- A task deve conter um unico campo `Status da task`; se houver duplicidade, ela deve ser reconciliada antes da abertura da branch.
- A branch base deve ser a branch atual no momento da aprovação.
- Se a branch de implementação já existir, o script deve selecionar a branch existente em vez de criar outro nome.
- O script `.ia/skills/branch-task-aprovada/create_task_implementation_branch.py` é a fonte de verdade para essa etapa.
- Usar `--dry-run` quando a intenção for apenas validar a regra sem alterar o estado Git.

# Checklist de qualidade
- A task está marcada como `approved` antes da execução.
- A task possui um unico campo `Status da task`.
- O script foi chamado com o caminho correto da task.
- A task registra `Branch base da implementacao` e `Branch de implementacao`.
- O status muda para `in_progress` após a criação ou seleção da branch.

# Referências locais
- `AGENTS.md`
- `.ia/skills/workflow-demandas/SKILL.md`
- `.ia/docs/templates/task-template.md`
- `.ia/skills/branch-task-aprovada/create_task_implementation_branch.py`
