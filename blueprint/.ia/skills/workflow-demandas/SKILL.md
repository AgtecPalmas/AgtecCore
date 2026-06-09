---
name: workflow-demandas
description: Orquestrar demandas assistidas por IA com task, seleção de skills e fechamento documental. Skill agnóstica de linguagem e framework — operacionaliza o ciclo de task (`planned` → `approved` → `in_progress` → `done`) sem assumir stack específica. Usar quando o pedido envolver tarefa, demanda, feature, bugfix, refactor, melhoria de testes, mudanças multi-arquivo ou alterações em `.ia/`.
---

# Objetivo
Reduzir ambiguidades operacionais em demandas multi-etapa, garantindo task rastreável, seleção consistente de skills e encerramento documental completo.

# Fluxo
1. Verificar `.ia/docs/tasks/todo/` e reutilizar uma task existente apenas quando for explicitamente informada pelo solicitante.
2. Se não houver task aberta compatível, criar uma nova usando `.ia/docs/templates/task-template.md` como base e nomeando o arquivo como `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`.
3. Registrar na task o plano de ação, referências consultadas, restrições, arquivos previstos, política de validação e `Controle de implementação`.
4. Identificar camadas impactadas e carregar as skills obrigatórias por camada antes da implementação.
5. **Nunca iniciar a implementação sem aprovação explícita, seja via revisão de código ou sinalização de um agente supervisor**.
6. Quando a task for aprovada para implementação, combinar com `branch-task-aprovada` antes de editar código.
7. Executar mudanças pequenas e rastreáveis, mantendo a task sincronizada durante a implementação.
8. Antes do fechamento, executar `rtk python .ia/skills/governanca-compliance/check_ia_governance.py` e garantir saída `OK`; resolver findings antes de prosseguir.
9. Ao concluir, preencher as seções `## Descricao da solucao implementada`, `## Trade-offs` e `## Arquivos alterados`, combinar com `task-encerramento` para validar o fechamento, atualizar o status para `done` e mover a task para `.ia/docs/tasks/done/`, preservando o mesmo hash do arquivo original.

# Regras obrigatórias
- Não agrupar mudanças sem relação direta na mesma task.
- Para mudanças documentais em `.ia/`, manter o fluxo de task quando a alteração envolver múltiplos arquivos ou impacto de processo.
- O identificador da task deve ser um hash alfanumérico de 10 caracteres e substituir a descrição textual no nome do arquivo.
- Datas de novos artefatos de governança devem usar `DD-MM-YYYY`; tasks antigas com `DD_MM_YYYY` são legado apenas para leitura e referência histórica.
- Não reutilizar fragmentos de segredo, credenciais ou dados sensíveis como hash de task.
- Toda task nova deve conter um unico campo `Status da task` em `## 1. Metadados` e a seção `Controle de implementação` com aprovação e campos de branch.
- Registrar explicitamente se os testes foram executados, não executados ou apenas sugeridos, sempre com motivo e comando segmentado quando aplicável.
- Combinar esta skill com as skills por camada disponíveis no projeto (por exemplo, no contexto Django: `django-models`, `django-api-views`; em outros stacks, as skills equivalentes) sempre que houver impacto técnico no código.
- Quando a task for aprovada para implementação, a abertura da branch deve ocorrer via `branch-task-aprovada`.
- Antes de invocar `task-encerramento`, executar `rtk python .ia/skills/governanca-compliance/check_ia_governance.py` e exigir saída zero.
- Quando a task estiver pronta para fechamento, o encerramento deve ocorrer via `task-encerramento`.
- Quando a demanda envolver especificação técnica para um stack específico (por exemplo, FastAPI), combinar com a skill correspondente e salvar o artefato em `.ia/docs/specs/`.

# Checklist de qualidade
- Existe uma task aberta ou reutilizada com justificativa clara.
- O nome do arquivo segue `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`.
- A task contém um unico campo `Status da task` e `Controle de implementação` preenchível.
- As skills por camada usadas na demanda foram registradas.
- Objetivo, critérios de aceite e restrições estão atualizados.
- A seção de observações de testes informa estado, motivo e comando sugerido ou executado.
- O encerramento preenche `## Descricao da solucao implementada`, `## Trade-offs` e `## Arquivos alterados`, atualiza o status para `done` e aplica a convenção `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md` com o mesmo hash original.

# Referências locais
- `.ia/docs/templates/task-template.md`
- `.ia/docs/architecture/overview.md`
- `.ia/docs/guides/patterns.md`
- `.ia/docs/guides/testing.md`
- `.ia/skills/branch-task-aprovada/SKILL.md`
- `.ia/skills/task-encerramento/SKILL.md`
