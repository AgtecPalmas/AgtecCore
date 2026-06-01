---
name: workflow-demandas
description: Orquestrar demandas assistidas por IA com task, seleção de skills e fechamento documental. Skill agnóstica de linguagem e framework — operacionaliza o ciclo de task (`planned` → `approved` → `in_progress` → `done`) sem assumir stack específica. Usar quando o pedido envolver tarefa, demanda, feature, bugfix, refactor, melhoria de testes, mudanças multi-arquivo ou alterações em `.ia/`.
---

# Objetivo
Reduzir ambiguidades operacionais em demandas multi-etapa, garantindo planejamento rastreável por spec ou task, seleção consistente de skills e implementação iniciada apenas a partir de task aprovada.

# Fluxo
1. Classificar a demanda como `spec-first` ou `task-first` antes de qualquer implementação.
2. Se a demanda exigir design upfront, criar ou atualizar uma spec em `.ia/docs/specs/`; se for execução direta e localizada, abrir uma task em `.ia/docs/tasks/todo/`.
3. Verificar `.ia/docs/tasks/todo/` e reutilizar uma task existente apenas quando ela for explicitamente informada pelo solicitante.
4. Se não houver task aberta compatível para a execução, criar uma nova usando `.ia/docs/templates/task-template.md` como base e nomeando o arquivo como `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`.
5. Registrar na spec e/ou task o plano de ação, referências consultadas, restrições, arquivos previstos, política de validação e `Controle de implementação`.
6. Identificar camadas impactadas e carregar as skills obrigatórias por camada antes da implementação.
7. **Nunca iniciar a implementação só com spec. Nunca iniciar a implementação sem aprovação explícita da task que será executada, seja via revisão de código ou sinalização de um agente supervisor**.
8. Quando a task estiver com `Status da task: approved`, combinar com `branch-task-aprovada` antes de editar código.
9. Executar mudanças pequenas e rastreáveis, mantendo a task sincronizada durante a implementação.
10. Antes do fechamento, executar `rtk python .ia/skills/governanca-compliance/check_ia_governance.py` e garantir saída `OK`; resolver findings antes de prosseguir.
11. Ao concluir, preencher as seções `## Descricao da solucao implementada`, `## Trade-offs` e `## Arquivos alterados`, combinar com `task-encerramento` para validar o fechamento, atualizar o status para `done` e mover a task para `.ia/docs/tasks/done/`, preservando o mesmo hash do arquivo original.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- Toda demanda deve começar com planejamento explícito em spec ou task, conforme escopo e tipo de mudança.
- Spec aprovada não substitui task de execução; qualquer implementação, inclusive documental relevante em `.ia/`, exige task derivada ou task direta com `Status da task: approved`.
- Não agrupar mudanças sem relação direta na mesma task.
- Para mudanças documentais em `.ia/`, manter o fluxo de task quando a alteração envolver múltiplos arquivos ou impacto de processo.
- O identificador da task deve ser um hash alfanumérico de 10 caracteres e substituir a descrição textual no nome do arquivo.
- Datas de novos artefatos de governança devem usar `DD-MM-YYYY`; tasks antigas com `DD_MM_YYYY` são legado apenas para leitura e referência histórica.
- Não reutilizar fragmentos de segredo, credenciais ou dados sensíveis como hash de task.
- Toda task nova deve conter um unico campo `Status da task` em `## 1. Metadados` e a seção `Controle de implementação` com aprovação e campos de branch.
- Registrar explicitamente se os testes foram executados, não executados ou apenas sugeridos, sempre com motivo e comando segmentado quando aplicável.
- Combinar esta skill com as skills por camada disponíveis no projeto (por exemplo, no contexto FastAPI: `adicionar-endpoint`, `refatorar-modulo`, `fastapi-tests-pytest`) sempre que houver impacto técnico no código.
- Quando a task for aprovada para implementação, a abertura da branch deve ocorrer via `branch-task-aprovada`.
- Antes de invocar `task-encerramento`, executar `rtk python .ia/skills/governanca-compliance/check_ia_governance.py` e exigir saída zero.
- Quando a task estiver pronta para fechamento, o encerramento deve ocorrer via `task-encerramento`.
- Quando a demanda envolver especificação técnica para um stack específico (por exemplo, FastAPI), combinar com a skill correspondente e salvar o artefato em `.ia/docs/specs/`.

# Checklist de qualidade
- Existe uma task aberta ou reutilizada com justificativa clara.
- Se a demanda começou por spec, existe rastreabilidade explícita entre spec aprovada e task de execução aprovada.
- O nome do arquivo segue `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`.
- A task contém um unico campo `Status da task` e `Controle de implementação` preenchível.
- As skills por camada usadas na demanda foram registradas.
- Objetivo, critérios de aceite e restrições estão atualizados.
- A seção de observações de testes informa estado, motivo e comando sugerido ou executado.
- O encerramento preenche `## Descricao da solucao implementada`, `## Trade-offs` e `## Arquivos alterados`, atualiza o status para `done` e aplica a convenção `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md` com o mesmo hash original.

# Referências locais
- `AGENTS.md`
- `.ia/docs/templates/task-template.md`
- `.ia/docs/architecture/overview.md`
- `.ia/docs/guides/patterns.md`
- `.ia/docs/testing/strategy.md`
