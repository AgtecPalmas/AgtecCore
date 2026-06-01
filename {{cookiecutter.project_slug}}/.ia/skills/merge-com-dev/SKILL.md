---
name: merge-com-dev
description: Fazer o merge de uma branch de task no padrão `task-DD-MM-YYYY-<hash_alfanumerico_10>` com a branch local `dev`. Skill agnóstica de linguagem e framework — opera apenas em Git. Usar quando o desenvolvedor pedir `merge com dev`, solicitar merge da branch atual da task para `dev` ou quiser validar esse fluxo com `--dry-run`.
---

# Objetivo
Garantir um fluxo determinístico e seguro para merge local de branches de task em `dev`.

# Fluxo
1. Confirmar que a branch atual segue o padrão `task-DD-MM-YYYY-<hash_alfanumerico_10>`.
2. Confirmar que o worktree Git está limpo antes de trocar de branch.
3. Executar `rtk python .ia/skills/merge-com-dev/merge_task_branch_with_dev.py`.
4. Informar ao desenvolvedor o nome da branch de task mergeada e que o HEAD final fica em `dev`.
5. Perguntar ao desenvolvedor se deseja excluir a branch mergeada.
6. Se houver confirmação explícita, executar `rtk python .ia/skills/merge-com-dev/merge_task_branch_with_dev.py --delete-merged-branch <nome_da_branch_task>`.

# Regras obrigatórias
- O script `.ia/skills/merge-com-dev/merge_task_branch_with_dev.py` é a fonte de verdade para a automação.
- Esta automação é a única exceção permitida à regra geral que proíbe `git commit` pela IA; a permissão existe apenas quando o merge for disparado pelo script Python oficial versionado.
- Usar `--dry-run` quando a intenção for apenas validar a branch alvo, o estado do repositório e a ação planejada.
- Não fazer `push`.
- Não executar o merge se houver alterações locais não commitadas.
- Não excluir a branch mergeada sem confirmação explícita do desenvolvedor.
- Falhar explicitamente se a branch atual não seguir o padrão de task aprovado pelo projeto.
- Branches antigas com `DD_MM_YYYY` só podem ser tratadas como legado quando derivadas de tasks históricas já existentes.

# Checklist de qualidade
- A branch atual começa com `task-`.
- O sufixo da branch tem exatamente 10 caracteres alfanuméricos.
- A branch `dev` existe localmente.
- O merge é executado localmente em `dev`, sem operações remotas.
- A exclusão da branch mergeada só acontece após confirmação e usando o modo explícito `--delete-merged-branch`.

# Referências locais
- `AGENTS.md`
- `.ia/skills/branch-task-aprovada/SKILL.md`
- `.ia/skills/merge-com-dev/merge_task_branch_with_dev.py`
