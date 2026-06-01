# Arquivo morto da skill `governanca-compliance`

Scripts one-shot ja cumpridos sao mantidos aqui apenas como registro historico. Eles **nao** sao executados pelo fluxo corrente da skill e **nao** devem ser referenciados por documentacao ativa.

## Inventario

| Script | Cumprido em | Proposito original |
|---|---|---|
| `migrate_task_fields_to_en.py` | onda de migracao para nomenclatura inglesa (spec `.ia/docs/specs/done/workflow-status-nomenclatura-ingles-spec-2026-05-28.md`) | Substituir valores enum em portugues (`concluida`, `alta`, `media`, `baixa`, `testes`, `governanca`) por equivalentes ingleses (`done`, `high`, `medium`, `low`, `tests`, `governance`) nos campos `Status da task`, `Prioridade` e `Tipo` das tasks `.ia/docs/tasks/**/*.md`. |

## Regras

- Nao remover este diretorio sem reavaliar se ainda ha valor historico.
- Nao reexecutar scripts arquivados sem decisao explicita e tarefa formal.
- Novos scripts one-shot da skill devem entrar aqui ao final do ciclo correspondente.
